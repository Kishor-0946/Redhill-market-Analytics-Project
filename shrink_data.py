import pandas as pd
import os

# The exact path to your dataset inside your separate data folder
file_path = "data/market_data.csv.csv"

print("--------------------------------------------------")
if not os.path.exists(file_path):
    print(f" Error: Cannot find your dataset file at: {file_path}")
    print("Please double check if your folder name is 'data' and the file is named 'market_data.csv.csv'")
else:
    print(" Reading your 10 Lakh row dataset from the E: Drive...")
    df = pd.read_csv(file_path)
    
    print(f" Original row count: {len(df)} rows.")
    
    # Randomly sample exactly 1 Lakh (100,000) rows safely
    target_rows = min(100000, len(df))
    shrunk_df = df.sample(n=target_rows, random_state=42)
    
    print(f" New shrunk row count: {len(shrunk_df)} rows (1 Lakh).")
    
    # Overwrite the original file with your lightweight dataset
    shrunk_df.to_csv(file_path, index=False)
    print(" Success! Your dataset has been reduced to exactly 1 Lakh rows.")
print("--------------------------------------------------")