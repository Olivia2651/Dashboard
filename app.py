import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time

# Load the data
df = pd.read_excel("streamlit.xlsx")

# Set page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# Streamlit App
st.title("Sales Dashboard")

# Function to simulate buffering
def simulate_buffering():
    st.write("Hold tight, we're conjuring up some magic ✨")
    for _ in range(10):
        time.sleep(0.5)
        st.write("🔮")

# Sidebar - Filters
st.sidebar.title("Filters")
selected_salesman = st.sidebar.selectbox("Salesman", [None] + list(df['Salesman'].unique()))
selected_product = st.sidebar.selectbox("Product", [None] + list(df['Product'].unique()))
selected_region = st.sidebar.selectbox("Region", [None] + list(df['Region'].unique()))

# Filtered Data based on Dropdown Selections
filtered_df = df
if selected_salesman is not None:
    filtered_df = filtered_df[filtered_df['Salesman'] == selected_salesman]
if selected_product is not None:
    filtered_df = filtered_df[filtered_df['Product'] == selected_product]
if selected_region is not None:
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Main Content - Dashboard Sections

# Summary Cards
st.markdown("<h1 style='text-align: center;'>Summary Cards</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", total_sales := filtered_df['Sales'].sum())
with col2:
    st.metric("Total Revenue", total_revenue := filtered_df['Revenue'].sum())
with col3:
    st.metric("Average Satisfaction", average_satisfaction := filtered_df['Client Satisfaction'].mean())

# Total Sales by Salesman, Sales by Product, Revenue by Region
st.markdown("<h1 style='text-align: center;'>Sales Overview</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h4>Total Sales by Salesman</h4>", unsafe_allow_html=True)
    st.bar_chart(filtered_df.groupby('Salesman')['Sales'].sum().sort_values(ascending=False), color='#ffaa00')

with col2:
    st.markdown("<h4>Sales by Product</h4>", unsafe_allow_html=True)
    st.bar_chart(filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False), color='#F08080')

with col3:
    st.markdown("<h4>Revenue by Region</h4>", unsafe_allow_html=True)
    st.bar_chart(filtered_df.groupby('Region')['Revenue'].sum().sort_values(ascending=False), color='#90EE90')

# Client Satisfaction Over Time, Client Satisfaction Distribution, Positive vs Negative Feedback
st.markdown("<h1 style='text-align: center;'>Client Satisfaction and Feedback</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h4>Client Satisfaction Over Time</h4>", unsafe_allow_html=True)
    client_satisfaction_data = filtered_df.groupby(['Sale Date', 'Salesman'])['Client Satisfaction'].mean().reset_index()
    fig = px.line(client_satisfaction_data, x='Sale Date', y='Client Satisfaction', color='Salesman', line_group='Salesman', markers=True, title="Client Satisfaction Over Time")
    fig.update_layout(xaxis_title='Date', yaxis_title='Client Satisfaction')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<h4>Client Satisfaction Distribution</h4>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Client Satisfaction'], bins=20, kde=True, color='salmon', ax=ax)
    st.pyplot(fig)

with col3:
    st.markdown("<h4>Positive vs Negative Feedback</h4>", unsafe_allow_html=True)
    positive_negative_feedback = filtered_df[['Positive', 'Negative']].sum()
    fig, ax = plt.subplots()
    sns.barplot(x=positive_negative_feedback.index, y=positive_negative_feedback, palette=['green', 'red'])
    st.pyplot(fig)

# Total Calls by Salesman, Sales Distribution by Product, Revenue Distribution by Region
st.markdown("<h1 style='text-align: center;'>Other Metrics</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h4>Total Calls by Salesman</h4>", unsafe_allow_html=True)
    st.bar_chart(filtered_df.groupby('Salesman')['Calls'].sum().sort_values(ascending=False), color='#D3D3D3')

with col2:
    st.markdown("<h4>Sales Distribution by Product</h4>", unsafe_allow_html=True)
    sales_distribution_data = filtered_df.groupby('Product')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(sales_distribution_data, labels=sales_distribution_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)

with col3:
    st.markdown("<h4>Revenue Distribution by Region</h4>", unsafe_allow_html=True)
    revenue_distribution_data = filtered_df.groupby('Region')['Revenue'].sum()
    fig, ax = plt.subplots()
    ax.pie(revenue_distribution_data, labels=revenue_distribution_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.add_artist(plt.Circle((0, 0), 0.6, fc='white'))  # Draw a white circle at the center to create a donut chart.
    st.pyplot(fig)

# Raw Data Section
if st.checkbox("Show Raw Data"):
    st.markdown("<h1 style='text-align: center;'>Raw Data</h1>", unsafe_allow_html=True)
    st.dataframe(filtered_df)
