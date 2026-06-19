import pandas as pd
import numpy as np
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("🐼 DAY 4: CONNECTING PURE PYTHON TO PANDAS & NUMPY")
print("==================================================")

if not os.path.exists(file_path):
    print(f"❌ Error: Cannot find dataset at {file_path}")
else:
    print("⏳ Loading dataset... Pandas automatically handles decimals and types!")
    # Pandas instantly converts the CSV table into a powerful DataFrame
    df = pd.read_csv(file_path)
    
    # --------------------------------------------------
    # CONCEPT 1: Dimension Check (Instead of manual loops)
    # --------------------------------------------------
    print("\n📊 STEP 1: VERIFYING TABLE DIMENSIONS")
    print("-" * 40)
    print(f"• In pure Python, we had to slice or loop to count data rows.")
    print(f"• Pandas tells us the matrix shape instantly:")
    print(f"  Total Rows: {df.shape[0]:,} | Total Columns: {df.shape[1]}")

    # --------------------------------------------------
    # CONCEPT 2: Column Extraction (Vector vs List Comprehension)
    # --------------------------------------------------
    print("\n🔢 STEP 2: HIGH-SPEED VECTOR STATS (NumPy)")
    print("-" * 40)
    # Instead of running a list comprehension loop, we isolate the column array.
    # We turn it into a high-speed NumPy vector block to process it instantly.
    prices_array = df['final_price'].to_numpy()
    
    avg_price = np.mean(prices_array)
    max_price = np.max(prices_array)
    
    print(f"• NumPy Calculated Average Price : Rs.{avg_price:.2f}")
    print(f"• NumPy Calculated Maximum Price : Rs.{max_price:.2f}")

    # --------------------------------------------------
    # CONCEPT 3: Boolean Mask Filtering (Instead of 'if' statements)
    # --------------------------------------------------
    print("\n🎯 STEP 3: DATA FILTERING WITH BOOLEAN MASKS")
    print("-" * 40)
    # Remember your line: [price for price in all_prices if price > 500]
    # Pandas creates a "Boolean Mask" (a list of True/False flags) across the column
    
    high_value_df = df[df['final_price'] > 500]
    print(f"• Filtered Rows where final_price > Rs.500: {len(high_value_df):,}")
    
    # Complex Filter: Let's find orders over Rs. 500 that were ALSO returned!
    returned_high_value = df[(df['final_price'] > 500) & (df['is_returned'] == 1)]
    print(f"• Alert: Found {len(returned_high_value):,} high-value returned transactions.")

    print("\n📋 PREVIEW OF MATCHING SUBSETS:")
    print(high_value_df[['user_id', 'category', 'final_price', 'location']].head(3))
    # --------------------------------------------------
    # CONCEPT 4: DATA QUIRKS & MISSING VALUE AUDIT
    # --------------------------------------------------
    print("\n🔍 STEP 4: DETECTING MISSING DATA BLANKS (NaN)")
    print("-" * 40)
    
    # .isnull().sum() checks every single cell and counts the empty ones per column
    missing_counts = df.isnull().sum()
    
    # Filter out columns that have at least 1 missing value
    columns_with_missing_data = missing_counts[missing_counts > 0]
    
    if len(columns_with_missing_data) > 0:
        print("⚠️ Found empty cells in the following attributes:")
        for col_name, count in columns_with_missing_data.items():
            percentage = (count / len(df)) * 100
            print(f"  • {col_name}: {count:,} missing rows ({percentage:.2f}%)")
            
        print("\n💡 Tip: On Day 5, we will learn how to clean these up using .fillna()")
    else:
        print("✅ Clean Data Check! No missing values or empty cells found across all 20 columns.")
print("==================================================")
