# Kaggle Datasets — Verified Real Public Sources

All datasets below were retrieved via Kaggle's public API on 2026-06-13. Links verified to exist. Replace `data/raw/*.csv` with these to swap synthetic for real data.

---

## A. PM-KISAN / PMJAY Alternatives (Direct Substitutes)

### 1. **PMFBY Statistics** — best PM-KISAN substitute
- **URL:** https://www.kaggle.com/datasets/pyatakov/india-pmfby-statistics
- **Owner:** Oleg Pyatakov
- **Size:** 3.5 MB
- **License:** CC BY-NC-SA 4.0
- **Upvotes:** 11
- **Real data:** "Coverage and enrollment data on PMFBY/WBCIS insurance schemes of India (02.2023)"
- **Why use:** Same enrolment-vs-coverage structure as PM-KISAN; government crop insurance scheme for farmers. Replicates the analysis pipeline identically.

### 2. **PMGSY — District-level Physical/Financial Progress**
- **URL:** https://www.kaggle.com/datasets/mohitdhami8/physical-and-financial-progress-of-pmgsy-india
- **Owner:** Mohit Sharma Dhami
- **Size:** 149 KB
- **License:** Other (specified in description)
- **Upvotes:** 0 (new)
- **Real data:** "District level progress data of Pradhan Mantri Gram Sadak Yojna (2024-2025)"
- **Why use:** **ACTUALLY district-level government scheme data!** PMGSY builds rural roads; same gap analysis (target vs actual) applies.

### 3. **MGNREGA — Govt Aided Employment 2011-2021**
- **URL:** https://www.kaggle.com/datasets/sumedhapoonia/govt-aided-employment-in-india-mgnrega-20112021
- **Owner:** Sumedha Poonia
- **Size:** 1.2 MB
- **License:** CC0: Public Domain
- **Upvotes:** 14
- **Real data:** "Mahatma Gandhi National Rural Employment Guarantee Act Data 2011-2021"
- **Why use:** Richest district-level welfare scheme dataset. Eligible workers vs. actual registered — exact same methodology as PM-KISAN/PMJAY.

### 4. **MGNREGA — Bridging Gaps in Rural India**
- **URL:** https://www.kaggle.com/datasets/jayesh134/mgnrega-bridging-gaps-in-rural-india
- **Owner:** Jayesh Patil
- **Size:** 75 KB
- **License:** CC0: Public Domain
- **Upvotes:** 14, usability 1.0
- **Why use:** Cleaner curated MGNREGA dataset for gap analysis.

---

## B. Demographics (Census control variables)

### 5. **India Census 2011** — best Census substitute
- **URL:** https://www.kaggle.com/datasets/danofer/india-census
- **Owner:** Dan Ofer
- **Size:** 624 KB
- **License:** Public
- **Upvotes:** 114
- **Real data:** "Demographic Census Data for India"
- **Why use:** Direct substitute for `census_district.csv`. State-level aggregates of literacy, SC/ST, sex ratio.

### 6. **Census 2001 District-wise**
- **URL:** https://www.kaggle.com/datasets/bazuka/census2001
- **Owner:** Bazuka
- **Size:** 149 KB
- **Upvotes:** 98
- **Why use:** Older but tested alternative if #5 unsuited.

### 7. **India Literacy Data — District Wise**
- **URL:** https://www.kaggle.com/datasets/satyampd/india-literacy-data-district-wise
- **Owner:** Satyam P D
- **Size:** 8 KB
- **Upvotes:** 82
- **Why use:** Single-variable district literacy — clean direct fit if you only need that variable.

### 8. **MHA Population Census Dataset** — full 35 states/UTs
- **URL:** https://www.kaggle.com/datasets/prasad22/mha-population-dataset
- **Owner:** Prasad
- **Size:** 5.8 MB
- **Upvotes:** 25
- **Why use:** "Government of India dataset spread across 35 state and union territories" — comprehensive Census alternative.

### 9. **Indian Census Household & Population 2011**
- **URL:** https://www.kaggle.com/datasets/shraddha4ever20/indian-census-household-and-population-data-2011
- **Owner:** Shraddha
- **Size:** 59 KB
- **Upvotes:** 12
- **Why use:** Household-level granularity if you need it.

### 10. **Govt of India Literacy Rate**
- **URL:** https://www.kaggle.com/datasets/doncorleone92/govt-of-india-literacy-rate
- **Size:** 1 KB
- **Upvotes:** 41
- **Why use:** Compact literacy/staff numbers table.

---

## C. NFHS-5 District Health Data (real district-level factsheets)

