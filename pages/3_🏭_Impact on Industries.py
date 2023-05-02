import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from wordcloud import WordCloud
import math
import numpy as np
from annotated_text import annotated_text

# Configure Page Title and Icon
st.set_page_config(page_title='Impact on Industries',page_icon='📊')

st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2 = st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')
with col2:
    next = st.button("➡️",help='Next Page')

if next:
     switch_page("Impact Over Time")
if back:
     switch_page("Impact on Companies")

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

# Group the data by Industry and get the sum of Laid_Off_Count for each group
industry_laid_off_count = layoff_df.groupby('INDUSTRY')['LAID_OFF_COUNT'].sum()

# Convert the result to a dictionary
result_dict = industry_laid_off_count.to_dict()

word_freq_clean = {k: 0 if math.isnan(v) else v for k, v in result_dict.items()}
# Generate the word cloud
wordcloud = WordCloud(width=600, height=400, background_color='white').generate_from_frequencies(word_freq_clean)


#### Annotated Text
annotated_text(
    "💡 Highest number of layoffs are in ",
    ("Consumer ",'',"#faa"),
    (' & '),
    (" Retail",'',"#faa"),
    " sector while industry with the lowest number of layoffs is ",
    ("Manufacturing",'', "#afa")
)
# Display the word cloud using Streamlit
st.image(wordcloud.to_array())
