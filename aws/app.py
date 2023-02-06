import time

import streamlit as st
import os
import json
import requests
from streamlit_lottie import st_lottie

path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()
from aws import get_files_from_noaa_bucket
from sql import main_database_func_trigger, fetch_data_from_table

main_database_func_trigger()

data_df = fetch_data_from_table()

# print(data_df)


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
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_satellite = "https://assets3.lottiefiles.com/private_files/lf30_cmdcmgh0.json"

st.markdown("<h1 style='text-align: center'>Data Explorator</h1>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>GEOS</h2>",unsafe_allow_html=True)
selected_year_geos = ""
selected_day_geos = ""
selected_hour_geos = ""
year,day,hour = st.columns([1,1,1])

with year:
    yl = data_df.year.unique().tolist()
    yl.insert(0, "Select Year")
    year = st.selectbox('Year', yl)
    # year = st.selectbox('Year', range(2020, 2023))
    selected_year_geos = year
days_of_selected_year = extract_values_from_df(data_df,"year",selected_year_geos,"day")
with day:
    dsyl = days_of_selected_year.tolist()
    dsyl.insert(0, "Select Day")
    day = st.selectbox('Day',dsyl)
    selected_day_geos = day
hours_of_selected_day = extract_values_from_df(data_df,"day",selected_day_geos,"hour")
with hour:
    hsdl = hours_of_selected_day.tolist()
    hsdl.insert(0,"Select Hour")
    hour = st.selectbox("Hour",hsdl)
    selected_hour_geos = hour
def return_list(dir_to_check_geos):
    noaa_files_list = []

    noaa_files_list = get_files_from_noaa_bucket(dir_to_check_geos)

    return noaa_files_list


# "st.session_state object:", st.session_state
dir_to_check_geos = ""
if (selected_hour_geos != "Select Hour") and (selected_day_geos != "Select Day") and (selected_year_geos != "Select Year"):
    dir_to_check_geos = f"ABI-L1b-RadC/{selected_year_geos}/{selected_day_geos}/{selected_hour_geos}"
# dir_to_check_geos = "ABI-L1b-RadC" + "/" + str(selected_year_geos) + "/" + str(selected_day_geos) + "/" + str( selected_hour_geos)
st.markdown(dir_to_check_geos)

l = return_list(dir_to_check_geos) if dir_to_check_geos != "" else []
selected_file = st.selectbox("Select a file",l)
fetching, image = st.columns([3, 1])
# fetch_btn = 0
# fetch_btn = 1 if st.button("Fetch Data") else 0

# if selected_year_geos != "Select Year" :
#     files_list = ["Select a file"]
#     # st.selectbox("Select an option",files_list)
#     not_empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty
#     # if fetch_btn:
        # if not_empty_selection:
# dir = "ABI-L1b-RadC/2022/209/00"
# files_list.extend(noaa_files_list)
# files_list = []
files_list = return_list(dir_to_check_geos)
# selected_file = st.selectbox("Select a file", noaa_files_list)
selected_file = st.multiselect(
    "Select a file",
    files_list)
st.write('You selected:', selected_file)

    # select_and_download_btn = st.button("select and download")

    # if select_and_download_btn:
    #     st.markdown("")

    # with image:
    #     lottie_hello = load_lottieurl(f"{lottie_satellite}")
    #     st_lottie(
    #         lottie_hello,
    #         speed=1,
    #         reverse=False,
    #         loop=True,
    #         height="450px",
    #         width=None,
    #         key=None,
    #     )
        # else:
        #     fetch_btn = 0
        #     st.markdown("please select all fields")

# else:
#     st.markdown("Select the details")
