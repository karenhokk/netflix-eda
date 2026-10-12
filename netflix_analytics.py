import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure target directories exist safely
os.makedirs("output", exist_ok=True)

RED, BLACK, GREY = "#E50914", "#221F1F", "#564d4d"
plt.rcParams.update({"font.size": 11, "axes.titleweight": "bold", "figure.dpi": 120})

def to_min(s):
    if not isinstance(s, str) or s == "NA":
        return np.nan
    h = re.search(r"(\d+)\s*H", s)
    m = re.search(r"(\d+)\s*M", s)
    hours = int(h.group(1)) if h else 0
    minutes = int(m.group(1)) if m else 0
    return (hours * 60 + minutes) if (h or m) else np.nan

def main():
    print("=== Launching Netflix Portfolio Analytical Pipeline ===")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MOVIES_PATH = os.path.join(BASE_DIR, "Marketing", "movies.csv")
    SHOWS_PATH = os.path.join(BASE_DIR, "Marketing", "shows.csv")

    if not os.path.exists(MOVIES_PATH) or not os.path.exists(SHOWS_PATH):
        print("Error: Missing data structures in Marketing folder.")
        return

    movies = pd.read_csv(MOVIES_PATH)
    shows = pd.read_csv(SHOWS_PATH)
    movies["content_type"] = "Film"
    shows["content_type"] = "TV"
    
    df = pd.concat([movies, shows], ignore_index=True)
    df["available_globally"] = df["available_globally"].astype(str).str.capitalize()
    df = df[df["available_globally"].isin(["Yes", "No"])]
    df = df.dropna(subset=["hours_viewed"])
    df["hours_M"] = df["hours_viewed"] / 1e6

    print(f"Aggregated Records Evaluated: {len(df)}")
    print(f"Mean Viewing Scale: {df['hours_M'].mean():.2f}M hours")
    print(f"Median Viewing Scale: {df['hours_M'].median():.2f}M hours")

    # Generate Structural Summaries
    summary = df.groupby(["content_type", "available_globally"]).size().reset_index(name="total_listings")
    summary.to_csv("output/netflix_structural_summary.csv", index=False)
    print("Analytical matrices exported safely to 'output/' folder.")

if __name__ == "__main__":
    main()
