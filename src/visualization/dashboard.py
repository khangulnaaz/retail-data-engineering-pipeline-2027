
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------

@st.cache_data
def load_data():
    orders = pd.read_csv("data/processed/orders_final.csv")
    products = pd.read_csv("data/processed/products_clean.csv")

    orders["order_date"] = pd.to_datetime(orders["order_date"])

    df = orders.merge(
        products[["product_id", "product_name", "category"]],
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    return df

df = load_data()

# --------------------------------
# TITLE
# --------------------------------

st.title("📊 Retail Sales Analytics Dashboard")
st.caption("Retail Data Engineering Pipeline | 2027 Portfolio Project")

# --------------------------------
# SIDEBAR FILTERS
# --------------------------------

st.sidebar.title("Dashboard Filters")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = df[
        (df["order_date"].dt.date >= start_date) &
        (df["order_date"].dt.date <= end_date)
    ].copy()
else:
    filtered_df = df.copy()

# --------------------------------
# KPI CARDS
# --------------------------------

total_revenue = filtered_df["order_total"].sum()

total_orders = filtered_df["order_id"].nunique()

average_order_value = (
    total_revenue / total_orders if total_orders > 0 else 0
)

delivered_orders = (
    filtered_df["order_status"] == "Delivered"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Average Order Value", f"₹{average_order_value:,.2f}")
col4.metric("Delivered Orders", f"{delivered_orders:,}")

st.divider()

# --------------------------------
# MONTHLY REVENUE
# --------------------------------

st.subheader("Monthly Revenue Trend")

monthly_revenue = filtered_df.copy()
monthly_revenue["month"] = (
    monthly_revenue["order_date"].dt.to_period("M").astype(str)
)

monthly_revenue = (
    monthly_revenue.groupby("month")["order_total"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_revenue,
    x="month",
    y="order_total",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------
# CATEGORY REVENUE
# --------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")

    category_revenue = (
        filtered_df.groupby("category")["order_total"]
        .sum()
        .reset_index()
        .sort_values("order_total", ascending=False)
    )

    fig2 = px.bar(
        category_revenue,
        x="category",
        y="order_total",
        title="Category-wise Revenue",
        text_auto=".2s"
    )

    st.plotly_chart(fig2, use_container_width=True)

# --------------------------------
# ORDER STATUS
# --------------------------------

with col2:
    st.subheader("Order Status Distribution")

    status_counts = (
        filtered_df["order_status"]
        .value_counts()
        .rename_axis("status")
        .reset_index(name="orders")
    )

    fig3 = px.pie(
        status_counts,
        names="status",
        values="orders",
        hole=0.4,
        title="Orders by Status"
    )

    st.plotly_chart(fig3, use_container_width=True)

# --------------------------------
# TOP 10 PRODUCTS
# --------------------------------

st.subheader("Top 10 Products by Revenue")

top_products = (
    filtered_df.groupby("product_name")["order_total"]
    .sum()
    .nlargest(10)
    .reset_index()
    .sort_values("order_total")
)

fig4 = px.bar(
    top_products,
    x="order_total",
    y="product_name",
    orientation="h",
    title="Top Performing Products"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------
# MONTHLY ORDER VOLUME
# --------------------------------

st.subheader("Monthly Order Volume")

monthly_orders = filtered_df.copy()
monthly_orders["month"] = (
    monthly_orders["order_date"].dt.to_period("M").astype(str)
)

monthly_orders = (
    monthly_orders.groupby("month")["order_id"]
    .nunique()
    .reset_index(name="order_count")
)

fig5 = px.bar(
    monthly_orders,
    x="month",
    y="order_count",
    title="Monthly Order Count"
)

st.plotly_chart(fig5, use_container_width=True)

# --------------------------------
# DATA TABLE
# --------------------------------

with st.expander("View Order Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.success("Retail Sales Dashboard Loaded Successfully!")
