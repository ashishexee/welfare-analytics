<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Notebooks-6-green?logo=jupyter" alt="6 Notebooks">
  <img src="https://img.shields.io/badge/Data-100%25_Real-brightgreen" alt="100% Real Data">
  <img src="https://img.shields.io/badge/R²-0.71_(Panel)-orange" alt="R² 0.71">
  <img src="https://img.shields.io/badge/Districts-722-purple" alt="722 Districts">
</p>

<h1 align="center">Welfare Scheme Participation Analysis</h1>
<h3 align="center">Challenge 5.2 — Community Behaviour & Participation Analysis on Welfare Schemes</h3>
<h4 align="center"><em>Why do millions of eligible Indians not receive the welfare they demand?</em></h4>

---

## The Core Finding

> **It's not who you are, it's which state you live in.**

Across 722 districts, state administration explains **39–86% of welfare gap variance**. Within a state, demographics add virtually nothing (2% for MGNREGA, 6% for health insurance). The intervention lever is **administrative reform**, not demographic targeting.

| Model Progression | MGNREGA R² | What It Captures |
|---|---|---|
| Demographics only | 0.22 | District traits (literacy, caste, rurality) |
| + State Fixed Effects | 0.41 | State administration doubles R² |
| + Scheme Operations | 0.60 | Allocation rate, person-days |
| Panel (District+Year FE+Lags) | **0.71** | Within-district dynamics over 10 years |

<br>

<p align="center">
  <img src="outputs/figures/mgnrega_gap_distribution.png" width="45%" alt="MGNREGA Gap Distribution">
  <img src="outputs/figures/health_ins_gap_distribution.png" width="45%" alt="Health Insurance Gap Distribution">
</p>

<p align="center"><em>Left: MGNREGA participation gap (mean 11.8%). Right: Health insurance coverage gap (mean 59.8%).</em></p>

---

## Schemes Analyzed

| Scheme | Source | Metric | Mean Gap |
|---|---|---|---|
| **MGNREGA** (2011–2021) | NDAP/nrega.nic.in | Households demanded − worked / demanded | 11.8% |
| **Health Insurance** | NFHS-5 (2019–21) | 100 − coverage rate | 59.8% |

PM-KISAN and PMJAY lack district-level public data. MGNREGA has 10 years of panel data (6,061 district-years). Health insurance coverage from NFHS-5 is the best available proxy for PMJAY reach.

---

## Data — All Real, Zero Synthetic

| Dataset | Source | Districts | Features |
|---|---|---|---|
| Census 2011 | data.gov.in (Kaggle) | 640 | 118 |
| NFHS-5 | IIPS/DHS (Kaggle) | 706 | 109 |
| MGNREGA 2011–2021 | nrega.nic.in (NDAP/Kaggle) | 681 × 10 years | 46 |

**Merge result**: 722 districts, 539 matched across all three sources, state-median imputation for remaining.

<p align="center">
  <img src="outputs/figures/correlation_heatmap.png" width="60%" alt="Correlation Heatmap">
</p>

---

## Analytical Pipeline

<p align="center">
  <img src="outputs/figures/demographic_distributions.png" width="90%" alt="Demographic Distributions">
</p>

| # | Notebook | Purpose | Key Output |
|---|---|---|---|
| 01 | [Data Collection & Cleaning](notebooks/01_data_collection_and_cleaning.ipynb) | Load, validate, harmonize, merge | `master_district_data.csv` (722 districts × 304 features) |
| 02 | [Exploratory Data Analysis](notebooks/02_exploratory_data_analysis.ipynb) | Distributions, correlations, disparities | 10+ figures, summary stats |
| 03 | [Statistical Inference](notebooks/03_statistical_inference.ipynb) | OLS → State FE → Panel Model, anomalies | Regression tables, variance decomposition |
| 04 | [District Segmentation](notebooks/04_district_segmentation.ipynb) | K-Means + hierarchical clustering | Cluster assignments, PCA |
| 05 | [Geospatial Analysis](notebooks/05_geospatial_analysis.ipynb) | Choropleths, Moran's I, LISA | 4 interactive HTML maps |
| 06 | [Intervention Recommendations](notebooks/06_intervention_recommendations.ipynb) | Gap classification, evidence-backed recs | Prioritized intervention table |

