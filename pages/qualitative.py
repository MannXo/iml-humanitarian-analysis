import json
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

# Initialize Streamlit app with a title
st.title("Quantitative Analysis")

# Load the CSV/JSON files
csv_path = r"results/pillar2/crisis_keyword_summary_with_outlets.csv"
associations_path = r"results/pillar2/associations_per_article.json"
framing_path = r"results/pillar2/framing_per_article.json"
sentiment_path = r"results/pillar2/sentiment_per_article.json"
victim_causor_path = r"results/pillar2/victim_causor_per_article.json"
humanitarian_path = r"results/pillar2/humanitarian_frame_results_outlets.json"
political_path = r"results/pillar2/political_accountability_frame_results_outlets.json"
geopolitics_path = r"results/pillar2/geopolitics_frame_results_outlets.json"
historical_path = r"results/pillar2/historical_legacy_frame_results_outlets.json"

# Load keyword summary data to get unique outlets
data = pd.read_csv(csv_path)
unique_outlets = ["All Outlets"] + sorted(data['outlet'].unique().tolist())
crises = ["Gaza and the Occupied Palestinian Territories", "Ukraine"]

# Step 1: Keyword Analysis
st.header("Step 1: Keyword Analysis")

# Dropdown for outlet selection
outlet_step1 = st.selectbox("Select Outlet for Keyword Analysis", unique_outlets, index=0, key="outlet_step1")

# Filter or aggregate data based on selected outlet
if outlet_step1 == "All Outlets":
    # Aggregate across all outlets for each crisis
    def aggregate_counts(items):
        total_counter = Counter()
        for item in items:
            total_counter.update(json.loads(item))
        # Since counts may be duplicated across outlets, use data from "All Outlets" directly if available
        return json.dumps(dict(total_counter))
    
    # Check if "All Outlets" data exists to avoid double-counting
    all_outlets_data = data[data['outlet'] == "All Outlets"]
    if not all_outlets_data.empty:
        step1_data = all_outlets_data[all_outlets_data['crisis_name'].isin(crises)][['crisis_name', 'article_count', 'top_by_total', 'top_by_average']]
    else:
        # Fallback to manual aggregation if "All Outlets" is not precomputed
        step1_data = data[data['outlet'] != "All Outlets"].groupby('crisis_name').agg({
            'article_count': 'sum',
            'top_by_total': aggregate_counts,
            'top_by_average': lambda x: json.dumps({})  # Will recalculate below
        }).reset_index()
    
    # Recalculate top_by_average based on aggregated article_count
    for idx, row in step1_data.iterrows():
        total_counts = json.loads(row['top_by_total'])
        article_count = row['article_count']
        top_by_average = {k: v / article_count for k, v in total_counts.items()}
        top_by_average = dict(sorted(top_by_average.items(), key=lambda item: item[1], reverse=True)[:10])
        step1_data.at[idx, 'top_by_average'] = json.dumps(top_by_average)
else:
    step1_data = data[data['outlet'] == outlet_step1]

# Check if data exists for the selected outlet
if step1_data.empty:
    st.warning(f"No keyword data available for outlet: {outlet_step1}")
else:
    # Loop through each crisis_name
    for crisis in crises:
        crisis_data = step1_data[step1_data['crisis_name'] == crisis]
        if crisis_data.empty:
            st.write(f"**Crisis: {crisis}**")
            st.info(f"No data available for {crisis} in outlet {outlet_step1}")
            st.write("---")
            continue
        
        st.subheader(f"Crisis: {crisis}")
        crisis_row = crisis_data.iloc[0]
        
        # Parse the JSON-like strings into dictionaries
        top_by_total_dict = json.loads(crisis_row['top_by_total'])
        top_by_average_dict = json.loads(crisis_row['top_by_average'])
        
        # Convert dictionaries to DataFrames for display
        total_df = pd.DataFrame(
            list(top_by_total_dict.items()),
            columns=['Keyword', 'Total Count']
        ).sort_values(by='Total Count', ascending=False)
        
        average_df = pd.DataFrame(
            list(top_by_average_dict.items()),
            columns=['Keyword', 'Average Count']
        ).sort_values(by='Average Count', ascending=False)
        
        # Display the two tables side by side using columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top by Total Count**")
            st.dataframe(total_df, use_container_width=True)
        
        with col2:
            st.write("**Top by Average Count**")
            st.dataframe(average_df, use_container_width=True)
        
        st.write("The tables display the total count of keywords and the average keyword count per article, respectively.")
        st.write("---")

# Step 2: Frame Analysis
st.header("Step 2: Frame Analysis")

