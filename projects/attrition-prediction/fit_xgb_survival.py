"""
Train a survival model with XGBoost (AFT or Cox) and compute 3/6/9 month risks.

This is designed for a GPU box (tree_method=gpu_hist), but will fall back to CPU
if GPU is unavailable. For absolute probabilities at specific horizons, use the
`survival:aft` objective; Cox only returns relative risks.
"""

import argparse
import os
from typing import List, Tuple, Optional, Dict

import numpy as np
import pandas as pd
from scipy.stats import norm
import xgboost as xgb

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sksurv.util import Surv
from sksurv.metrics import concordance_index_censored


# ------------------------- Data helpers -------------------------

def ensure_dir(d: str):
    os.makedirs(d, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Fit XGBoost survival model (AFT or Cox) for attrition.")
    p.add_argument("--data", required=True, help="Path to synthetic_attrition_2007_2025.csv")
    p.add_argument("--out", default="out_xgb", help="Output directory")
    p.add_argument("--cutoff", default="2020-01-01", help="Hire-date cutoff for time-aware split (YYYY-MM-DD)")
    p.add_argument("--objective", choices=["aft", "cox"], default="aft", help="Use survival:aft for calibrated probs; survival:cox for relative risk")
    p.add_argument("--horizons", nargs="+", type=int, default=[90, 180, 270], help="Horizons (days) for risk estimates")
    # XGBoost hyperparameters (conservative defaults)
    p.add_argument("--n_estimators", type=int, default=400)
    p.add_argument("--learning_rate", type=float, default=0.05)
    p.add_argument("--max_depth", type=int, default=8)
    p.add_argument("--subsample", type=float, default=0.8)
    p.add_argument("--colsample_bytree", type=float, default=0.8)
    p.add_argument("--min_child_weight", type=float, default=1.0)
    p.add_argument("--reg_alpha", type=float, default=0.0)
    p.add_argument("--reg_lambda", type=float, default=1.0)
    p.add_argument("--gamma", type=float, default=0.0)
    p.add_argument("--aft_loss_distribution", default="normal", help="AFT distribution (normal/logistic/extreme) for survival:aft")
    p.add_argument("--aft_sigma", type=float, default=1.5, help="Scale (sigma) for AFT distribution")
    p.add_argument("--tree_method", default="gpu_hist", help="gpu_hist (preferred) or hist")
    p.add_argument("--max_bin", type=int, default=256)
    p.add_argument("--predict_batch_size", type=int, default=4096, help="Batch size for inference")
    p.add_argument("--random_state", type=int, default=42)
    return p.parse_args()


def make_ohe():
    # Compatible with sklearn old/new
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=True, dtype=np.float32)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=True, dtype=np.float32)


def select_features(df: pd.DataFrame):
    cat_cols = ["department", "job_family", "level", "gender", "education_level", "contract_type", "visa_status", "product_area"]
    num_cols = [
        "manager_span", "age_at_hire", "comp_ratio", "salary_band", "base_pay",
        "variable_pay_pct", "perf_rating", "pip_flag", "engagement_score", "remote",
        "years_experience_at_hire", "commute_km", "union_member", "stock_grants",
        "promotions_last_3y", "training_hours_last_yr", "overtime_hours_mo", "team_size",
        "travel_pct", "schedule_flexibility", "market_pay_index", "org_changes_last_yr"
    ]
    X = df[cat_cols + num_cols].copy()
    return X, cat_cols, num_cols


def make_labels(df: pd.DataFrame, censor_date: pd.Timestamp) -> Tuple[Surv, np.ndarray, np.ndarray]:
    end_date = df["attrition_date"].fillna(censor_date)
    durations = (end_date - df["hire_date"]).dt.days.astype("float64").to_numpy()
    events = df["attrition_date"].notna().to_numpy()
    y = Surv.from_arrays(event=events, time=durations)
    return y, durations, events


def time_split_by_hire(df: pd.DataFrame, cutoff: pd.Timestamp):
    train_idx = (df["hire_date"] < cutoff).to_numpy()
    test_idx = ~train_idx
    return train_idx, test_idx


def build_preprocessor(cat_cols: List[str], num_cols: List[str]) -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("cat", make_ohe(), cat_cols),
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler(with_mean=False))]), num_cols),
        ],
        remainder="drop",
        sparse_threshold=0.3,
    )


# ------------------------- XGBoost survival helpers -------------------------

def make_dmatrix(objective: str, X_enc, durations: np.ndarray, events: np.ndarray) -> xgb.DMatrix:
    dtrain = xgb.DMatrix(X_enc, label=durations)
    if objective == "aft":
        lower = durations.copy()
        upper = durations.copy()
        upper[~events] = np.inf
        dtrain.set_float_info("label_lower_bound", lower)
        dtrain.set_float_info("label_upper_bound", upper)
    else:  # cox
        # Weight by event indicator so censored rows have reduced influence
        dtrain.set_weight(events.astype(np.float32))
    return dtrain


