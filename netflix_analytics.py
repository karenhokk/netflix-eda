"""Exploratory charts for the Netflix engagement sample in Marketing/.

Reads Marketing/movies.csv and Marketing/shows.csv (a fixed sample of the
public "What We Watched" tables, not the full extract) and writes PNGs to
output/. See README.md for the sampling rule and the figures this run prints.
"""

import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MOVIES_PATH = os.path.join(BASE_DIR, "Marketing", "movies.csv")
SHOWS_PATH = os.path.join(BASE_DIR, "Marketing", "shows.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

RED, BLACK, GREY = "#E50914", "#221F1F", "#564d4d"
plt.rcParams.update({"font.size": 11, "axes.titleweight": "bold", "figure.dpi": 120})


def to_min(value):
    if not isinstance(value, str) or value == "NA":
        return np.nan
    hours_match = re.search(r"(\d+)\s*H", value)
    minutes_match = re.search(r"(\d+)\s*M", value)
    if not hours_match and not minutes_match:
        return np.nan
    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0
    return hours * 60 + minutes


def prefix_share(hours_desc, fraction):
    """Share of hours held by the first fraction of a descending series."""
    count = int(fraction * len(hours_desc))
    if count < 1 or hours_desc.sum() == 0:
        return np.nan
    return hours_desc[:count].sum() / hours_desc.sum()


def main():
    movies = pd.read_csv(MOVIES_PATH)
    shows = pd.read_csv(SHOWS_PATH)
    print(f"Film rows read: {len(movies)}")
    print(f"Show rows read: {len(shows)}")
    if "data_scope" in movies.columns or "data_scope" in shows.columns:
        scopes = pd.concat(
            [
                movies.get("data_scope", pd.Series(dtype=str)),
                shows.get("data_scope", pd.Series(dtype=str)),
            ],
            ignore_index=True,
        ).dropna().astype(str).unique()
        print(f"data_scope: {', '.join(scopes) if len(scopes) else 'unlabeled'}")

    movies["content_type"] = "Film"
    shows["content_type"] = "TV"
    df = pd.concat([movies, shows], ignore_index=True)

    df["available_globally"] = df["available_globally"].astype(str).str.strip().str.capitalize()
    df = df[df["available_globally"].isin(["Yes", "No"])]

    df = df[df["hours_viewed"].astype(str) != "NA"]
    df["hours_viewed"] = pd.to_numeric(df["hours_viewed"], errors="coerce")
    df = df.dropna(subset=["hours_viewed"])
    df["hours_M"] = df["hours_viewed"] / 1e6
    print(f"Analysis rows after cleaning: {len(df)}")
    if df.empty:
        raise SystemExit("No rows left after cleaning. Check Marketing/movies.csv and Marketing/shows.csv.")

    # ---- Figure A - distribution ----
    skew = df.hours_M.skew()
    mean_m = df.hours_M.mean()
    median_m = df.hours_M.median()
    print(f"\nSkewness = {skew:.2f}")
    print(f"Mean = {mean_m:.2f}M   Median = {median_m:.2f}M")
    plt.figure(figsize=(7.5, 4.2))
    plt.hist(df.hours_M.clip(upper=120), bins=40, color=BLACK, alpha=0.85)
    plt.axvline(mean_m, color=RED, ls="--", lw=2.5, label=f"Mean {mean_m:.1f}M")
    plt.axvline(median_m, color="#F5C518", ls="--", lw=2.5, label=f"Median {median_m:.1f}M")
    plt.title("Figure A - Hours viewed per title")
    plt.xlabel("Hours per title (millions, capped at 120 for display)")
    plt.ylabel("Number of titles")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_skew.png"), dpi=200)
    plt.close()

    # ---- Figure B - outliers ----
    q1, q3 = df.hours_M.quantile([0.25, 0.75])
    fence = q3 + 1.5 * (q3 - q1)
    n_out = int((df.hours_M > fence).sum())
    print(f"IQR fence = {fence:.1f}M -> {n_out} outlier titles")
    plt.figure(figsize=(7.5, 2.6))
    plt.boxplot(
        df.hours_M.clip(upper=120),
        orientation="horizontal",
        patch_artist=True,
        boxprops=dict(facecolor=GREY),
    )
    plt.title("Figure B - Boxplot of hours viewed")
    plt.xlabel("Hours per title (millions, capped at 120 for display)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_outliers.png"), dpi=200)
    plt.close()

    # ---- Figure C - global vs regional ----
    grouped = df.groupby("available_globally")["hours_M"].agg(["median", "mean", "count"])
    print("\nGlobal vs regional (computed):")
    print(grouped.round(2))
    groups = [
        ("No", "Regionally restricted"),
        ("Yes", "Available globally"),
    ]
    present = [(flag, label) for flag, label in groups if flag in grouped.index]
    if len(present) < 2:
        missing = [label for flag, label in groups if flag not in grouped.index]
        print("Figure C not drawn; this file is missing: " + ", ".join(missing))
    else:
        labels = [label for _, label in present]
        med = [grouped.loc[flag, "median"] for flag, _ in present]
        mean = [grouped.loc[flag, "mean"] for flag, _ in present]
        x = np.arange(len(present))
        width = 0.35
        plt.figure(figsize=(7.5, 4.5))
        plt.bar(x - width / 2, med, width, label="Median", color=BLACK, edgecolor="black")
        plt.bar(x + width / 2, mean, width, label="Mean", color=RED, edgecolor="black")
        for i, (med_i, mean_i) in enumerate(zip(med, mean)):
            plt.text(i - width / 2, med_i, f"{med_i:.1f}M", ha="center", va="bottom", fontsize=10, weight="bold")
            plt.text(i + width / 2, mean_i, f"{mean_i:.1f}M", ha="center", va="bottom", fontsize=10, weight="bold")
        plt.xticks(x, labels)
        plt.ylabel("Hours viewed per title (millions)")
        plt.title("Figure C - Hours viewed by global availability")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "chart_global.png"), dpi=200)
        plt.close()

    # ---- Figure D - concentration ----
    hours_desc = np.sort(df.hours_viewed.values)[::-1]
    top1 = prefix_share(hours_desc, 0.01)
    top10 = prefix_share(hours_desc, 0.10)
    top1_n = int(0.01 * len(hours_desc))
    top10_n = int(0.10 * len(hours_desc))
    print(
        f"\nTop 1% of titles (n={top1_n}) = {top1:.1%} of hours; "
        f"top 10% (n={top10_n}) = {top10:.1%}"
    )
    cumulative = np.cumsum(hours_desc) / hours_desc.sum()
    xx = np.arange(1, len(cumulative) + 1) / len(cumulative) * 100
    plt.figure(figsize=(7.5, 4.5))
    plt.plot(xx, cumulative * 100, lw=2.5, color=BLACK, label="Cumulative % of hours")
    plt.plot([0, 100], [0, 100], ":", color=GREY, label="Even distribution")
    if np.isfinite(top1) and np.isfinite(top10):
        plt.scatter([1, 10], [top1 * 100, top10 * 100], color=RED, zorder=5, s=50)
        plt.annotate(
            f"top 10% = {top10:.0%}",
            (10, top10 * 100),
            xytext=(28, min(top10 * 100 + 15, 88)),
            arrowprops=dict(arrowstyle="->"),
        )
    plt.xlabel("Share of titles, best first (%)")
    plt.ylabel("Cumulative share of hours (%)")
    plt.title("Figure D - Cumulative share of viewing hours")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_pareto.png"), dpi=200)
    plt.close()

    # ---- Figure E - correlation ----
    df["runtime_min"] = df["runtime"].apply(to_min)
    df["views"] = pd.to_numeric(df["views"], errors="coerce")
    numeric = df[["hours_viewed", "views", "runtime_min"]].dropna()
    print(f"\nCorrelation rows: {len(numeric)}")
    if len(numeric) < 3:
        print("Figure E not drawn; fewer than 3 rows have hours, views, and runtime.")
    else:
        corr = numeric.corr()
        print(corr.round(2))
        plt.figure(figsize=(5.5, 4.5))
        sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f", square=True)
        plt.title("Figure E - Correlation heatmap")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "chart_heatmap.png"), dpi=200)
        plt.close()

    # ---- Figure F - report windows ----
    trend = df.groupby("report")["hours_viewed"].sum() / 1e9
    trend = trend.reindex([r for r in ["2023Jul-Dec", "2024Jan-Jun", "2024Jul-Dec", "2025Jan-Jun"] if r in trend.index])
    print("\nTotal hours by report window (billions):")
    print(trend.round(2))
    plt.figure(figsize=(7.5, 4))
    x_indexes = np.arange(len(trend))
    plt.plot(x_indexes, trend.values, marker="o", color=RED, lw=2.5)
    span = float(np.max(trend.values) - np.min(trend.values)) if len(trend) else 0
    offset = span * 0.08 if span else float(np.max(trend.values)) * 0.02
    for i, value in enumerate(trend.values):
        plt.text(i, value + offset, f"{value:.2f}B", ha="center", weight="bold")
    plt.title("Figure F - Total hours in this sample, by report window")
    plt.ylabel("Billion hours (sample only)")
    plt.xticks(x_indexes, trend.index, rotation=15)
    plt.ylim(0, float(np.max(trend.values)) * 1.18)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_trend.png"), dpi=200)
    plt.close()

    print(f"\nAll figures computed and saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
