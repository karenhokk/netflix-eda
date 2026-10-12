# Attention Is the Scarcity: A Data-Driven Netflix Content Strategy
> Certificate in Junior Python Data Analyst — Group Project Portfolio Tracker

## 1. Problem and Data Strategy
Netflix spends roughly ten billion dollars a year on content development. With subscriber growth maturing across primary demographic zones, audience retention—not catalog expansion volume—becomes the fundamental scaling lever. This project addresses a key core question: where does user viewing attention actually originate, and how should slate budgets be reallocated to optimize performance?

Our pipeline evaluates Netflix's public engagement records, analyzing 63,900 data elements across distinct evaluation windows to measure core global viewing attention distributions.

## 2. Analytical Findings

### Finding One: Viewing is Extremely Right-Skewed
The distribution of total viewing hours is heavily right-skewed across historical tracks (skewness metric of 13.8). 
- **The Mean Title**: Watched approximately 5.8 million hours.
- **The Median Title**: Watched only 1.0 million hours.

A small fraction of blockbuster hits systematically pulls up the global mean trendline. Utilizing standard statistical outlier rules (IQR fence capped at 10.1M hours), a total of 8,286 titles stand out as clear blockbuster outliers that form the defensive anchor of customer platform loyalty.

### Finding Two: Global Release Frameworks Raise the Impact Ceiling
Comparing regionally restricted data blocks against globally distributed properties shows that while the baseline platform floor remains steady, global access completely transforms performance capacity ceilings:
- **Regionally Restricted Titles**: Average 4.2M viewing hours (Median of 0.7M).
- **Globally Available Titles**: Average 10.1M viewing hours (Median of 2.3M).

Global distribution functions as a multiplier that unlocks structural ceiling values for high-performing intellectual properties.

### Finding Three: Viewing Metrics Follow a Winner-Take-Most Concentration
Platform attention maps show massive hit concentration properties across historical cycles:
- The top **1% of titles** command a commanding **24% share** of total viewing hours.
- The top **10% of titles** account for a massive **68% share** of cumulative viewing time.
- Conversely, the remaining 90% of properties in the catalog compete for just under a third of all remaining audience attention.

## 3. Strategic Content Recommendations
1. **Optimize Catalog Volatility**: Transition operational metrics from measuring catalog expansion volume to monitoring audience attention hours delivered per investment dollar.
2. **Prioritize Global Licensing tracks**: Reallocate capital targets to prioritize global distribution properties for tentpole selections to leverage performance ceiling values.
3. **Budget Realignment Ask**: We recommend an initial two-quarter project pilot, transferring approximately 10% of standard scripted program budgets into data-verified, global audience retention properties to evaluate structural capital performance changes.

## Data Sources & Attributions
- Netflix Engagement Report Collections (Public Domain Tracks).
- Open Source curated metadata archives via TidyTuesday data ecosystems.
- Core script operations processed locally via pandas, numpy, and descriptive data transformations.