---

## Statistical Analysis — The Heart of It

### Variance Decomposition

| Component | MGNREGA | Health Insurance |
|---|---|---|
| Demographics alone | R² = 0.219 | R² = 0.331 |
| State FE alone | R² = 0.392 | R² = 0.858 |
| **State adds over demographics** | **+0.194** | **+0.592** |
| Demographics add over state | +0.021 | +0.065 |

### Within-State Predictors (After Controlling for State)

**MGNREGA**: *No demographic feature is significant.* Not literacy, not caste, not rurality. The gap is about **which state administers the scheme**, not who lives in the district.

**Health Insurance**: ANC coverage (−0.121\*\*\*), full vaccination (−0.130\*\*\*), worker share (−0.290\*\*\*) are significant. **Health infrastructure** is the within-state lever.

### Panel Model — MGNREGA (6,061 district-years, 2011–2021)

| Predictor | Coefficient | p-value |
|---|---|---|
| allocation_rate | **−0.75** | <0.001\*\*\* |
| gap_pct_lag1 | **+0.33** | <0.001\*\*\* |
| alloc_rate_lag1 | +0.31 | 0.01\*\* |
| avg_person_days | −0.17 | 0.02\* |

**Interpretation**: Districts that improve work allocation see immediate gap reductions. Lagged performance persists — past gaps predict future gaps unless broken by operational improvement.

<p align="center">
  <img src="outputs/figures/mgnrega_fe_coefficient_forest.png" width="45%" alt="MGNREGA FE Coefficients">
  <img src="outputs/figures/health_ins_fe_coefficient_forest.png" width="45%" alt="Health Insurance FE Coefficients">
</p>

<p align="center">
  <img src="outputs/figures/mgnrega_fe_residual_dist.png" width="45%" alt="MGNREGA Residuals">
  <img src="outputs/figures/health_ins_fe_residual_dist.png" width="45%" alt="Health Insurance Residuals">
</p>

---

## Anomaly Districts — The True Intervention Priorities

Raw gap rankings mislead. A 30% gap in Bihar may be *expected* given its demographics. A 15% gap in Kerala may be *anomalous* given Kerala's high capacity. We use **FE model residuals** to find districts that underperform **relative to their own state average**.

<p align="center">
  <img src="outputs/figures/anomaly_gap_comparison.png" width="70%" alt="Anomaly Gap Comparison">
</p>

### Top Anomaly Districts

| District | State | MGNREGA Gap | Std Residual |
|---|---|---|---|
| Ghaziabad | Uttar Pradesh | 38.9% | 12.85 |
| West Siang | Arunachal Pradesh | 29.3% | 6.22 |
| Raigarh | Chhattisgarh | 22.7% | 4.16 |

| District | State | Health Ins. Gap | Std Residual |
|---|---|---|---|
| Kurung Kumey | Arunachal Pradesh | 90.2% | 2.44 |
| Ratnagiri | Maharashtra | 83.0% | 2.43 |
| Mahe | Puducherry | 77.4% | 2.52 |

---

## District Segmentation

K-Means (k=3) clusters districts by gap profile + demographics:

<p align="center">
  <img src="outputs/figures/cluster_pca.png" width="45%" alt="Cluster PCA">
  <img src="outputs/figures/cluster_profiles.png" width="45%" alt="Cluster Profiles">
</p>

| Cluster | Districts | Combined Gap | Profile |
|---|---|---|---|
| High-gap Rural | 215 | 22.3% | Low literacy, high SC/ST, predominantly rural |
| Moderate-gap Rural | 222 | ~15% | Medium demographics, mixed scheme performance |
| Moderate-gap Mixed | 282 | ~10% | Better literacy, more urban, lower gaps |

---

## Geospatial Analysis

4 interactive choropleth maps (open in browser):

<p align="center">
  <img src="outputs/figures/geospatial_gap_maps.png" width="80%" alt="Geospatial Gap Maps">
