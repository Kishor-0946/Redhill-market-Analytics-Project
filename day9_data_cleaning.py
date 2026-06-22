import pandas as pd
import numpy as np

def load_and_clean_market_data():
    print("🚀 Starting Day 9: Advanced Data Cleaning Pipeline...")
    
    # 1. Simulate receiving a raw, dirty regional transaction dataset
    # This dataset includes missing values, mismatched types, and extreme anomalies (outliers)
    raw_data = {
        'transaction_id': ['TXN_001', 'TXN_002 ', 'TXN_003', 'TXN_004', 'TXN_005', 'TXN_006'],
        'region': ['Mumbai', 'Delhi', ' bangalore ', 'Chennai', 'Mumbai', 'Delhi'],
        'sale_price': ['12000', '15500', None, '9800', '250000', '11200'], # Note '250000' is an artificial outlier; one None value
        'discount_applied': [10.5, None, 5.0, 0.0, 15.0, 8.5],
        'customer_rating': ['4.5', '3.8', '4.2', 'not_rated', '5.0', '4.1'] # Mismatched data types
    }
    
    df = pd.DataFrame(raw_data)
    print("\n📊 Initial Raw Dataset Snapshot:")
    print(df)
    
    # ==========================================
    # 📝 PHASE 1: DATA TYPE FORMATTING & STRUCTURAL CLEANING
    # ==========================================
    print("\n⚙️ Phase 1: Formatting string boundaries and explicit types...")
    
    # Trim whitespaces and clean categorical formatting
    df['transaction_id'] = df['transaction_id'].str.strip()
    df['region'] = df['region'].str.strip().str.capitalize()
    
    # Handle data type conversions with safe error coercion
    df['sale_price'] = pd.to_numeric(df['sale_price'], errors='coerce')
    df['customer_rating'] = pd.to_numeric(df['customer_rating'], errors='coerce')
    
    # ==========================================
    # 🧼 PHASE 2: HANDLING MISSING VALUES (IMPUTATION)
    # ==========================================
    print("\n🧼 Phase 2: Resolving missing values (NaN Imputation)...")
    
    # Impute Sale Price with the column median
    median_price = df['sale_price'].median()
    df['sale_price'] = df['sale_price'].fillna(median_price)
    
    # Impute Discounts with a default corporate strategy of 0
    df['discount_applied'] = df['discount_applied'].fillna(0.0)
    
    # Impute Customer Rating with the column mean (rounded up)
    mean_rating = round(df['customer_rating'].mean(), 2)
    df['customer_rating'] = df['customer_rating'].fillna(mean_rating)
    
    # ==========================================
    # 🔍 PHASE 3: OUTLIER DETECTION & HANDLING (IQR METHOD)
    # ==========================================
    print("\n🔍 Phase 3: Executing statistical Interquartile Range (IQR) filter...")
    
    # Calculate Statistical Quartiles
    Q1 = df['sale_price'].quantile(0.25)
    Q3 = df['sale_price'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"   [Stats Engine] Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
    print(f"   [Stats Engine] Outlier Threshold Boundary: Values must be between {lower_bound} and {upper_bound}")
    
    # Identify and flag outliers
    outliers = df[(df['sale_price'] < lower_bound) | (df['sale_price'] > upper_bound)]
    print(f"   ⚠️ Found {len(outliers)} statistical outlier record(s):")
    print(outliers)
    
    # Clip/Cap the outliers to the upper bound threshold to prevent downstream analytical bias
    df['sale_price'] = np.where(df['sale_price'] > upper_bound, upper_bound, df['sale_price'])
    df['sale_price'] = np.where(df['sale_price'] < lower_bound, lower_bound, df['sale_price'])
    
    print("\n✅ Cleaned, Reformatted, and Outlier-Capped Dataset:")
    print(df)
    
    # Save clean dataset back as a reliable CSV source file
    df.to_csv("day9_clean_market_data.csv", index=False)
    print("\n💾 File successfully written to: day9_clean_market_data.csv")

if __name__ == "__main__":
    load_and_clean_market_data()