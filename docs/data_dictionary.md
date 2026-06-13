# Data Dictionary — Welfare Scheme Participation Analysis

## Master Dataset: `data/processed/master_district_data.csv`

722 districts × 304 features (288 raw + 16 engineered)

### Key Features Used in Analysis

| Column | Source | Type | Description |
|--------|--------|------|-------------|
| `state` | All | string | State/UT name (normalized) |
| `district` | All | string | District name (normalized) |
| `population_total` | Census | int | Total population (Census 2011) |
| `literacy_rate` | Census | float | Literacy rate (%) = Literate / Population × 100 |
| `female_literacy_rate` | Census | float | Female literacy rate (%) |
| `rural_pct` | Census | float | Rural households % = Rural_HH / Total_HH × 100 |
| `sc_pct` | Census | float | Scheduled Caste % = SC / Population × 100 |
| `st_pct` | Census | float | Scheduled Tribe % = ST / Population × 100 |
| `sex_ratio` | Census | float | Females per 1000 males |
| `below_poverty_pct` | Census | float | Below poverty proxy = Power_Parity < Rs.45000 / Total × 100 |
| `agri_worker_pct` | Census | float | Agricultural workers % of total workers |
| `electricity_pct` | Census | float | Households with electric lighting % |
| `latrine_pct` | Census | float | Households with latrine within premises % |
| `women_literacy_pct` | NFHS-5 | float | Women (15-49) literacy rate (%) |
| `health_insurance_pct` | NFHS-5 | float | Households with health insurance coverage (%) |
| `institutional_births_pct` | NFHS-5 | float | Institutional births (%) |
| `stunting_pct` | NFHS-5 | float | Children under 5 who are stunted (%) |
| `clean_fuel_pct` | NFHS-5 | float | Households using clean fuel for cooking (%) |
| `hh_demanded_work` | MGNREGA | int | Households that demanded work (2019-20) |
| `hh_worked` | MGNREGA | int | Households that worked under MGNREGA |
| `hh_allotted_work` | MGNREGA | int | Households allotted work |
| `persondays_total` | MGNREGA | int | Total person-days worked |
| `persondays_women` | MGNREGA | int | Person-days worked by women |
| `labour_expenditure` | MGNREGA | float | Labour expenditure disbursed (Rs. lakhs) |
| `works_completed` | MGNREGA | int | Number of works completed |

### Engineered Features

| Column | Formula | Description |
|--------|---------|-------------|
| `mgnrega_gap_pct` | (hh_demanded - hh_worked) / hh_demanded × 100 | MGNREGA participation gap |
| `mgnrega_participation_rate` | hh_worked / hh_demanded × 100 | MGNREGA participation rate |
| `mgnrega_allocation_rate` | hh_allotted / hh_demanded × 100 | Work allocation rate |
| `mgnrega_avg_person_days` | persondays_total / hh_worked | Avg person-days per household |
| `mgnrega_women_work_share` | persondays_women / persondays_total × 100 | Women's share of person-days |
| `health_insurance_gap_pct` | 100 - health_insurance_pct | Health insurance coverage gap |
| `vulnerable_pct` | sc_pct + st_pct | SC+ST combined share |
| `combined_gap_score` | 0.5 × mgnrega_gap + 0.5 × health_ins_gap | Weighted combined gap |
| `literacy_x_rural` | literacy_rate × rural_pct | Interaction term |
| `vulnerable_x_bpl` | vulnerable_pct × below_poverty_pct | Interaction term |
