# synthetic_attrition_generator_v4.py
# - Avg active headcount ~8k, with shock-driven dips into the 7k range
# - Office removed; years_experience_at_hire added
# - Early exits common, 6–30y rarer, 30y+ mostly retire
# - Computing depts more "poachable" than physics/life/HR

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

SEED = 7
np.random.seed(SEED)

START = pd.Timestamp("2007-01-01")
END   = pd.Timestamp("2025-12-31")
SNAPSHOT = END

# ---------- Headcount control ----------
TARGET_HEADCOUNT   = 8000
START_HEADCOUNT    = 8000
REPLACEMENT_RATIO  = 0.93          # baseline replacement of monthly attritions
BASELINE_HIRES     = 40            # small steady intake
FEEDBACK_GAIN      = 0.06          # pull back toward target
MAX_FEEDBACK_STEP  = 400           # avoid whiplash

# ---------- Attrition count shape (per month) ----------
BASELINE = 90
SEASONAL_AMPL = 14
BUS_CYCLE_AMPL = 10
NOISE_SD = 6
SHOCKS = [
    {"center": "2009-05-01", "ampl": 200, "width": 2.0},
    {"center": "2018-10-01", "ampl": 95,  "width": 1.3},
    {"center": "2022-03-01", "ampl": 70,  "width": 1.0},
]

# Hiring reaction to shocks:
# - "core" window (center-1 .. center+1): strong freeze
# - "extended" recovery (center+2 .. center+7): slow ramp
CORE_RR_MULT   = 0.25   # multiply replacement ratio in core window
CORE_BASE_MULT = 0.20   # multiply baseline hires in core window
CORE_FB_MULT   = 0.40   # multiply feedback in core window (slows recovery)
EXT_RR_MULT    = 0.70   # extended window (first 6 months after core)
EXT_BASE_MULT  = 0.60
EXT_FB_MULT    = 0.70

# ---------- Category spaces ----------
DEPARTMENTS = [
    "Software","IT","DataScience","Hardware","Product",
    "Sales","Marketing","Finance","HR","Operations",
    "Support","Legal","LifeSciences","Physics"
]
JOB_FAMILIES = ["IC","Mgr","Exec","SalesIC","SalesMgr","OpsIC","OpsMgr","TechLead"]
LEVELS       = [f"L{i}" for i in range(1,9)]
EDU          = ["HS","Assoc","Bach","Master","PhD"]
GENDER       = ["F","M","X"]
CONTRACT     = ["FTE","Contractor"]
VISA         = ["None","H1B","L1","Other"]
PRODUCTS     = ["Core","Platform","Payments","Ads","Cloud","HW","Services","Internal"]

# External opportunity pressure per dept (SV-ish)
DEPT_OPPORTUNITY = {
    "Software":1.30, "IT":1.18, "DataScience":1.25, "Hardware":1.12, "Product":1.10,
    "Sales":1.03, "Marketing":1.00, "Finance":0.98, "HR":0.90, "Operations":0.97,
    "Support":0.96, "Legal":0.92, "LifeSciences":0.92, "Physics":0.88
}

# ---------- Helpers ----------
def month_range(start, end):
    out, t = [], pd.Timestamp(start.year, start.month, 1)
    while t <= end:
        out.append(t); t = t + relativedelta(months=1)
    return pd.Index(out)

def month_index(dates, m):
    return int((m.year - dates[0].year) * 12 + (m.month - dates[0].month))

def gaussian_pulse(x, mu, sigma): return np.exp(-0.5*((x-mu)/sigma)**2)
def sigmoid(z): return 1/(1+np.exp(-z))
def rchoice(a, size=None, p=None): return np.random.choice(a, size=size, p=p)

# ---------- Build monthly attrition counts ----------
months = month_range(START, END)
T = len(months); t = np.arange(T)
seasonality = SEASONAL_AMPL * np.sin(2*np.pi*(t % 12)/12.0 + 0.8)
bus_cycle   = BUS_CYCLE_AMPL * np.sin(2*np.pi*t/60.0 - 1.1)
shock_curve = np.zeros(T)
for s in SHOCKS:
    mu = month_index(months, pd.Timestamp(s["center"]))
    shock_curve += s["ampl"] * gaussian_pulse(t, mu, s["width"])
raw_counts = BASELINE + seasonality + bus_cycle + shock_curve + np.random.normal(0, NOISE_SD, T)
counts = np.clip(np.round(raw_counts).astype(int), 20, None)

