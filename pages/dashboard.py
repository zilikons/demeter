import streamlit as st
import geopandas as gpd
from data_queries import *
from params import *
st.set_page_config(layout='wide',
                   page_title='Urban Assessment Dashboard',
                   initial_sidebar_state='collapsed')
st.title('Urban Assessment Dashboard')


col1,col2,col3 = st.columns((2,2,1))

@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/zilikons/demeter/master/data/berlin_with_features.json"
    data = gpd.read_file(url)
    return data

data = get_data()


with col3:
    feature1= st.selectbox('pick the first feature',FEATURE_COLUMN_NAMES.keys())
    feature2= st.selectbox('pick the second feature',FEATURE_COLUMN_NAMES.keys())

with col1:
    fig = feature_histogram_side_by_side(data,feature1,feature2)
    st.pyplot(fig)

with col2:
    fig2 = plot_correlation(data,FEATURE_COLUMN_NAMES[feature1])
    st.pyplot(fig2)
