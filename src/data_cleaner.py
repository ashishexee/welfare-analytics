import pandas as pd
import numpy as np
import re
from src.config import PROCESSED_DIR, MASTER_DATA, SEED


DISTRICT_NAME_FIXES = {
    "bangalore": "bengaluru", "bangalore rural": "bengaluru rural",
    "bangalore urban": "bengaluru urban", "belgaum": "belagavi",
    "bellary": "ballari", "mysore": "mysuru", "gulbarga": "kalaburagi",
    "chikmagalur": "chikkamagaluru", "dakshin kannad": "dakshina kannada",
    "dakshin kanara": "dakshina kannada", "uttar kannad": "uttara kannada",
    "uttar kanara": "uttara kannada", "shimoga": "shivamogga",
    "mangalore": "mangaluru", "tumkur": "tumakuru",
    "badgam": "budgam", "baramula": "baramulla", "bandipore": "bandipora",
    "punch": "poonch", "shupiyan": "shopian",
    "leh(ladakh)": "leh", "doda": "doda",
    "kozhikode": "kozhikode", "trivandrum": "thiruvananthapuram",
    "alleppey": "alappuzha", "quinlon": "kollam", "cannanore": "kannur",
    "palghat": "palakkad", "trichur": "thrissur",
    "baroda": "vadodara",
    "calcutta": "kolkata", "kanpur city": "kanpur nagar",
    "lucknow city": "lucknow", "varanasi city": "varanasi",
    "allahabad": "prayagraj", "allhabad": "prayagraj",
    "faizabad": "ayodhya", "jyotiba phule nagar": "amroha",
    "kanshiram nagar": "kasganj",
    "chittaurgarh": "chittorgarh", "firozpur": "firozepur",
    "dakshin dinajpur": "dakshin dinajpur", "north twenty four parganas": "north 24 parganas",
    "south twenty four parganas": "south 24 parganas",
    "paschim medinipur": "paschim medinipur", "purba medinipur": "purba medinipur",
    "hugli": "hooghly", "haora": "howrah",
    "north  and middle andaman": "north and middle andaman",
    "south andaman": "south andaman",
    "nabarangapur": "nabarangpur", "saraikela-kharsawan": "saraikela kharsawan",
    "warangal": "warangal rural", "karimnagar": "karimnagar",
    "nizamabad": "nizamabad", "mahbubnagar": "mahabubnagar",
    "khammam": "khammam", "medak": "medak",
    "adilabad": "adilabad", "nalgonda": "nalgonda",
    "kushinagar": "kushinagar",
    "jaintia hills": "west jaintia hills",
    "mahamaya nagar": "hathras",
    "pondicherry": "puducherry",
    "nct of delhi": "delhi",
}


STATE_NAME_FIXES = {
    "jammu and kashmir": "jammu and kashmir",
    "jammu & kashmir": "jammu and kashmir",
    "orissa": "odisha", "nct of delhi": "delhi",
    "andaman & nicobar island": "andaman and nicobar islands",
    "andaman & nicobar islands": "andaman and nicobar islands",
    "andaman and nicobar islands": "andaman and nicobar islands",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "dadra & nagar haveli & daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "the dadra and nagar haveli and daman and diu": "dadra and nagar haveli and daman and diu",
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "chattisgarh": "chhattisgarh",
    "pondicherry": "puducherry",
    "telengana": "telangana",
    "maharastra": "maharashtra",
}


def normalize_district_name(name):
    if pd.isna(name):
        return name
    name = str(name).strip().lower()
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[^a-z\s\(\)]', '', name)
    name = name.strip()
    if name in DISTRICT_NAME_FIXES:
        name = DISTRICT_NAME_FIXES[name]
    return name


def normalize_state_name(name):
    if pd.isna(name):
        return name
    name = str(name).strip().lower()
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    for old, new in STATE_NAME_FIXES.items():
        if name == old:
            name = new
            break
    return name


TELANGANA_DISTRICTS = {
    "adilabad", "nizamabad", "karimnagar", "medak", "hyderabad",
    "rangareddy", "mahbubnagar", "nalgonda", "warangal", "khammam",
}


