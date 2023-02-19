import pandas as pd
import streamlit as st
import os
import json
import requests
from streamlit_lottie import st_lottie
import logging
import folium
from aws_nexrad import get_files_from_nexrad_bucket, get_noaa_nexrad_url, copy_s3_nexrad_file, get_my_s3_url_nex, get_dir_from_filename_nexrad
# from aws_nexrad import get_dir_from_filename_nexrad, get_files_from_nexrad_bucket, get_noaa_nexrad_url
from nex_sql import fetch_data_from_table
# from aws_geos import get_files_from_noaa_bucket, get_noaa_geos_url, copy_s3_file, get_my_s3_url, \
#     get_dir_from_filename_geos
from streamlit_folium import folium_static
path = os.path.dirname(__file__)
from dotenv import load_dotenv

load_dotenv()

st.markdown("<h1 style='text-align: center'>Data Explorator</h1>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>NEXRAD</h2>",unsafe_allow_html=True)


# """
# returns values from df of selected column
# """

def extract_values_from_df(df, key, value, col):
    # Extract the rows where key is equal to value
    filtered_df = df[df[key] == value]

    # Return all the values from the specified column
    return filtered_df[col].unique().tolist()

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_satellite = "https://assets3.lottiefiles.com/private_files/lf30_cmdcmgh0.json"

with st.sidebar:
    lottie_pro = load_lottieurl(f"{lottie_satellite}")
    st_lottie(
        lottie_pro,
        speed=1,
        reverse=False,
        loop=True,
        height="450px",
        width=None,
        key=None,
    )

selected_year_nexrad = ""
selected_month_nexrad = ""
selected_day_nexrad = ""
selected_station_nexrad = ""

#creating columns to show year, day, hour to user to select
year, month, day, station_code = st.columns([1, 1, 1, 1])

data_df = fetch_data_from_table()

with year:
    yl = data_df.year.unique().tolist()
    # yl = [int(item) for item in yl]
    # yl.sort()
    # yl = [str(item) for item in yl]
    yl.insert(0, "Select Year")
    year = st.selectbox('Year', yl)
    # year = st.selectbox('Year', range(2020, 2023))
    selected_year_nexrad = year
month_of_selected_year = extract_values_from_df(data_df[data_df.year==selected_year_nexrad], "year", selected_year_nexrad, "month")
with month:
    msyl = month_of_selected_year
    # msyl = [int(item) for item in msyl]
    # msyl.sort()
    # msyl=[str(item) for item in msyl]
    msyl.insert(0, "Select Month")
    month = st.selectbox('Month', msyl)
    selected_month_nexrad = month
day_of_selected_month = extract_values_from_df(data_df[(data_df.year==selected_year_nexrad) & (data_df.month==selected_month_nexrad)], "month", selected_month_nexrad, "day")

with day:
    dsml = day_of_selected_month
    # dsml = [int(item) for item in dsml]
    # dsml.sort()
    # dsml = [str(item) for item in dsml]
    dsml.insert(0, "Select Day")
    day = st.selectbox("Day", dsml)
    selected_day_nexrad = day
station_code_of_selected_hour = extract_values_from_df(data_df[(data_df.year==selected_year_nexrad) & (data_df.month==selected_month_nexrad) & (data_df.day==selected_day_nexrad)],"day", selected_day_nexrad, "station")

with station_code:
    scshl = station_code_of_selected_hour
    # scshl = [int(item) for item in scshl]
    # scshl.sort()
    # scshl = [str(item) for item in scshl]
    scshl.insert(0,"Select station")
    station = st.selectbox("Station Code",scshl)
    selected_station_nexrad = station
    # """
    # takes geos dir as input and returns al the files in that dir as list
    # """
def return_list(dir_to_check_geos):
    noaa_files_list = []

    noaa_files_list = get_files_from_nexrad_bucket(dir_to_check_geos)

    return noaa_files_list

#creating dir based on user input
dir_to_check_nexrad = ""
if ((selected_year_nexrad != "Select Year") and (selected_month_nexrad != "Select Month") and (
        selected_day_nexrad != "Select Day") and (selected_station_nexrad != "Select station")):
