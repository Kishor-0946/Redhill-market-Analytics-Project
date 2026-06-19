import pandas as pd
import numpy as np
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("🚀 DAY 6: ADVANCED GROUP AGGREGATIONS & SEGMENTS")
print("==================================================")

if not os.path.exists(file_path):
    print(f"❌ Error: Cannot find dataset at {file_path}")
else:
    print("⏳ Ingesting and auto-cleaning market data dataset...")
    df = pd.read_csv(file_path)
    
    # Quick structural cleaning from Day 5 to keep data math stable
    if 'discount' in df.columns: df['discount'] = df['discount'].fillna(0)
    if 'rating' in df.columns: df['rating'] = df['rating'].fillna(df['rating'].mean())

    # --------------------------------------------------
    # TASK 1: CATEGORICAL GROUP SEGMENTATION
    # --------------------------------------------------
    print("\n🛒 TASK 1: SPENDING BEHAVIOR PER PRODUCT CATEGORY")
    print("-" * 55)
    
    # Grouping by 'category' and pulling out the 'final_price' mean for each group
    category_spending = df.groupby('category')['final_price'].mean()
    print("• Average Customer Wallet Spend per Category:")
    print(category_spending.round(2).to_string())

    # --------------------------------------------------
    # TASK 2: MULTI-VARIABLE PIVOT MATRICES
    # --------------------------------------------------
    print("\n🗺️ TASK 2: REGIONAL PERFORMANCE & PERFORMANCE MATRICES")
    print("-" * 55)
    
    # We group by 'location' and pass a dictionary to .agg() 
    # specifying exactly which different math operations to run on which column.
    regional_summary = df.groupby('location').agg(
        total_transactions=('user_id', 'count'),
        average_spend=('final_price', 'mean'),
        total_revenue=('final_price', 'sum'),
        average_user_rating=('rating', 'mean')
    )
    
    # Sorting the output so the location making the highest total revenue is at the top
    sorted_regional_summary = regional_summary.sort_values(by='total_revenue', ascending=False)
    
    print("• Multi-Variable Summary Matrix per Region (Sorted by Revenue):")
    # Formatting total revenue column to look neat with commas
    pd.options.display.float_format = '{:,.2f}'.format
    print(sorted_regional_summary)

print("==================================================")