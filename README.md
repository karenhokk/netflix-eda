# Attention Is the Scarcity: A Data-Driven Netflix Content Strategy
> Certificate in Junior Python Data Analyst 

This repository contains an exploratory data analysis (EDA) pipeline that evaluates viewing attention distributions using Netflix's public engagement records from H2-2023 through H1-2025.

## 🛡️ Data Privacy & Governance
1. **Public Domain Dataset**: This project exclusively references public metadata distributions and contains no PII or secure corporate metrics.
2. **Dynamic Workspace Isolation**: System logs and local visualization environments are safely blocked from public repository pushes using standardized configuration filters.

## Project Objective
Analyze 63,900 film and series records to identify audience retention levers, evaluate the viewing impact of global rights availability, and measure concentration metrics across the platform.

## Tech Stack
Python, pandas, numpy, matplotlib, seaborn

## How to Run
1. Clone this repository to your machine.
2. Install the necessary analysis data structures:
```bash
pip install pandas numpy matplotlib seaborn
```
3. Run the processing script to calculate distributions and generate data heatmaps:
```bash
python netflix_analytics.py
```
