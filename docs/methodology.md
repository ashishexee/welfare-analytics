# Methodology — Welfare Scheme Participation Analysis

## Research Question

Why do some Indian districts exhibit welfare scheme participation gaps that exceed what their demographic profile would predict?

## Analytical Framework

### 1. Data Integration
Three publicly available datasets merged at district level:
- **Census 2011**: 640 districts, demographic baseline
- **NFHS-5 (2019-21)**: 706 districts, health & welfare indicators
- **MGNREGA (2019-20)**: 681 districts, rural employment scheme data

539 districts matched across all three sources. District name harmonization applied (see `data_sources.md`).

### 2. Outcome Variables
- **MGNREGA participation gap**: % of households that demanded work but did not receive it
- **Health insurance coverage gap**: 100% minus district coverage rate (NFHS-5)

### 3. OLS with State Fixed Effects + HC3 Robust Standard Errors

We estimate both a base model and a fixed-effects model:

**Base model** (demographics only):
```
gap_i = β₀ + β₁·literacy_i + β₂·rural_i + ... + ε_i
```

**Fixed-effects model** (demographics + state):
```
gap_i = β₀ + β₁·literacy_i + β₂·rural_i + ... + Σⱼ γⱼ·State_j + ε_i
```

**Why state fixed effects?** Welfare schemes in India are administered at the state level. State FE absorbs administrative capacity, governance quality, political will, and other unobserved state-level confounders. The variance decomposition reveals:
- MGNREGA: State explains 39% of gap variance; demographics add only 2% within-state
- Health Insurance: State explains 86% of gap variance; demographics add 6% within-state

**Why HC3?** District-level data exhibits heteroskedasticity. HC3 is the most conservative heteroskedasticity-consistent estimator (MacKinnon & White, 1985).

**Why not causal inference?** No valid instruments exist at district level. We explicitly frame results as **associative**, not causal.

**VIF check**: All features have VIF < 10 (no multicollinearity concern).

### 4. Anomaly Detection via FE Model Residuals

After the FE model, we compute standardized residuals:
```
std_residual_i = (gap_i - predicted_i) / σ(residuals)
```

Districts with **std_residual ≥ 95th percentile** are flagged as anomalies — their gaps exceed **within-state predictions**. This is more principled than base-model anomalies because it controls for state-level administration. A district is anomalous only if it underperforms relative to its own state average.

**Key insight**: Raw gap rankings and base-model residuals mislead because they conflate between-state and within-state variation. FE-model residuals isolate the within-state dimension where district-level interventions can actually make a difference.

### 5. District Segmentation (KMeans + PCA)

Features: gap metrics + demographics, standardized via Z-score. Optimal k selected by silhouette score. PCA for 2D visualization.

### 6. Geospatial Analysis (Moran's I + LISA)

Spatial autocorrelation tests whether gaps cluster geographically:
- **Global Moran's I**: Is there spatial structure in gap patterns?
- **Local LISA**: Where are the hot spots (high-gap surrounded by high-gap)?

Queen contiguity weights used for 594 district polygons.

### 7. Intervention Recommendations

Root cause classification for anomaly districts:
- **Awareness**: Low literacy + high rural → IEC campaigns
- **Administrative**: Low allocation rate → Facilitation cells
- **Infrastructural**: Low institutional births + high poverty → Mobile health camps
- **Economic**: High poverty + rural → Convergence with NRLM
- **Demographic**: High SC/ST → Community monitoring + sub-plan convergence

Evidence backing from J-PAL, 3ie, and government pilot evaluations.

## Limitations

1. Census 2011 demographics are 8-10 years older than NFHS-5/MGNREGA data
2. 539/722 districts have all three data sources; remainder imputed by state median
3. OLS is associative, not causal — omitted variable bias likely present
4. MGNREGA gap captures only the demand-to-completion gap, not latent unmet demand
5. GeoJSON contains 594 districts vs. 722 in data — some new districts lack polygon boundaries
6. State FE absorbs both administrative capacity and unobserved state-level confounders — we cannot distinguish these
