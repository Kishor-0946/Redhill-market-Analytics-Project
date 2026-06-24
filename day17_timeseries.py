import os
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_time_series_foundations():
    print("🕒 Starting Day 17: Time-Series Foundations & Trend Analysis...")
    
    # 1. Establish database connection
    db_path = "redhill_market_duckdb.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Run previous pipeline steps.")
        
    conn = duckdb.connect(db_path)
    
    # Using row_number() to generate sequential ordering since transaction_id is omitted,
    # and tracking regional_demand_index as our volume indicator proxy.
    query = """
    SELECT 
        row_number() OVER () as simulated_sequence_id,
        regional_demand_index
    FROM regional_market_data
    WHERE regional_demand_index IS NOT NULL
    """
    df = conn.execute(query).df()
    conn.close()
    
    print(f"📋 Retrieved {len(df)} sequential records from the SQL engine.")
    
    # 2. Simulate Chronological Time Intervals
    # Grouping every 100 consecutive records into an engineered "Time Block" 
    df['time_block'] = df['simulated_sequence_id'] // 100
    time_series_df = df.groupby('time_block')['regional_demand_index'].mean().reset_index()
    
    # 3. Apply Rolling Statistics (Simple Moving Averages)
    time_series_df['SMA_5'] = time_series_df['regional_demand_index'].rolling(window=5, min_periods=1).mean()
    time_series_df['SMA_20'] = time_series_df['regional_demand_index'].rolling(window=20, min_periods=1).mean()
    
    print("📈 Rolling window statistics calculated successfully using regional_demand_index.")
    
    # 4. Generate Trend Visualization
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")
    
    # Plot original data noise
    plt.plot(time_series_df['time_block'], time_series_df['regional_demand_index'], 
             label='Raw regional_demand_index (Mean per 100 entries)', color='lightgray', alpha=0.7, linewidth=1)
    
    # Plot short-term rolling trend
    plt.plot(time_series_df['time_block'], time_series_df['SMA_5'], 
             label='5-Block Moving Average Trend (SMA 5)', color='teal', linewidth=2)
    
    # Plot long-term macro trend
    plt.plot(time_series_df['time_block'], time_series_df['SMA_20'], 
             label='20-Block Macro Average Trend (SMA 20)', color='crimson', linestyle='--', linewidth=2.5)
    
    # UPDATED TITLES AND AXIS LABELS MAPPED TO DATASET COLUMNS
    plt.title("Day 17 Time-Series Analysis: Smoothing regional_demand_index via Rolling Window SMA", fontsize=14, fontweight='bold')
    plt.xlabel("Simulated Timeline (Sequential Chunks of 100 Dataset Records)", fontsize=12)
    plt.ylabel("Observed regional_demand_index Value", fontsize=12)
    
    plt.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    
    # Save chart asset
    output_img = "day17_time_series_trends.png"
    plt.savefig(output_img, dpi=300)
    plt.close()
    
    print(f"💾 Time-series trend graphic saved as: '{output_img}'")
    print("✅ Day 17 foundations completed successfully with proper dataset names.")

if __name__ == "__main__":
    run_time_series_foundations()