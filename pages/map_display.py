import streamlit as st
from demeter.main_interface.y_plot import make_plotly_plot,get_plotly_data

st.set_page_config(
    layout='wide'
)

st.title('Map Layer Display')
city_choice = st.selectbox('Select your city!',['Berlin'])
@st.cache_data
def get_data():
    data = get_plotly_data(city_choice)
    return data

data = get_data()

feature_choice = st.selectbox('Select your layer!',['Vegetation Intensity','Road Density',
                                'Water', 'Residential Density', 'Non-Residential Density',
                                'Population', 'Biodiversity'])

plotly_fig = make_plotly_plot(data,feature_choice)

st.plotly_chart(plotly_fig,use_container_width=True)
