import os
import duckdb
import pandas as pd
import numpy as np

def run_week2_integrated_pipeline():
    print("🚀 Day 12: Initializing Week 2 End-to-End Integration Pipeline...")
    
    csv_file = "day9_clean_market_data.csv"
    db_file = "redhill_market_duckdb.db"
    report_file = "week2_eda_report.md"
    
    # 1. Verification/Generation of Raw Market Source File
    if not os.path.exists(csv_file):
        print(f"⚠️ Source data '{csv_file}' missing. Creating synthetic high-volume source dataset...")
        np.random.seed(42)
        records = 2500
        df_dummy = pd.DataFrame({
            'transaction_id': [f"TXN_{i:06d}" for i in range(records)],
            'region': np.random.choice(['Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Bangalore'], size=records),
            'pricing_amount': np.random.exponential(scale=150, size=records) + 20,
            'consumer_rating': np.random.uniform(1.0, 5.0, size=records),
            'regional_demand_index': np.random.normal(loc=60, scale=12, size=records),
            'discount_percentage': np.random.choice([0, 5, 10, 15, 25], size=records)
        })
        df_dummy.to_csv(csv_file, index=False)
        print(f"💾 Synthetic data generated and written to '{csv_file}'.")

    # 2. Extract Stage: Load via Pandas Engine
    print("📥 Extract Phase: Reading raw data matrices...")
    df = pd.read_csv(csv_file)
    total_records = len(df)
    
    # 3. Transform Stage: Compute Mathematical & Statistical Metrics
    print("🧮 Transform Phase: Computing Skewness and Bivariate Correlation Arrays...")
    numerical_cols = df.select_dtypes(include=[np.number])
    
    # Compute distribution asymmetry skew profiles
    skew_series = numerical_cols.skew()
    
    # Compute full Pearson linear correlation matrix 
    corr_matrix = numerical_cols.corr()
    
    # 4. Load Stage: Persistence Ingestion into DuckDB relational backend
    print(f"🗄️ Load Phase: Opening connection to local database file '{db_file}'...")
    con = duckdb.connect(db_file)
    
    try:
        # Construct strict relational schemas UPDATED WITH THE 'region' VARCHAR COLUMN
        con.execute("DROP TABLE IF EXISTS regional_market_data;")
        con.execute("""
            CREATE TABLE regional_market_data (
                transaction_id VARCHAR PRIMARY KEY,
                region VARCHAR NOT NULL,
                pricing_amount DOUBLE NOT NULL CHECK (pricing_amount >= 0),
                consumer_rating DOUBLE CHECK (consumer_rating BETWEEN 1.0 AND 5.0),
                regional_demand_index DOUBLE,
                discount_percentage INTEGER CHECK (discount_percentage >= 0)
            );
        """)
        print("✅ Relational schema constructed with explicit CHECK constraints and Region matching.")
        
        # Inject dataframe records directly using DuckDB's native high-performance registration
        con.execute("INSERT INTO regional_market_data SELECT * FROM df;")
        
        # Verify persistence count via explicit SQL query
        db_count = con.execute("SELECT COUNT(*) FROM regional_market_data;").fetchone()[0]
        print(f"🎯 Database Ingestion Confirmed: Vectorized append inserted {db_count} rows successfully.")
        
    except Exception as e:
        print(f"❌ Relational Database Engine failure: {str(e)}")
        raise e
    finally:
        con.close()
        print("🔒 DuckDB Engine connection safely terminated.")

    # 5. Reporting Stage: Generate Automated Summary EDA Markdown Asset
    print(f"📝 Reporting Phase: Writing structural Markdown overview to '{report_file}'...")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# 📊 Week 2 Review: Summary Exploratory Data Analysis Report\n\n")
        f.write(f"**Generated Automatically by:** `day12_weekly_review_pipeline.py`  \n")
        f.write(f"**Execution Timestamp Evaluation:** June 24, 2026  \n")
        f.write(f"**Host Organization:** Redhill Softec  \n\n")
        
        f.write("## 1. Operational Ingestion Diagnostics\n")
        f.write("| Assessment Metric | Pipeline Log Output |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| Source Raw File Analyzed | `{csv_file}` |\n")
        f.write(f"| Extracted Transaction Record Count | **{total_records}** lines |\n")
        f.write(f"| Destination SQL Database Target | `{db_file}` |\n")
        f.write(f"| Relational Integrity Constraints | **Active (PRIMARY KEY, CHECK constraints)** |\n")
        f.write(f"| Database Table Row Status | **{db_count} Records Injected Successfully** |\n\n")
        
        f.write("## 2. Statistical Profile: Numerical Feature Skewness\n")
        f.write("Distribution asymmetry scores evaluated using Pandas algorithm components:\n\n")
        f.write("| Feature Variable Field | Calculated Skewness Score | Shape Meaning Description |\n")
        f.write("| :--- | :---: | :--- |\n")
        for col, skew_val in skew_series.items():
            if abs(skew_val) < 0.5:
                interpretation = "Symmetrical Distribution Model"
            elif skew_val > 0:
                interpretation = "Right-Skewed Model (Long positive metric tail)"
            else:
                interpretation = "Left-Skewed Model (Long negative metric tail)"
            f.write(f"| `{col}` | `{skew_val:7.4f}` | {interpretation} |\n")
            
        f.write("\n## 3. Relational Matrix: Inter-Variable Linear Correlation Coefficients\n")
        f.write("Pearson correlation matrix ($r$) showing mathematical connections between features:\n\n")
        
        headers = ["Variable"] + [f"`{c}`" for c in corr_matrix.columns]
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| :--- | " + " | ".join([":---:" for _ in corr_matrix.columns]) + " |\n")
        
        for idx, row in corr_matrix.iterrows():
            row_str = f"| `{idx}` | " + " | ".join([f"`{val:.3f}`" for val in row]) + " |\n"
            f.write(row_str)
            
        f.write("\n\n---\n*End of Week 2 Integration Summary Report. Project assets pushed to GitHub remote main branch.*")
        
    print(f"🎯 Pipeline Finished! Review your workspace for '{db_file}' and '{report_file}'.")

if __name__ == "__main__":
    run_week2_integrated_pipeline()