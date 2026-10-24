# Attention Is the Scarcity: Netflix Engagement EDA

Portfolio exploratory analysis of Netflix's public "What We Watched" engagement reports.

The files in this repository are a **fixed sample of 280 titles** (160 films and 120 shows). Every number below is what `python netflix_analytics.py` prints on that sample. The full public tables are linked in [Data](#data) and are omitted here.

## Run it

Python 3.12 and the pins in `requirements.txt` were used to produce the transcript below.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python netflix_analytics.py
```

On Windows, activate the environment with `.venv\Scripts\activate`.

The script reads `Marketing/movies.csv` and `Marketing/shows.csv` from the repository directory (so it still works if you launch it from another working directory) and writes six PNGs to `output/`:

- `output/chart_skew.png`
- `output/chart_outliers.png`
- `output/chart_global.png`
- `output/chart_pareto.png`
- `output/chart_heatmap.png`
- `output/chart_trend.png`

`output/` is gitignored. A fresh clone has the CSVs and the script; run the script to regenerate the charts.

A matching run prints:

```text
Film rows read: 160
Show rows read: 120
data_scope: committed_sample
Analysis rows after cleaning: 280

Skewness = 13.58
Mean = 7.25M   Median = 1.10M
IQR fence = 11.8M -> 38 outlier titles

Global vs regional (computed):
                    median   mean  count
available_globally
No                    0.60   3.71    204
Yes                   2.75  16.75     76

Top 1% of titles (n=2) = 31.2% of hours; top 10% (n=28) = 71.0%

Correlation rows: 276
              hours_viewed  views  runtime_min
hours_viewed          1.00   0.94         0.18
views                 0.94   1.00         0.07
runtime_min           0.18   0.07         1.00

Total hours by report window (billions):
report
2023Jul-Dec    0.59
2024Jan-Jun    0.82
2024Jul-Dec    0.25
2025Jan-Jun    0.37
```

## What this sample shows

These figures describe the 280 committed rows.

Hours viewed are right-skewed. Skewness is 13.58. The mean title was watched 7.25 million hours; the median title was watched 1.10 million hours. The 1.5-IQR fence sits at 11.8 million hours, and 38 titles fall above it. Figures A and B cap the displayed axis at 120 million hours so the body of the distribution stays readable. The printed mean, median, skewness, and outlier count use the uncapped hours.

Globally available titles in the sample sit higher than regionally restricted ones. The 204 regional rows have a median of 0.60 million hours and a mean of 3.71 million. The 76 global rows have a median of 2.75 million hours and a mean of 16.75 million. The global group is smaller, so a handful of hits moves its mean.

Viewing hours are concentrated. The top 1% of this sample is 2 titles and accounts for 31.2% of sample hours. The top 10% is 28 titles and accounts for 71.0%.

On the 276 rows with a parseable runtime, hours viewed and views correlate at 0.94. Runtime correlates with hours at 0.18 and with views at 0.07. In the source tables, views are hours viewed divided by runtime, so the hours-views correlation is built into the columns. Four shows have a blank runtime (`Paradise PD: Part 3`, `Haikyu!! TO THE TOP`, `Blood Blockade Battlefront`, `Spy Kids: Mission Critical: Season 2`) and drop out of the heatmap only.

Figure F sums hours for the titles drawn into each report window: 0.59, 0.82, 0.25, and 0.37 billion hours. Each window is its own draw of 40 films and 30 shows, so those totals stay inside the sample.

## Data

`Marketing/movies.csv` and `Marketing/shows.csv` carry a `data_scope` column set to `committed_sample` on every row.

| File | Rows | How many per report window |
| --- | --- | --- |
| `Marketing/movies.csv` | 160 films | 40 |
| `Marketing/shows.csv` | 120 shows | 30 |

Report windows: `2023Jul-Dec`, `2024Jan-Jun`, `2024Jul-Dec`, `2025Jan-Jun`.

Columns: `source`, `report`, `title`, `available_globally`, `release_date`, `hours_viewed`, `runtime`, `views`, `data_scope`.

The rows come from the TidyTuesday 2025-07-29 release of Netflix's public engagement reports. That release stacks the four "What We Watched" workbooks Netflix published for those windows.

- TidyTuesday index: https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-07-29
- Films: https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-07-29/movies.csv
- Shows: https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-07-29/shows.csv
- Netflix's write-up of the first half of 2025: https://about.netflix.com/news/what-we-watched-the-first-half-of-2025

Sampling rule, applied once with `numpy.random.default_rng(20250729)` on numpy 2.5.4:

1. From each TidyTuesday file, keep rows whose `available_globally` is `Yes` or `No` and whose `hours_viewed` is numeric. That drops sheet-header leftovers such as a row titled `Available Globally?`.
2. Walk the report windows in the order listed above. Draw 40 films from each window, then draw 30 shows from each window. Draws are without replacement.
3. Sort each committed file by `report`, then `hours_viewed` descending, then `title`.

The CSVs in git are the files to run. Re-downloading the source is only needed if you want to rebuild or replace the sample.

The full TidyTuesday files contain 36,121 film rows and 27,803 show rows. The same cleaning this script already does leaves 63,900 analysis rows. Those files are omitted from this repository. An earlier README quoted summary statistics for that full extract; this clone prints the sample transcript above instead. To run the script on the complete public tables, replace the two CSVs with the TidyTuesday files (same column names). `data_scope` is optional, and the script still runs when it is absent.

## Stack

Python, pandas, numpy, matplotlib, and seaborn. Install the tested versions from `requirements.txt`.
