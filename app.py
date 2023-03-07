import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import contextily as cx
from construct_grid import make_grid

st.set_page_config(
    page_title="Urban Assessment Dashboard",
    page_icon="✅",
    layout="wide",
)

st.markdown('''# European City Maps!!
            ''')

@st.cache_data
def get_data():
    land_use = gpd.read_file('raw_data/berlin_landuse.gpkg')
    cities = gpd.read_file('raw_data/eu_cities.json')
    gridded_city = make_grid(cities[cities['city_name']=='Berlin'],250)
    #berlin = gpd.sjoin(gridded_city,land_use)
    return land_use, cities

berlin, cities = get_data()
selection = st.selectbox('Select your city', cities['city_name'].sort_values().drop_duplicates())

col1, col2, col3 = st.columns(3)

fig, axs = plt.subplots()
city_choice = cities[cities['city_name']==selection].reset_index(drop=True)
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
with col1:
    st.header('Plot 1')
    st.pyplot(fig)

fig, axs = plt.subplots()
city_choice = cities[cities['city_name']==selection].reset_index(drop=True)
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

with col2:
    st.header('Plot 2')
    st.pyplot(fig)

fig, axs = plt.subplots()
city_choice = cities[cities['city_name']==selection].reset_index(drop=True)
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

with col3:
    st.header('Plot 3')
    st.pyplot(fig)
