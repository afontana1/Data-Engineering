# fit_rsf.py (memory-safe v2)
"""
https://arxiv.org/pdf/0811.1645
https://xgboost.readthedocs.io/en/latest/tutorials/aft_survival_analysis.html
"""
import argparse, os
from typing import List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.inspection import permutation_importance
from sklearn.base import BaseEstimator

from sksurv.util import Surv
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import (
    concordance_index_censored,
    integrated_brier_score,
    brier_score,
    cumulative_dynamic_auc,
)
from sksurv.nonparametric import kaplan_meier_estimator


# ------------------------- Helpers -------------------------

def ensure_dir(d: str):
    os.makedirs(d, exist_ok=True)

def log(msg: str):
    print(f"[RSF] {msg}", flush=True)

def parse_args():
    p = argparse.ArgumentParser(description="Fit Random Survival Forest to attrition data (memory-safe).")
    p.add_argument("--data", required=True, help="Path to synthetic_attrition_2007_2025.csv")
    p.add_argument("--out", default="out_rsf", help="Output directory")
    p.add_argument("--cutoff", default="2020-01-01", help="Hire-date cutoff for time-aware split (YYYY-MM-DD)")
    p.add_argument("--horizons", nargs="+", type=int, default=[90, 180, 270],
                   help="Horizons in days (space-separated). Defaults to 3/6/9 months.")
    # Conservative defaults to limit RAM; tune up later
    p.add_argument("--n_estimators", type=int, default=300)
    p.add_argument("--min_samples_split", type=int, default=12)
    p.add_argument("--min_samples_leaf", type=int, default=15)
    p.add_argument("--max_depth", type=int, default=12)
    p.add_argument("--max_features", default="sqrt")
    p.add_argument("--n_jobs", type=int, default=2, help="Parallel workers for RSF (2 is RAM-friendlier than -1)")
    p.add_argument("--random_state", type=int, default=42)
    p.add_argument("--grid_points", type=int, default=30, help="# time points for IBS grid (smaller -> less RAM)")
    p.add_argument("--predict_batch_size", type=int, default=4000, help="Batch size for survival predictions (memory guard)")
    p.add_argument("--eval_subsample", type=int, default=20000, help="Subsample test rows for metrics; set 0 to use all")
    p.add_argument("--permute_subsample", type=int, default=3000, help="Rows used for permutation importance (post-eval subsample)")
    return p.parse_args()

def make_ohe():
    # Compatible with sklearn old/new
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype=np.float32)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False, dtype=np.float32)

def to_float32(X):
    # Downcast the preprocessed matrix to float32 (halves memory)
    return np.asarray(X, dtype=np.float32)

def make_labels(df: pd.DataFrame, censor_date: pd.Timestamp) -> Tuple[Surv, np.ndarray, np.ndarray]:
    end_date = df["attrition_date"].fillna(censor_date)
    durations = (end_date - df["hire_date"]).dt.days.astype("float64").to_numpy()
    events = df["attrition_date"].notna().to_numpy()
    y = Surv.from_arrays(event=events, time=durations)
    return y, durations, events

def select_features(df: pd.DataFrame):
    cat_cols = ["department","job_family","level","gender","education_level","contract_type","visa_status","product_area"]
    num_cols = [
        "manager_span","age_at_hire","comp_ratio","salary_band","base_pay",
        "variable_pay_pct","perf_rating","pip_flag","engagement_score","remote",
        "years_experience_at_hire","commute_km","union_member","stock_grants",
        "promotions_last_3y","training_hours_last_yr","overtime_hours_mo","team_size",
        "travel_pct","schedule_flexibility","market_pay_index","org_changes_last_yr"
    ]
    X = df[cat_cols + num_cols].copy()
    return X, cat_cols, num_cols

def time_split_by_hire(df: pd.DataFrame, cutoff: pd.Timestamp):
    train_idx = (df["hire_date"] < cutoff).to_numpy()
    test_idx = ~train_idx
    return train_idx, test_idx

def build_pipeline(cat_cols: List[str], num_cols: List[str], args) -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            ("cat", make_ohe(), cat_cols),
            ("num", SimpleImputer(strategy="median"), num_cols),
        ],
        remainder="drop",
    )
    rsf = RandomSurvivalForest(
        n_estimators=args.n_estimators,
        min_samples_split=args.min_samples_split,
        min_samples_leaf=args.min_samples_leaf,
        max_features=args.max_features,
        max_depth=args.max_depth,
        n_jobs=args.n_jobs,
        random_state=args.random_state,
    )
    pipe = Pipeline([("pre", pre), ("to32", FunctionTransformer(to_float32)), ("model", rsf)])
    return pipe

# --- Key memory-safe idea: evaluate survival only on small sets of times, batched ---

def _iter_batches(n: int, batch_size: int):
    for start in range(0, n, batch_size):
        yield slice(start, min(start + batch_size, n))