# if (selected_day_nexrad != "Select Hour") and (selected_month_nexrad != "Select Day") and (selected_year_nexrad != "Select Year") and (selected_station_nexrad != "Select station"):
    dir_to_check_nexrad = f"{selected_year_nexrad}/{selected_month_nexrad}/{selected_day_nexrad}/{selected_station_nexrad}"
# st.markdown(dir_to_check_nexrad)


fetching, image = st.columns([3, 1])

#     not_empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty

#Takes list of files from user selected directory and showing them in selectbox
noaa_files_list = return_list(dir_to_check_nexrad) if dir_to_check_nexrad != "" else []
selected_file = st.selectbox("Select a file", noaa_files_list)



#retrieving url from AWS s3 bucket for selected file
nexrad_file_url = get_noaa_nexrad_url(f"{dir_to_check_nexrad}/{selected_file}")
get_url_btn = st.button("Get Url")
my_s3_file_url = ""
# empty_selection = all(map(bool, [selected_year_geos, selected_day_geos, selected_hour_geos])) #returns a bool on checking if all fields are empty

if get_url_btn:
    if((selected_year_nexrad != "Select Year") and (selected_month_nexrad != "Select Month") and (selected_day_nexrad != "Select Day") and (selected_station_nexrad != "Select station")):
    # if ((selected_day_nexrad != "Select Hour") and (selected_month_nexrad != "Select Day") and (selected_year_nexrad != "Select Year")):
        src_bucket = "noaa-nexrad-level2"
        des_bucket = "damg7245-ass1"
        # copying user selected file from AWS s3 bucket to our bucket
        copy_s3_nexrad_file(src_bucket, selected_file, des_bucket, selected_file)
        # getting url of user selected file from our s3 bucket
        my_s3_file_url = get_my_s3_url_nex(selected_file)
        st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
        with st.expander("Expand for URL"):
            text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
            st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
            logging.info("URL has been generated")
    else:
        st.error("Please select all fields!")




st.markdown("----------------------------------------------------------------------------------------------------")
st.markdown("<h2 style='text-align: center'>Download Using FileName</h2>",unsafe_allow_html=True)
given_file_name = st.text_input("Enter File Name")
button_url = st.button("Get url")

if button_url:
    if given_file_name != "":
        src_bucket = "noaa-nexrad-level2"
        des_bucket = "damg7245-ass1"

        # copying user selected file from AWS s3 bucket to our bucket
        full_file_name = get_dir_from_filename_nexrad(given_file_name)

        # copied_flag return true if file copied
        copied_flag = copy_s3_nexrad_file(src_bucket, full_file_name, des_bucket, full_file_name)

        # getting url of user selected file from our s3 bucket
        dir_to_check = f"{selected_year_nexrad}/{selected_month_nexrad}/{selected_day_nexrad}/{selected_station_nexrad}"

        # copied_flag returns true if file copied
        if copied_flag: #returns true if file copied
            my_s3_file_url = (f"https://damg7245-ass1.s3.amazonaws.com/{full_file_name}")
            st.success(f"Download link has been generated!\n [URL]({my_s3_file_url})")
            logging.info("Download link generated")

            # displaying url through expander
            with st.expander("Expand for URL"):
                text2 = f"<p style='font-size: 20px; text-align: center'><span style='color: #15b090; font-weight:bold ;'>{my_s3_file_url}</span></p>"
                st.markdown(f"[{text2}]({my_s3_file_url})", unsafe_allow_html=True)
                logging.info("URL has been generated")
        else:
            st.error("File not found in NEXRAD Dataset, Please enter a valid filename")

    else:
        st.error("Please Enter a file name")



DATA_URL = ('nexrad.csv')
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x:str(x).lower()
    return data
data = load_data(10000)
df = pd.DataFrame({'name': data['NAME'],'lat': data['LAT'],'lon':data['LON']})

m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
# st.map(df)
for i in range(0,len(data)):
   folium.Marker(
      location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
      popup=df.iloc[i]['name'],
   ).add_to(m)
# st.markdown()
folium_static(m)