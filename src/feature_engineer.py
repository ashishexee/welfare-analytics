import pandas as pd
import numpy as np
from src.config import MASTER_DATA, PROCESSED_DIR, SEED


def compute_mgnrega_features(df):
    df = df.copy()
    df["mgnrega_participation_rate"] = np.where(
        df["hh_demanded_work"] > 0,
        df["hh_worked"] / df["hh_demanded_work"] * 100,
        np.nan
    )
    df["mgnrega_gap_pct"] = np.where(
        df["hh_demanded_work"] > 0,
        (df["hh_demanded_work"] - df["hh_worked"]) / df["hh_demanded_work"] * 100,
        np.nan
    )
    df["mgnrega_allocation_rate"] = np.where(
        df["hh_demanded_work"] > 0,
        df["hh_allotted_work"] / df["hh_demanded_work"] * 100,
        np.nan
    )
    df["mgnrega_avg_person_days"] = np.where(
        df["hh_worked"] > 0,
        df["persondays_total"] / df["hh_worked"],
        np.nan
    )
    df["mgnrega_sc_work_share"] = np.where(
        df["hh_worked"] > 0,
        df["hh_sc_worked"] / df["hh_worked"] * 100,
        np.nan
    )
    df["mgnrega_st_work_share"] = np.where(
        df["hh_worked"] > 0,
        df["hh_st_worked"] / df["hh_worked"] * 100,
        np.nan
    )
    df["mgnrega_women_work_share"] = np.where(
        df["persondays_total"] > 0,
        df["persondays_women"] / df["persondays_total"] * 100,
        np.nan
    )
    df["mgnrega_expenditure_per_hh"] = np.where(
        df["hh_worked"] > 0,
        df["labour_expenditure"] / df["hh_worked"],
        np.nan
    )
    df["mgnrega_100day_rate"] = np.where(
        df["hh_worked"] > 0,
        df["hh_100day"] / df["hh_worked"] * 100,
        np.nan
    )
    df["mgnrega_demand_rate"] = np.where(
        df["job_cards_issued"] > 0,
        df["hh_demanded_work"] / df["job_cards_issued"] * 100,
        np.nan
    )
    df["mgnrega_works_per_hh"] = np.where(
        df["hh_worked"] > 0,
        df["works_completed"] / df["hh_worked"],
        np.nan
    )
    return df


def compute_health_insurance_gap(df):
    df = df.copy()
    df["health_insurance_gap_pct"] = np.where(
        df["health_insurance_pct"].notna(),
        100 - df["health_insurance_pct"],
        np.nan
    )
    return df


def compute_combined_features(df):
    df = df.copy()
    df["vulnerable_pct"] = df["sc_pct"] + df["st_pct"]
    df["combined_gap_score"] = (
        df["mgnrega_gap_pct"].fillna(0) * 0.5 +
        df["health_insurance_gap_pct"].fillna(0) * 0.5
    )
    df["literacy_x_rural"] = df["literacy_rate"] * df["rural_pct"]
    df["vulnerable_x_bpl"] = df["vulnerable_pct"] * df["below_poverty_pct"]
    return df


def build_features(df):
    df = compute_mgnrega_features(df)
    df = compute_health_insurance_gap(df)
    df = compute_combined_features(df)
    return df
