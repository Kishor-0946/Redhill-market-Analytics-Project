import csv
import os

file_path = "data/market_data.csv.csv"

print("==================================================")
print("🐍 DAY 3: CORE PYTHON APPLIED TO REAL CSV DATA")
print("==================================================")

if not os.path.exists(file_path):
    print(f"❌ Error: Cannot find dataset at {file_path}")
else:
    print("⏳ Reading data using pure Python (No Pandas)...")
    
    # We will load a few rows into a raw Python list to inspect them
    raw_rows = []
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        # csv.DictReader automatically converts each row into a Python DICTIONARY!
        # The keys of the dictionary will be your column headers (user_id, final_price, etc.)
        csv_reader = csv.DictReader(file)
        
        # Grab the first 10 rows using a simple loop
        for index, row in enumerate(csv_reader):
            if index >= 10:
                break
            raw_rows.append(row)

    # --------------------------------------------------
    # 1. DICTIONARIES: Accessing specific column keys
    # --------------------------------------------------
    print("\n🔹 CONCEPT 1: ACCESSING DICTIONARY DATA")
    print("-" * 40)
    # Let's take the very first order record (index 0) from our list
    first_order = raw_rows[0]
    
    # Print specific details using the exact column keys you provided
    print(f"• User ID       : {first_order['user_id']}")
    print(f"• Category      : {first_order['category']}")
    print(f"• Final Price   : Rs.{first_order['final_price']}")
    print(f"• Location      : {first_order['location']}")

# --------------------------------------------------
    # 2. LIST COMPREHENSION 1: Extracting an Array
    # --------------------------------------------------
    print("\n🔹 CONCEPT 2: EXTRACTING A LIST OF PRICES")
    print("-" * 40)
    # FIX: We use float(order['final_price']) instead of int() to support decimals!
    all_prices = [float(order['final_price']) for order in raw_rows]
    print(f"• List of extracted prices: {all_prices}")

    # --------------------------------------------------
    # 3. LIST COMPREHENSION 2: Filtering Data
    # --------------------------------------------------
    print("\n🔹 CONCEPT 3: FILTERING WITH LIST COMPREHENSIONS")
    print("-" * 40)
    # Goal: Filter out only the prices that are greater than Rs. 500.00
    high_value_prices = [price for price in all_prices if price > 500]
    print(f"• Filtered High-Value Prices (>500): {high_value_prices}")
    
    # Goal: Find all orders where the user returned the item ('is_returned' == '1')
    returned_orders = [order['user_id'] for order in raw_rows if order['is_returned'] == '1']
    print(f"• User IDs who returned items: {returned_orders}") 
    