# Identify core and extended shock windows
core_shock_months = set()
extended_shock_months = set()
for s in SHOCKS:
    c = pd.Timestamp(s["center"])
    for k in range(-1, 2):  # center-1 .. center+1
        core_shock_months.add(pd.Timestamp(c.year, c.month, 1) + relativedelta(months=k))
    for k in range(2, 8):   # +2 .. +7
        extended_shock_months.add(pd.Timestamp(c.year, c.month, 1) + relativedelta(months=k))

# ---------- Employee factory (≈30 features; no "office") ----------
EMP_ID = 1
def new_hires(n, month_start):
    global EMP_ID
    month_end = month_start + relativedelta(months=1) - relativedelta(days=1)
    days_in_month = (month_end - month_start).days + 1
    hire_days = month_start + pd.to_timedelta(np.random.randint(0, days_in_month, size=n), unit="D")

    dept = rchoice(DEPARTMENTS, size=n)
    fam  = rchoice(JOB_FAMILIES, size=n)
    lvl  = rchoice(LEVELS, size=n)
    edu  = rchoice(EDU, size=n)
    gen  = rchoice(GENDER, size=n, p=[0.45,0.45,0.10])
    contr= rchoice(CONTRACT, size=n, p=[0.93,0.07])
    visa = rchoice(VISA, size=n, p=[0.80,0.13,0.04,0.03])
    prod = rchoice(PRODUCTS, size=n)

    age_at_hire = np.clip(np.random.normal(30, 7, size=n), 18, 60)
    exp_raw = np.random.gamma(2.5, 2.0, size=n)  # mean ~5y
    years_experience = np.minimum(exp_raw, np.maximum(age_at_hire - 18, 0))
    remote = (np.random.rand(n) < 0.18).astype(int)

    manager_span = np.clip(np.random.normal(6, 3, size=n), 0, 30).astype(int)
    comp_ratio = np.clip(np.random.normal(1.0, 0.12, size=n), 0.6, 1.6)
    perf_rating = np.clip(np.round(np.random.normal(3.4, 0.8, size=n)), 1, 5).astype(int)
    pip_flag = (np.random.rand(n) < 0.035).astype(int)
    engagement = np.clip(np.random.normal(72, 12, size=n), 0, 100)
    salary_band = rchoice(np.arange(1,10), size=n)
    base_pay = np.clip(np.random.normal(75000 + 9000*salary_band, 12000, size=n), 35000, 450000)
    var_pay_pct = np.clip(np.random.normal(0.07 + (fam=="SalesIC")*0.08 + (fam=="SalesMgr")*0.12, 0.03, n), 0, 0.45)
    commute_km = np.where(remote==1, 0, np.clip(np.random.exponential(8, size=n), 0, 60))
    union_member = (np.random.rand(n) < 0.08).astype(int)
    stock_grants = np.clip(np.random.normal(15000 + 1500*salary_band, 8000, size=n), 0, 220000)
    promos_3y = np.clip(np.random.poisson(0.3, size=n), 0, 3)
    training_hours = np.clip(np.random.normal(24, 10, size=n), 0, 200)
    overtime_hours = np.clip(np.random.normal(8, 10, size=n), 0, 80)
    team_size = np.clip(np.random.normal(12, 6, size=n), 1, 60).astype(int)
    travel_pct = np.clip(np.random.normal(0.07, 0.06, size=n) + (fam=="SalesIC")*0.07, 0, 0.6)
    schedule_flex = np.clip(np.random.normal(0.6, 0.15, size=n), 0, 1)
    market_pay_index = np.clip(np.random.normal(1.0, 0.07, size=n), 0.7, 1.5)
    org_changes_1y = np.clip(np.random.poisson(0.6, size=n), 0, 6)

    ids = np.arange(EMP_ID, EMP_ID+n); EMP_ID += n
    df = pd.DataFrame({
        "employee_id": ids, "hire_date": hire_days,
        "department": dept, "job_family": fam, "level": lvl,
        "manager_span": manager_span, "age_at_hire": np.round(age_at_hire,1),
        "gender": gen, "education_level": edu, "comp_ratio": np.round(comp_ratio,3),
        "salary_band": salary_band, "base_pay": np.round(base_pay,2),
        "variable_pay_pct": np.round(var_pay_pct,3), "perf_rating": perf_rating,
        "pip_flag": pip_flag, "engagement_score": np.round(engagement,1), "remote": remote,
        "contract_type": contr, "years_experience_at_hire": np.round(years_experience,1),
        "visa_status": visa, "commute_km": np.round(commute_km,1), "union_member": union_member,
        "stock_grants": np.round(stock_grants,2), "promotions_last_3y": promos_3y,
        "training_hours_last_yr": np.round(training_hours,1), "overtime_hours_mo": np.round(overtime_hours,1),
        "team_size": team_size, "product_area": prod, "travel_pct": np.round(travel_pct,3),
        "schedule_flexibility": np.round(schedule_flex,3), "market_pay_index": np.round(market_pay_index,3),
        "org_changes_last_yr": org_changes_1y,
    })
    df["attrition_date"] = pd.NaT
    df["event"] = 0
    df["event_type"] = None
    return df

