import streamlit as st
import pandas as pd
import plotly.express as px
from run_election import run_election
# Set page config
st.set_page_config(layout="wide", page_title="Prahran By-Election Simulator")

# Title
st.title("Prahran By-Election")

# Create sidebar controls
with st.sidebar:
    st.header("Preference Settings")

    st.markdown("**How will the people who voted ALP last time choose between GRN and LIB?**") 
    # ALP to GRN preference flow
    alp_to_grn = st.slider(
        "% of nominal ALP voters voting GRN over LIB",
        min_value=0.0,
        max_value=100.0,
        value=85.0,
        help="Percentage of ALP voters who vote GRN ahead of LIB"
    )
    st.markdown("**Will there be a swing to or away from GRN otherwise?**") 
    
    grn_swing = st.slider(
        "% swing to GRN",
        min_value=-20.0,
        max_value=20.0,
        value=0.0,
        help="Change in GRN primary vote share among other voters"
    )
    st.header("Primary Votes")

    grn_vote = 36.4 + grn_swing + (alp_to_grn/100 * 26.6)
    # Primary vote controls
    grn_primary = st.slider("GRN Primary", min_value=0.0, max_value=100.0, value=grn_vote, disabled=True)
    lib_primary = st.slider("LIB Primary", min_value=0.0, max_value=100.0, value=31.1 + ((100 - alp_to_grn)/100)*26.6)
    ajp_primary = st.slider("AJP Primary", min_value=0.0, max_value=100.0, value=3.2)
    st.markdown("**The rest of the vote - independents and micros**") 
    ind_primary = st.slider("IND Primary", min_value=0.0, max_value=100.0, value=100 - (grn_primary + lib_primary + ajp_primary), disabled=True)

    # st.markdown(f"Green vote: {alp_to_grn:.1f}% of nominal ALP voters + {grn_primary:.1f}% of other voters") 
    # Calculate IND as remainder
    # ind_primary = 100 - (grn_primary + lib_primary + ajp_primary)
    # st.metric("IND Primary", f"{ind_primary:.1f}%")
    
    st.header("Other Preference Flows")
    
    # Other preference flows to GRN
    ajp_to_grn = st.slider("% of AJP to GRN", min_value=0, max_value=100, value=85)
    ind_to_grn = st.slider("% of IND to GRN", min_value=0, max_value=100, value=50)

# Create two columns for the plots
col1, col2 = st.columns(2)

# Define color scheme
color_map = {
    'GRN': 'green',
    'LIB': 'blue',
    'AJP': 'purple',
    'IND': 'orange'
}

# Primary vote visualization
with col1:
    # st.subheader("Primary Votes")
    
    primary_data = pd.DataFrame({
        'Party': ['GRN', 'LIB', 'IND', 'AJP'],
        'Votes': [grn_primary, lib_primary, ajp_primary, ind_primary]
    })
    
    fig_primary = px.bar(
        primary_data,
        x='Party',
        y='Votes',
        title='Primary Vote Share',
        labels={'Votes': 'Percentage'},
        color='Party',
        color_discrete_map=color_map
    )
    st.plotly_chart(fig_primary, use_container_width=True)

pref_flows = {"ALP": alp_to_grn,
             "AJP": ajp_to_grn,
             "IND": ind_to_grn}
result = run_election(grn_primary, lib_primary, ajp_primary, pref_flows)
# Calculate two-party preferred
# grn_tpp = (grn_primary + 
        #    (ajp_primary * ajp_to_grn/100) + 
        #    (ind_primary * ind_to_grn/100))
# lib_tpp = 100 - grn_tpp
grn_tpp = result['GRN']
lib_tpp = result['LIB']

# Two-party preferred visualization
with col2:
    # st.subheader("Two-Party Preferred")
    
    tpp_data = pd.DataFrame({
        'Party': ['GRN', 'LIB'],
        'Votes': [grn_tpp, lib_tpp]
    })
    
    fig_tpp = px.bar(
        tpp_data,
        x='Party',
        y='Votes',
        title='Two-Party Preferred Result',
        labels={'Votes': 'Percentage'},
        color='Party',
        color_discrete_map=color_map
    )
    # Increase font size of axes
    fig_tpp.update_layout(
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18)
    )
    # Add a horizontal line at 50%
    fig_tpp.add_hline(y=50, line_dash="dash", line_color="red")
    st.plotly_chart(fig_tpp, use_container_width=True)
