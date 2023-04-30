
import streamlit as st
from snowflake.snowpark import Session
from st_aggrid import AgGrid

st.title('Layoffs Tracker')

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
    return table

# Table present in Snowflake
table_name = "STREAMLIT_DEMO.STREAMLIT.LAYOFFS"

# Displaying data
df = snowflake_loader(table_name)
st.dataframe(df)
AgGrid(df)