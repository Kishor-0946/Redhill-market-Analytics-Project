import pandas as pd
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print(" RUNNING DATASET EXPLORATION")
print("==================================================")

if not os.path.exists(file_path):
    print(f" Error: Cannot find the dataset file at {file_path}")
else:
    # Read just the first few rows to inspect the structure safely
    print(" Loading dataset structure...")
    df = pd.read_head = pd.read_csv(file_path, nrows=5)
    
    print("\n SUCCESS: Dataset found!")
    print(f" Total Columns found: {len(df.columns)}")
    print("--------------------------------------------------")
    print("COLUMN NAMES:")
    print(", ".join(df.columns))
    print("--------------------------------------------------")
    print(" FIRST 2 ROWS OF DATA:")
    print(df.head(2))
print("==================================================")