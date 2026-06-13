import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
from src.config import FIGURES_DIR, PLOT_STYLE


def setup_plot_style():
    plt.rcParams.update({
        "figure.figsize": PLOT_STYLE["figsize"],
        "figure.dpi": PLOT_STYLE["dpi"],
        "axes.titlesize": PLOT_STYLE["title_size"],
        "axes.labelsize": PLOT_STYLE["label_size"],
        "xtick.labelsize": PLOT_STYLE["tick_size"],
        "ytick.labelsize": PLOT_STYLE["tick_size"],
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })
    sns.set_palette(PLOT_STYLE["palette"])


def save_figure(fig, name, formats=("png",)):
    for fmt in formats:
        path = f"{FIGURES_DIR}/{name}.{fmt}"
        fig.savefig(path, bbox_inches="tight", dpi=PLOT_STYLE["dpi"],
                    facecolor="white", edgecolor="none")
    plt.close(fig)
    return path


def plot_distribution(df, column, title, xlabel, color=None, save_name=None):
    fig, ax = plt.subplots(figsize=PLOT_STYLE["figsize"])
    data = df[column].dropna()
    ax.hist(data, bins=50, color=color or "#4c72b0", edgecolor="white", alpha=0.85)
    ax.axvline(data.median(), color="red", linestyle="--", linewidth=2,
               label=f"Median: {data.median():.1f}")
    ax.axvline(data.mean(), color="orange", linestyle=":", linewidth=2,
               label=f"Mean: {data.mean():.1f}")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of Districts")
    ax.legend()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_scatter(df, x, y, title, xlabel, ylabel, hue=None,
                 annotate_outliers=True, n_annotate=5, save_name=None):
    fig, ax = plt.subplots(figsize=PLOT_STYLE["figsize"])
    if hue and hue in df.columns:
        scatter = sns.scatterplot(data=df, x=x, y=y, hue=hue,
                                   palette=PLOT_STYLE["cmap_cluster"],
                                   ax=ax, alpha=0.7, s=60)
    else:
        ax.scatter(df[x], df[y], alpha=0.5, s=40, color="#4c72b0")

    if annotate_outliers:
        top_gap = df.nlargest(n_annotate, y)
        for _, row in top_gap.iterrows():
            ax.annotate(row["district"].title(),
                        (row[x], row[y]),
                        fontsize=8, alpha=0.7,
                        xytext=(5, 5), textcoords="offset points")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if hue:
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc="upper left")
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_correlation_heatmap(df, columns, title, save_name=None):
    fig, ax = plt.subplots(figsize=(14, 10))
    corr = df[columns].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, ax=ax,
                square=True, linewidths=0.5)
    ax.set_title(title)
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_coefficient_forest(result, title, save_name=None):
    params = result.params.drop("const", errors="ignore")
    ci = result.conf_int().drop("const", errors="ignore")
    pvals = result.pvalues.drop("const", errors="ignore")

    fig, ax = plt.subplots(figsize=(10, max(6, len(params) * 0.5)))
    y_pos = range(len(params))

    for i, (feat, coef) in enumerate(params.items()):
        color = "#d62728" if pvals[feat] < 0.05 else "#1f77b4"
        marker = "o" if pvals[feat] < 0.05 else "s"
        ax.plot(coef, i, marker=marker, color=color, markersize=8, zorder=3)
        ax.hlines(i, ci.loc[feat, 0], ci.loc[feat, 1],
                  color=color, linewidth=2, zorder=2)

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params.index)
    ax.set_xlabel("Coefficient (with 95% CI)")
    ax.set_title(title)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="o", color="#d62728", label="p < 0.05",
               markersize=8, linestyle="None"),
        Line2D([0], [0], marker="s", color="#1f77b4", label="p >= 0.05",
               markersize=8, linestyle="None"),
    ]
    ax.legend(handles=legend_elements, loc="best")

    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_residual_distribution(std_residuals, title, save_name=None):
    fig, ax = plt.subplots(figsize=PLOT_STYLE["figsize"])
    ax.hist(std_residuals, bins=50, color="#4c72b0", edgecolor="white", alpha=0.85)
    ax.axvline(-2, color="red", linestyle="--", label="Under-performers (resid < -2 SD)")
    ax.axvline(2, color="green", linestyle="--", label="Over-performers (resid > 2 SD)")
    ax.set_title(title)
    ax.set_xlabel("Standardized Residual")
    ax.set_ylabel("Count")
    ax.legend()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_elbow_curve(k_results, save_name=None):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].plot(k_results["k"], k_results["inertia"], "bo-")
    axes[0].set_title("Elbow Method (Inertia)")
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("Inertia")

    axes[1].plot(k_results["k"], k_results["silhouette"], "go-")
    axes[1].set_title("Silhouette Score")
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("Silhouette")

    axes[2].plot(k_results["k"], k_results["calinski_harabasz"], "ro-")
    axes[2].set_title("Calinski-Harabasz Index")
    axes[2].set_xlabel("k")
    axes[2].set_ylabel("CH Index")

    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_cluster_pca(components, labels, title, save_name=None):
    fig, ax = plt.subplots(figsize=(10, 8))
    palette = sns.color_palette(PLOT_STYLE["cmap_cluster"], n_colors=len(set(labels)))
    for i, label in enumerate(sorted(set(labels))):
        mask = labels == label
        ax.scatter(components[mask, 0], components[mask, 1],
                   c=[palette[i]], label=f"Cluster {label}", alpha=0.6, s=50)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title(title)
    ax.legend()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_cluster_profiles(cluster_profiles, features, title, save_name=None):
    fig, ax = plt.subplots(figsize=(14, 6))
    data = cluster_profiles[features].T
    data.plot(kind="bar", ax=ax, width=0.8)
    ax.set_title(title)
    ax.set_ylabel("Mean Value")
    ax.set_xlabel("Feature")
    ax.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_gap_comparison(bottom10_mgnrega, bottom10_health_ins, save_name=None):
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    mgnrega_data = bottom10_mgnrega.copy().sort_values("mgnrega_gap_pct", ascending=True)
    mgnrega_labels = [f"{d.title()}, {s.title()}"
                      for d, s in zip(mgnrega_data["district"], mgnrega_data["state"])]
    axes[0].barh(mgnrega_labels, mgnrega_data["mgnrega_gap_pct"],
                 color="#d62728", alpha=0.85, edgecolor="white")
    axes[0].set_title("MGNREGA: Bottom 10 Anomalies (gap above predicted)")
    axes[0].set_xlabel("Participation Gap (%)")
    for i, v in enumerate(mgnrega_data["mgnrega_gap_pct"]):
        axes[0].text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9)

    health_data = bottom10_health_ins.copy().sort_values("health_insurance_gap_pct", ascending=True)
    health_labels = [f"{d.title()}, {s.title()}"
                     for d, s in zip(health_data["district"], health_data["state"])]
    axes[1].barh(health_labels, health_data["health_insurance_gap_pct"],
                 color="#9467bd", alpha=0.85, edgecolor="white")
    axes[1].set_title("Health Insurance: Bottom 10 Anomalies (gap above predicted)")
    axes[1].set_xlabel("Coverage Gap (%)")
    for i, v in enumerate(health_data["health_insurance_gap_pct"]):
        axes[1].text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9)

    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_feature_importance_bar(result, df, features, title, save_name=None):
    coefs = result.params.drop("const", errors="ignore")
    sig = result.pvalues.drop("const", errors="ignore")
    importance = []
    for feat in coefs.index:
        std_x = df[feat].std() if feat in df.columns else 1
        coef = coefs[feat]
        std_effect = abs(coef) * std_x
        importance.append({
            "feature": feat,
            "std_effect": std_effect,
            "signed_effect": coef * std_x,
            "significant": sig[feat] < 0.05,
        })
    imp_df = pd.DataFrame(importance).sort_values("std_effect", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = ["#d62728" if sig else "#7f7f7f" for sig in imp_df["significant"]]
    bars = ax.barh(imp_df["feature"], imp_df["std_effect"], color=colors, edgecolor="white")
    ax.set_xlabel("|Coefficient| x SD(X)  --  standard-deviation effect on gap")
    ax.set_title(title)
    for bar, sig in zip(bars, imp_df["significant"]):
        marker = "*" if sig else ""
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                marker, va="center", fontsize=14, fontweight="bold")
    ax.text(0.99, 0.02, "* = statistically significant (p < 0.05)",
            transform=ax.transAxes, ha="right", fontsize=9, color="#d62728")
    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    return fig


def plot_mgnrega_trends(mgnrega_all, metric_col, metric_name, top_n=5, save_name=None):
    year_col = "year"
    agg = mgnrega_all.groupby(year_col)[metric_col].mean().reset_index()
    fig, ax = plt.subplots(figsize=PLOT_STYLE["figsize"])
    ax.plot(agg[year_col], agg[metric_col], "bo-", linewidth=2, markersize=8)
    ax.set_title(f"MGNREGA National Trend: {metric_name}")
    ax.set_xlabel("Financial Year")
    ax.set_ylabel(metric_name)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    return fig
