import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.metric_cards import style_metric_cards
import folium
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Configure Page Title and Icon
st.set_page_config(page_title='Overall Impact',page_icon='📊')

st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2= st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')
with col2:
    next = st.button("➡️",help='Next Page')

if next:
     switch_page("Impact on Companies")
if back:
     switch_page("Home")

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
table_name = "STREAMLIT_DEMO.STREAMLIT.LAYOFFS_FINAL" 

# Displaying data
layoff_df=snowflake_loader(table_name)
layoff_df.dropna(subset=['LAID_OFF_COUNT'], inplace=True)
year = st.radio(
    'Select year',
    ['2021', '2022', '2023'],
    index=2,horizontal=True
)

# Companies
Companies_TY=layoff_df.loc[layoff_df['DATE'].dt.year == int(year), 'COMPANY'].nunique()
Companies_LY=layoff_df.loc[layoff_df['DATE'].dt.year == (int(year)-1), 'COMPANY'].nunique()
Companies_delta=((Companies_TY-Companies_LY)/Companies_LY)*100

# Employees
Employees_TY = layoff_df.loc[layoff_df['DATE'].dt.year == int(year), 'LAID_OFF_COUNT'].sum()
Employees_LY = layoff_df.loc[layoff_df['DATE'].dt.year == (int(year)-1), 'LAID_OFF_COUNT'].sum()
Employees_delta=((Employees_TY-Employees_LY)/Employees_LY)*100

# Countries
Countries_TY=layoff_df.loc[layoff_df['DATE'].dt.year == int(year), 'COUNTRY'].nunique()
Countries_LY=layoff_df.loc[layoff_df['DATE'].dt.year == (int(year)-1), 'COUNTRY'].nunique()
Countries_delta=((Countries_TY-Countries_LY)/Countries_LY)*100

if year is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Companies that laid off", value=int(Companies_TY), delta=f"{round(Companies_delta, 2)} % vs PY")
    col2.metric(label="Total Employees Laid off", value=f"{int((Employees_TY/1000)):.1f} K", delta=f"{round(Employees_delta, 2)} % vs PY")
    col3.metric(label="Countries Affected", value=int(Countries_TY), delta=f"{round(Countries_delta, 2)} % vs PY")
    style_metric_cards()


st.info('Explore the Companies around the world that have made layoffs by clicking the circles on the map')

########## MAP
def generate_map(layoff_df):
    layoff_df = layoff_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Create a map centered on the mean LATITUDE and LONGITUDE of the data
    m = folium.Map(location=[51.5074, -0.0278], zoom_start=1.5, height=400)
    # Create a marker cluster layer and add it to the map
    marker_cluster = MarkerCluster().add_to(m)
    # Create a set to keep track of the unique companies
    unique_companies = set()
    # Loop through the data and add markers to the marker cluster layer for unique companies only
    for index, row in layoff_df.iterrows():
        if row['COMPANY'] not in unique_companies:
            popup_text = f"Company: {row['COMPANY']}<br> Laid off count: {int(row['LAID_OFF_COUNT'])} <br><br> More Details <br> Industry: {row['INDUSTRY']} <br> HQ Location: {row['LOCATION_HQ']}  "
            iframe = folium.IFrame(popup_text)
            popup = folium.Popup(iframe,
                     min_width=200,
                     max_width=500,
                     height=90)
            folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=popup, color="red",min_width=5000).add_to(marker_cluster)
            unique_companies.add(row['COMPANY'])

    return m



# Generate the map
map = generate_map(layoff_df[layoff_df['DATE'].dt.year == int(year)])

# Use Streamlit to display the map
folium_static(map)
