import duckdb
import pandas as pd
import scipy.stats as stats

def run_inferential_analytics():
    print("Connecting to local database layer...")
    con = duckdb.connect("redhill_market_duckdb.db")
    
    # Target your verified table and columns directly
    query = "SELECT pricing_amount, region FROM regional_market_data;"
    print(f"🚀 Executing Query: {query}")
    df = con.execute(query).df()
    
    print(f"Successfully loaded {len(df)} rows into the Pandas matrix.\n")
    
    # Get unique regions present in your dataset dynamically
    unique_regions = df['region'].dropna().unique()
    print(f"🌍 Regions detected in data: {list(unique_regions)}")
    
    if len(unique_regions) < 2:
        print("❌ Error: Need at least 2 distinct regions to perform a T-Test comparison.")
        con.close()
        return
        
    # Pick the first two regions for our comparative hypothesis test
    region_a = unique_regions[0]
    region_b = unique_regions[1]
    
    # --- STATISTICAL HYPOTHESIS TESTING FRAMEWORK ---
    print(f"\n--- Running Independent Two-Sample T-Test ---")
    print(f"Null Hypothesis (H0): Mean pricing amount in {region_a} == Mean pricing amount in {region_b}")
    print(f"Alternative Hypothesis (H1): Mean pricing amount in {region_a} != Mean pricing amount in {region_b}\n")
    
    # Slice pricing vectors using your exact database column values
    group_a_prices = df[df['region'] == region_a]['pricing_amount']
    group_b_prices = df[df['region'] == region_b]['pricing_amount']
    
    print(f"Group '{region_a}' Sample Size: {len(group_a_prices)}")
    print(f"Group '{region_b}' Sample Size: {len(group_b_prices)}")
    
    if len(group_a_prices) > 1 and len(group_b_prices) > 1:
        # Perform Welch's T-Test (equal_var=False handles variance mismatch safely)
        t_stat, p_val = stats.ttest_ind(group_a_prices, group_b_prices, equal_var=False)
        
        print(f"\n📊 T-Statistic: {t_stat:.4f}")
        print(f"📊 P-Value: {p_val:.4f}")
        
        # Standard alpha significance threshold (0.05)
        if p_val < 0.05:
            print(f"Decision: Reject Null Hypothesis (Significant difference in market pricing between {region_a} and {region_b}).")
        else:
            print(f"Decision: Fail to Reject Null Hypothesis (No statistically significant pricing difference found).")
    else:
        print("Skipping T-Test: Insufficient data distributions within the selected regions.")
        
    con.close()
    print("\nDatabase session closed safely.")

if __name__ == "__main__":
    run_inferential_analytics()