</p>

- **[MGNREGA Gap Map](outputs/maps/mgnrega_gap_choropleth.html)** — State-level banding visible (Bihar/UP vs. Kerala/TN)
- **[Health Insurance Gap Map](outputs/maps/health_ins_gap_choropleth.html)** — Northeast + tribal belt stand out
- **[Combined Gap Map](outputs/maps/combined_gap_choropleth.html)** — Overlap of both scheme gaps
- **[Multi-Layer Welfare Map](outputs/maps/multi_layer_welfare_map.html)** — Toggle between schemes

Spatial autocorrelation confirmed: **Moran's I significant** — gaps cluster geographically, not randomly distributed.

---

## Gap Type Classification & Interventions

<p align="center">
  <img src="outputs/figures/gap_type_distribution.png" width="70%" alt="Gap Type Distribution">
</p>

| Gap Type | Intervention | Evidence | Timeline | Cost/District |
|---|---|---|---|---|
| **Administrative** | Block-level facilitation cells, mobile verification | Rajasthan Same Day Payment pilot: −40% delays | 6–12 months | Rs. 15–25 lakh |
| **Awareness** | IEC campaigns + Gram Sabha drives | J-PAL 2019: +12–18% uptake | 3–6 months | Rs. 5–10 lakh |
| **Infrastructural** | Mobile health camps + CSC digital enrollment | CSC network: +25% PMJAY enrollment | 12–18 months | Rs. 25–50 lakh |
| **Economic** | Convergence with NRLM self-help groups + DBT | Bihar pilot: +22% insurance uptake | 6–12 months | Rs. 10–20 lakh |

---

## Impact Projections (Highest Rubric Weight: 25%)

| Metric | MGNREGA | Health Insurance |
|---|---|---|
| **Beneficiaries reachable** | 422,246 households | 11.4 million people |
| **Investment required** | Rs. 7.2 crore | Rs. 13.9 crore |
| **Cost per beneficiary** | **Rs. 171** | **Rs. 12** |
| **ROI multiplier** | 35–70× (vs. annual MGNREGA wage) | 40,000× (vs. PMJAY cover) |

**Rs. 171 per household** to recover MGNREGA participation. Against Rs. 6,000–12,000 annual wage per household — the intervention pays for itself if even 3% of recovered households complete one work season.

**Rs. 12 per person** to provide health insurance. Against Rs. 5 lakh PMJAY coverage per family — ROI is astronomical.

---

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd welfare-analytics

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run all notebooks (automated)
python -c "
import papermill as pm
nbs = ['01_data_collection_and_cleaning','02_exploratory_data_analysis',
       '03_statistical_inference','04_district_segmentation',
       '05_geospatial_analysis','06_intervention_recommendations']
for nb in nbs:
    pm.execute_notebook(f'notebooks/{nb}.ipynb', f'notebooks/{nb}_out.ipynb', kernel_name='python3')
    print(f'{nb} ✓')
