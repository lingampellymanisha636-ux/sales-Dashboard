import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------------
# 1. Load Dataset
# -------------------------------
data = pd.read_csv("sales_data.csv")  # Make sure CSV file is in same folder

# Rename columns to standard names (adjust if your CSV differs)
data.rename(columns={
    'Sale_Date': 'Date',
    'Product_ID': 'Product',
    'Quantity_Sold': 'Quantity',
    'Unit_Price': 'UnitPrice',
    'Sales_Rep': 'Salesperson'
}, inplace=True)

# Convert Date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Calculate Revenue
data['Revenue'] = data['Quantity'] * data['UnitPrice']

# -------------------------------
# 2. Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

# Product filter
product_filter = st.sidebar.multiselect(
    "Select Product",
    options=data['Product'].unique(),
    default=data['Product'].unique()
)

# Region filter
region_filter = st.sidebar.multiselect(
    "Select Region",
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

# Date range filter
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

# Apply filters
filtered_data = data[
    (data['Product'].isin(product_filter)) &
    (data['Region'].isin(region_filter)) &
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]

# -------------------------------
# 3. KPIs
# -------------------------------
st.title("📊 Sales & Revenue Dashboard")

total_revenue = filtered_data['Revenue'].sum()
total_units = filtered_data['Quantity'].sum()
avg_order_value = filtered_data['Revenue'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Units Sold", f"{total_units}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# -------------------------------
# 4. Revenue Trend Chart
# -------------------------------
revenue_trend = filtered_data.groupby('Date')['Revenue'].sum().reset_index()
fig_trend = px.line(
    revenue_trend,
    x='Date',
    y='Revenue',
    title="Revenue Trend Over Time",
    markers=True
)
st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------
# 5. Top Products Chart
# -------------------------------
top_products = filtered_data.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
fig_top = px.bar(
    x=top_products.index,
    y=top_products.values,
    labels={'x': 'Product', 'y': 'Revenue'},
    title="Top 5 Products by Revenue"
)
st.plotly_chart(fig_top, use_container_width=True)

# -------------------------------
# 6. Revenue by Region Chart
# -------------------------------
region_revenue = filtered_data.groupby('Region')['Revenue'].sum().reset_index()
fig_region = px.pie(
    region_revenue,
    names='Region',
    values='Revenue',
    title="Revenue by Region"
)
st.plotly_chart(fig_region, use_container_width=True)