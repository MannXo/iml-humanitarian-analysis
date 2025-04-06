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

# Step 1: Keyword Analysis
st.header("Step 1: Keyword Analysis")

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

# Step 2: Frame Analysis
st.header("Step 2: Frame Analysis")

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
        "json_file": r"results/pillar2/humanitarian_frame_results.json"
    },
    "Frame 2: Political Accountability": {
        "attributes": [
            ("political.transparency", "How open are the government and any other parties involved about the actions and decisions taken as part of the conflict?"),
            ("political.responsiveness", "How responsive are the government and any other parties involved to various accusations as part of the conflict?"),
            ("political.rule_of_law", "Are the rule of law principles maintained during the conflict?"),
            ("political.communication", "What channels of communication do the governments and other parties involved use to convey their messages?"),
            ("political.public_participation", "How much is the public opinion taken into account in the decision-making process as part of the conflict?")
        ],
        "json_file": r"results/pillar2/political_accountability_frame_results.json"
    },
    "Frame 3: Geopolitics": {
        "attributes": [
            ("geopolitics.international_alliances", "What are the international alliances most mentioned in the coverage (including regimes supporting various parts in the conflict)?"),
            ("geopolitics.national_security", "How is national security presented or defined in media coverage?"),
            ("geopolitics.sources_of_information", "What sources of information are most used in the media coverage and how are they referred to?"),
            ("geopolitics.contextualization", "Does media coverage offer sufficient contextualization for the overall crisis they cover?"),
            ("geopolitics.key_actors", "How does the media portray various countries, organizations and individuals (leaders) involved in the crisis?")
        ],
        "json_file": r"results/pillar2/geopolitics_frame_results.json"
    },
    "Frame 4: Historical Legacy and Perspectives for the Future": {
        "attributes": [
            ("historical.cultural_memory", "What past events/leaders are mentioned the most and in what context?"),
            ("historical.trauma_legacy", "How much are past atrocities, injustices or traumas mentioned in coverage related to the crisis?"),
            ("historical.symbolism", "What historical symbols resonating with the conflict are most prominent in media coverage?"),
            ("historical.polarization_of_perspectives", "What narratives in the coverage reinforce social divisions and exacerbate tensions?"),
            ("historical.post_crisis_future", "What are the scenarios for the future most widely disseminated through media coverage?")
        ],
        "json_file": r"results/pillar2/historical_legacy_frame_results.json"
    }
}

# Load crisis names (hardcoded for now, adjust as needed)
crises = ["Gaza and the Occupied Palestinian Territories", "Ukraine"]

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
    
    # Loop through attributes and research questions
    for attr, question in frame_info["attributes"]:
        st.markdown(f"**Attribute: {attr.split('.')[-1].capitalize()}** - *{question}*")
        
        # Prepare data for Gaza and Ukraine
        gaza_data = frame_data.get(crises[0], {}).get(attr, {}).get("mentions_per_article", {})
        ukraine_data = frame_data.get(crises[1], {}).get(attr, {}).get("mentions_per_article", {})
        
        # Convert to DataFrames
        gaza_df = pd.DataFrame(
            list(gaza_data.items()),
            columns=["Item", "Mentions per Article"]
        ).sort_values(by="Mentions per Article", ascending=False)
        gaza_df["Percentage of Articles"] = gaza_df["Mentions per Article"].apply(
            lambda x: f"{round(x * 100, 1)}%"  # Round to 1 decimal place for clarity
        )
        gaza_df = gaza_df[["Item", "Percentage of Articles"]]  # Drop raw value
    
        ukraine_df = pd.DataFrame(
            list(ukraine_data.items()),
            columns=["Item", "Mentions per Article"]
        ).sort_values(by="Mentions per Article", ascending=False)
        ukraine_df["Percentage of Articles"] = ukraine_df["Mentions per Article"].apply(
            lambda x: f"{round(x * 100, 1)}%"  # Round to 1 decimal place for clarity
        )
        ukraine_df = ukraine_df[["Item", "Percentage of Articles"]]
        
        # Display tables side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{crises[0]}**")
            st.dataframe(
                gaza_df,
                use_container_width=True,
                height=300  # Approx height for 10 rows, adjust as needed
            )
        
        with col2:
            st.write(f"**{crises[1]}**")
            st.dataframe(
                ukraine_df,
                use_container_width=True,
                height=300  # Approx height for 10 rows, adjust as needed
            )
    
    # Add spacing between frames
    st.write("---")

