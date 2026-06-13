import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
from src.config import PROCESSED_DIR, REGRESSION_RESULTS, ANOMALY_DISTRICTS, SEED


MGNREGA_FEATURES = [
    "literacy_rate", "rural_pct", "sc_pct", "st_pct",
    "below_poverty_pct", "agri_worker_pct", "latrine_pct",
    "electricity_pct", "women_literacy_pct", "worker_pct", "muslim_pct",
]

HEALTH_INS_FEATURES = [
    "literacy_rate", "rural_pct", "sc_pct", "st_pct",
    "below_poverty_pct", "institutional_births_pct",
    "electricity_pct", "anc_4plus_pct", "full_vaccination_pct",
    "worker_pct", "muslim_pct", "sex_ratio",
]

MGNREGA_EXPANDED = [
    "literacy_rate", "rural_pct", "sc_pct", "st_pct",
    "below_poverty_pct", "agri_worker_pct", "worker_pct",
    "electricity_pct", "latrine_pct", "lpg_pct", "tv_pct", "phone_pct",
    "women_literacy_pct", "institutional_births_pct",
    "stunting_pct", "anc_4plus_pct", "full_vaccination_pct",
    "clean_fuel_pct", "improved_sanitation_pct",
    "muslim_pct",
    "mgnrega_allocation_rate", "mgnrega_avg_person_days",
    "mgnrega_100day_rate", "mgnrega_women_work_share",
    "mgnrega_expenditure_per_hh", "mgnrega_sc_work_share", "mgnrega_st_work_share",
    "mgnrega_works_per_hh",
]


def make_state_dummies(df):
    return pd.get_dummies(df["state"], prefix="state", drop_first=True).astype(float)


def run_ols(df, target, features, robust=True):
    X = df[features].copy().astype(float)
    y = df[target].copy().astype(float)
    mask = X.notna().all(axis=1) & y.notna()
    X = X.loc[mask]
    y = y.loc[mask]
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    if robust:
        result = model.fit(cov_type="HC3")
    else:
        result = model.fit()
    return result, mask


def run_ols_fe(df, target, features, robust=True):
    state_dummies = make_state_dummies(df)
    X = pd.concat([df[features].astype(float), state_dummies], axis=1)
    y = df[target].copy().astype(float)
    mask = X.notna().all(axis=1) & y.notna()
    X = X.loc[mask]
    y = y.loc[mask]
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    if robust:
        result = model.fit(cov_type="HC3")
    else:
        result = model.fit()
    return result, mask


def compute_vif(df, features):
    X = df[features].dropna().astype(float)
    X = sm.add_constant(X)
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i)
        for i in range(X.shape[1])
    ]
    vif_data = vif_data[vif_data["feature"] != "const"].reset_index(drop=True)
    return vif_data


def detect_anomalies(df, result, target, features, use_fe=True, threshold_percentile=5):
    if use_fe:
        state_dummies = make_state_dummies(df)
        X = pd.concat([df[features].astype(float), state_dummies], axis=1)
    else:
        X = df[features].copy().astype(float)
    mask = X.notna().all(axis=1) & df[target].notna()
    df_sub = df.loc[mask].copy()
    X_sub = sm.add_constant(X.loc[mask])
    predicted = result.predict(X_sub)
    residuals = df_sub[target].astype(float) - predicted
    std_residuals = (residuals - residuals.mean()) / residuals.std()
    anomaly_threshold = np.percentile(std_residuals, 100 - threshold_percentile)
    anomalies = df_sub[std_residuals >= anomaly_threshold].copy()
    anomalies["residual"] = residuals.loc[anomalies.index]
    anomalies["std_residual"] = std_residuals.loc[anomalies.index]
    anomalies["predicted_gap"] = predicted.loc[anomalies.index]
    anomalies = anomalies.sort_values("std_residual", ascending=False)
    return anomalies, std_residuals


def variance_decomposition(df, target, features):
    state_dummies = make_state_dummies(df)
    y = df[target].astype(float)
    mask_demo = df[features].notna().all(axis=1) & y.notna()
    mask_state = state_dummies.notna().all(axis=1) & y.notna()
    mask_joint = mask_demo & mask_state
    X_demo = sm.add_constant(df.loc[mask_joint, features].astype(float))
    X_state = sm.add_constant(state_dummies.loc[mask_joint])
    X_joint = pd.concat([df.loc[mask_joint, features].astype(float), state_dummies.loc[mask_joint]], axis=1)
    X_joint = sm.add_constant(X_joint)
    y_sub = y.loc[mask_joint]
    r_demo = sm.OLS(y_sub, X_demo).fit().rsquared
    r_state = sm.OLS(y_sub, X_state).fit().rsquared
    r_joint = sm.OLS(y_sub, X_joint).fit(cov_type="HC3").rsquared
    return {
        "r_demographics": r_demo,
        "r_state_fe": r_state,
        "r_joint": r_joint,
        "demographics_add": r_joint - r_state,
        "state_adds": r_joint - r_demo,
    }


