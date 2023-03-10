import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from params import *


@st.cache_data
def get_geolayer():
    gdf = gpd.read_file('https://raw.githubusercontent.com/zilikons/demeter/master/data/berlin_with_features.json')
    return gdf
gdf = get_geolayer()
color_scale = ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']
features = list(gdf.columns)
features.remove('geometry')
features.remove('y')

if 'selected_column' not in st.session_state:
    st.session_state['selected_column'] = features[0]



def normalize(column):
    print(column.head(3))
    column = (column-column.min())/(column.max()-column.min())
    return column

def style_function(feature):
    column = st.session_state['selected_column']
    value = feature['properties'][column]  # Replace 'value' with the name of the column containing the values
    color_index = min(int(value * len(color_scale)), len(color_scale)-1)
    color = color_scale[color_index]
    return {'fillColor': color, 'color': '#000000', 'weight': 1, 'fillOpacity': 0.3}

# Create a map object using Folium
m = folium.Map(location=[52.50380, 13.39515], zoom_start=11)

# Add a marker to the map
for column in features:
    gdf[column] = normalize(gdf[column].astype(float))
geojson_data = gdf.to_json()
for column in features:
    gdf[column] = gdf[column].astype(float)
    folium.GeoJson(geojson_data, name=column, style_function=style_function).add_to(m)


folium.LayerControl().add_to(m)
# Use the folium_static function to display the map in Streamlit
folium_static(m)


selected_column = st.selectbox('Select a column:', features, index=0, key='selected_column')
st.session_state['selected_column'] = selected_column
