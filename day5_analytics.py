import pandas as pd
import numpy as np
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("📊 DAY 5: DATA WRANGLING & DESCRIPTIVE STATISTICS")
print("==================================================")

if not os.path.exists(file_path):
    print(f"❌ Error: Cannot find dataset at {file_path}")
else:
    print("⏳ Ingesting 1 Lakh rows of market data into memory...")
    df = pd.read_csv(file_path)
    
    # --------------------------------------------------
    # TASK 1: DATA WRANGLING (CLEANING MISSING GAPS)
    # --------------------------------------------------
    print("\n🧼 TASK 1: WRANGLING & CLEANING DATA QUIRKS")
    print("-" * 50)
    
    # Check original count of missing rows before handling them
    initial_nan = df.isnull().sum().sum()
    print(f"• Total missing cells found initially: {initial_nan:,}")
    
    # Let's cleanly fill missing numeric columns safely
    # If discount is missing, change it to 0
    if 'discount' in df.columns:
        df['discount'] = df['discount'].fillna(0)
        
    # If ratings are missing, fill them with the average (mean) rating of the platform
    if 'rating' in df.columns:
        mean_rating = df['rating'].mean()
        df['rating'] = df['rating'].fillna(mean_rating)
        
    # For all other remaining empty cells, we'll replace them with 0 or 'Unknown' safely
    df = df.infer_objects(copy=False) # Keeps types stable
    df.fillna({'review_count': 0, 'stock': 0, 'location': 'Unknown'}, inplace=True)
    
    remaining_nan = df.isnull().sum().sum()
    print(f"• Cleaning complete! Remaining missing cells: {remaining_nan}")

    # --------------------------------------------------
    # TASK 2: DESCRIPTIVE STATISTICS (MATHEMATICAL METRICS)
    # --------------------------------------------------
    print("\n🔢 TASK 2: DESCRIPTIVE STATISTICAL DASHBOARD")
    print("-" * 50)
    
    # Isolate key numeric columns to inspect your customer spending habits
    target_numerical_cols = ['price', 'discount', 'final_price', 'rating']
    
    # .describe() automatically calculates mean, std, min, max, and quantiles!
    stats_summary = df[target_numerical_cols].describe()
    print(stats_summary.round(2))
    
    # Advanced: Manually extract variance using NumPy on final_price to show dispersion
    final_price_vector = df['final_price'].to_numpy()
    price_variance = np.var(final_price_vector)
    price_std_dev = np.std(final_price_vector)
    
    print(f"\n💡 Deep-Dive Dispersion Stats for 'final_price':")
    print(f"  • Standard Deviation (Spread) : Rs.{price_std_dev:.2f}")
    print(f"  • Variance (Squared Spread)   : {price_variance:.2f}")

    # --------------------------------------------------
    # TASK 3: VALUE DISTRIBUTION TRACKING (CATEGORICAL METRICS)
    # --------------------------------------------------
    print("\n🎯 TASK 3: MARKET SHARE & DEMOGRAPHIC SPREAD")
    print("-" * 50)
    
    print("🛒 Top 5 Category Volumes across 1 Lakh transactions:")
    print(df['category'].value_counts().head(5))
    
    print("\n💳 Most Popular Payment Methods Used:")
    print(df['payment_method'].value_counts())

print("==================================================")