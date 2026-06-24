import os
import duckdb
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def run_regression_pipeline():
    print("=== Day 15: Regression Analysis Engine ===")
    
    # 1. Connect to local DuckDB and fetch data
    db_path = "redhill_market_duckdb.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file '{db_path}' not found!")
        
    conn = duckdb.connect(db_path)
    
    # Using the exact validated columns present in your database schema
    query = """
        SELECT 
            pricing_amount, 
            discount_percentage, 
            regional_demand_index, 
            region 
        FROM regional_market_data
    """
    
    print("📥 Extracting valid feature matrix from DuckDB...")
    df = conn.execute(query).df()
    conn.close()
    
    print(f"📊 Extraction Successful! Shape: {df.shape}\n")
    
    # Handle missing values safely if any exist
    df = df.dropna()

    # =========================================================================
    # PART A: SIMPLE LINEAR REGRESSION (SLR)
    # Target (Y) = pricing_amount, Predictor (X) = discount_percentage
    # =========================================================================
    print("--- 1. Simple Linear Regression Model (statsmodels) ---")
    Y_slr = df['pricing_amount']
    X_slr = df['discount_percentage']
    
    # statsmodels needs an explicit intercept (constant column of 1s) added
    X_slr_with_const = sm.add_constant(X_slr)
    
    slr_model = sm.OLS(Y_slr, X_slr_with_const).fit()
    print(slr_model.summary().tables[1])  # Print the coefficients block cleanly
    print(f"Simple Regression R-squared: {slr_model.rsquared:.4f}\n")
    
    # =========================================================================
    # PART B: MULTIPLE LINEAR REGRESSION (MLR)
    # Target (Y) = pricing_amount
    # Predictors (X) = discount_percentage, regional_demand_index, region
    # =========================================================================
    print("--- 2. Multiple Linear Regression Data Prep & Modeling ---")
    
    # One-hot encode categorical variable 'region' safely, dropping the first column to prevent multi-collinearity
    df_encoded = pd.get_dummies(df, columns=['region'], drop_first=True, dtype=int)
    
    # Define Target and Predictors
    Y_mlr = df_encoded['pricing_amount']
    X_mlr = df_encoded.drop(columns=['pricing_amount'])
    
    # Fit model using statsmodels for deep mathematical reporting
    X_mlr_with_const = sm.add_constant(X_mlr)
    mlr_stats_model = sm.OLS(Y_mlr, X_mlr_with_const).fit()
    
    # Fit model using scikit-learn for algorithmic cross-checking
    sk_model = LinearRegression()
    sk_model.fit(X_mlr, Y_mlr)
    sk_preds = sk_model.predict(X_mlr)
    
    # =========================================================================
    # PART C: MODEL METRICS COMPILATION
    # =========================================================================
    print("\n--- 3. Structural Evaluation Metrics Summary ---")
    print(f"Statsmodels Adjusted R-squared : {mlr_stats_model.rsquared_adj:.4f}")
    print(f"Scikit-Learn R-squared score   : {r2_score(Y_mlr, sk_preds):.4f}")
    print(f"Root Mean Squared Error (RMSE) : {np.sqrt(mean_squared_error(Y_mlr, sk_preds)):.2f}")
    print(f"Overall Model F-pvalue         : {mlr_stats_model.f_pvalue:.4e}")
    
    print("\n💡 Detailed Predictor Coefficients & Significance:")
    # Extract coefficients and p-values into a readable summary table
    summary_df = pd.DataFrame({
        'Coefficient (Beta)': mlr_stats_model.params,
        'P-Value (P>|t|)': mlr_stats_model.pvalues
    })
    print(summary_df.to_string())
    
    # Export full OLS statistical summary report to text file asset
    with open("day15_regression_summary.txt", "w") as f:
        f.write(mlr_stats_model.summary().as_text())
    print("\n💾 Formatted OLS report safely exported to 'day15_regression_summary.txt'")

if __name__ == "__main__":
    run_regression_pipeline()