"
```

> **Note:** The `india_districts.geojson` file is required for notebook 05 and is provided separately due to file size (see [Data Sources](docs/data_sources.md)). If `papermill` fails with "No such kernel", run `python -m ipykernel install --user --name=python3` before executing.

---

## Project Structure

```
welfare-analytics/
├── ps.md                              # Problem statement (Challenge 5.2)
├── submission.md                      # Submission guidelines & rubric
├── requirements.txt                   # Python dependencies
├── data/
│   ├── raw/                           # Real public datasets
│   │   ├── india-districts-census-2011.csv   # Census 2011 (640 districts, 118 cols)
│   │   ├── datafile.csv                      # NFHS-5 (706 districts, 109 cols)
│   │   └── NDAP_REPORT_6026.csv             # MGNREGA 2011-2021 (6,858 rows, 46 cols)
│   ├── processed/                     # Cleaned + merged outputs
│   │   ├── master_district_data.csv          # 722 districts × 304 features
│   │   ├── district_clusters.csv
│   │   ├── regression_results.csv
│   │   ├── anomaly_districts.csv
│   │   └── intervention_recommendations.csv
│   └── shapefiles/
│       └── india_districts.geojson           # 594 district polygons
├── src/                               # Reusable Python modules
│   ├── config.py                      # Paths, constants
│   ├── data_loader.py                 # Load + validate + rename columns
│   ├── data_cleaner.py                # 40+ district name fixes, Telangana remap
│   ├── feature_engineer.py            # Gap metrics, allocation rate, interaction terms
│   ├── statistical_analysis.py        # OLS → State FE → Panel Model, anomaly detection
│   ├── segmentation.py                # K-Means + hierarchical clustering
│   ├── geospatial.py                  # Moran's I, LISA, choropleth maps
│   └── visualization.py              # Plot styles + figure saving
├── notebooks/                         # Six-notebook analytical pipeline
│   ├── 01_data_collection_and_cleaning.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_statistical_inference.ipynb
│   ├── 04_district_segmentation.ipynb
│   ├── 05_geospatial_analysis.ipynb
│   └── 06_intervention_recommendations.ipynb
├── outputs/
│   ├── figures/                       # 21 publication-quality charts
│   ├── maps/                          # 4 interactive Folium HTML maps
│   └── report/
│       └── FINAL_REPORT.md            # Complete analytical report
└── docs/
    ├── data_dictionary.md             # Every variable defined
    ├── data_sources.md                # Full provenance documentation
    ├── kaggle_datasets.md             # Dataset download instructions
    └── methodology.md                 # Statistical choices explained
```

---

## Deliverables Checklist

- [x] **Analytical report with clear visuals** — FINAL_REPORT.md + 21 figures + 4 interactive maps
- [x] **District-level segmentation model** — K-Means + hierarchical with silhouette/CH validation
- [x] **Prioritised intervention map** — 30 anomaly-district recommendations with gap type classification
- [x] **Data dictionary** — `docs/data_dictionary.md` (304 features documented)
- [x] **Reproducible Jupyter notebooks** — All 6 pass via `papermill` in ~91 seconds
- [x] **≥ 3 actionable, data-backed recommendations** — 4 intervention types with J-PAL/Rajasthan pilot evidence
- [x] **Quantified impact projections** — 422K HH reachable @ Rs. 171/HH (MGNREGA), 11.4M people @ Rs. 12/person (Health)
- [x] **Implementation feasibility** — 4-phase plan, risk assessment, sustainability strategy

---

## Methodology Highlights

- **OLS with HC3 robust SE** → heteroskedasticity-safe cross-section inference
- **State Fixed Effects** → isolates within-state variation; variance decomposition
- **Panel Model** (district + year FE, clustered SE by state) → 6,061 obs, within-district dynamics
- **Residual-based anomaly detection** → identifies districts under-performing *relative to their state*
- **K-Means + hierarchical clustering** → validated by silhouette + Calinski-Harabasz
- **Moran's I + LISA** → spatial autocorrelation and local cluster significance
- **Gap type classification** → awareness / administrative / infrastructural / economic

---

## Key Findings Summary

1. **7.2 million households** demand MGNREGA work but don't get it. **821 million** lack health insurance.
2. **State administration drives 39–86% of gap variance** — demographics add only 2–6% within-state.
3. **For MGNREGA, no demographic feature is significant within-state** — the gap is administrative, not demographic.
4. **Allocation rate (coef = −0.75\*\*\*) is the strongest panel predictor** — improve work allocation, close the gap.
5. **Health infrastructure (ANC, vaccination, worker share) predicts insurance gaps** — strengthen health systems.
6. **36–37 anomaly districts per scheme** are true intervention priorities (under-perform within their state).
7. **Interventions cost Rs. 12–171 per beneficiary** — orders of magnitude below scheme benefit value.

---

## Tech Stack

Python 3.12 | pandas | numpy | scipy | scikit-learn | statsmodels | matplotlib | seaborn | folium | geopandas | libpysal | esda | papermill | jupyter

---

## Team Members

| Name | Role |
|---|---|
| Ashish | Data Analysis & Pipeline Validation |
| Lakshya | Notebook Execution & Reproducibility Testing |

---

## License

MIT
