# 📊 Week 2 Review: Summary Exploratory Data Analysis Report

**Generated Automatically by:** `day12_weekly_review_pipeline.py`  
**Execution Timestamp Evaluation:** June 24, 2026  
**Host Organization:** Redhill Softec  

## 1. Operational Ingestion Diagnostics
| Assessment Metric | Pipeline Log Output |
| :--- | :--- |
| Source Raw File Analyzed | `day9_clean_market_data.csv` |
| Extracted Transaction Record Count | **2500** lines |
| Destination SQL Database Target | `redhill_market_duckdb.db` |
| Relational Integrity Constraints | **Active (PRIMARY KEY, CHECK constraints)** |
| Database Table Row Status | **2500 Records Injected Successfully** |

## 2. Statistical Profile: Numerical Feature Skewness
Distribution asymmetry scores evaluated using Pandas algorithm components:

| Feature Variable Field | Calculated Skewness Score | Shape Meaning Description |
| :--- | :---: | :--- |
| `pricing_amount` | ` 1.9096` | Right-Skewed Model (Long positive metric tail) |
| `consumer_rating` | ` 0.0424` | Symmetrical Distribution Model |
| `regional_demand_index` | ` 0.0024` | Symmetrical Distribution Model |
| `discount_percentage` | ` 0.4017` | Symmetrical Distribution Model |

## 3. Relational Matrix: Inter-Variable Linear Correlation Coefficients
Pearson correlation matrix ($r$) showing mathematical connections between features:

| Variable | `pricing_amount` | `consumer_rating` | `regional_demand_index` | `discount_percentage` |
| :--- | :---: | :---: | :---: | :---: |
| `pricing_amount` | `1.000` | `0.022` | `0.004` | `-0.039` |
| `consumer_rating` | `0.022` | `1.000` | `-0.009` | `-0.010` |
| `regional_demand_index` | `0.004` | `-0.009` | `1.000` | `-0.010` |
| `discount_percentage` | `-0.039` | `-0.010` | `-0.010` | `1.000` |


---
*End of Week 2 Integration Summary Report. Project assets pushed to GitHub remote main branch.*