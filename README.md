# Assignment 1 - Exploration of GOES and NEXRAD Datasets

<h3> Problem Statement </h3>
Build a data exploration tool for a Geospatial startup that leverages publically available data and allows data analysts to download it. GOES and NEXRAD satellite datasets are the main data sources available on the NOAA's (National Oceanic and Atmospheric Administration) website.

<h3> Description </h3>

GOES is a satellite that provides atmospheric measurements and advanced imagery that helps meteorologists observe and predict local weather like, hurricanes, severe floods, thunderstorms, fog etc, and help in monitoring volcanic eruptions and forest fires.

NEXRAD systems are weather radars that detect and produce over 100 different long-range and high-altitude weather observations and products, including areas of precipitation, winds, and thunderstorms.

<h3> Flow of Data</h3>

1. NOAA's website has raw GOES and NEXRAD satellite data.
2. This data is scraped in order to generate metadata, which is then stored in SQLite.
3. These values pertain to metadata directories.
4. The user has access to our Exploration Web App, where he must specify the 'Year,' 'Day,' and 'Hour'.
5. Using these values, a unique file is fetched and a link to download the file displayed.
8. User can also use the filename to retrive and download the file.
9. Downloaded file is in .NC format, used to store multidimensional data.

<h3> Built With </h3>

Following are the stacks used to build this project

1. AWS
2. SQLite3
3. Python 3.9.x
4. Streamlit 1.12.x

<h3> Contribution </h3>

1. Akash : 25%
2. Bhakti : 25%
3. Bhargavi : 25%
4. Charu : 25%