def predict_surv_on_times(pipe: Pipeline, X: pd.DataFrame, times: np.ndarray, batch_size: int) -> np.ndarray:
    """Return survival matrix [n_samples, len(times)] by evaluating step functions only at desired times."""
    model = pipe.named_steps["model"]
    pre = pipe.named_steps["pre"]
    chunks = []
    for sl in _iter_batches(len(X), batch_size):
        Xp = pre.transform(X.iloc[sl])
        Xp = to_float32(Xp)
        funcs = model.predict_survival_function(Xp)  # list of step functions
        chunks.append(np.vstack([f(times) for f in funcs]))
    return np.vstack(chunks)

def risk_by_horizon_from_pipe(pipe: Pipeline, X: pd.DataFrame, horizon_days: int, batch_size: int) -> np.ndarray:
    times = np.array([horizon_days], dtype=float)
    surv = predict_surv_on_times(pipe, X, times, batch_size)
    return 1.0 - surv[:, 0]

def auc_at_time(pipe: Pipeline, X_train, y_train, X_test, y_test, t: int) -> float:
    scores = risk_by_horizon_from_pipe(pipe, X_test, t, batch_size=len(X_test))
    auc, _ = cumulative_dynamic_auc(y_train, y_test, scores, times=np.array([t]))
    return float(auc[0])

def brier_at_time(y_train, y_test, pipe: Pipeline, X_test, t: int) -> float:
    S_T = predict_surv_on_times(pipe, X_test, np.array([t]), batch_size=len(X_test))
    _, bs = brier_score(y_train, y_test, S_T, np.array([t]))
    return float(bs)

def calibration_curve_at_T(y_test, p_event_T: np.ndarray, T: int, n_bins: int = 10) -> pd.DataFrame:
    bins = pd.qcut(p_event_T, q=n_bins, duplicates="drop")
    rows = []
    for b in bins.unique().sort_values():
        mask = (bins == b).to_numpy()
        if mask.sum() < 20:
            continue
        times = y_test["time"][mask]
        events = y_test["event"][mask]
        tt, ss = kaplan_meier_estimator(events, times)
        idx = np.searchsorted(tt, T, side="right") - 1
        idx = np.clip(idx, 0, len(tt)-1)
        observed = 1 - ss[idx]
        predicted = float(p_event_T[mask].mean())
        rows.append({"bin": str(b), "pred": predicted, "obs": float(observed), "n": int(mask.sum())})
    return pd.DataFrame(rows)

class HorizonRiskEstimator(BaseEstimator):
    """Wrapper so permutation_importance can call .predict() on risk-by-horizon."""
    def __init__(self, pipe: Pipeline, horizon_days: int, batch_size: int = 2048):
        self.pipe = pipe
        self.h = horizon_days
        self.batch_size = batch_size
    def fit(self, X, y=None):
        return self
    def predict(self, X):
        return risk_by_horizon_from_pipe(self.pipe, X, self.h, batch_size=self.batch_size)
    def score(self, X, y):
        p = self.predict(X)
        return -np.mean((p - y) ** 2)

# ------------------------- Main -------------------------

