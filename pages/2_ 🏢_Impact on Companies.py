import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from annotated_text import annotated_text

# Configure Page Title and Icon
st.set_page_config(page_title='Impact on Companies',page_icon='📊')

st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2 = st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')
with col2:
    next = st.button("➡️",help='Next Page')

if next:
     switch_page("Impact on Industries")
if back:
     switch_page("Overall Impact")

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

# Bar Chart of top five countries
import matplotlib.pyplot as plt
# group by country and company, and sum the employees
grouped_country = layoff_df.groupby(['COUNTRY']).sum('LAID_OFF_COUNT')
grouped_company = layoff_df.groupby(['COMPANY']).sum('LAID_OFF_COUNT')

# sort by employees in descending order, and reset index
sorted_df_country = grouped_country.reset_index().sort_values('LAID_OFF_COUNT', ascending=False).head(5)
sorted_df_company = grouped_company.reset_index().sort_values('LAID_OFF_COUNT', ascending=False).head(5)


import altair as alt

chart1 = alt.Chart(sorted_df_company).mark_bar().encode(
    x=alt.X('LAID_OFF_COUNT:Q'),
    y=alt.Y('COMPANY:O', sort='-x'),
    text='LAID_OFF_COUNT:Q',
    color=alt.Color('LAID_OFF_COUNT:Q', scale=alt.Scale(scheme='blues'))
).configure_axis(
    grid=False,  # hide grid lines
    domain=False,  # hide axis line and ticks
).properties(
   height=300,  # set height to 400 pixels
)

annotated_text(
    ("💡 Tech gaints like Amazon, Meta & Google have laid off more than"),
    ('50k+ employees ','','#faa')
)

st.altair_chart(chart1,use_container_width=True)


st.subheader('More Headlines')
c1, c2, c3 = st.columns(3)
with c1:
    st.error('**Apple** paused hiring')
with c2:
    st.error('**Quallcomm** froze hiring')
with c3:
    st.error('**Twitter** laidoff half of its staff')



