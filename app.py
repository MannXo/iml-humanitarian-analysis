import pandas as pd

import streamlit as st

from plots import (plot_coverage, plot_crisis_coverage_vs_urgency,
                   plot_interactive_grouped_coverage_by_country,
                   plot_monthly_crisis_coverage, plot_spider_chart)

# Load data (assuming CSVs are in the same directory)
chart1_df = pd.read_csv('results/chart1_overall_coverage_bar.csv')
chart2_df = pd.read_csv('results/chart2_coverage_by_country.csv')
chart3_df = pd.read_csv('results/chart3_monthly_coverage.csv')
chart4_df = pd.read_csv('results/chart4_spider_chart.csv')
chart5_df = pd.read_csv('results/chart5_attention_vs_urgency.csv')

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
outlet_name = st.selectbox('Select an outlet:', chart4_df['matched_outlet'].unique())
fig4 = plot_spider_chart(chart4_df[chart4_df['matched_outlet'] == outlet_name], outlet_name)
st.plotly_chart(fig4)

import json
with open("results/dashboard_results.json", "r") as f:
    dashboard_data = json.load(f)


st.subheader("🟦 Answers to questions regarding how outlets covered the crises 🟦")
st.write("Note that the results are normalized to coverage per day")

# 1️⃣ Outlets that covered Ukraine more than Gaza
st.subheader("Outlets that Covered Ukraine More Than Gaza")
st.write("These outlets gave more coverage to Ukraine compared to Gaza.")
if dashboard_data["outlets_more_ukraine"]:
    st.write(", ".join(dashboard_data["outlets_more_ukraine"]))
else:
    st.write("No outlets met this criterion.")

# 2️⃣ Outlets that covered Ukraine & Gaza similarly
st.subheader("⚖️ Outlets that Covered Ukraine & Gaza Proportionally")
if dashboard_data["outlets_similar_ukraine_gaza"]:
    st.write(", ".join(dashboard_data["outlets_similar_ukraine_gaza"]))
else:
    st.write("No outlets met this criterion.")

# 3️⃣ Outlets that covered another crisis more than Ukraine & Gaza
st.subheader("Outlets that Prioritized Other Crises Over Ukraine & Gaza")
st.write("The only crisis that was covered more than Gaza by some outlets was Ukraine. The following are the outlets covered a crisis more than Ukraine (excluding Gaza) ")
if dashboard_data["outlets_other_crisis"]:
    for outlet, crises in dashboard_data["outlets_other_crisis"].items():
        st.write(f"**{outlet}**: {', '.join(crises)}")
else:
    st.write("No outlets met this criterion.")

# 4️⃣ Most balanced outlets
st.subheader("📊 Most Balanced Outlets Across All Crises")
st.write("Outlets That Covered the Other 8 Crises the Most")
if dashboard_data["most_balanced_outlets"]:
    st.write(", ".join(dashboard_data["most_balanced_outlets"]))
else:
    st.write("No outlets met this criterion.")


# Chart 5: Crisis Attention vs Urgency
# st.subheader("Crisis Attention vs Urgency")
# fig5 = plot_crisis_coverage_vs_urgency(chart5_df)
# st.plotly_chart(fig5)
