import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def perform_exploratory_analysis():
    print("🚀 Day 11: Starting Exploratory Data Analysis Engine...")
    
    # 1. Load the clean dataset generated on Day 9
    try:
        df = pd.read_csv("day9_clean_market_data.csv")
        print("💾 Clean market data successfully loaded.")
    except FileNotFoundError:
        print("❌ Error: 'day9_clean_market_data.csv' not found. Generating dummy dataset for analysis...")
        # Fallback dummy dataset matching the project context
        np.random.seed(42)
        records = 1000
        df = pd.DataFrame({
            'transaction_id': [f"TXN_{i:06d}" for i in range(records)],
            'pricing_amount': np.random.exponential(scale=200, size=records) + 10,
            'consumer_rating': np.random.uniform(1.0, 5.0, size=records),
            'regional_demand_index': np.random.normal(loc=50, scale=15, size=records),
            'discount_percentage': np.random.choice([0, 5, 10, 15, 20], size=records)
        })

    # 2. Select only numerical columns for correlation matrix and skewness
    numerical_cols = df.select_dtypes(include=[np.number])
    
    print("\n--- 📊 STATISTICAL PROFILE: SKEWNESS ANALYSIS ---")
    # Calculate skewness: 0 means perfectly symmetrical, >0 means right-skewed, <0 means left-skewed
    skew_values = numerical_cols.skew()
    for col, skew_val in skew_values.items():
        if abs(skew_val) < 0.5:
            desc = "Fairly Symmetrical"
        elif skew_val > 0:
            desc = "Moderately/Highly Right-Skewed (Positive Tail)"
        else:
            desc = "Moderately/Highly Left-Skewed (Negative Tail)"
        print(f"🔹 {col:<25} | Skewness: {skew_val:>7.3f} | Profile: {desc}")

    print("\n--- 🧮 CORRELATION ENGINE: PEARSON COEFFICIENTS ---")
    # Compute the linear correlation matrix
    correlation_matrix = numerical_cols.corr()
    print(correlation_matrix.round(3))

    # 3. Generating High-Resolution Graphic Assets
    print("\n🎨 Generating annotated Correlation Heatmap layout...")
    plt.figure(figsize=(8, 6))
    
    # Render heatmap layout using Seaborn
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap="coolwarm", 
        fmt=".2f", 
        linewidths=0.5, 
        vmin=-1, 
        vmax=1
    )
    
    plt.title("Regional Market Analytics: Metric Correlation Matrix", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    
    # Exporting visual asset straight to directory
    output_img = "day11_correlation_matrix.png"
    plt.savefig(output_img, dpi=300)
    plt.close()
    print(f"🎯 Visual asset saved successfully as '{output_img}'.")
    print("✅ Day 11 Exploratory Data Analysis execution completed successfully.")

if __name__ == "__main__":
    perform_exploratory_analysis()
    