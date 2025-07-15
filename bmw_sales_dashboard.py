import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='BMW Car Sales Dashboard', layout='wide')

# --- BMW Logo (local image) ---
st.image('BMW.jpeg', width=100)

st.title('BMW Car Sales Interactive Dashboard (Plotly)')

# --- About/Instructions ---
with st.expander('ℹ️ About / Instructions'):
    st.markdown('''
    **BMW Car Sales Dashboard**
    
    - Explore BMW car sales data interactively.
    - Use the sidebar to filter by year, region, model, fuel type, transmission, and color.
    - All charts and stats update instantly based on your filters.
    - Download the filtered data for your own analysis.
    ''')

# Load data
df = pd.read_csv('BMW_Car_Sales_Classification.csv')

# --- Sidebar filters ---
years = sorted(df['Year'].unique())
regions = sorted(df['Region'].unique())
models = sorted(df['Model'].unique())
fuel_types = sorted(df['Fuel_Type'].unique())
transmissions = sorted(df['Transmission'].unique())
colors = sorted(df['Color'].unique())

st.sidebar.header('Filter Data')
selected_years = st.sidebar.multiselect('Year', years, default=years)
selected_regions = st.sidebar.multiselect('Region', regions, default=regions)
selected_models = st.sidebar.multiselect('Model', models, default=models)
selected_fuels = st.sidebar.multiselect('Fuel Type', fuel_types, default=fuel_types)
selected_trans = st.sidebar.multiselect('Transmission', transmissions, default=transmissions)
selected_colors = st.sidebar.multiselect('Color', colors, default=colors)

# Filter data
df_filtered = df[
    df['Year'].isin(selected_years) &
    df['Region'].isin(selected_regions) &
    df['Model'].isin(selected_models) &
    df['Fuel_Type'].isin(selected_fuels) &
    df['Transmission'].isin(selected_trans) &
    df['Color'].isin(selected_colors)
]

st.write(f"### Showing {len(df_filtered)} records after filtering.")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cars", len(df_filtered))
col2.metric("Total Sales", int(df_filtered['Sales_Volume'].sum()))
col3.metric("Avg Price (USD)", f"${int(df_filtered['Price_USD'].mean()):,}" if len(df_filtered) else "N/A")
if len(df_filtered):
    top_model = df_filtered.groupby('Model')['Sales_Volume'].sum().idxmax()
else:
    top_model = "N/A"
col4.metric("Top Model", top_model)

# --- Download filtered data ---
st.download_button('Download Filtered Data as CSV', data=df_filtered.to_csv(index=False), file_name='BMW_Car_Sales_Filtered.csv', mime='text/csv')

# --- Show raw data (optional) ---
with st.expander('Show Raw Data'):
    st.dataframe(df_filtered.head(100))

# --- Main Visualizations ---
# 1. Sales trend over years
st.subheader('Total Sales Volume by Year')
trend = df_filtered.groupby('Year')['Sales_Volume'].sum().reset_index()
fig1 = px.line(trend, x='Year', y='Sales_Volume', markers=True)
st.plotly_chart(fig1, use_container_width=True)

# 2. Sales by Region (Pie)
st.subheader('Sales Distribution by Region')
region_sales = df_filtered.groupby('Region')['Sales_Volume'].sum().reset_index()
fig2 = px.pie(region_sales, names='Region', values='Sales_Volume', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# 3. Top 10 selling models
st.subheader('Top 10 BMW Models by Sales Volume')
top_models = df_filtered.groupby('Model')['Sales_Volume'].sum().reset_index().sort_values('Sales_Volume', ascending=False).head(10)
fig3 = px.bar(top_models, x='Model', y='Sales_Volume', color='Model', text='Sales_Volume')
st.plotly_chart(fig3, use_container_width=True)

# 4. Price vs Sales Volume
st.subheader('Price vs Sales Volume')
fig4 = px.scatter(df_filtered, x='Price_USD', y='Sales_Volume', color='Model', hover_data=['Region', 'Year'], opacity=0.6)
st.plotly_chart(fig4, use_container_width=True)

# 5. Engine Size vs Sales Classification
st.subheader('Engine Size by Sales Classification')
fig5 = px.box(df_filtered, x='Sales_Classification', y='Engine_Size_L', color='Sales_Classification')
st.plotly_chart(fig5, use_container_width=True)

# 6. Correlation matrix
st.subheader('Correlation Matrix for Numeric Features')
numeric_cols = ['Year', 'Engine_Size_L', 'Mileage_KM', 'Price_USD', 'Sales_Volume']
corr = df_filtered[numeric_cols].corr()
fig6 = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Blues',
    zmin=-1, zmax=1,
    colorbar=dict(title='Correlation')
))
fig6.update_layout(width=600, height=500)
st.plotly_chart(fig6, use_container_width=True)

# 7. Price Histogram
st.subheader('Price Distribution')
fig7 = px.histogram(df_filtered, x='Price_USD', nbins=30, color='Region', marginal='box')
st.plotly_chart(fig7, use_container_width=True)

# 8. Engine Size Histogram
st.subheader('Engine Size Distribution')
fig8 = px.histogram(df_filtered, x='Engine_Size_L', nbins=20, color='Fuel_Type', marginal='box')
st.plotly_chart(fig8, use_container_width=True)

st.markdown('---')
st.caption('Developed BY Sofien Meftahi | BMW Car Sales Dashboard') 