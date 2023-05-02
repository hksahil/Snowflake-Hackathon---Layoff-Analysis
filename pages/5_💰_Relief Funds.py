import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import altair as alt
import plotly.graph_objects as go
from annotated_text import annotated_text
import seaborn as sns

# Configure Page Title and Icon
st.set_page_config(page_title='Relief Funds',page_icon='📊')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2 = st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')
with col2:
    next = st.button("➡️",help='Next Page')

if next:
     switch_page("Playground for Analysis")
if back:
     switch_page("Impact over Time")

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

layoff_df["DATE"] = pd.to_datetime(layoff_df["DATE"])

layoff_df["DATE"] = pd.to_datetime(layoff_df["DATE"])

# Get the top 10 countries by laid off count
top_countries = layoff_df["COMPANY"].value_counts().nlargest(10).index.tolist()

# Filter the data to include only the top 5 countries
layoff_df = layoff_df[layoff_df["COMPANY"].isin(top_countries)]

# Group the data by country and year, and sum the funds_raised column
layoff_df["YEAR"] = layoff_df["DATE"].dt.year
df_agg = layoff_df.groupby(["YEAR", "COMPANY"])["FUNDS_RAISED"].sum().reset_index()

# Pivot the data to create a table with years as rows and countries as columns
df_agg["DATE"] = df_agg["YEAR"].astype(str)
df_pivot = df_agg.pivot(index="DATE", columns="COMPANY", values="FUNDS_RAISED")


annotated_text(
    ("💡 Companies have been "),
    (" raising relief funds ",'','#afa'),
    (' to sustain and expand their operations')
)
# Create a heatmap using Seaborn
sns.set(rc={'figure.figsize':(11, 5)})
sns.heatmap(df_pivot, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Funds raised ($)'})
st.pyplot()
