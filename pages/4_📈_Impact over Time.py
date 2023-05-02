import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import altair as alt

# Configure Page Title and Icon
st.set_page_config(page_title='Impact over Time',page_icon='📊')


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
     switch_page("Impact on Industries")

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

# Area Chart
# Convert "Date" column to datetime type
layoff_df["DATE"] = pd.to_datetime(layoff_df["DATE"], format="%d/%m/%y")

# Group by year and sum the "Laid_Off_Count" column
df_grouped = layoff_df.groupby(layoff_df["DATE"].dt.year)["LAID_OFF_COUNT"].sum().reset_index()

# Create the area chart
chart = alt.Chart(df_grouped).mark_area(opacity=0.4,color="red").encode(
    x=alt.X("DATE:N", title="Year"),
    y=alt.Y("LAID_OFF_COUNT:Q", title="Laid Off Count", axis=alt.Axis(format=",.0f")),
)


# combine the chart and the labels

# configure axis options
chart = chart.configure_axis(
    grid=False,
    domain=False,
    tickSize=0
).properties(
   height=450,  # set height to 400 pixels
)

#### Annotated Text
from annotated_text import annotated_text
annotated_text(
    "💡 Companies are resorting to massive layoffs with the numbers consistently ",
    (" increasing from 2020 to 2023 📉  ",'',"#faa"),
    (' leaving many individuals struggling to make ends meet '),
)

# Show the chart in Streamlit app
st.altair_chart(chart, use_container_width=True)