def prepare_mgnrega_panel(mgnrega_all):
    renames = {
        "State": "state", "District": "district", "Year": "year",
        "Households that demanded work": "hh_demanded_work",
        "Households that were allotted work": "hh_allotted_work",
        "Households that worked under mahatma gandhi national rural employment guarantee act (mgnrega)": "hh_worked",
        "Job cards issued": "job_cards_issued",
        "Total person days": "persondays_total",
        "Total person days worked by women": "persondays_women",
        "Households that reached a 100 day limit": "hh_100day",
        "Scheduled caste houeholds that worked": "hh_sc_worked",
        "Scheduled tribe houeholds that worked": "hh_st_worked",
        "Labour expenditure that has been disbursed": "labour_expenditure",
        "Material expenditure that has been disbursed": "material_expenditure",
        "Works under mahatma gandhi national rural employment guarantee act (mgnrega)": "works_completed",
        "Persons that worked under mahatma gandhi national rural employment guarantee act (mgnrega)": "persons_worked",
        "Households that applied for a job card": "hh_applied",
        "Job cards issued for scheduled caste": "job_cards_sc",
        "Job cards issued for scheduled tribes": "job_cards_st",
    }
    panel = mgnrega_all.rename(columns={k: v for k, v in renames.items() if k in mgnrega_all.columns}).copy()
    from src.data_cleaner import normalize_state_name, normalize_district_name
    panel["state"] = panel["state"].apply(normalize_state_name)
    panel["district"] = panel["district"].apply(normalize_district_name)

    panel["gap_pct"] = np.where(panel["hh_demanded_work"] > 0,
        (panel["hh_demanded_work"] - panel["hh_worked"]) / panel["hh_demanded_work"] * 100, np.nan)
    panel["avg_pd"] = np.where(panel["hh_worked"] > 0, panel["persondays_total"] / panel["hh_worked"], np.nan)
    panel["women_share"] = np.where(panel["persondays_total"] > 0, panel["persondays_women"] / panel["persondays_total"] * 100, np.nan)
    panel["alloc_rate"] = np.where(panel["hh_demanded_work"] > 0, panel["hh_allotted_work"] / panel["hh_demanded_work"] * 100, np.nan)
    panel["day100_rate"] = np.where(panel["hh_worked"] > 0, panel["hh_100day"] / panel["hh_worked"] * 100, np.nan)
    panel["demand_rate"] = np.where(panel["job_cards_issued"] > 0, panel["hh_demanded_work"] / panel["job_cards_issued"] * 100, np.nan)
    panel["exp_per_hh"] = np.where(panel["hh_worked"] > 0, panel["labour_expenditure"] / panel["hh_worked"], np.nan)
    panel["sc_share"] = np.where(panel["hh_worked"] > 0, panel["hh_sc_worked"] / panel["hh_worked"] * 100, np.nan)
    panel["st_share"] = np.where(panel["hh_worked"] > 0, panel["hh_st_worked"] / panel["hh_worked"] * 100, np.nan)
    panel["works_per_hh"] = np.where(panel["hh_worked"] > 0, panel["works_completed"] / panel["hh_worked"], np.nan)
    panel["pd_per_person"] = np.where(panel["persons_worked"] > 0, panel["persondays_total"] / panel["persons_worked"], np.nan)
    panel["sc_card_share"] = np.where(panel["job_cards_issued"] > 0, panel["job_cards_sc"] / panel["job_cards_issued"] * 100, np.nan)
    panel["st_card_share"] = np.where(panel["job_cards_issued"] > 0, panel["job_cards_st"] / panel["job_cards_issued"] * 100, np.nan)
    panel["mat_per_work"] = np.where(panel["works_completed"] > 0, panel["material_expenditure"] / panel["works_completed"], np.nan)

    panel = panel.sort_values(["state", "district", "year"])
    for col in ["gap_pct", "avg_pd", "alloc_rate", "demand_rate", "exp_per_hh", "day100_rate", "works_per_hh"]:
        panel[f"{col}_lag1"] = panel.groupby(["state", "district"])[col].shift(1)

    return panel


PANEL_FEATURES = [
    "avg_pd", "women_share", "alloc_rate", "day100_rate", "demand_rate",
    "exp_per_hh", "sc_share", "st_share", "works_per_hh", "pd_per_person",
    "sc_card_share", "st_card_share", "mat_per_work",
    "gap_pct_lag1", "avg_pd_lag1", "alloc_rate_lag1", "demand_rate_lag1",
    "exp_per_hh_lag1", "day100_rate_lag1", "works_per_hh_lag1",
]


