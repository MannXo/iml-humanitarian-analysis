import streamlit as st
import pandas as pd
import json

# Initialize Streamlit app with a title
st.title("Quantitative Analysis")

# Load the CSV file (adjust the path as needed)
csv_path = r"results/pillar2/crisis_keyword_summary.csv"  # Replace with your actual CSV file path
data = pd.read_csv(csv_path)

# Ensure we have exactly 2 unique crisis names
unique_crises = data['crisis_name'].unique()


# Loop through each crisis_name
for crisis in unique_crises:
    st.subheader(f"Crisis: {crisis}")
        
    # Filter data for the current crisis
    crisis_data = data[data['crisis_name'] == crisis].iloc[0]  # Take the first row (assuming one row per crisis)
        
    # Parse the JSON-like strings into dictionaries
    top_by_total_dict = json.loads(crisis_data['top_by_total'])
    top_by_average_dict = json.loads(crisis_data['top_by_average'])
        
    # Convert dictionaries to DataFrames for display
    total_df = pd.DataFrame(
        list(top_by_total_dict.items()),
        columns=['Keyword', 'Total Count']
    ).sort_values(by='Total Count', ascending=False)  # Sort by count
        
    average_df = pd.DataFrame(
        list(top_by_average_dict.items()),
        columns=['Keyword', 'Average Count']
    ).sort_values(by='Average Count', ascending=False)  # Sort by count
     
    # Display the two tables side by side using columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top by Total Count**")
        st.dataframe(total_df, use_container_width=True)
    
    with col2:
        st.write("**Top by Average Count**")
        st.dataframe(average_df, use_container_width=True)
    # Add some spacing between crises
    st.write("---")