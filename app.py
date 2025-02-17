import pandas as pd

import streamlit as st

from plots import (plot_coverage, plot_crisis_coverage_vs_urgency,
                   plot_interactive_grouped_coverage_by_country,
                   plot_monthly_crisis_coverage, plot_spider_chart)

# Load data (assuming CSVs are in the same directory)
chart1_df = pd.read_csv(r'results\\chart1_overall_coverage_bar.csv')
chart2_df = pd.read_csv(r'results\\chart2_coverage_by_country.csv')
chart3_df = pd.read_csv(r'results\\chart3_monthly_coverage.csv')
chart4_df = pd.read_csv(r'results\\chart4_spider_chart.csv')
chart5_df = pd.read_csv(r'results\\chart5_attention_vs_urgency.csv')

# Initialize Streamlit app with a title
st.title("Impact Media Lab - Top 10 Humanitarian Crises")

# Create a dropdown on the main page (not in the sidebar)
normalization = st.selectbox(
    'Select normalization method:',
    ('per_day', 'per_funding', 'per_people', 'raw'),
    index=0  # Default is per_day
)

# Creating a page for "Quantitative Analysis"
st.header("Quantitative Analysis")

# Chart 1: Overall Coverage
st.subheader("Overall Coverage")
fig1 = plot_coverage(chart1_df, normalization=normalization)
st.plotly_chart(fig1)

# Chart 2: Coverage by Country
st.subheader("Coverage by Country")
fig2 = plot_interactive_grouped_coverage_by_country(chart2_df, normalization=normalization)
st.plotly_chart(fig2)

# Chart 3: Monthly Crisis Coverage
st.subheader("Monthly Crisis Coverage")
fig3 = plot_monthly_crisis_coverage(chart3_df)
st.plotly_chart(fig3)

# Chart 4: Spider Chart (Outlet Selection)
st.subheader("Media Outlet Focus Across Crises")
outlet_name = st.selectbox('Select an outlet:', chart4_df['outlet_name'].unique())
fig4 = plot_spider_chart(chart4_df[chart4_df['outlet_name'] == outlet_name], outlet_name)
st.plotly_chart(fig4)

# Chart 5: Crisis Attention vs Urgency
st.subheader("Crisis Attention vs Urgency")
fig5 = plot_crisis_coverage_vs_urgency(chart5_df)
st.plotly_chart(fig5)