### 11. **NFHS-5 District Factsheets 2019-21** — best for `nfhs5_district.csv`
- **URL:** https://www.kaggle.com/datasets/bhanupratapbiswas/national-family-health-survey-nfhs-2019-21
- **Owner:** Bhanu Pratap Biswas
- **Size:** 166 KB
- **Upvotes:** 56
- **Real data:** "National Family Health Survey-5 (NFHS-5) - India Districts Factsheet Data"
- **Why use:** Direct substitute for `nfhs5_district.csv` — exactly what we need.

### 12. **NFHS India 2019-21 (alternative)**
- **URL:** https://www.kaggle.com/datasets/kmldas/india-national-family-health-survey-nfhs
- **Size:** 158 KB
- **Upvotes:** 28
- **Why use:** Backup option if #11 schema differs.

### 13. **NFHS_india_district_insights**
- **URL:** https://www.kaggle.com/datasets/iamdivyanshukumar/nfhs-india-district-insights
- **Size:** 131 KB
- **Subtitle:** "District-level health, population, and development indicators from India's NFHS"
- **Why use:** Already cleaned/curated.

### 14. **NFHS-5: 131 Key Indicators of States/UT**
- **URL:** https://www.kaggle.com/datasets/abhinavkum/india-national-family-health-survey-nfhs5
- **Size:** 72 KB
- **Why use:** Smaller summary table.

### 15. **All India Factsheets of (NFHS)-5, 2019-2021**
- **URL:** https://www.kaggle.com/datasets/ananyaagrawal17/all-india-factsheets-of-nfhs-5-2019-2021
- **Size:** 337 KB
- **Why use:** Comprehensive structure but larger.

---

## D. Scheme-specific health (PMJAY substitute)

### 16. **Andhra Pradesh Health Insurance Data** (2007 Rajiv Arogyasri scheme — predecessor of PMJAY)
- **URL:** https://www.kaggle.com/datasets/phiiitm/andhra-pradesh-health-data
- **Owner:** Pranav Hari
- **Size:** 23 MB
- **Upvotes:** 22
- **Why use:** Real state-level health insurance claims data from AP's pre-PMJAY scheme. Best PMJAY analogue available.

### 17. **India Hospital Readmission Dataset 2015-2024**
- **URL:** https://www.kaggle.com/datasets/digutlaranjithkumar/india-hospital-readmission-dataset-20152024
- **Size:** 27 MB
- **Upvotes:** 2
- **Why use:** Real hospital claims data; per-district if available, full India otherwise.

---

## E. UDISE+ District Education Data (literacy proxy)

### 18. **UDISE+ Student Enrolment District-wise**
- **URL:** https://www.kaggle.com/datasets/mwnaseem/udise-education-dataset-student-enrolment
- **Owner:** Dr Wajahatullah Naseem
- **Size:** 3.3 MB
- **Subtitle:** "Student Enrolment by Age, Class, State, District, Wise"
- **Why use:** Real district-level education proxy for literacy.

### 19. **All 16 lakh Schools in India**
- **URL:** https://www.kaggle.com/datasets/hritikakolkar/schools
- **Owner:** Hritik Akolkar
- **Size:** 38 MB
- **Upvotes:** 82
- **Why use:** Department of School Education and Literacy, Government of India source. School-level geo-tagged.

---

## Recommended 3-Dataset Replacement Strategy

To make this portfolio project use **only real data**, do this minimal swap:

| Replace synthetic file | With | URL |
|---|---|---|
| `census_district.csv` | **#5 India Census 2011** | https://www.kaggle.com/datasets/danofer/india-census |
| `nfhs5_district.csv` | **#11 NFHS-5 Factsheets** | https://www.kaggle.com/datasets/bhanupratapbiswas/national-family-health-survey-nfhs-2019-21 |
| `pmkisan_district.csv` | **#3 MGNREGA** (better than #1 PMFBY) | https://www.kaggle.com/datasets/sumedhapoonia/govt-aided-employment-in-india-mgnrega-20112021 |
| `pmjay_district.csv` | **#16 AP Health Insurance** (state-level, NOT district) | https://www.kaggle.com/datasets/phiiitm/andhra-pradesh-health-data |

For **a single most-portable swap** use just **#3 + #4 (MGNREGA)** — the methodology is identical, the data is genuinely district-level, and you'll have a fully real-data pipeline.

After downloading, rename columns to match `docs/data_dictionary.md` schema and place in `data/raw/`. Skip `python -m src.generate_data` and run notebooks directly.