def main():
    args = parse_args()
    ensure_dir(args.out)
    rng = np.random.default_rng(args.random_state)

    log("Loading data")
    df = pd.read_csv(args.data, parse_dates=["hire_date","attrition_date"])
    censor_date = pd.Timestamp("2025-12-31")

    # 2) Labels & features
    log("Preparing labels and features")
    y, _, _ = make_labels(df, censor_date)
    X, cat_cols, num_cols = select_features(df)

    # 3) Time-aware split
    log(f"Time split with cutoff {args.cutoff}")
    cutoff = pd.Timestamp(args.cutoff)
    train_mask, test_mask = time_split_by_hire(df, cutoff)
    X_train, X_test = X.loc[train_mask], X.loc[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]

    # 4) Pipeline & fit (with graceful fallback if memory blows up)
    log("Fitting RSF")
    pipe = build_pipeline(cat_cols, num_cols, args)
    try:
        pipe.fit(X_train, y_train)
    except MemoryError:
        print("[WARN] OOM during fit. Retrying with smaller forest and less parallelism")
        pipe.set_params(
            model__n_estimators=max(150, args.n_estimators//2),
            model__max_depth=min(10, args.max_depth or 10),
            model__min_samples_leaf=max(20, args.min_samples_leaf),
            model__n_jobs=1
        )
        pipe.fit(X_train, y_train)
    log("Fit complete")

    # Optional subsample for metrics to avoid OOM
    if args.eval_subsample and len(X_test) > args.eval_subsample:
        log(f"Subsampling eval set to {args.eval_subsample}")
        idx = rng.choice(len(X_test), size=args.eval_subsample, replace=False)
        X_eval = X_test.iloc[idx]
        y_eval = y_test[idx]
    else:
        X_eval, y_eval = X_test, y_test

    # 5) Discrimination: global C-index
    # use horizon-based risk (avoids large hazard matrices in predict)
    log("Computing C-index via horizon risk")
    rank_T_for_cidx = 180 if 180 in args.horizons else max(args.horizons)
    risk_scores = risk_by_horizon_from_pipe(pipe, X_eval, rank_T_for_cidx, batch_size=args.predict_batch_size)
    cindex = float(concordance_index_censored(y_eval["event"], y_eval["time"], risk_scores)[0])

    # 6) IBS on a small grid (memory-safe, clipped to follow-up)
    log("Computing IBS")
    t_grid_raw = np.quantile(y_train["time"], np.linspace(0.1, 0.9, args.grid_points))
    t_grid = np.clip(t_grid_raw, 1e-6, y_eval["time"].max() - 1e-6)
    t_grid = np.unique(t_grid)
    if len(t_grid) == 0:
        t_grid = np.array([min(180.0, y_eval["time"].max() * 0.8)])
    surv_on_grid = predict_surv_on_times(pipe, X_eval, t_grid, batch_size=args.predict_batch_size)
    ibs = float(integrated_brier_score(y_train, y_eval, surv_on_grid, t_grid))

    # 7) AUC/Brier and risks at requested horizons
    log("Computing AUC/Brier and risks at horizons")
    horizons = sorted(set(args.horizons))
    aucs, briers, risks_by_T = {}, {}, {}
    max_eval_time = float(y_eval["time"].max())
    for T in horizons:
        if T >= max_eval_time:
            log(f"Skipping AUC/Brier at {T}d (beyond eval follow-up {max_eval_time:.1f})")
            aucs[T] = float("nan")
            briers[T] = float("nan")
        else:
            aucs[T] = auc_at_time(pipe, X_train, y_train, X_eval, y_eval, T)
            briers[T] = brier_at_time(y_train, y_eval, pipe, X_eval, T)
        risks_by_T[T] = risk_by_horizon_from_pipe(pipe, X_test, T, batch_size=args.predict_batch_size)

    # 8) Save metrics
    with open(os.path.join(args.out, "rsf_metrics.txt"), "w") as f:
        f.write(f"C-index (test): {cindex:.4f}\n")
        f.write(f"Integrated Brier Score (test): {ibs:.4f}\n")
        for T in horizons:
            f.write(f"AUC@{T}d: {aucs[T]:.4f} | Brier@{T}d: {briers[T]:.4f}\n")

    # 9) Ranked risk table (by 180d or max horizon)
    log("Saving ranked risk table")
    rank_T = 180 if 180 in horizons else max(horizons)
    ranked = (
        df.loc[test_mask, ["employee_id","hire_date","department","job_family","level","age_at_hire"]]
          .assign(**{f"risk_{T}d": np.round(risks_by_T[T], 6) for T in horizons})
          .sort_values(f"risk_{rank_T}d", ascending=False)
    )
    ranked.to_csv(os.path.join(args.out, "top_risk.csv"), index=False)

    # 10) Permutation importance @ rank_T (quick)
    log("Running permutation importance")
    perm_X = X_eval
    perm_y = y_eval
    if args.permute_subsample and len(X_eval) > args.permute_subsample:
        idx = rng.choice(len(X_eval), size=args.permute_subsample, replace=False)
        perm_X = X_eval.iloc[idx]
        perm_y = y_eval[idx]
    y_bin = ((perm_y["event"]) & (perm_y["time"] <= rank_T)).astype(int).to_numpy()
    hrest = HorizonRiskEstimator(pipe, horizon_days=rank_T, batch_size=args.predict_batch_size)
    perm = permutation_importance(hrest, perm_X, y_bin, n_repeats=6, random_state=args.random_state)
    imp_df = pd.DataFrame({"feature": X_test.columns, "importance": perm.importances_mean}).sort_values("importance", ascending=False)
    imp_df.to_csv(os.path.join(args.out, f"permutation_importance_{rank_T}d.csv"), index=False)

    # 11) Calibration @ rank_T
    cal_df = calibration_curve_at_T(y_test, risks_by_T[rank_T], rank_T, n_bins=10)
    cal_df.to_csv(os.path.join(args.out, f"calibration_{rank_T}d.csv"), index=False)

    plt.figure()
    plt.plot([0,1],[0,1], linestyle="--")
    plt.scatter(cal_df["pred"], cal_df["obs"])
    plt.xlabel(f"Predicted P(event by {rank_T}d)")
    plt.ylabel(f"Observed P(event by {rank_T}d) (KM)")
    plt.title(f"Calibration @ {rank_T} days (test)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, f"calibration_{rank_T}d.png"), dpi=160)
    plt.close()

    # 12) Console summary
    print("=== RSF Results ===")
    print(f"C-index: {cindex:.3f}")
    print(f"IBS: {ibs:.3f}")
    for T in horizons:
        print(f"AUC@{T}d: {aucs[T]:.3f} | Brier@{T}d: {briers[T]:.3f}")
    print(f"Saved outputs in: {os.path.abspath(args.out)}")

if __name__ == "__main__":
    """
    python fit_rsf.py --data synthetic_attrition_2007_2025.csv --out out_rsf --horizons 90 180 270 --n_estimators 300 --max_depth 12 --n_jobs 4 --predict_batch_size 1000 --eval_subsample 15000 --permute_subsample 2000
    """
    main()
