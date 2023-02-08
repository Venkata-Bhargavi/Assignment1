import streamlit as st
import os
import json
import requests

from sql import fetch_data_from_table
from aws_geos import get_files_from_noaa_bucket, get_noaa_geos_url, copy_s3_file, get_my_s3_url

path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()


data_df = fetch_data_from_table()


# """
# returns values from df of selected column
# """

def extract_values_from_df(df, key, value, col):
    # Extract the rows where key is equal to value
    filtered_df = df[df[key] == value]

    # Return all the values from the specified column
    return filtered_df[col].values


# st.set_page_config(  # Alternate names: setup_page, page, layout
#     layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
#     initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
#     page_title='Venkata_Bhargavi_Sikhakolli',  # String or None. Strings get appended with "• Streamlit".
#     page_icon= None,  # String, anything supported by st.image, or None.
# )


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

#creating columns to show year, day, hour to user to select
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

    # """
    # takes geos dir as input and returns al the files in that dir as list
    # """
def return_list(dir_to_check_geos):
    noaa_files_list = []

    noaa_files_list = get_files_from_noaa_bucket(dir_to_check_geos)

    return noaa_files_list

#creating dir based on user input
dir_to_check_geos = ""
if (selected_hour_geos != "Select Hour") and (selected_day_geos != "Select Day") and (selected_year_geos != "Select Year"):
    dir_to_check_geos = f"ABI-L1b-RadC/{selected_year_geos}/{selected_day_geos}/{selected_hour_geos}"
st.markdown(dir_to_check_geos)


fetching, image = st.columns([3, 1])

#     not_empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty

#Takes list of files from user selected directory and showing them in selectbox
noaa_files_list = return_list(dir_to_check_geos) if dir_to_check_geos != "" else []
selected_file = st.selectbox("Select a file", noaa_files_list)



#retrieving url from AWS s3 bucket for selected file
geos_file_url = get_noaa_geos_url(f"{dir_to_check_geos}/{selected_file}")
get_url_btn = st.button("Get Url")
my_s3_file_url = ""
if get_url_btn:
    src_bucket = "noaa-goes18"
    des_bucket = "damg7245-ass1"
    #copying user selected file from AWS s3 bucket to our bucket
    copy_s3_file(src_bucket,selected_file,des_bucket,selected_file)
    #getting url of user selected file from our s3 bucket
    my_s3_file_url = get_my_s3_url(dir_to_check_geos,selected_file)
    st.markdown(f"{my_s3_file_url}")
st.markdown(f"[Download]({my_s3_file_url})",unsafe_allow_html= True)
