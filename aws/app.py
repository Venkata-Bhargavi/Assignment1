import streamlit as st
import os
path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()
from aws import get_files_from_noaa_bucket
from sql import main_database_func_trigger, fetch_data_from_table

main_database_func_trigger()

data_df = fetch_data_from_table()

print(data_df)


def extract_values_from_df(df, key, value, col):
    # Extract the rows where key is equal to value
    filtered_df = df[df[key] == value]

    # Return all the values from the specified column
    return filtered_df[col].values


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
    year = st.selectbox('Year', options= data_df.year.unique().tolist())
    # year = st.selectbox('Year', range(2020, 2023))
    selected_year_geos = year
days_of_selected_year = extract_values_from_df(data_df,"year",selected_year_geos,"day")
with day:
    day = st.selectbox('Day',days_of_selected_year.tolist())
    selected_day_geos = day
hours_of_selected_day = extract_values_from_df(data_df,"day",selected_day_geos,"hour")
with hour:
    hour = st.selectbox("Hour",hours_of_selected_day.tolist())
    selected_hour_geos = hour

dir_to_check_geos = "ABI-L1b-RadC" + "/" + str(selected_year_geos) + "/" + str(selected_day_geos) + "/" + str(selected_hour_geos)
print(dir_to_check_geos,"////////////////")

btn = st.button("Fetch Data")
not_empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos]))
if btn:
    if not_empty_selection:
        dir = "ABI-L1b-RadC/2022/209/00"
        files_list = get_files_from_noaa_bucket(dir_to_check_geos)
        st.selectbox("Select an option", files_list)
    else:
        st.markdown("please select all fields")
