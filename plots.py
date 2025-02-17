import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go



def plot_coverage(df, normalization="per_day"):
    normalization_map = {
        "raw": "raw_coverage",
        "per_day": "coverage_per_day",
        "per_funding": "coverage_per_funding",
        "per_people": "coverage_per_people",
    }
    
    column = normalization_map[normalization]
    
    # Sort the dataframe by the specified coverage column
    sorted_df = df.sort_values(by=column, ascending=False).reset_index()

    # Create the Plotly bar chart
    fig = px.bar(sorted_df, 
                 x="crisis_name", 
                 y=column, 
                 color="crisis_name", 
                 title=f"Overall Coverage ({normalization.replace('_', ' ').title()})",
                 labels={"crisis_name": "Crisis", column: "Coverage"})

    # Update layout for better visibility
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Crisis",
        yaxis_title="Coverage Count" if normalization == "raw" else "Normalized Coverage",
        legend_title="Crisis",
        margin=dict(r=100)  # Space for legend
    )

    return fig


def plot_interactive_grouped_coverage_by_country(df, normalization="per_day"):
    normalization_map = {
        "raw": "raw_coverage",
        "per_day": "coverage_per_day",
        "per_funding": "coverage_per_funding",
        "per_people": "coverage_per_people",
    }
    
    column = normalization_map[normalization]
    df_reset = df.sort_values(by=column, ascending=False).reset_index()


    # Create the Plotly bar chart
    fig = px.bar(df_reset, 
                 x="crisis_name", 
                 y=column, 
                 color="country", 
                 barmode="group", 
                 title=f"Coverage by Crisis and Country ({normalization.replace('_', ' ').title()})",
                 labels={"crisis_name": "Crisis", "country": "Country", column: "Coverage"})

    # Update layout for better visibility
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Crisis",
        yaxis_title="Coverage Count" if normalization == "raw" else "Normalized Coverage",
        legend_title="Country",
        legend=dict(x=1.05, y=1),  # Move legend outside of the chart
        margin=dict(r=100)  # Space for legend
    )

    return fig

def plot_monthly_crisis_coverage(monthly_coverage_df):
    monthly_coverage_df["year_month"] = monthly_coverage_df["year_month"].astype(str)
    fig = px.line(monthly_coverage_df, 
                  x="year_month", 
                  y="coverage_count", 
                  color="crisis_name", 
                  title="Monthly Crisis Coverage",
                  labels={"coverage_count": "Number of Articles", "year_month": "Month"},
                  line_group="crisis_name",
                  template="plotly_dark")

    # Make sure the chart has interactive elements
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Coverage Count",
        showlegend=True
    )

    return fig

def plot_spider_chart(coverage_df, outlet_name):
    # Filter the data for the selected outlet
    outlet_data = coverage_df[coverage_df['outlet_name'] == outlet_name]
    
    # Sort the data to ensure we have a consistent order (e.g., based on crisis_name)
    outlet_data = outlet_data.sort_values('crisis_name')

    # Prepare the data for the Spider Chart
    categories = outlet_data['crisis_name'].tolist()  # List of crises
    values = outlet_data['coverage_count'].tolist()  # Corresponding coverage counts
    
    # Create a Radar (Spider) chart
    fig = go.Figure(data=[go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=outlet_name
    )])

    # Update the layout for a better visual
    fig.update_layout(
        title=f"Crisis Coverage by {outlet_name}",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) + 10])  # Adjust range for better visualization
        ),
        showlegend=False,
        template="plotly_dark"
    )

    return fig


def plot_crisis_coverage_vs_urgency(df):
    # Normalize the data for consistency in scale
    df['normalized_coverage'] = df['coverage_count'] / df['coverage_count'].max()
    df['normalized_fund'] = df['fund_required'] / df['fund_required'].max()
    df['normalized_people'] = df['people_affected'] / df['people_affected'].max()

    # Combine fund_required and people_affected to get urgency
    df['normalized_urgency'] = (df['normalized_fund'] + df['normalized_people']) / 2
    
    # Create the scatter plot
    fig = px.scatter(df, 
                     x='normalized_coverage', 
                     y='normalized_fund', 
                     color='crisis_name', 
                     hover_name='crisis_name', 
                     size='coverage_count', 
                     size_max=20, 
                     title="Crisis Attention vs. Humanitarian Urgency",
                     labels={'normalized_coverage': 'Normalized Media Coverage', 
                             'normalized_fund': 'Normalized Urgency'},
                     template='plotly_dark')
    
    # Add quadrant lines
    fig.add_vline(x=0.5, line=dict(color="gray", dash="dash"))
    fig.add_hline(y=0.5, line=dict(color="gray", dash="dash"))

    fig.update_layout(
        xaxis_title="Media Coverage (Normalized)",
        yaxis_title="Urgency (Normalized)",
        showlegend=True
    )

    return fig