# Seed population back 35y so 30y+ tenure exists
def seed_population(n):
    hire_start = START - relativedelta(years=35)
    span_days = (START - hire_start).days
    pop = new_hires(n, hire_start)
    pop["hire_date"] = hire_start + pd.to_timedelta(np.random.randint(0, span_days, size=n), unit="D")
    return pop

active = seed_population(START_HEADCOUNT)
everyone = []

dept_base_risk = {d: np.clip(np.random.normal(1.0, 0.06), 0.88, 1.18) for d in DEPARTMENTS}
family_risk    = {f: np.clip(np.random.normal(1.0, 0.10), 0.82, 1.25) for f in JOB_FAMILIES}

# ---------- Risk model for sampling who leaves ----------
def risk_weights(df, month_start):
    tenure = ((month_start - df["hire_date"]).dt.days.clip(lower=0) / 365.25).values
    age_now = df["age_at_hire"].values + tenure
    exp_at_hire = df["years_experience_at_hire"].values

    early_peak = 1.8 * np.exp(-0.5*((tenure-2.0)/1.3)**2) + 0.6*np.exp(-tenure/3.5)
    mid_dip    = 0.6 * np.exp(-0.5*((tenure-14)/6.0)**2)
    late_rise  = 0.5 * sigmoid((tenure-30)/2.0) + 0.6 * (age_now>62)

    perf = (5 - df["perf_rating"].values)/4.0
    low_comp = np.clip(1.0 - df["comp_ratio"].values, 0, 0.6)
    pip = df["pip_flag"].values * 1.8
    engagement = np.clip((100 - df["engagement_score"].values)/100.0, 0, 1.0)
    overtime = df["overtime_hours_mo"].values/80.0
    promos = (df["promotions_last_3y"].values==0).astype(float)*0.25
    contractor = (df["contract_type"].values=="Contractor").astype(float)*0.6
    visa = (df["visa_status"].values!="None").astype(float)*0.12
    union = df["union_member"].values*0.1
    exp_effect = 0.25 * sigmoid((6 - exp_at_hire)/1.5)

    dept_mul = np.array([dept_base_risk[d] for d in df["department"].values])
    fam_mul  = np.array([family_risk[f] for f in df["job_family"].values])

    opp = np.array([DEPT_OPPORTUNITY[d] for d in df["department"].values])
    opp_factor = 0.6 + 0.6*sigmoid((6 - np.maximum(tenure, 0.1))) + 0.25*sigmoid((18 - tenure))
    opp_effect = opp ** opp_factor

    w = (0.6 + early_peak - mid_dip + late_rise + exp_effect
         + 0.7*perf + 0.5*low_comp + pip + 0.7*engagement + 0.3*overtime
         + promos + contractor + visa + union)
    w = np.clip(w, 1e-6, None) * dept_mul * fam_mul * opp_effect
    return w + np.random.rand(len(w))*0.05

# ---------- Simulation ----------
monthly_attr = []
monthly_head = []