def remap_telangana_in_census(df):
    df = df.copy()
    mask = (df["state"] == "andhra pradesh") & (df["district"].isin(TELANGANA_DISTRICTS))
    df.loc[mask, "state"] = "telangana"
    return df


def clean_census(df):
    df = df.copy()
    df["state"] = df["state"].apply(normalize_state_name)
    df["district"] = df["district"].apply(normalize_district_name)
    df = remap_telangana_in_census(df)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(lower=0)
    return df


def clean_nfhs(df):
    df = df.copy()
    df["state"] = df["state"].apply(normalize_state_name)
    df["district"] = df["district"].apply(normalize_district_name)
    pct_cols = [c for c in df.columns if "(%)" in c or "(Rs.)" in c]
    for col in pct_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_mgnrega(df):
    df = df.copy()
    df["state"] = df["state"].apply(normalize_state_name)
    df["district"] = df["district"].apply(normalize_district_name)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(lower=0)
    return df


def derive_census_features(df):
    df = df.copy()
    df["population_total"] = df["Population"]
    df["sc_pct"] = np.where(df["Population"] > 0, df["SC"] / df["Population"] * 100, np.nan)
    df["st_pct"] = np.where(df["Population"] > 0, df["ST"] / df["Population"] * 100, np.nan)
    df["literacy_rate"] = np.where(df["Population"] > 0, df["Literate"] / df["Population"] * 100, np.nan)
    df["female_literacy_rate"] = np.where(df["Female"] > 0, df["Female_Literate"] / df["Female"] * 100, np.nan)
    df["rural_pct"] = np.where(df["Households"] > 0, df["Rural_Households"] / df["Households"] * 100, np.nan)
    df["sex_ratio"] = np.where(df["Male"] > 0, df["Female"] / df["Male"] * 1000, np.nan)
    df["worker_pct"] = np.where(df["Population"] > 0, df["Workers"] / df["Population"] * 100, np.nan)
    df["agri_worker_pct"] = np.where(df["Workers"] > 0, df["Agricultural_Workers"] / df["Workers"] * 100, np.nan)
    df["hindu_pct"] = np.where(df["Population"] > 0, df["Hindus"] / df["Population"] * 100, np.nan)
    df["muslim_pct"] = np.where(df["Population"] > 0, df["Muslims"] / df["Population"] * 100, np.nan)
    df["electricity_pct"] = np.where(df["Households"] > 0, df["Housholds_with_Electric_Lighting"] / df["Households"] * 100, np.nan)
    df["latrine_pct"] = np.where(df["Households"] > 0, df["Having_latrine_facility_within_the_premises_Total_Households"] / df["Households"] * 100, np.nan)
    df["internet_pct"] = np.where(df["Households"] > 0, df["Households_with_Internet"] / df["Households"] * 100, np.nan)
    df["below_poverty_pct"] = np.where(df["Total_Power_Parity"] > 0, df["Power_Parity_Less_than_Rs_45000"] / df["Total_Power_Parity"] * 100, np.nan)
    df["dilapidated_pct"] = np.where(df["Households"] > 0, df["Condition_of_occupied_census_houses_Dilapidated_Households"] / df["Households"] * 100, np.nan)
    df["lpg_pct"] = np.where(df["Households"] > 0, df["LPG_or_PNG_Households"] / df["Households"] * 100, np.nan)
    df["tv_pct"] = np.where(df["Households"] > 0, df["Households_with_Television"] / df["Households"] * 100, np.nan)
    df["phone_pct"] = np.where(df["Households"] > 0, df["Households_with_Telephone_Mobile_Phone"] / df["Households"] * 100, np.nan)
    return df


