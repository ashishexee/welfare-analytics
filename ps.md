# Challenge 5.2 — Community Behaviour & Participation Analysis on Welfare Schemes

## Domain / Track
Analytics & Insights

## Background & Context
India publishes vast open data on welfare-scheme uptake (PM-KISAN, Ayushman Bharat, MGNREGA dashboards). Yet uptake varies wildly by district and demography in ways policymakers don't always investigate. A J-PAL South Asia analysis showed eligible-but-not-enrolled gaps of 30–50% in several major schemes.

## Problem Statement
Use publicly available datasets to analyse participation trends in one or two major welfare schemes, identify geographic and demographic blind spots, and recommend evidence-backed outreach interventions for the worst-performing 10 districts.

## Why This Matters
Targeted outreach is dramatically more cost-effective than broad-spectrum campaigns. Surfacing blind spots is a public good.

## Project Objectives
1. Pick 1–2 schemes (PM-KISAN, Ayushman Bharat PMJAY).
2. Perform exploratory + statistical analysis on uptake vs. eligibility proxies.
3. Produce a prioritised intervention map for the bottom 10 districts.

## Key Questions to Explore
- Where is the uptake gap statistically anomalous (controlling for income, literacy, etc.)?
- Are there gender/caste/age disparities visible in the data?
- What outreach intervention is most likely to close each kind of gap?

## Schemes Selected
| Scheme | Domain | Target Population | Key Metric |
|---|---|---|---|
| **PM-KISAN** | Agriculture | Landholding farmer families | Beneficiaries / eligible farmers |
| **Ayushman Bharat PMJAY** | Health | Bottom 40% economically | Claims / eligible families |

## Analytical Pipeline
1. **Data Collection & Cleaning** — harmonise district names, merge Census + NFHS + scheme data
2. **Exploratory Data Analysis** — distributions, correlations, disparity analysis
3. **Statistical Inference** — OLS regression, residual analysis, anomaly detection
4. **District Segmentation** — K-Means + hierarchical clustering, cluster profiling
5. **Geospatial Analysis** — choropleth maps, Moran's I, LISA cluster maps
6. **Intervention Recommendations** — classify gap types, recommend interventions for bottom-10

## Expected Deliverables
- [ ] Analytical report with clear visuals
- [ ] District-level segmentation model
- [ ] Prioritised intervention map
- [ ] Data dictionary
- [ ] Reproducible Jupyter notebooks on GitHub

## Success Metrics
- Statistical methodology peer-reviewed by a faculty mentor
- ≥ 3 actionable, data-backed recommendations
- Reproducible notebook published on GitHub

## Potential Impact
Findings actionable by state administrations and CSO networks; methodology replicable for every welfare scheme.
