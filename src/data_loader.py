import pandas as pd
import numpy as np
from src.config import MGNREGA_RAW, CENSUS_RAW, NFHS_RAW


def load_census(filepath=CENSUS_RAW):
    df = pd.read_csv(filepath)
    df = df.rename(columns={
        "District code": "district_code",
        "State name": "state",
        "District name": "district",
    })
    return df


def load_nfhs(filepath=NFHS_RAW):
    df = pd.read_csv(filepath)
    df = df.rename(columns={
        "District Names": "district",
        "State/UT": "state",
    })
    return df


def load_mgnrega(filepath=MGNREGA_RAW, year="2019-20"):
    df = pd.read_csv(filepath)
    df = df.rename(columns={
        "State": "state",
        "District": "district",
        "Year": "year",
        "Households that applied for a job card": "hh_applied_job_card",
        "Job cards issued": "job_cards_issued",
        "Job cards issued for scheduled caste": "job_cards_sc",
        "Job cards issued for scheduled tribes": "job_cards_st",
        "Households that demanded work": "hh_demanded_work",
        "Persons who demanded work": "persons_demanded_work",
        "Households that were allotted work": "hh_allotted_work",
        "Persons that were allotted work": "persons_allotted_work",
        "Households that worked under mahatma gandhi national rural employment guarantee act (mgnrega)": "hh_worked",
        "Persons that worked under mahatma gandhi national rural employment guarantee act (mgnrega)": "persons_worked",
        "Households that reached a 100 day limit": "hh_100day",
        "Scheduled caste houeholds that worked": "hh_sc_worked",
        "Total person days worked scheduled caste persons": "persondays_sc",
        "Scheduled tribe houeholds that worked": "hh_st_worked",
        "Total person days worked scheduled tribe persons": "persondays_st",
        "Total person days worked by women": "persondays_women",
        "Total person days": "persondays_total",
        "Labour expenditure that has been disbursed": "labour_expenditure",
        "Material expenditure that has been disbursed": "material_expenditure",
        "Amount sanctioned": "amount_sanctioned",
        "Works under mahatma gandhi national rural employment guarantee act (mgnrega)": "works_completed",
        "Total bank accounts": "bank_accounts",
        "Individual bank accounts": "individual_bank_accounts",
    })
    df_latest = df[df["year"] == year].copy()
    return df_latest, df


def validate_district_coverage(df, name="dataset"):
    n_states = df["state"].nunique()
    n_districts = df["district"].nunique()
    null_districts = df["district"].isna().sum()
    dup_districts = df.duplicated(subset=["state", "district"]).sum()
    print(f"[{name}] States: {n_states}, Districts: {n_districts}, "
          f"Null districts: {null_districts}, Duplicates: {dup_districts}")
    return {
        "dataset": name, "n_states": n_states, "n_districts": n_districts,
        "null_districts": null_districts, "duplicate_districts": dup_districts,
    }


def load_all_data(mgnrega_year="2019-20"):
    census = load_census()
    nfhs = load_nfhs()
    mgnrega, mgnrega_all = load_mgnrega(year=mgnrega_year)
    reports = [
        validate_district_coverage(census, "Census"),
        validate_district_coverage(nfhs, "NFHS-5"),
        validate_district_coverage(mgnrega, "MGNREGA"),
    ]
    report_df = pd.DataFrame(reports)
    return census, nfhs, mgnrega, mgnrega_all, report_df
