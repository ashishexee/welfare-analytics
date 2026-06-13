# Welfare Scheme Participation Analysis — Data Sources

## Datasets Used

All data is from publicly available sources. **Zero synthetic values.**

### 1. Census of India 2011
- **Source**: `india-districts-census-2011.csv` (Kaggle mirror of data.gov.in)
- **Records**: 640 districts across 35 states/UTs
- **Features**: 118 columns — population, literacy, caste, religion, housing, infrastructure
- **License**: Government Open Data (CC0 equivalent)

### 2. National Family Health Survey (NFHS-5), 2019-21
- **Source**: `datafile.csv` (Kaggle mirror of IIPS DHS Program)
- **Records**: 706 districts across 36 states/UTs
- **Features**: 109 columns — health insurance coverage, maternal health, nutrition, disease prevalence
- **Key column**: "Households with any usual member covered under a health insurance/financing scheme (%)"
- **License**: Public use (IIPS/DHS)

### 3. MGNREGA Dashboard Data (2011-2021)
- **Source**: `NDAP_REPORT_6026.csv` (Kaggle/NDAP mirror of nrega.nic.in)
- **Records**: 681 districts × 10 years = 6,858 rows
- **Features**: 46 columns — job cards, work demanded, work completed, expenditure, person-days
- **Year used**: 2019-20 (most recent complete year)
- **License**: Government Open Data (CC0 equivalent)

### 4. India District GeoJSON
- **Source**: `india_districts.geojson` (github.com/geohacker/india)
- **Records**: 594 district polygons
- **Properties**: NAME_1 (state), NAME_2 (district)
- **License**: CC0

## Data Processing

### District Name Harmonization
District and state names differ across sources. We normalize via:
1. Lowercase, strip whitespace, remove special characters
2. Known alias mapping (e.g., "Bangalore" → "Bengaluru", "Baroda" → "Vadodara")
3. State name fixes (e.g., "Jammu & Kashmir" → "Jammu and Kashmir", "Maharastra" → "Maharashtra")
4. Telangana remap: Census 2011 lists Telangana districts under "Andhra Pradesh"; we reassign them to "Telangana"

### Merge Strategy
- Outer join on (state, district) across Census + NFHS-5
- Left join with MGNREGA (not all districts have MGNREGA data)
- Result: 722 districts (539 matched in all 3 sources)
- Missing values imputed by state median, then overall median

### Feature Engineering
All derived features computed from raw counts:
- **MGNREGA gap**: (hh_demanded - hh_worked) / hh_demanded × 100
- **Health insurance gap**: 100 - coverage_rate
- **Demographic rates**: SC%, ST%, literacy%, rural% all from Census raw counts