def run_panel_model(panel):
    existing = [f for f in PANEL_FEATURES if f in panel.columns]
    year_dummies = pd.get_dummies(panel["year"], prefix="yr", drop_first=True).astype(float)
    dist_key = panel["district"] + "_" + panel["state"]
    dist_dummies = pd.get_dummies(dist_key, prefix="d", drop_first=True).astype(float)

    X = pd.concat([panel[existing].astype(float), year_dummies], axis=1)
    y = panel["gap_pct"].astype(float)
    mask = X.notna().all(axis=1) & y.notna() & np.isfinite(y)

    X_full = pd.concat([X.loc[mask], dist_dummies.loc[mask]], axis=1)
    y_sub = y.loc[mask]

    model = sm.OLS(y_sub, sm.add_constant(X_full)).fit(
        cov_type="cluster",
        cov_kwds={"groups": panel.loc[mask, "state"]}
    )
    summary = {
        "n_obs": int(mask.sum()),
        "r_squared": model.rsquared,
        "adj_r_squared": model.rsquared_adj,
        "n_districts": panel.loc[mask, "district"].nunique(),
        "n_years": panel.loc[mask, "year"].nunique(),
    }
    return model, summary, existing


def run_full_analysis(df, scheme="mgnrega"):
    if scheme == "mgnrega":
        target = "mgnrega_gap_pct"
        features = MGNREGA_FEATURES
    else:
        target = "health_insurance_gap_pct"
        features = HEALTH_INS_FEATURES

    result_base, mask_base = run_ols(df, target, features, robust=True)
    result_fe, mask_fe = run_ols_fe(df, target, features, robust=True)
    vif = compute_vif(df, features)
    anomalies, std_residuals = detect_anomalies(df, result_fe, target, features, use_fe=True)
    vdec = variance_decomposition(df, target, features)

    if scheme == "mgnrega":
        result_expanded, mask_exp = run_ols_fe(df, target, MGNREGA_EXPANDED, robust=True)
    else:
        result_expanded = None

    summary = {
        "scheme": scheme,
        "target": target,
        "n_obs": int(mask_fe.sum()),
        "r_squared_base": result_base.rsquared,
        "adj_r_squared_base": result_base.rsquared_adj,
        "r_squared_fe": result_fe.rsquared,
        "adj_r_squared_fe": result_fe.rsquared_adj,
        "f_statistic": result_fe.fvalue,
        "f_pvalue": result_fe.f_pvalue,
        "aic": result_fe.aic,
        "bic": result_fe.bic,
        "var_demo": vdec["r_demographics"],
        "var_state": vdec["r_state_fe"],
        "var_joint": vdec["r_joint"],
        "demo_adds_over_state": vdec["demographics_add"],
        "state_adds_over_demo": vdec["state_adds"],
    }
    if result_expanded is not None:
        summary["r_squared_expanded_fe"] = result_expanded.rsquared

    return {
        "model_base": result_base,
        "model_fe": result_fe,
        "model_expanded": result_expanded,
        "vif": vif,
        "anomalies": anomalies,
        "std_residuals": std_residuals,
        "mask": mask_fe,
        "summary": summary,
        "var_decomposition": vdec,
    }


def save_regression_results(mgnrega_result, health_ins_result):
    rows = []
    for name, result in [("MGNREGA", mgnrega_result), ("Health Insurance", health_ins_result)]:
        for feat, coef, pval in zip(
            result["model_fe"].params.index,
            result["model_fe"].params.values,
            result["model_fe"].pvalues.values,
        ):
            ci = result["model_fe"].conf_int().loc[feat]
            rows.append({
                "scheme": name,
                "variable": feat,
                "coefficient": coef,
                "p_value": pval,
                "ci_lower": ci[0],
                "ci_upper": ci[1],
                "significant_05": pval < 0.05,
            })
    df = pd.DataFrame(rows)
    df.to_csv(REGRESSION_RESULTS, index=False)
    return df


def save_anomaly_districts(mgnrega_anomalies, health_ins_anomalies):
    mgnrega_anomalies = mgnrega_anomalies.copy()
    health_ins_anomalies = health_ins_anomalies.copy()
    mgnrega_anomalies["scheme"] = "MGNREGA"
    health_ins_anomalies["scheme"] = "Health Insurance"
    combined = pd.concat([mgnrega_anomalies, health_ins_anomalies], ignore_index=True)
    combined.to_csv(ANOMALY_DISTRICTS, index=False)
    return combined
