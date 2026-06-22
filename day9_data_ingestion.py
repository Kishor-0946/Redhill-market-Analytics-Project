import os
import time
import duckdb
import pandas as pd

# Define paths (Ensure these point to your Week 1 outputs)
DB_PATH = "redhill_market_duckdb.db"
# Assuming your week 1 clean dataset was saved as a CSV or parquet file
CLEAN_DATA_PATH = "cleaned_market_data.csv" 

def run_high_volume_pipeline():
    print("🚀 Day 9: Starting High-Volume Data Ingestion Pipeline...")
    
    # 1. Establish localized database handshake
    conn = duckdb.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS regional_market_data")
    
    # Ensure the table exists from previous setups (Mock schema alignment check)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regional_market_data (
            transaction_id VARCHAR PRIMARY KEY,
            region VARCHAR NOT NULL,
            product_category VARCHAR,
            revenue FLOAT,
            user_rating FLOAT
        );
    """)
    
    # 2. Check if clean source file exists; if not, generate mock data for validation
    if not os.path.exists(CLEAN_DATA_PATH):
        print(f"⚠️ Clean file not found at {CLEAN_DATA_PATH}. Generating ~100,000 mock records...")
        import numpy as np
        regions = ["Mumbai", "Delhi", "Hyderabad", "Chennai", "Bangalore"]
        categories = ["Electronics", "Apparel", "Home Decor", "Groceries"]
        
        mock_data = pd.DataFrame({
            'transaction_id': [f"TXN_{i:06d}" for i in range(100000)],
            'region': np.random.choice(regions, 100000),
            'product_category': np.random.choice(categories, 100000),
            'revenue': np.random.uniform(500, 50000, 100000).round(2),
            'user_rating': np.random.uniform(1.0, 5.0, 100000).round(1)
        })
        mock_data.to_csv(CLEAN_DATA_PATH, index=False)
        print(f"✅ Mock records generated and cached successfully.")

    # 3. Stream Bulk Data Migration Layer & Measure Ingestion Performance
    start_time = time.time()
    
    print("📥 Loading operational dataset into memory matrix...")
    df_to_insert = pd.read_csv(CLEAN_DATA_PATH)
    
    print(f"🔄 Migrating {len(df_to_insert):,} records directly into SQL engine...")
    # DuckDB can register and read a Pandas DataFrame directly from memory
    print(df_to_insert.dtypes)
    print(df_to_insert.head())
    cursor.execute("INSERT INTO regional_market_data SELECT * FROM df_to_insert;")
    
    # 4. Enforce Transactional Integrity Commit
    conn.commit() 
    ingestion_time = time.time() - start_time
    print(f"💾 Database .commit() successful. Ingestion completed in {ingestion_time:.4f} seconds.")
    
    # 5. Execute Structured Analytical Queries (SQL vs. Pandas Translation)
    print("\n📊 Executing Analytical Queries Directly inside SQL Engine...")
    
    # Metric Query: Extract transactional metrics aggregated by region
    sql_query = """
        SELECT 
            region, 
            COUNT(transaction_id) AS total_transactions,
            ROUND(AVG(revenue), 2) AS average_revenue,
            ROUND(AVG(user_rating), 2) AS average_rating
        FROM regional_market_data
        GROUP BY region
        ORDER BY total_transactions DESC;
    """
    
    query_start = time.time()
    results_df = cursor.execute(sql_query).df()
    query_time = time.time() - query_start
    
    print("\n--- REGIONAL SHARE METRICS DUMP ---")
    print(results_df.to_string(index=False))
    print(f"-----------------------------------")
    print(f"⏱️ SQL query execution response latency: {query_time:.5f} seconds.")
    
    # Clean workspace connection handshakes
    cursor.close()
    conn.close()
    print("\n🔒 Connection handshake safely terminated. Pipeline clear.")

if __name__ == "__main__":
    run_high_volume_pipeline()
    