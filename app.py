import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicle Data Explorer", layout="wide")

st.title("🚗 Vehicle Data Explorer")
st.markdown(
    "Explore used vehicle listings through interactive charts and filters. "
    "This dashboard helps identify patterns in pricing, mileage, and vehicle characteristics."
)

# Load data
car_data = pd.read_csv("vehicles_us.csv")

# Sidebar filters
st.sidebar.header("Filters")

filtered_data = car_data.copy()

if "manufacturer" in filtered_data.columns:
    manufacturers = sorted(filtered_data["manufacturer"].dropna().unique())
    selected_manufacturers = st.sidebar.multiselect(
        "Select manufacturer",
        manufacturers,
        default=manufacturers[:5] if len(manufacturers) >= 5 else manufacturers
    )
    if selected_manufacturers:
        filtered_data = filtered_data[filtered_data["manufacturer"].isin(selected_manufacturers)]

if "condition" in filtered_data.columns:
    conditions = sorted(filtered_data["condition"].dropna().unique())
    selected_conditions = st.sidebar.multiselect(
        "Select condition",
        conditions,
        default=conditions
    )
    if selected_conditions:
        filtered_data = filtered_data[filtered_data["condition"].isin(selected_conditions)]

if "price" in filtered_data.columns:
    min_price = int(filtered_data["price"].min())
    max_price = int(filtered_data["price"].max())
    price_range = st.sidebar.slider(
        "Price range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, min(max_price, min_price + 50000))
    )
    filtered_data = filtered_data[
        (filtered_data["price"] >= price_range[0]) &
        (filtered_data["price"] <= price_range[1])
    ]

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Vehicles", f"{len(filtered_data):,}")

with col2:
    if "price" in filtered_data.columns:
        st.metric("Average Price", f"${filtered_data['price'].mean():,.0f}")

with col3:
    if "odometer" in filtered_data.columns:
        st.metric("Average Mileage", f"{filtered_data['odometer'].mean():,.0f} mi")

st.markdown("---")

# Histogram
st.subheader("Mileage Distribution")

if "odometer" in filtered_data.columns:
    fig_hist = px.histogram(
        filtered_data,
        x="odometer",
        nbins=30,
        title="Distribution of Vehicle Mileage",
        labels={"odometer": "Mileage (mi)"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Scatter plot
st.subheader("Price vs Mileage")

if "price" in filtered_data.columns and "odometer" in filtered_data.columns:
    color_col = "condition" if "condition" in filtered_data.columns else None
    fig_scatter = px.scatter(
        filtered_data,
        x="odometer",
        y="price",
        color=color_col,
        hover_data=filtered_data.columns,
        title="Vehicle Price vs Mileage",
        labels={
            "odometer": "Mileage (mi)",
            "price": "Price (USD)"
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Extra chart
if "manufacturer" in filtered_data.columns and "price" in filtered_data.columns:
    st.subheader("Average Price by Manufacturer")
    avg_price_brand = (
        filtered_data.groupby("manufacturer", as_index=False)["price"]
        .mean()
        .sort_values("price", ascending=False)
        .head(10)
    )

    fig_bar = px.bar(
        avg_price_brand,
        x="manufacturer",
        y="price",
        title="Top 10 Manufacturers by Average Price",
        labels={
            "manufacturer": "Manufacturer",
            "price": "Average Price (USD)"
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("Key Insights")
st.markdown(
    """
- Higher mileage vehicles generally tend to have lower prices.
- Vehicle condition can significantly influence price distribution.
- Manufacturer-level comparisons help identify premium and budget market segments.
"""
)

st.markdown("---")
st.markdown("Built by **Karen Cruz** | Data Scientist")
