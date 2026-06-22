import duckdb
import pandas as pd
import numpy as np
import scipy.stats as stats

def run_day13_statistical_profiling():
    print("📊 Day 13: Executing Point-Estimate Descriptive Statistics & Z-Score Anomaly Matrix...")
    
    db_path = "redhill_market_duckdb.db"
    
    # 1. CONNECT TO SQL ENGINE AND EXTRACT UNIFIED MATRIX
    con = duckdb.connect(db_path)
    try:
        df = con.execute("SELECT * FROM regional_market_data;").df()
        print(f"📥 Successfully extracted {len(df)} records from database for mathematical profiling.")
    except Exception as e:
        print(f"❌ Extraction failure. Verify database file exists at {db_path}")
        raise e
    finally:
        con.close()
        
    # 2. COMPUTE NATIVE STATISTICAL CHARACTERISTICS VIA SCIPY & PANDAS
    mean_price = np.mean(df["pricing_amount"])
    median_price = np.median(df["pricing_amount"])
    variance_price = stats.tvar(df["pricing_amount"])  # Sample variance (N-1 denominator) via SciPy
    skew_price = stats.skew(df["pricing_amount"])      # Distribution skewness index
    
    print("\n=======================================================")
    print("📋 SYSTEM PARAMETRIC STATISTICAL PROFILE (PRICING AMOUNT)")
    print("=======================================================")
    print(f"• Expected Value (Mean μ) : Rs. {mean_price:.2f}")
    print(f"• Middle Boundary (Median) : Rs. {median_price:.2f}")
    print(f"• Sample Variance (σ²)    : {variance_price:.4f}")
    print(f"• Distribution Skewness   : {skew_price:.4f}")
    print("=======================================================\n")
    
    # 3. VECTOR-MAPPING Z-SCORES FOR STRUCTURAL ANOMALY DETECTION
    # Mathematical formulation: Z = (X - μ) / σ
    df["price_z_score"] = stats.zscore(df["pricing_amount"])
    
    # Define an academic significance threshold: data points beyond +/- 2.5 standard deviations
    outlier_threshold = 2.5
    outliers = df[df["price_z_score"].abs() > outlier_threshold]
    
    print(f"🚨 Statistical Anomalies Detected (|Z| > {outlier_threshold}): {len(outliers)} rows")
    if not outliers.empty:
        # Display anomalies up to top 15 records for quick terminal verification
        print(outliers[["transaction_id", "region", "pricing_amount", "price_z_score"]].head(15).to_string(index=False))
        
    # 4. EXPORT STATISTICALLY PROFILED RUNTIME DATASETS FOR INFERENTIAL CHECKS
    output_path = "day13_statistical_profiles.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Data vectors with calculated Z-scores exported to '{output_path}'. Ready for Day 14 testing.")

if __name__ == "__main__":
    run_day13_statistical_profiling()
    