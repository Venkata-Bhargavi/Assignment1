import streamlit as st
import os
path = os.path.dirname(__file__)

from aws.main import get_files_from_noaa_bucket


st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title='Venkata_Bhargavi_Sikhakolli',  # String or None. Strings get appended with "• Streamlit".
    page_icon= None,  # String, anything supported by st.image, or None.
)

st.header("Data Explorator")

st.markdown("<h1 style='text-align: center'>Data Explorator</h1>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>GEOS</h2>",unsafe_allow_html=True)
selected_year_geos = ""
selected_day_geos = ""
selected_hour_geos = ""
year,day,hour = st.columns([1,1,1])
with year:
    year = st.selectbox('Year', range(2020, 2023))
    selected_year_geos = year
with day:
    day = st.selectbox('Day',range(1,260))
    selected_day_geos = day
with hour:
    hour = st.selectbox("Hour",range(0,23))
    selected_hour_geos = hour

dir_to_check_geos = str(selected_year_geos) + "/" + str(selected_day_geos) + "/" + str(selected_hour_geos)


files_list = get_files_from_noaa_bucket(dir_to_check_geos)
st.selectbox(files_list)
