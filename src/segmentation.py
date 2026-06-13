import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage
from src.config import PROCESSED_DIR, CLUSTER_DATA, SEED


SEGMENTATION_FEATURES = [
    "mgnrega_gap_pct", "health_insurance_gap_pct",
    "literacy_rate", "rural_pct", "vulnerable_pct",
    "below_poverty_pct", "women_literacy_pct",
    "combined_gap_score",
]


def prepare_clustering_data(df, features=SEGMENTATION_FEATURES):
    valid = df[features].notna().all(axis=1)
    df_valid = df.loc[valid].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_valid[features])
    return df_valid, X_scaled, scaler


def find_optimal_k(X_scaled, k_range=range(2, 11)):
    inertias = []
    silhouettes = []
    calinski = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))
        calinski.append(calinski_harabasz_score(X_scaled, labels))
    results = pd.DataFrame({
        "k": list(k_range),
        "inertia": inertias,
        "silhouette": silhouettes,
        "calinski_harabasz": calinski,
    })
    return results


def fit_kmeans(X_scaled, df_valid, k, features=SEGMENTATION_FEATURES):
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    labels = km.fit_predict(X_scaled)
    df_valid = df_valid.copy()
    df_valid["cluster"] = labels

    cluster_profiles = df_valid.groupby("cluster")[features].mean()
    cluster_sizes = df_valid.groupby("cluster").size().rename("n_districts")
    cluster_profiles = cluster_profiles.join(cluster_sizes)

    cluster_labels = label_clusters(cluster_profiles)
    df_valid["cluster_label"] = df_valid["cluster"].map(cluster_labels)

    return km, labels, cluster_profiles, df_valid


def fit_hierarchical(X_scaled, k):
    hc = AgglomerativeClustering(n_clusters=k, linkage="ward")
    labels = hc.fit_predict(X_scaled)
    return hc, labels


def compute_linkage_matrix(X_scaled):
    return linkage(X_scaled, method="ward")


def run_pca(X_scaled, n_components=2):
    pca = PCA(n_components=n_components, random_state=SEED)
    components = pca.fit_transform(X_scaled)
    return pca, components, pca.explained_variance_ratio_


def label_clusters(cluster_profiles):
    labels = {}
    gap_75 = cluster_profiles["combined_gap_score"].quantile(0.75)
    gap_25 = cluster_profiles["combined_gap_score"].quantile(0.25)
    rural_median = cluster_profiles["rural_pct"].median()
    literacy_median = cluster_profiles["literacy_rate"].median()
    vuln_median = cluster_profiles["vulnerable_pct"].median()

    for idx, row in cluster_profiles.iterrows():
        gap = row.get("combined_gap_score", 0)
        rural = row.get("rural_pct", 0)
        vulnerable = row.get("vulnerable_pct", 0)
        literacy = row.get("literacy_rate", 0)

        if gap >= gap_75 and vulnerable >= vuln_median and rural >= rural_median:
            labels[idx] = "High-gap Rural Vulnerable"
        elif gap >= gap_75 and rural >= rural_median and literacy <= literacy_median:
            labels[idx] = "High-gap Rural Low-literacy"
        elif gap >= gap_75:
            labels[idx] = "High-gap Infrastructure-starved"
        elif gap <= gap_25 and literacy >= literacy_median and rural <= rural_median:
            labels[idx] = "Well-served Urban"
        elif gap <= gap_25 and vulnerable <= vuln_median:
            labels[idx] = "Well-served Low-vulnerability"
        elif gap <= gap_25:
            labels[idx] = "Moderate-gap Rural"
        else:
            labels[idx] = "Moderate-gap Mixed"
    return labels


def save_cluster_assignments(df_valid):
    save_cols = ["state", "district", "cluster", "cluster_label",
                 "mgnrega_gap_pct", "health_insurance_gap_pct", "combined_gap_score"]
    save_cols = [c for c in save_cols if c in df_valid.columns]
    df_valid[save_cols].to_csv(CLUSTER_DATA, index=False)
    return df_valid
