import streamlit as st
from params import *
import streamlit_folium
import folium
import leafmap.foliumap as leaf
import geopandas as gpd
from streamlit_folium import folium_static
import requests
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import ee
import geemap.foliumap as geemap

st.set_page_config(layout="wide")

@st.cache_data
def get_half_city(city_choice):
    url = DOCKER_URL+f'{city_choice.lower()}_data_1'
    response = requests.get(url).json()
    half_city = gpd.read_file(response)
    return half_city

@st.cache_data
def get_other_half(city_choice):
    url = DOCKER_URL+f'{city_choice.lower()}_data_2'
    response = requests.get(url).json()
    half_city = gpd.read_file(response)
    return half_city

city_selection = st.selectbox('Choose your city!',['Berlin'])
first_half = get_half_city(city_selection)
second_half = get_other_half(city_selection)
dataframe_list = [first_half,second_half]



berlin_data = gpd.GeoDataFrame(pd.concat(dataframe_list, ignore_index=True), crs=dataframe_list[0].crs)
berlin_data = berlin_data.to_crs(epsg=4326)
features = list(berlin_data.columns)
features.remove('geometry')
features.remove('id')
features.remove('y')
berlin_data['land_use_code'] = berlin_data['land_use_code'].astype(int)
berlin_data = berlin_data.replace({'land_use_code':URBAN_ATLAS_LAND_USE})

CENTER_LOC = [52.50148, 13.40198]
INIT_ZOOM = 10

# col1, col2 = st.columns([4, 1])

# Map = folium.Map()
# Map.add_basemap("ESA WorldCover 2020 S2 FCC")
# Map.add_basemap("ESA WorldCover 2020 S2 TCC")
# Map.add_basemap("HYBRID")
# with col1:
#     Map.to_streamlit(height=750)
# left_layer = berlin_data[['geometry','veg']].to_json()
# #right_layer = berlin_data[['geometry','log_y']].to_json()

# m = leaf.Map(location=CENTER_LOC,zoom_start=INIT_ZOOM)
# #left_group = folium.FeatureGroup(name='Left')
# #right_group = folium.FeatureGroup(name='Right')

# layer = leaf.geojson_layer(data=left_layer, name='veg')
# #folium.GeoJson(right_layer, name='biodiversity').add_to(right_group)
# m.add_layer(layer)
# m.add_layer_control(position='topleft')
# m.to_streamlit(height=600)

# #right_group.add_to(m)

# #leafmap.split_map()




feature_selection = st.selectbox('Choose your feature!',list(FEATURE_COLUMN_NAMES.keys()))
if feature_selection == 'Land Use':
    legend_choice = False
    legend_keys = {"pad": 0.01}
else:
    legend_choice = True
    legend_keys = {"orientation": "horizontal", "pad": 0.01}
fig, axs = plt.subplots()
berlin_data.plot(column=FEATURE_COLUMN_NAMES[feature_selection],ax=axs,legend=legend_choice,
                 legend_kwds=legend_keys)
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
#leg = axs.get_legend()
#leg.set_bbox_to_anchor((0.5,1.05))
st.pyplot(fig)