# Dropdown for outlet selection
outlet_step2 = st.selectbox("Select Outlet for Frame Analysis", unique_outlets, index=0, key="outlet_step2")

# Define the frames and their attributes/research questions
frames = {
    "Frame 1: Humanitarian Crisis": {
        "attributes": [
            ("humanitarian.victim", "Who are the individuals and communities affected by the crisis?"),
            ("humanitarian.cause", "What are the root causes of the crisis? Who or what is to blame?"),
            ("humanitarian.response", "What are the actions taken by governments, NGOs, and international organizations?"),
            ("humanitarian.human_rights", "What human rights are violated during the crisis and how is this addressed or should be addressed?"),
            ("humanitarian.morality", "Are there references to morality, God and other religious tenets? Do stories offer specific social prescriptions about how to behave?"),
            ("humanitarian.impact", "What are the impacts of this crisis?")
        ],
        "json_file": humanitarian_path
    },
    "Frame 2: Political Accountability": {
        "attributes": [
            ("political.transparency", "How open are the government and any other parties involved about the actions and decisions taken as part of the conflict?"),
            ("political.responsiveness", "How responsive are the government and any other parties involved to various accusations as part of the conflict?"),
            ("political.rule_of_law", "Are the rule of law principles maintained during the conflict?"),
            ("political.communication", "What channels of communication do the governments and other parties involved use to convey their messages?"),
            ("political.public_participation", "How much is the public opinion taken into account in the decision-making process as part of the conflict?")
        ],
        "json_file": political_path
    },
    "Frame 3: Geopolitics": {
        "attributes": [
            ("geopolitics.international_alliances", "What are the international alliances most mentioned in the coverage (including regimes supporting various parts in the conflict)?"),
            ("geopolitics.national_security", "How is national security presented or defined in media coverage?"),
            ("geopolitics.sources_of_information", "What sources of information are most used in the media coverage and how are they referred to?"),
            ("geopolitics.contextualization", "Does media coverage offer sufficient contextualization for the overall crisis they cover?"),
            ("geopolitics.key_actors", "How does the media portray various countries, organizations and individuals (leaders) involved in the crisis?")
        ],
        "json_file": geopolitics_path
    },
    "Frame 4: Historical Legacy and Perspectives for the Future": {
        "attributes": [
            ("historical.cultural_memory", "What past events/leaders are mentioned the most and in what context?"),
            ("historical.trauma_legacy", "How much are past atrocities, injustices or traumas mentioned in coverage related to the crisis?"),
            ("historical.symbolism", "What historical symbols resonating with the conflict are most prominent in media coverage?"),
            ("historical.polarization_of_perspectives", "What narratives in the coverage reinforce social divisions and exacerbate tensions?"),
            ("historical.post_crisis_future", "What are the scenarios for the future most widely disseminated through media coverage?")
        ],
        "json_file": historical_path
    }
}

# Loop through each frame
for frame_name, frame_info in frames.items():
    st.subheader(frame_name)
    
    # Load the JSON file for this frame
    try:
        with open(frame_info["json_file"], "r") as f:
            frame_data = json.load(f)
    except FileNotFoundError:
        st.error(f"JSON file {frame_info['json_file']} not found. Please ensure it exists.")
        continue
    
    # Select the outlet data
    frame_outlet_data = frame_data.get(outlet_step2, {})
    if not frame_outlet_data:
        st.warning(f"No frame data available for outlet: {outlet_step2}")
        continue
    
    # Loop through attributes and research questions
    for attr, question in frame_info["attributes"]:
        st.markdown(f"**Attribute: {attr.split('.')[-1].capitalize()}** - *{question}*")
        
        # Prepare data for Gaza and Ukraine
        gaza_data = frame_outlet_data.get(crises[0], {}).get(attr, {}).get("mentions_per_article", {})
        ukraine_data = frame_outlet_data.get(crises[1], {}).get(attr, {}).get("mentions_per_article", {})
        
        # Convert to DataFrames
        gaza_df = pd.DataFrame(
            list(gaza_data.items()),
            columns=["Item", "Mentions per Article"]
        ).sort_values(by="Mentions per Article", ascending=False)
        gaza_df["Percentage of Articles"] = gaza_df["Mentions per Article"].apply(
            lambda x: f"{round(x * 100, 1)}%" if pd.notnull(x) else "0%"
        )
        gaza_df = gaza_df[["Item", "Percentage of Articles"]]
    
        ukraine_df = pd.DataFrame(
            list(ukraine_data.items()),
            columns=["Item", "Mentions per Article"]
        ).sort_values(by="Mentions per Article", ascending=False)
        ukraine_df["Percentage of Articles"] = ukraine_df["Mentions per Article"].apply(
            lambda x: f"{round(x * 100, 1)}%" if pd.notnull(x) else "0%"
        )
        ukraine_df = ukraine_df[["Item", "Percentage of Articles"]]
        
        # Display tables side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{crises[0]}**")
            if gaza_df.empty:
                st.info(f"No data for {crises[0]} in outlet {outlet_step2}")
            else:
                st.dataframe(
                    gaza_df,
                    use_container_width=True,
                    height=300
                )
        
        with col2:
            st.write(f"**{crises[1]}**")
            if ukraine_df.empty:
                st.info(f"No data for {crises[1]} in outlet {outlet_step2}")
            else:
                st.dataframe(
                    ukraine_df,
                    use_container_width=True,
                    height=300
                )

    st.write("The tables present each frame's attributes and the corresponding percentage of articles that incorporate each attribute, providing insight into their prevalence across the dataset")
    st.write("---")

