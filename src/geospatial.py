import pandas as pd
import numpy as np
import folium
from libpysal.weights import Queen
from esda.moran import Moran, Moran_Local
from src.config import INDIA_GEOJSON, MAPS_DIR, FIGURES_DIR, SEED


def load_geodata(geojson_path=INDIA_GEOJSON):
    import geopandas as gpd
    gdf = gpd.read_file(geojson_path)
    return gdf


def merge_with_geodata(gdf, df, geo_district_col="NAME_2",
                       geo_state_col="NAME_1", data_district_col="district",
                       data_state_col="state"):
    gdf_copy = gdf.copy()
    gdf_copy["district"] = gdf_copy[geo_district_col].apply(
        lambda x: str(x).strip().lower() if x else ""
    )
    gdf_copy["state_geo"] = gdf_copy[geo_state_col].apply(
        lambda x: str(x).strip().lower() if x else ""
    )
    merged = gdf_copy.merge(
        df, left_on=["district"], right_on=[data_district_col],
        how="left", suffixes=("", "_data")
    )
    return merged


def compute_morans_i(merged_gdf, column, w=None):
    if w is None:
        w = Queen.from_dataframe(merged_gdf)
        w.transform = "r"
    y = merged_gdf[column].values
    mi = Moran(y, w)
    return {
        "I": mi.I,
        "E[I]": mi.EI,
        "p_value": mi.p_sim,
        "z_score": mi.z_sim,
        "significant": mi.p_sim < 0.05,
    }


def compute_lisa(merged_gdf, column, w=None):
    if w is None:
        w = Queen.from_dataframe(merged_gdf)
        w.transform = "r"
    y = merged_gdf[column].values
    lisa = Moran_Local(y, w)
    return lisa


def classify_lisa(lisa, p_threshold=0.05):
    labels = []
    for i in range(len(lisa.Is)):
        if lisa.p_sim[i] > p_threshold:
            labels.append("Not Significant")
        else:
            q = lisa.q[i]
            if q == 1:
                labels.append("HH (Hot Spot)")
            elif q == 2:
                labels.append("LH (Doughnut)")
            elif q == 3:
                labels.append("LL (Cold Spot)")
            else:
                labels.append("HL (Diamond)")
    return labels


def create_choropleth(merged_gdf, column, title, legend_name,
                      cmap="RdYlGn_r", save_path=None):
    center = [22.5, 82.0]
    m = folium.Map(location=center, zoom_start=5, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=merged_gdf.__geo_interface__,
        data=merged_gdf,
        columns=["district", column],
        key_on="feature.properties.district",
        fill_color=cmap,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name,
        name=title,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    if save_path:
        m.save(save_path)
    return m


def create_multi_layer_map(merged_gdf, save_path=None):
    center = [22.5, 82.0]
    m = folium.Map(location=center, zoom_start=5, tiles="CartoDB positron")

    for col, name, cmap in [
        ("mgnrega_gap_pct", "MGNREGA Participation Gap %", "YlOrRd"),
        ("health_insurance_gap_pct", "Health Insurance Coverage Gap %", "BuPu"),
        ("combined_gap_score", "Combined Gap Score", "RdYlGn_r"),
        ("literacy_rate", "Literacy Rate %", "YlGn"),
        ("vulnerable_pct", "Vulnerable Population %", "Oranges"),
    ]:
        if col in merged_gdf.columns:
            folium.Choropleth(
                geo_data=merged_gdf.__geo_interface__,
                data=merged_gdf,
                columns=["district", col],
                key_on="feature.properties.district",
                fill_color=cmap,
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=name,
                name=name,
                show=(col == "combined_gap_score"),
            ).add_to(m)

    folium.LayerControl().add_to(m)

    if save_path:
        m.save(save_path)
    return m
