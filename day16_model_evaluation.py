import os
import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score

def run_model_diagnostics():
    print("🚀 Starting Day 16: Model Diagnostics & Residual Analysis...")
    
    # 1. Establish database connection
    db_path = "redhill_market_duckdb.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Please run previous data pipelines.")
    
    conn = duckdb.connect(db_path)
    
    # Executing query over structural columns
    query = """
    SELECT pricing_amount, regional_demand_index, consumer_rating
    FROM regional_market_data
    WHERE pricing_amount IS NOT NULL AND regional_demand_index IS NOT NULL AND consumer_rating IS NOT NULL
    """
    df = conn.execute(query).df()
    conn.close()
    
    print(f"📋 Loaded {len(df)} rows for statistical validation modeling.")
    
    # 2. Define features (X) and target variable (y)
    X = df[['regional_demand_index', 'consumer_rating']]
    y = df['pricing_amount']
    
    X_with_constant = sm.add_constant(X)
    
    # 3. Fit OLS Model
    model = sm.OLS(y, X_with_constant).fit()
    y_pred = model.predict(X_with_constant)
    residuals = model.resid
    
    # 4. Calculate Model Performance Metrics
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)
    
    print("\n================ MODEL PERFORMANCE METRICS ================")
    print(f"📈 R-squared (Coefficient of Determination): {r2:.4f}")
    print(f"📊 Adjusted R-squared:                  {model.rsquared_adj:.4f}")
    print(f"📉 Mean Squared Error (MSE):             {mse:.2f}")
    print(f"📏 Root Mean Squared Error (RMSE):       {rmse:.2f}")
    print("===========================================================\n")
    
    # 5. Generate Diagnostic Plot Matrix
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Residuals vs Fitted values
    sns.scatterplot(x=y_pred, y=residuals, ax=axes[0], alpha=0.6, color='teal')
    axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    axes[0].set_title("Residual Variance Analysis", fontsize=12)
    
    # UPDATED AXIS NAMES: Explicit mapping to dataset columns and model calculations
    axes[0].set_xlabel("Predicted Model Output [Predicted pricing_amount]")
    axes[0].set_ylabel("Residual Errors [Actual pricing_amount - Predicted Value]")
    
    # Plot 2: Normal Q-Q Plot
    sm.qqplot(residuals, line='45', fit=True, ax=axes[1])
    axes[1].set_title("Residual Error Distribution (Q-Q Plot)", fontsize=12)
    
    # UPDATED AXIS NAMES: Clear tracking for statistical quantiles
    axes[1].set_xlabel("Theoretical Quantiles (Perfect Normal Curve Target)")
    axes[1].set_ylabel("Sample Quantiles (Observed Errors from pricing_amount model)")
    
    plt.tight_layout()
    
    # Save chart
    output_img = "day16_residual_analysis.png"
    plt.savefig(output_img, dpi=300)
    plt.close()
    print(f"💾 Validation plots saved successfully as: '{output_img}'")
    print("✅ Day 16 execution completed with updated dataset labels.")

if __name__ == "__main__":
    run_model_diagnostics()