# Step 3: Comparative Analysis
st.header("Step 3: Comparative Analysis")

# Dropdown for outlet selection
outlet_step3 = st.selectbox("Select Outlet for Comparative Analysis", unique_outlets, index=0, key="outlet_step3")

# Function to plot associations (human rights or casualties)
def plot_associations(input_file, figures, assoc_type, title, outlet):
    df = pd.read_json(input_file)
    if outlet == "All Outlets":
        # Aggregate by taking the mean of mentions_per_article for each figure and assoc_type
        df = df.groupby(['figure', 'assoc_type', 'crisis_name'])['mentions_per_article'].mean().reset_index()
    else:
        df = df[df["outlet"] == outlet]
    plot_df = df[(df["figure"].isin(figures)) & (df["assoc_type"] == assoc_type)]
    
    if plot_df.empty:
        return None
    
    fig = px.bar(
        plot_df,
        x="figure",
        y="mentions_per_article",
        color="figure",
        title=title,
        labels={"figure": "Figure", "mentions_per_article": f"{assoc_type.capitalize()} Mentions per Article"},
        text=plot_df["mentions_per_article"].round(2).astype(str)
    )
    fig.update_layout(
        xaxis_title="Figure",
        yaxis_title=f"{assoc_type.capitalize()} Mentions per Article",
        legend_title="Figure",
        showlegend=False,
        margin=dict(r=100)
    )
    fig.update_traces(textposition="auto")
    return fig

# Function to plot framing by crisis
def plot_framing(input_file, crisis_name, title, outlet):
    df = pd.read_json(input_file)
    if outlet == "All Outlets":
        # Aggregate by taking the mean of mentions_per_article for each framing type
        df = df.groupby(['crisis_name', 'framing'])['mentions_per_article'].mean().reset_index()
    else:
        df = df[df["outlet"] == outlet]
    plot_df = df[df["crisis_name"] == crisis_name].sort_values("mentions_per_article", ascending=False)
    
    if plot_df.empty:
        return None
    
    fig = px.bar(
        plot_df,
        x="framing",
        y="mentions_per_article",
        color="framing",
        title=title,
        labels={"framing": "Framing Type", "mentions_per_article": "Mentions per Article"},
        text=plot_df["mentions_per_article"].round(2).astype(str)
    )
    fig.update_layout(
        xaxis_title="Framing Type",
        yaxis_title="Mentions per Article",
        legend_title="Framing",
        showlegend=False,
        xaxis_tickangle=45,
        margin=dict(r=100)
    )
    fig.update_traces(textposition="auto")
    return fig

# Function to plot sentiment for leaders
def plot_sentiment(input_file, title, outlet):
    df = pd.read_json(input_file)
    if outlet == "All Outlets":
        # Aggregate by taking the mean of mentions_per_article for each entity and sentiment
        df = df.groupby(['entity', 'sentiment', 'crisis_name'])['mentions_per_article'].mean().reset_index()
    else:
        df = df[df["outlet"] == outlet]
    if df.empty:
        return None
    
    color_map = {"positive": "#00FF00", "neutral": "#808080", "negative": "#FF0000"}
    
    fig = px.bar(
        df,
        x="entity",
        y="mentions_per_article",
        color="sentiment",
        title=title,
        labels={"entity": "Leader", "mentions_per_article": "Mentions per Article", "sentiment": "Sentiment"},
        category_orders={"sentiment": ["positive", "neutral", "negative"]},
        text=df["mentions_per_article"].round(2).astype(str),
        color_discrete_map=color_map
    )
    fig.update_layout(
        xaxis_title="Leader",
        yaxis_title="Mentions per Article",
        legend_title="Sentiment",
        xaxis_tickangle=45,
        barmode="stack",
        margin=dict(r=100)
    )
    fig.update_traces(textposition="inside")
    return fig