import plotly.express as px

# Step 3: Comparative Analysis
st.header("Step 3: Comparative Analysis")

# Function to plot associations (human rights or casualties)
def plot_associations(input_file, figures, assoc_type, title):
    df = pd.read_json(input_file)
    plot_df = df[(df["figure"].isin(figures)) & (df["assoc_type"] == assoc_type)]
    
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
def plot_framing(input_file, crisis_name, title):
    df = pd.read_json(input_file)
    plot_df = df[df["crisis_name"] == crisis_name].sort_values("mentions_per_article", ascending=False)
    
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
def plot_sentiment(input_file, title):
    df = pd.read_json(input_file)
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

# Function to plot victim/causor framing (note: uses mentions_per_article)
def plot_victim_causor(input_file, framing_type, title):
    df = pd.read_json(input_file)
    plot_df = df[df["framing_type"] == framing_type]
    
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
with col1:
    st.plotly_chart(
        plot_associations(
            r"results/pillar2/associations_per_article.json",
            ["Putin", "Netanyahu"],
            "human_rights",
            "Human Rights: Putin vs. Netanyahu"
        ),
        use_container_width=True
    )
    st.plotly_chart(
        plot_associations(
            r"results/pillar2/associations_per_article.json",
            ["Putin", "Zelensky"],
            "human_rights",
            "Human Rights: Putin vs. Zelensky"
        ),
        use_container_width=True
    )
with col2:
    st.plotly_chart(
        plot_associations(
            r"results/pillar2/associations_per_article.json",
            ["Putin", "Netanyahu"],
            "casualties",
            "Casualties: Putin vs. Netanyahu"
        ),
        use_container_width=True
    )
    st.plotly_chart(
        plot_associations(
            r"results/pillar2/associations_per_article.json",
            ["Putin", "Zelensky"],
            "casualties",
            "Casualties: Putin vs. Zelensky"
        ),
        use_container_width=True
    )

st.plotly_chart(
    plot_associations(
        r"results/pillar2/associations_per_article.json",
        ["Netanyahu", "Hamas"],
        "human_rights",
        "Human Rights: Netanyahu vs. Hamas"
    ),
    use_container_width=True
)
st.plotly_chart(
    plot_associations(
        r"results/pillar2/associations_per_article.json",
        ["Netanyahu", "Hamas"],
        "casualties",
        "Casualties: Netanyahu vs. Hamas"
    ),
    use_container_width=True
)

st.subheader("Framing Narratives")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        plot_framing(
            r"results/pillar2/framing_per_article.json",
            "Ukraine",
            "Framing Narrative: Ukraine"
        ),
        use_container_width=True
    )
with col2:
    st.plotly_chart(
        plot_framing(
            r"results/pillar2/framing_per_article.json",
            "Gaza and the Occupied Palestinian Territories",
            "Framing Narrative: Gaza"
        ),
        use_container_width=True
    )

st.subheader("Leader Sentiment")
st.plotly_chart(
    plot_sentiment(
        r"results/pillar2/sentiment_per_article.json",  # Updated to match your file name
        "Comparative Sentiment: Leaders"
    ),
    use_container_width=True
)

st.subheader("Victim and Causor Framing")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        plot_victim_causor(
            r"results/pillar2/victim_causor_per_article.json",
            "victim",
            "Victim Framing (Q7)"
        ),
        use_container_width=True
    )
with col2:
    st.plotly_chart(
        plot_victim_causor(
            r"results/pillar2/victim_causor_per_article.json",
            "causor",
            "Conflict Cause Framing (Q8)"
        ),
        use_container_width=True
    )

st.write("---")