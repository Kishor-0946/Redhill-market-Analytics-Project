import os
import duckdb
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ==========================================
# 1. PAGE SETUP & CANVAS INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Redhill Integrated Analytics System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check database existence before continuing
DB_PATH = "redhill_market_duckdb.db"
if not os.path.exists(DB_PATH):
    st.error(f"❌ Database file '{DB_PATH}' was not found in your active directory. Run previous extraction files.")
    st.stop()

# ==========================================
# 2. SIDEBAR FILTER INPUT CONTROLS (Day 20 Context)
# ==========================================
with st.sidebar:
    st.header("🔑 Control Panel Filters")
    st.markdown("Adjust parameters to query the DuckDB layer dynamically:")
    st.markdown("---")
    
    # Filter A: Target Market Regions Selector
    available_regions = ["Mumbai", "Delhi", "Hyderabad", "Chennai", "Bangalore"]
    selected_regions = st.multiselect(
        label="🌍 Select Target Market Regions",
        options=available_regions,
        default=available_regions,
        help="Slices rows based on geographic attributes."
    )
    
    # Filter B: Minimum Consumer Rating Slider
    min_rating = st.slider(
        label="⭐ Minimum Consumer Rating Threshold",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.1
    )
    
    # Filter C: Product Pricing Range Window Slider
    price_range = st.slider(
        label="💰 Product Pricing Window (Rs.)",
        min_value=1000,
        max_value=20000,
        value=(2000, 18000),
        step=500
    )
    
    st.markdown("---")
    st.info(
        "**Student:** Kishor\n\n"
        "**Track:** B.Sc. Data Analytics\n\n"
        "**Stack:** DuckDB + Streamlit + Plotly"
    )

# ==========================================
# 3. CORE DATABASE HOOKS & EXECUTIONS (Day 22)
# ==========================================
def fetch_filtered_market_data(regions, min_rate, min_price, max_price):
    """Establishes a safe, parameterized SQL read stream from DuckDB."""
    if not regions:
        return pd.DataFrame() # Return empty skeleton frame if no regions are selected
        
    conn = duckdb.connect(DB_PATH)
    
    # Constructing a dynamic placeholder string matching selected regions array len (?, ?, ...)
    placeholders = ", ".join(["?"] * len(regions))
    
    query = f"""
    SELECT 
        row_number() OVER () as sequence_id,
        pricing_amount,
        consumer_rating,
        regional_demand_index
    FROM regional_market_data
    WHERE region IN ({placeholders})
      AND consumer_rating >= ?
      AND pricing_amount BETWEEN ? AND ?
    """
    
    # Flatten variables array to feed the parameterized engine safely
    execution_parameters = regions + [min_rate, min_price, max_price]
    
    # Execute query and parse straight into a Pandas memory DataFrame matrix
    df = conn.execute(query, execution_parameters).df()
    conn.close()
    return df

# Trigger active data stream query
with st.spinner("Executing dynamic query over local DuckDB partitions..."):
    market_df = fetch_filtered_market_data(selected_regions, min_rating, price_range[0], price_range[1])

# ==========================================
# 4. MAIN CANVAS PLATFORM HEADER
# ==========================================
st.title("📊 Open-Source Regional Market & Trend Analytics System")
st.markdown(
    f"This integrated environment runs a safe read pipe straight to **`{DB_PATH}`**. "
    "Adjusting the sidebar filters updates your SQL execution variables, queries your data rows, and re-renders your analytical charts instantly."
)
st.markdown("---")

# Verify row footprint availability
if market_df.empty:
    st.warning("⚠️ No records match your active parameter filter constraints. Adjust your sidebar filters to see your charts.")
else:
    # KPI Performance Row Matrix
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Queried Record Footprint", value=f"{len(market_df):,} Rows")
    with col_kpi2:
        st.metric(label="Computed Mean Pricing", value=f"Rs. {market_df['pricing_amount'].mean():,.2f}")
    with col_kpi3:
        st.metric(label="Observed Average Consumer Rating", value=f"{market_df['consumer_rating'].mean():.2f} ⭐")
        
    st.markdown("---")

    # ==========================================
    # 5. DYNAMIC VISUALIZATION CANVAS (Day 21)
    # ==========================================
    st.subheader("🖼️ Interactive Operational Chart Canvas")
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.subheader("Regression Field Diagnostics")
        st.markdown("*OLS Fit Trend Line: consumer_rating vs. pricing_amount*")
        
        # Build an interactive Plotly scatter map with an auto-calculated OLS trendline vector
        fig_scatter = px.scatter(
            market_df,
            x="consumer_rating",
            y="pricing_amount",
            trendline="ols",
            color_discrete_sequence=["teal"],
            trendline_color_override="crimson",
            labels={"consumer_rating": "Recorded Consumer Rating", "pricing_amount": "Pricing Level (Rs.)"}
        )
        fig_scatter.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with viz_col2:
        st.subheader("Time-Series Macro Trend Frame")
        st.markdown("*Engineered Timeline Chunks: Rolling Simple Moving Average*")
        
        # Calculate moving variables on the fly using our filtered dataset rows
        market_df['time_block'] = market_df['sequence_id'] // 50
        ts_grouped = market_df.groupby('time_block')['regional_demand_index'].mean().reset_index()
        
        ts_grouped['SMA_5'] = ts_grouped['regional_demand_index'].rolling(window=5, min_periods=1).mean()
        ts_grouped['SMA_20'] = ts_grouped['regional_demand_index'].rolling(window=20, min_periods=1).mean()
        
        # Melt dataframe matrix shape for multi-line plotting layout inside Plotly
        ts_melted = pd.melt(
            ts_grouped,
            id_vars=["time_block"],
            value_vars=["regional_demand_index", "SMA_5", "SMA_20"],
            var_name="Trend Metrics",
            value_name="Value"
        )
        
        fig_line = px.line(
            ts_melted,
            x="time_block",
            y="Value",
            color="Trend Metrics",
            color_discrete_map={"regional_demand_index": "lightgray", "SMA_5": "darkorange", "SMA_20": "blue"},
            labels={"time_block": "Sequential Record Time Blocks (Chunks of 50)", "Value": "Demand Scale Metrics"}
        )
        fig_line.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig_line, use_container_width=True)