# Function to plot victim/causor framing
def plot_victim_causor(input_file, framing_type, title, outlet):
    df = pd.read_json(input_file)
    if outlet == "All Outlets":
        # Aggregate by taking the mean of mentions_per_article for each group and framing_type
        df = df.groupby(['group', 'framing_type', 'crisis_name'])['mentions_per_article'].mean().reset_index()
    else:
        df = df[df["outlet"] == outlet]
    plot_df = df[df["framing_type"] == framing_type]
    
    if plot_df.empty:
        return None
    
    fig = px.bar(
        plot_df,
        x="group",
        y="mentions_per_article",
        color="group",
        title=title,
        labels={"group": "Group", "mentions_per_article": "Mentions per Article"},
        text=plot_df["mentions_per_article"].round(2).astype(str)
    )
    fig.update_layout(
        xaxis_title="Group",
        yaxis_title="Mentions per Article",
        legend_title="Group",
        showlegend=False,
        xaxis_tickangle=45,
        margin=dict(r=100)
    )
    fig.update_traces(textposition="auto")
    return fig

# Generate and display charts
st.subheader("Associations with Human Rights and Casualties")
col1, col2 = st.columns(2)

# Plot associations
associations_plots = [
    (col1, ["Putin", "Netanyahu"], "human_rights", "Human Rights: Putin vs. Netanyahu"),
    (col1, ["Putin", "Zelensky"], "human_rights", "Human Rights: Putin vs. Zelensky"),
    (col2, ["Putin", "Netanyahu"], "casualties", "Casualties: Putin vs. Netanyahu"),
    (col2, ["Putin", "Zelensky"], "casualties", "Casualties: Putin vs. Zelensky")
]

for col, figures, assoc_type, title in associations_plots:
    fig = plot_associations(associations_path, figures, assoc_type, title, outlet_step3)
    if fig:
        col.plotly_chart(fig, use_container_width=True)
    else:
        col.info(f"No {assoc_type} data for {title} in outlet {outlet_step3}")

# Full-width plots
for figures, assoc_type, title in [
    (["Netanyahu", "Hamas"], "human_rights", "Human Rights: Netanyahu vs. Hamas"),
    (["Netanyahu", "Hamas"], "casualties", "Casualties: Netanyahu vs. Hamas")
]:
    fig = plot_associations(associations_path, figures, assoc_type, title, outlet_step3)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No {assoc_type} data for {title} in outlet {outlet_step3}")
    
st.write("The bar chart illustrates the average number of mentions per article.")
st.write("---")


st.subheader("Framing Narratives")
col1, col2 = st.columns(2)

# Plot framing
framing_plots = [
    (col1, "Ukraine", "Framing Narrative: Ukraine"),
    (col2, "Gaza and the Occupied Palestinian Territories", "Framing Narrative: Gaza")
]

for col, crisis_name, title in framing_plots:
    fig = plot_framing(framing_path, crisis_name, title, outlet_step3)
    if fig:
        col.plotly_chart(fig, use_container_width=True)
    else:
        col.info(f"No framing data for {crisis_name} in outlet {outlet_step3}")
st.write("The bar chart illustrates the average number of mentions per article for each frame, calculated by dividing the total number of frame mentions by the total number of articles for a specific crisis and outlet.")
st.write("---")


st.subheader("Leader Sentiment")
fig = plot_sentiment(sentiment_path, "Comparative Sentiment: Leaders", outlet_step3)
if fig:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No sentiment data in outlet {outlet_step3}")
st.write("The stacked bar chart demonstrates the proportions of positive, negative and neutral sentiments associated to each entity.")
st.write("---")

st.subheader("Victim and Causor Framing")
col1, col2 = st.columns(2)

# Plot victim/causor
victim_causor_plots = [
    (col1, "victim", "Victim Framing (Q7)"),
    (col2, "causor", "Conflict Cause Framing (Q8)")
]

for col, framing_type, title in victim_causor_plots:
    fig = plot_victim_causor(victim_causor_path, framing_type, title, outlet_step3)
    if fig:
        col.plotly_chart(fig, use_container_width=True)
    else:
        col.info(f"No {framing_type} framing data in outlet {outlet_step3}")

st.write("The bar chart illustrates the average number of mentions per article of Causor and Victim frames for each of the parties.")
st.write("---")