def derive_nfhs_features(df):
    df = df.copy()
    rename_map = {}
    for col in df.columns:
        if "health insurance" in col.lower() and "scheme" in col.lower():
            rename_map[col] = "health_insurance_pct"
        elif "electricity" in col.lower() and "living" in col.lower():
            rename_map[col] = "electricity_pct_nfhs"
        elif "improved drinking-water" in col.lower():
            rename_map[col] = "improved_water_pct"
        elif "improved sanitation" in col.lower():
            rename_map[col] = "improved_sanitation_pct"
        elif "clean fuel" in col.lower():
            rename_map[col] = "clean_fuel_pct"
        elif "women (age 15-49) who are literate" in col.lower():
            rename_map[col] = "women_literacy_pct"
        elif "married before age 18" in col.lower():
            rename_map[col] = "child_marriage_pct"
        elif "institutional births (in the 5 years" in col.lower():
            rename_map[col] = "institutional_births_pct"
        elif "fully vaccinated based on information from either" in col.lower():
            rename_map[col] = "full_vaccination_pct"
        elif "stunted (height-for-age)" in col.lower():
            rename_map[col] = "stunting_pct"
        elif "wasted (weight-for-height)" in col.lower() and "severely" not in col.lower():
            rename_map[col] = "wasting_pct"
        elif "underweight (weight-for-age)" in col.lower():
            rename_map[col] = "underweight_children_pct"
        elif "anaemic (<11.0 g/dl)" in col.lower() and "children" in col.lower():
            rename_map[col] = "anemia_children_pct"
        elif "all women age 15-49 years who are anaemic" in col.lower():
            rename_map[col] = "anemia_women_pct"
        elif "bmi is below normal" in col.lower():
            rename_map[col] = "underweight_women_pct"
        elif "overweight or obese" in col.lower() and "women" in col.lower():
            rename_map[col] = "overweight_women_pct"
        elif "tobacco" in col.lower() and "women" in col.lower():
            rename_map[col] = "tobacco_women_pct"
        elif "tobacco" in col.lower() and "men" in col.lower():
            rename_map[col] = "tobacco_men_pct"
        elif "alcohol" in col.lower() and "women" in col.lower():
            rename_map[col] = "alcohol_women_pct"
        elif "antenatal check-up in the first trimester" in col.lower():
            rename_map[col] = "anc_first_trimester_pct"
        elif "at least 4 antenatal care" in col.lower():
            rename_map[col] = "anc_4plus_pct"
        elif "iodized salt" in col.lower():
            rename_map[col] = "iodized_salt_pct"
        elif "birth was registered" in col.lower() and "civil" in col.lower():
            rename_map[col] = "birth_registration_pct"
        elif "population below age 15" in col.lower():
            rename_map[col] = "pop_below15_pct"
        elif "sex ratio of the total population" in col.lower():
            rename_map[col] = "sex_ratio_nfhs"
    df = df.rename(columns=rename_map)
    return df


def merge_all_data(census, nfhs, mgnrega):
    keys = ["state", "district"]
    census = census.drop_duplicates(subset=keys, keep="first")
    nfhs = nfhs.drop_duplicates(subset=keys, keep="first")
    mgnrega = mgnrega.drop_duplicates(subset=keys, keep="first")
    master = census.merge(nfhs, on=keys, how="outer", validate="1:1")
    master = master.merge(mgnrega, on=keys, how="left", validate="1:1")
    master = master.drop_duplicates(subset=keys)
    master = master.sort_values(keys).reset_index(drop=True)
    return master


def impute_missing(master):
    numeric_cols = master.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if master[col].isna().any():
            state_medians = master.groupby("state")[col].transform("median")
            master[col] = master[col].fillna(state_medians)
            overall_median = master[col].median()
            master[col] = master[col].fillna(overall_median)
    return master


def build_master_dataset(census, nfhs, mgnrega):
    census_clean = clean_census(census)
    census_feat = derive_census_features(census_clean)
    nfhs_clean = clean_nfhs(nfhs)
    nfhs_feat = derive_nfhs_features(nfhs_clean)
    mgnrega_clean = clean_mgnrega(mgnrega)
    master = merge_all_data(census_feat, nfhs_feat, mgnrega_clean)
    master = impute_missing(master)
    master.to_csv(MASTER_DATA, index=False)
    print(f"Master dataset saved: {len(master)} districts x {len(master.columns)} features")
    return master
