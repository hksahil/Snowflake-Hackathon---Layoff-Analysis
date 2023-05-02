import streamlit as st
from snowflake.snowpark import Session
import time
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from PIL import Image

# Configure Page Title and Icon
st.set_page_config(page_title='Layoffs Analysis',page_icon=':🏡:')

st.title('Layoffs :red[Tracker] 💼🚪 ')

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
# layoff_df=snowflake_loader(table_name)
# st.write(layoff_df)

from annotated_text import annotated_text
annotated_text(
    " Tech companies thrived during the pandemic with remarkable ",
    ("revenue ",'',"#afa"),
    (' & '),
    ("employee headcount ",'',"#afa"),
    (" However, they are now "),
    (" cutting thousands of jobs globally",'','#faa')
)

c1, c2 = st.columns(2)
c1.image(Image.open('Images/Amazonv1.png'))
c2.image(Image.open('Images/Google.png'))

c1, c2 = st.columns(2)
c1.image(Image.open('Images/Meta.png'))
c2.image(Image.open('Images/Salesforce.png'))

c1, c2 = st.columns(2)
c1.image(Image.open('Images/Uber.png'))
c2.image(Image.open('Images/Microsoft.png'))

st.subheader('This dashboard provides an overview of the situation.')
## Navigation

col1,col2=st.columns(2)
with col1:
    st.write('(*Use the arrow to navigate the dashboard*)', unsafe_allow_html=True)
with col2:
    next = st.button("➡️",help='Next Page')

st.markdown("""---""")
st.warning('ℹ️ Dataset is taken from [Kaggle](https://www.kaggle.com/datasets/theakhilb/layoffs-data-2022) and contains data from Jan 2020 to May 2023')
if next:
     switch_page("Overall Impact")
