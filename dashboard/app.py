import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Sales Profit Leakage Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("data/clean_superstore.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.title("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

filtered = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# -----------------------
# Title
# -----------------------
st.title("📊 Sales Profit Leakage Dashboard")
st.caption("Business analytics project using Superstore data")

# -----------------------
# KPI Cards
# -----------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
c3.metric("Orders", f"{filtered['Order ID'].nunique():,}")
c4.metric("Avg Margin", f"{filtered['Profit Margin %'].mean():.1f}%")

# -----------------------
# Row 1
# -----------------------
col1, col2 = st.columns(2)

with col1:
    region_profit = filtered.groupby("Region")["Profit"].sum().reset_index()
    fig = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    cat_sales = filtered.groupby("Category")["Sales"].sum().reset_index()
    fig = px.bar(
        cat_sales,
        x="Sales",
        y="Category",
        orientation="h",
        title="Sales by Category",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Row 2
# -----------------------
col3, col4 = st.columns(2)

with col3:
    leak = filtered.groupby("Sub-Category")["Profit"].sum().reset_index()
    leak = leak[leak["Profit"] < 0].sort_values("Profit")
    fig = px.bar(
        leak,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        title="Loss-Making Sub-Categories",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    monthly = filtered.resample("M", on="Order Date")["Sales"].sum().reset_index()
    fig = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Bottom Chart
# -----------------------
discount = filtered.groupby("Discount")["Profit Margin %"].mean().reset_index()

fig = px.line(
    discount,
    x="Discount",
    y="Profit Margin %",
    title="Average Margin by Discount Level",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)