import pandas as pd
import numpy as np
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("DAY 4: CONNECTING CORE PYTHON TO PANDAS")
print("==================================================")

if not os.path.exists(file_path):
    print(f" Error: Cannot find dataset at {file_path}")
else:
    print("⏳ Loading dataset... Pandas automatically handles decimals and rows!")
    # Pandas reads the data and automatically fixes data types (strings vs decimals)
    df = pd.read_csv(file_path)
    
    # --------------------------------------------------
    # LINK TO DAY 3 - CONCEPT 1: Dimension Check
    # --------------------------------------------------
    print("\n STEP 1: COMPARED TO PURE PYTHON LISTS")
    print("-" * 40)
    print(f"• In pure Python, you had to loop to count rows.")
    print(f"• Pandas tells us instantly using '.shape':")
    print(f"  Total Rows: {df.shape[0]:,} | Total Columns: {df.shape[1]}")

    # --------------------------------------------------
    # LINK TO DAY 3 - CONCEPT 2: Extracting Column (NumPy Vector)
    # --------------------------------------------------
    print("\n🔢 STEP 2: NO COMPREHENSION LOOPS NEEDED")
    print("-" * 40)
    # Instead of running a list comprehension loop, we grab the column instantly.
    # We turn it into a high-speed NumPy array vector to calculate statistics.
    prices_array = df['final_price'].to_numpy()
    
    avg_price = np.mean(prices_array)
    print(f"• Average Final Price computed instantly: Rs.{avg_price:.2f}")

    # --------------------------------------------------
    # LINK TO DAY 3 - CONCEPT 3: Boolean Mask Filtering
    # --------------------------------------------------
    print("\n🎯 STEP 3: HIGH-SPEED BOOLEAN MASK FILTERING")
    print("-" * 40)
    # Remember your line: [price for price in all_prices if price > 500]
    # In Pandas, we use a "Boolean Mask" which maps True/False flags across the table.
    
    high_value_mask = df['final_price'] > 500
    high_value_df = df[high_value_mask]
    
    print(f"• Filtered Rows where final_price > 500: {len(high_value_df):,}")
    print("\n📋 Previewing the top 3 matches:")
    print(high_value_df[['user_id', 'category', 'final_price', 'location']].head(3))

print("==================================================")