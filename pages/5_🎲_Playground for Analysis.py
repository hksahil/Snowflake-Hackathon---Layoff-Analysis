import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.dataframe_explorer import dataframe_explorer
from annotated_text import annotated_text

# Configure Page Title and Icon
st.set_page_config(page_title='Playground for Analysis',page_icon=':smile:')


st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2 = st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')
with col2:
    next = st.button("➡️",help='Next Page')

if next:
     switch_page("Track my Job")
if back:
     switch_page("Impact over Time")


#### Annotated Text
annotated_text(
    "💡 Feel free to ",
    (" explore the dataset  ",'',"#afa"),
    (' using the Filter feature '),
)

# Snowflake Connection
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()

session = create_session()

# Table Loader
@st.cache_data
def snowflake_loader(table_name):
    table = session.table(table_name)
    table = table.collect()
    df = pd.DataFrame(table)
    return df

# Table present in Snowflake
table_name = "STREAMLIT_DEMO.STREAMLIT.LAYOFFS" 

# Displaying data
layoff_df=snowflake_loader(table_name)
layoff_df.dropna(subset=['LAID_OFF_COUNT'], inplace=True)
filtered_df = dataframe_explorer(layoff_df, case=False)
st.dataframe(filtered_df, use_container_width=True)