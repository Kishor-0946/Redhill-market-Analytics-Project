import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_distribution_plots():
    print("🚀 Starting Day 10: Data Distribution Visualization Engine...")
    
    # 1. Load the cleaned source file produced on Day 9
    source_file = "day9_clean_market_data.csv"
    
    if not os.path.exists(source_file):
        print(f"❌ Error: {source_file} not found! Please run your Day 9 cleaning script first.")
        return
        
    df = pd.read_csv(source_file)
    print("📋 Cleaned Dataset loaded successfully. Generating analytical plots...")
    
    # 2. Configure global aesthetic settings using Seaborn styles
    sns.set_theme(style="whitegrid")
    
    # 3. Initialize a 1-row, 2-column Matplotlib figure context canvas
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Day 10: Regional Market Analytics - Statistical Distribution Profiles', fontsize=16, fontweight='bold')
    
    # --- PLOT 1: HISTOGRAM WITH KDE FOR SALE PRICE DISTRIBUTION ---
    print("📊 Rendering Subplot 1: Continuous Sale Price Histogram...")
    sns.histplot(
        data=df, 
        x='sale_price', 
        kde=True, 
        color='royalblue', 
        bins=5, 
        ax=axes[0],
        line_kws={'linewidth': 2.5}
    )
    axes[0].set_title('Frequency Count & Density Estimate of Sale Prices', fontsize=12, fontweight='semibold')
    axes[0].set_xlabel('Capped Sale Price (INR)', fontsize=10)
    axes[0].set_ylabel('Transaction Frequency Count', fontsize=10)
    
    # --- PLOT 2: SEABORN DISTRIBUTION & RUG PLOT FOR CUSTOMER RATINGS ---
    print("📊 Rendering Subplot 2: Customer Ratings Probability Density...")
    sns.kdeplot(
        data=df, 
        x='customer_rating', 
        color='darkorange', 
        fill=True, 
        alpha=0.3, 
        linewidth=2, 
        ax=axes[1]
    )
    # Add a rug plot underneath to mark individual transaction observation vectors
    sns.rugplot(data=df, x='customer_rating', color='crimson', ax=axes[1], height=0.05)
    
    axes[1].set_title('Probability Density Curve of Evaluated Customer Ratings', fontsize=12, fontweight='semibold')
    axes[1].set_xlabel('Standardized Customer Rating (Scale 1-5)', fontsize=10)
    axes[1].set_ylabel('Statistical Density Probability', fontsize=10)
    
    # 4. Optimize spacing layouts tightly to avoid overlapping annotations
    plt.tight_layout()
    
    # 5. Export and persist the generated plot figures as a high-resolution PNG image
    output_image = "day10_market_distributions.png"
    plt.savefig(output_image, dpi=300)
    print(f"💾 Graph graphic successfully saved to file asset: {output_image}")
    
    # Display the visual plot container window
    print("👁️ Displaying generated interactive visual canvas...")
    plt.show()

if __name__ == "__main__":
    generate_distribution_plots()