import streamlit as st
from demeter.main_interface.y_plot import make_plotly_plot,get_plotly_data

st.set_page_config(
    layout='wide',
    page_title='Feature Map Display',
    initial_sidebar_state='collapsed'
)

st.title('Feature Map Display')
city_choice = st.selectbox('Select your city!',['Berlin','Paris','Athens','Barcelona','Zurich','London','Ljubljana'])
@st.cache_data
def get_data(city_choice):
    data = get_plotly_data(city_choice)
    return data

data = get_data(city_choice)

feature_choice = st.selectbox('Select your layer!',['Vegetation Intensity','Road Density',
                                'Water', 'Residential Density', 'Non-Residential Density',
                                'Population', 'Biodiversity'])

plotly_fig = make_plotly_plot(data,feature_choice)

st.plotly_chart(plotly_fig,use_container_width=True)
