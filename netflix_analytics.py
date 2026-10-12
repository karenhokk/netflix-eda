import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the output directory folder is automatically generated if missing
os.makedirs("output", exist_ok=True)

RED, BLACK, GREY = "#E50914", "#221F1F", "#564d4d"
plt.rcParams.update({"font.size": 11, "axes.titleweight": "bold", "figure.dpi": 120})

# Dynamically map your project paths to avoid file missing errors on different systems
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_PATH = os.path.join(BASE_DIR, "Marketing", "movies.csv")
SHOWS_PATH = os.path.join(BASE_DIR, "Marketing", "shows.csv")

def to_min(s):
    if not isinstance(s, str) or s == "NA":
        return np.nan
    h = re.search(r"(\d+)\s*H", s)
    m = re.search(r"(\d+)\s*M", s)
    hours = int(h.group(1)) if h else 0
    minutes = int(m.group(1)) if m else 0
    return (hours * 60 + minutes) if (h or m) else np.nan

def main():
    # Load datasets safely
    movies = pd.read_csv(MOVIES_PATH)
    shows  = pd.read_csv(SHOWS_PATH)

    movies["content_type"] = "Film"
    shows["content_type"]  = "TV"
    df = pd.concat([movies, shows], ignore_index=True)          # MERGE

    # Standardize casing since shows and movies mix 'Yes' and 'yes'
    df["available_globally"] = df["available_globally"].astype(str).str.capitalize()
    df = df[df["available_globally"].isin(["Yes", "No"])]       # clean flag

    df = df[df["hours_viewed"] != "NA"]
    df["hours_viewed"] = pd.to_numeric(df["hours_viewed"])
    df = df.dropna(subset=["hours_viewed"])                     # DROPNA
    df["hours_M"] = df["hours_viewed"] / 1e6

    # ---- Figure A - Skewness ----
    print(f"\nSkewness = {df.hours_M.skew():.2f}")
    print(f"Mean = {df.hours_M.mean():.2f}M   Median = {df.hours_M.median():.2f}M")
    plt.figure(figsize=(7.5, 4.2))
    plt.hist(df.hours_M.clip(upper=120), bins=60, color=BLACK, alpha=0.85)
    plt.axvline(df.hours_M.mean(), color=RED, ls="--", lw=2.5, label=f"Mean {df.hours_M.mean():.1f}M")
    plt.axvline(df.hours_M.median(), color="white", ls="--", lw=2.5, label=f"Median {df.hours_M.median():.1f}M")
    plt.title("Figure A - Hours viewed is extremely right-skewed")
    plt.xlabel("Hours per title (millions)"); plt.ylabel("Number of titles"); plt.legend()
    plt.tight_layout(); plt.savefig("output/chart_skew.png", dpi=200); plt.close()

    # ---- Figure B - Outliers ----
    q1, q3 = df.hours_M.quantile([.25, .75]); fence = q3 + 1.5*(q3-q1)
    n_out = (df.hours_M > fence).sum()
    print(f"IQR fence = {fence:.1f}M -> {n_out} outlier titles (the monster hits)")
    plt.figure(figsize=(7.5, 2.6))
    plt.boxplot(df.hours_M.clip(upper=120), vert=False, patch_artist=True, boxprops=dict(facecolor=GREY))
    plt.title("Figure B - Boxplot: outliers are the blockbuster hits")
    plt.xlabel("Hours per title (M, capped 120M)")
    plt.tight_layout(); plt.savefig("output/chart_outliers.png", dpi=200); plt.close()

    # ---- Figure C - Global vs Regional ----
    gv = df.groupby("available_globally")["hours_M"].agg(["median", "mean"])
    print("\nGlobal vs regional (computed):\n", gv.round(2))
    labels = ["Regionally restricted", "Available globally"]
    med = [gv.loc["No","median"], gv.loc["Yes","median"]]
    mean = [gv.loc["No","mean"], gv.loc["Yes","mean"]]
    x = np.arange(2); w = 0.35
    plt.figure(figsize=(7.5, 4.5))
    plt.bar(x-w/2, med, w, label="Median (typical title / floor)", color=BLACK, edgecolor="black")
    plt.bar(x+w/2, mean, w, label="Mean (hit ceiling)", color=RED, edgecolor="black")
    for i,(m,n) in enumerate(zip(med,mean)):
        plt.text(i-w/2, m+0.2, f"{m:.1f}M", ha="center", fontsize=10, weight="bold")
        plt.text(i+w/2, n+0.2, f"{n:.1f}M", ha="center", fontsize=10, weight="bold")
    plt.xticks(x, labels); plt.ylabel("Hours viewed per title (millions)")
    plt.title("Figure C - Global release: similar floor, much higher ceiling")
    plt.legend(); plt.tight_layout(); plt.savefig("output/chart_global.png", dpi=200); plt.close()

    # ---- Figure D - Pareto Concentration ----
    h = np.sort(df.hours_viewed.values)[::-1]; cum = np.cumsum(h)/h.sum()
    top10 = cum[int(.1*len(cum))-1]; top1 = cum[int(.01*len(cum))-1]
    print(f"\nTop 1% titles = {top1:.0%} of hours ; Top 10% = {top10:.0%}")
    xx = np.arange(1,len(cum)+1)/len(cum)*100
    plt.figure(figsize=(7.5, 4.5))
    plt.plot(xx, cum*100, lw=2.5, color=BLACK, label="Cumulative % of hours")
    plt.plot([0,100],[0,100],":", color=GREY, label="Even distribution")
    plt.scatter([1,10],[top1*100,top10*100], color=RED, zorder=5, s=50)
    plt.annotate(f"top 10% = {top10:.0%}", (10,top10*100), xytext=(25,72), arrowprops=dict(arrowstyle="->"))
    plt.xlabel("Share of titles, best first (%)"); plt.ylabel("Cumulative share of hours (%)")
    plt.title("Figure D - Winner-take-most: top 10% drive most viewing")
    plt.legend(loc="lower right"); plt.tight_layout(); plt.savefig("output/chart_pareto.png", dpi=200); plt.close()

    # ---- Figure E - Correlation Heatmap ----
    df["runtime_min"] = df["runtime"].apply(to_min)
    df["views"] = pd.to_numeric(df["views"], errors='coerce')
    num = df[["hours_viewed","views","runtime_min"]].dropna()
    plt.figure(figsize=(5.5,4.5))
    sns.heatmap(num.corr(), annot=True, cmap="RdBu_r", center=0, fmt=".2f", square=True)
    plt.title("Figure E - Correlation heatmap"); plt.tight_layout()
    plt.savefig("output/chart_heatmap.png", dpi=200); plt.close()

    # ---- Figure F - Line Trend ----
    trend = df.groupby("report")["hours_viewed"].sum()/1e9
    plt.figure(figsize=(7.5,4))
    x_indexes = np.arange(len(trend))
    plt.plot(x_indexes, trend.values, marker="o", color=RED, lw=2.5)
    for i,v in enumerate(trend.values):
        plt.text(i, v + (max(trend.values)*0.01), f"{v:.1f}B", ha="center", weight="bold")
    plt.title("Figure F - Total hours watched per half-year (gentle growth)")
    plt.ylabel("Billion hours")
    plt.xticks(x_indexes, trend.index, rotation=15)
    plt.tight_layout(); plt.savefig("output/chart_trend.png", dpi=200); plt.close()

    print("\nAll figures computed and saved to output/")

if __name__ == "__main__":
    main()
