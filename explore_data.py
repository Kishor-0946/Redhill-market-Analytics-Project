import pandas as pd
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("🔍 SYSTEM CHECK: EXTRACTING ALL DATASET COLUMNS")
print("==================================================")

if not os.path.exists(file_path):
    print(f"❌ Error: Cannot find the dataset file at: {file_path}")
else:
    print("⏳ Reading dataset structure from E: Drive...\n")
    # Read just the header row to make it super fast
    df = pd.read_csv(file_path, nrows=1)
    
    print(f"✅ Success! Total Columns Found: {len(df.columns)}")
    print("--------------------------------------------------")
    print("📊 VERTICAL COLUMN LIST:")
    print("--------------------------------------------------")
    
    # Loop through columns and print them vertically with numbers
    for index, column_name in enumerate(df.columns, start=1):
        print(f"{index}. {column_name}")
        
print("==================================================")