def train_xgb(args, dtrain: xgb.DMatrix):
    base_params = dict(
        learning_rate=args.learning_rate,
        max_depth=args.max_depth,
        subsample=args.subsample,
        colsample_bytree=args.colsample_bytree,
        min_child_weight=args.min_child_weight,
        reg_alpha=args.reg_alpha,
        reg_lambda=args.reg_lambda,
        gamma=args.gamma,
        tree_method=args.tree_method,
        max_bin=args.max_bin,
        objective="survival:aft" if args.objective == "aft" else "survival:cox",
        eval_metric="aft-nloglik" if args.objective == "aft" else "cox-nloglik",
        seed=args.random_state,
    )
    if args.objective == "aft":
        base_params.update(
            aft_loss_distribution=args.aft_loss_distribution,
            aft_loss_distribution_scale=args.aft_sigma,
        )
    try:
        booster = xgb.train(base_params, dtrain, num_boost_round=args.n_estimators)
    except xgb.core.XGBoostError as e:
        if "GPU is not enabled" in str(e) and args.tree_method == "gpu_hist":
            print("[WARN] GPU not available, retrying with tree_method=hist")
            base_params["tree_method"] = "hist"
            booster = xgb.train(base_params, dtrain, num_boost_round=args.n_estimators)
        else:
            raise
    return booster


def predict_mu(args, booster: xgb.Booster, dmat: xgb.DMatrix, batch_size: int) -> np.ndarray:
    preds = []
    n = dmat.num_row()
    for start in range(0, n, batch_size):
        end = min(start + batch_size, n)
        block = dmat.slice(list(range(start, end)))
        preds.append(booster.predict(block, output_margin=True))
    return np.concatenate(preds)


def risk_at_horizons_aft(mu: np.ndarray, sigma: float, horizons: List[int]) -> Dict[int, np.ndarray]:
    risks = {}
    for T in horizons:
        logT = np.log(max(T, 1e-3))
        z = (logT - mu) / sigma
        p_event = norm.cdf(z)  # log-normal CDF at T
        risks[T] = p_event.astype(np.float32)
    return risks


def cindex_from_preds(y: Surv, risk_scores: np.ndarray) -> float:
    return float(concordance_index_censored(y["event"], y["time"], risk_scores)[0])


# ------------------------- Main -------------------------


def main():
    args = parse_args()
    ensure_dir(args.out)
    rng = np.random.default_rng(args.random_state)

    df = pd.read_csv(args.data, parse_dates=["hire_date", "attrition_date"])
    censor_date = pd.Timestamp("2025-12-31")

    y, durations, events = make_labels(df, censor_date)
    X, cat_cols, num_cols = select_features(df)

    cutoff = pd.Timestamp(args.cutoff)
    train_mask, test_mask = time_split_by_hire(df, cutoff)

    X_train, X_test = X.loc[train_mask], X.loc[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    dur_train, dur_test = durations[train_mask], durations[test_mask]
    evt_train, evt_test = events[train_mask], events[test_mask]

    # Preprocess
    pre = build_preprocessor(cat_cols, num_cols)
    X_train_enc = pre.fit_transform(X_train)
    X_test_enc = pre.transform(X_test)

    # Train
    dtrain = make_dmatrix(args.objective, X_train_enc, dur_train, evt_train)
    booster = train_xgb(args, dtrain)

    # Predict
    dtest = make_dmatrix(args.objective, X_test_enc, dur_test, evt_test)
    mu_test = predict_mu(args, booster, dtest, batch_size=args.predict_batch_size)

    # Metrics
    if args.objective == "aft":
        # Use mu as log(time); lower mu => earlier event => higher risk
        risk_scores = -mu_test
    else:
        risk_scores = mu_test  # Cox: higher margin = higher risk
    cindex = cindex_from_preds(y_test, risk_scores)

    # Horizon risks (AFT only)
    risks_by_T: Dict[int, Optional[np.ndarray]] = {}
    if args.objective == "aft":
        risks_by_T = risk_at_horizons_aft(mu_test, args.aft_sigma, args.horizons)
    else:
        risks_by_T = {T: None for T in args.horizons}

    # Save metrics
    with open(os.path.join(args.out, "xgb_metrics.txt"), "w") as f:
        f.write(f"Objective: {args.objective}\n")
        f.write(f"C-index (test): {cindex:.4f}\n")
        if args.objective != "aft":
            f.write("NOTE: Cox objective outputs relative risk only; horizon probabilities not computed.\n")

    # Save ranked risks
    rank_T = 180 if 180 in args.horizons else max(args.horizons)
    base_cols = ["employee_id", "hire_date", "department", "job_family", "level", "age_at_hire"]
    ranked = df.loc[test_mask, base_cols].copy()
    if args.objective == "aft":
        for T in args.horizons:
            ranked[f"risk_{T}d"] = np.round(risks_by_T[T], 6)
        ranked = ranked.sort_values(f"risk_{rank_T}d", ascending=False)
    else:
        ranked["relative_risk"] = risk_scores
        ranked = ranked.sort_values("relative_risk", ascending=False)
    ranked.to_csv(os.path.join(args.out, "xgb_top_risk.csv"), index=False)

    print("=== XGBoost Survival Results ===")
    print(f"Objective: {args.objective}")
    print(f"C-index: {cindex:.3f}")
    if args.objective == "aft":
        for T in args.horizons:
            print(f"Mean predicted P(event by {T}d): {float(risks_by_T[T].mean()):.3f}")
    else:
        print("Relative risks only (Cox); horizon probabilities not computed.")
    print(f"Saved outputs in: {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
