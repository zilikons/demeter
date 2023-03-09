import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import contextily as cx
from shapely.geometry import Point
import matplotlib.colors as colors
#from construct_grid import make_grid
from demeter.main_interface.y_plot import make_plotly_plot

# page configuration
st.set_page_config(
    page_title="Urban Assessment Dashboard",
    page_icon="✅",
    layout="wide",
)

st.header('Berlin biodiversity')
st.write("Interactive biodervisty dashboard")

@st.cache_data
def get_data():
    land_use = gpd.read_file('raw_data/land_use.gpkg')
    cities = gpd.read_file('raw_data/eu_cities.json')
    url = "https://github.com/eurostat/Nuts2json/raw/master/2021/4326/20M/nutsrg_3.json"
    european_countries = gpd.read_file(url)
    berlin_gridded_y_fig = make_plotly_plot('raw_data/berlin_grid_y.json',cities,'Berlin','ylgnbu')
    #gridded_city = make_grid(cities[cities['city_name']=='Berlin'],250)
    #berlin = gpd.sjoin(gridded_city,land_use)
    return land_use, cities, european_countries, berlin_gridded_y_fig

berlin, cities, european_countries, city_grid_y = get_data()

with st.sidebar:
    selection = st.selectbox('Select your city', cities['city_name'].sort_values().drop_duplicates())
selected_city_info = cities[cities['city_name']==selection].reset_index(drop=True)
selected_city_geojson = selected_city_info.geometry.__geo_interface__
location_name = selected_city_info['city_name']
location_lat = selected_city_info['geometry'].centroid.y[0]
location_lon = selected_city_info['geometry'].centroid.x[0]
location_point = Point(location_lon, location_lat)
location_country = european_countries[european_countries.contains(location_point)].iloc[0]
location_data = pd.DataFrame({"Name": [location_name], "Latitude": [location_lat], "Longitude": [location_lon]})


fig, axs = plt.subplots()
city_choice = selected_city_info
city_choice.plot(ax=axs,legend=False)
axs.set_title(f'Amazing {selection} plot!')
axs.tick_params(
    axis='both',
    which='both',
    left = False,
    right=False,
    bottom=False,
    top=False,
    labelleft=False,
    labelbottom=False
)

col1, col2 = st.columns((2,2))

with col1:
    st.header('Basic plot')
    st.pyplot(fig)

location_data['Name'] = location_data['Name'].astype(str)
fig = px.choropleth_mapbox(location_data, geojson=location_country.geometry.__geo_interface__, color="Name",
locations='Name', featureidkey="properties.NUTS_ID",
mapbox_style="carto-positron", zoom=10, center={"lat": location_lat, "lon": location_lon},
opacity=0.8, labels={'Name': 'Location'}, hover_name='Name', hover_data=['Name','Latitude','Longitude'])
trace = go.Choroplethmapbox(
    geojson=selected_city_geojson,
    locations=selected_city_info.index,
    z=[4],##TODO: CHANGE ME
    colorscale='Reds',
    marker_opacity=0.5,
    marker_line_width=0,
    name='Hover Title',
    showlegend=False,
)
fig.add_trace(trace)
fig.update_traces(hovertemplate=None)
fig.update_layout(showlegend=False)

with col2:
    st.header('Interactive plot')
    st.plotly_chart(fig)


with st.expander('Bonus Berlin Plot!'):
    st.plotly_chart(city_grid_y)
