import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SHAPEFILE_DIR = os.path.join(DATA_DIR, "shapefiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
MAPS_DIR = os.path.join(OUTPUT_DIR, "maps")
REPORT_DIR = os.path.join(OUTPUT_DIR, "report")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
SRC_DIR = os.path.join(BASE_DIR, "src")

MGNREGA_RAW = os.path.join(RAW_DIR, "NDAP_REPORT_6026.csv")
CENSUS_RAW = os.path.join(RAW_DIR, "india-districts-census-2011.csv")
NFHS_RAW = os.path.join(RAW_DIR, "datafile.csv")
INDIA_GEOJSON = os.path.join(SHAPEFILE_DIR, "india_districts.geojson")

MASTER_DATA = os.path.join(PROCESSED_DIR, "master_district_data.csv")
CLUSTER_DATA = os.path.join(PROCESSED_DIR, "district_clusters.csv")
REGRESSION_RESULTS = os.path.join(PROCESSED_DIR, "regression_results.csv")
ANOMALY_DISTRICTS = os.path.join(PROCESSED_DIR, "anomaly_districts.csv")
INTERVENTION_TABLE = os.path.join(PROCESSED_DIR, "intervention_recommendations.csv")

SEED = 42

PLOT_STYLE = {
    "figsize": (12, 7),
    "dpi": 150,
    "title_size": 16,
    "label_size": 12,
    "tick_size": 10,
    "palette": "viridis",
    "cmap_gap": "RdYlGn",
    "cmap_cluster": "Set2",
}

for d in [RAW_DIR, PROCESSED_DIR, SHAPEFILE_DIR,
          FIGURES_DIR, MAPS_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)