for i, m in enumerate(months):
    # 1) Attritions: take from prebuilt counts
    M = int(min(counts[i], len(active)))

    # 2) Choose leavers by risk
    w = risk_weights(active, m)
    idx = np.random.choice(active.index.values, size=M, replace=False, p=w/w.sum())
    leaving = active.loc[idx].copy()

    # 3) Dates & event types
    month_end = m + relativedelta(months=1) - relativedelta(days=1)
    dpm = (month_end - m).days + 1
    leave_days = m + pd.to_timedelta(np.random.randint(0, dpm, size=M), unit="D")
    leaving["attrition_date"] = leave_days
    leaving["event"] = 1

    tenure_now = ((m - leaving["hire_date"]).dt.days.values/365.25)
    age_now = leaving["age_at_hire"].values + tenure_now
    dept_opp = np.array([DEPT_OPPORTUNITY[d] for d in leaving["department"].values])

    # Layoffs spike in core, elevated in extended
    if m in core_shock_months:
        p_layoff = 0.45
    elif m in extended_shock_months:
        p_layoff = 0.25
    else:
        p_layoff = 0.07

    retire_signal = (tenure_now-30)/2.2 + (age_now-60)/3.0
    p_retire = 0.95 * sigmoid(retire_signal)
    p_perf   = 0.04 + 0.18*(leaving["pip_flag"].values==1)
    base_quit = 0.45 * (1 - 0.6*sigmoid((tenure_now-28)/2.0))
    p_quit_raw = base_quit * (0.9 + 0.4*(dept_opp-1.0))
    total = p_retire + p_perf + p_layoff + p_quit_raw
    p_retire, p_perf, p_quit = [x/total for x in (p_retire, p_perf, p_quit_raw)]
    p_layoff = p_layoff/total

    etypes = []
    for pr, pp, pl, pq in zip(p_retire, p_perf, np.full(M, p_layoff), p_quit):
        etypes.append(np.random.choice(["Retire","Performance","Layoff","Quit"], p=[pr,pp,pl,pq]))
    leaving["event_type"] = etypes

    # 4) Remove leavers
    monthly_attr.append({"month": m, "attritions": M})
    active = active.drop(index=idx)

    # 5) Hires with staged freeze/slow recovery
    gap = TARGET_HEADCOUNT - len(active)
    feedback = int(np.clip(FEEDBACK_GAIN * gap, -MAX_FEEDBACK_STEP, MAX_FEEDBACK_STEP))

    rr_mult = base_mult = fb_mult = 1.0
    if m in core_shock_months:
        rr_mult, base_mult, fb_mult = CORE_RR_MULT, CORE_BASE_MULT, CORE_FB_MULT
    elif m in extended_shock_months:
        rr_mult, base_mult, fb_mult = EXT_RR_MULT, EXT_BASE_MULT, EXT_FB_MULT

    hires_expected = (REPLACEMENT_RATIO * rr_mult) * M + (BASELINE_HIRES * base_mult) + (feedback * fb_mult)
    base_hires = int(max(0, np.random.poisson(max(0.0, hires_expected))))
    hires = new_hires(base_hires, m)
    active = pd.concat([active, hires], ignore_index=True)

    # 6) Record headcount after hiring
    monthly_head.append({"month": m, "active_headcount": len(active)})

    # 7) Bucket leavers
    everyone.append(leaving)

# Censor remaining actives
censored = active.copy()
censored["event"] = 0
censored["event_type"] = None
censored["attrition_date"] = pd.NaT
everyone.append(censored)

employees = pd.concat(everyone, ignore_index=True).sort_values("employee_id").reset_index(drop=True)
employees.loc[employees["attrition_date"].isna(), "event"] = 0
employees["attrition_date"] = employees["attrition_date"].where(employees["attrition_date"]<=SNAPSHOT, pd.NaT)

# ---------- Save ----------
employees.to_csv("synthetic_attrition_2007_2025.csv", index=False)
pd.DataFrame(monthly_attr).set_index("month").sort_index().to_csv("monthly_attrition_counts.csv")
pd.DataFrame(monthly_head).set_index("month").sort_index().to_csv("monthly_headcount.csv")

# ---------- Quick summary ----------
monthly = pd.read_csv("monthly_attrition_counts.csv", parse_dates=["month"]).set_index("month")
headc = pd.read_csv("monthly_headcount.csv", parse_dates=["month"]).set_index("month")
print("Rows (employees):", len(employees))
print("Events (attritions):", int((employees['event']==1).sum()))
print("Censored:", int((employees['event']==0).sum()))
print("Attritions — mean/min/max:", float(monthly['attritions'].mean()),
      int(monthly['attritions'].min()), int(monthly['attritions'].max()))
print("Headcount  — mean/min/max:", int(headc['active_headcount'].mean()),
      int(headc['active_headcount'].min()), int(headc['active_headcount'].max()))
