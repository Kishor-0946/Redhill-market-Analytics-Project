# Week 2 Summary EDA & Pipeline Integration Report

### 📊 System Status: **Production Operational**

- **Total Ingested Relational Records:** 2500 rows
- **Calculated Target Skewness (Pricing):** 1.9096
- **Calculated Target Skewness (Consumer Ratings):** 0.0424
- **Pearson Bivariate Correlation (Price ↔ Rating):** 0.0217

## Feature Dependecy Correlation Matrix

|                       |   pricing_amount |   consumer_rating |   regional_demand_index |   discount_percentage |
|:----------------------|-----------------:|------------------:|------------------------:|----------------------:|
| pricing_amount        |        1         |        0.0217212  |              0.0035534  |           -0.0385676  |
| consumer_rating       |        0.0217212 |        1          |             -0.00892894 |           -0.00977192 |
| regional_demand_index |        0.0035534 |       -0.00892894 |              1          |           -0.00970685 |
| discount_percentage   |       -0.0385676 |       -0.00977192 |             -0.00970685 |            1          |

*Report automatically compiled via Day 12 Unified Data Engineering Pipeline Framework.*