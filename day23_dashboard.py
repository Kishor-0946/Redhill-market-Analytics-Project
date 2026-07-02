import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Redhill Market Analytics", layout="wide")
st.title("📈 Regional Market & Trend Analytics System")
st.markdown("### Executive Performance Dashboard (Optimized)")

# ---------------------------------------------------------
# CACHED DATABASE FUNCTIONS
# ---------------------------------------------------------
# The decorator below tells Streamlit to save the output of this function.
# If the user selects the same region and price bounds again, it skips the SQL query
# and loads the DataFrame instantly from RAM.

@st.cache_data(ttl=3600) # Cache expires after 1 hour (3600 seconds)
def fetch_market_data(selected_regions, min_price, max_price):
    """
    Connects to DuckDB, safely queries the data using parameterized inputs, 
    and returns a Pandas DataFrame.
    """
    # If no regions are selected, return an empty dataframe
    if not selected_regions:
        return pd.DataFrame()
    
    # Open connection
    conn = duckdb.connect("redhill_market_duckdb.db")
    
    # Prepare the query using parameters to prevent SQL injection
    # We dynamically generate the correct number of question marks for the IN clause
    placeholders = ", ".join(["?"] * len(selected_regions))
    
    query = f"""
        SELECT 
            transaction_id, 
            region, 
            pricing_amount, 
            consumer_rating, 
            discount_percentage
        FROM regional_market_data
        WHERE region IN ({placeholders})
        AND pricing_amount BETWEEN ? AND ?
    """
    
    # Combine all parameters into a single tuple
    params = tuple(selected_regions) + (min_price, max_price)
    
    # Execute and fetch data
    df = conn.execute(query, params).df()
    conn.close()
    
    return df

# ---------------------------------------------------------
# SIDEBAR UI CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Filter Market Data")

# Define available regions 
available_regions = ["Mumbai", "Delhi", "Hyderabad", "Chennai", "Bangalore"]

# Multi-select for regions
regions = st.sidebar.multiselect(
    "Select Regions:",
    options=available_regions,
    default=available_regions
)

# Slider for price range
price_range = st.sidebar.slider(
    "Pricing Amount Bounds (Rs.):",
    min_value=0,
    max_value=100000,
    value=(0, 50000),
    step=1000
)

# ---------------------------------------------------------
# MAIN DASHBOARD LOGIC
# ---------------------------------------------------------
# Display a loading spinner ONLY when the cache is missed and the DB is queried
with st.spinner("Fetching data from backend..."):
    # Call our cached function
    data = fetch_market_data(regions, price_range[0], price_range[1])

if data.empty:
    st.warning("No data available for the selected filters. Please adjust your criteria.")
else:
    # --- Top KPI Metrics ---
    total_transactions = len(data)
    avg_price = data['pricing_amount'].mean()
    avg_rating = data['consumer_rating'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{total_transactions:,}")
    col2.metric("Average Order Value", f"Rs. {avg_price:,.2f}")
    col3.metric("Average Consumer Rating", f"{avg_rating:.2f} / 5.0")
    
    st.markdown("---")
    
    # --- Dynamic Visualizations (Plotly) ---
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Price vs. Rating Distribution")
        fig_scatter = px.scatter(
            data, 
            x="pricing_amount", 
            y="consumer_rating", 
            color="region",
            trendline="ols",
            title="Regression Vector Scatter",
            opacity=0.6
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with chart_col2:
        st.subheader("Revenue Contribution by Region")
        # Aggregate locally in pandas for the pie chart
        region_revenue = data.groupby("region")["pricing_amount"].sum().reset_index()
        fig_pie = px.pie(
            region_revenue, 
            names="region", 
            values="pricing_amount",
            title="Market Share",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)