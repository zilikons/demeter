import streamlit as st
import geopandas as gpd
from data_queries import *
from params import *
from demeter.main_interface.altair_dashboard_plot import altair_plot
import hydralit_components as hc
st.set_page_config(layout='wide',
                   page_title='Urban Assessment Dashboard',
                   page_icon=":sunflower:",
                   initial_sidebar_state='collapsed')
st.title('Urban Assessment Dashboard')

option = st.selectbox(
    'Choose a city', (
        'Berlin',
        'Paris',
        'Athens',
        'Zürich',
        'Barcelona',
        'London',
        'Ljubljana'
    )
)
selection_dict = {
    'Berlin' : 'berlin',
    'Paris' : 'paris',
    'Athens' : 'athens',
    'Zürich' : 'zurich',
    'Barcelona' : 'barcelona',
    'London' : 'london',
    'Ljubljana':'ljubljana'
}
@st.cache_data
def get_data(option):
    url = 'https://raw.githubusercontent.com/zilikons/demeter/master/data/' + selection_dict[option] + '_with_features.json'
    data = gpd.read_file(url)
    return data
with hc.HyLoader('Loading data...',hc.Loaders.pacman):
    data = get_data(option)
col1, col2 = st.columns((2, 2))
col3 = st.columns((1,))




#path = 'https://raw.githubusercontent.com/zilikons/demeter/master/data/' + selection_dict[option] + '_with_features.json'


feature_list = list(FEATURE_COLUMN_NAMES.keys())
feature_list.remove('Land Use')
with col1:
    feature1= st.selectbox('Select the first feature',feature_list)

with col2:
    feature2= st.selectbox('Select the second feature',feature_list,index=5)

#with col3[0]:
    #fig = feature_histogram_side_by_side(data,feature1,feature2)
    #st.pyplot(fig)
if feature1 == feature2:
    with col3[0]:
        fig_ft1 = feature_histogram(data,feature1)
        st.pyplot(fig_ft1)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig2 = plot_correlation(data,FEATURE_COLUMN_NAMES[feature1])
        st.pyplot(fig2)
else:
    with col1:
        fig_ft1 = feature_histogram(data,feature1)
        st.pyplot(fig_ft1)
        st.set_option('deprecation.showPyplotGlobalUse', False)
    with col2:
        fig_ft2 = feature_histogram(data,feature2)
        st.pyplot(fig_ft2)
        st.set_option('deprecation.showPyplotGlobalUse', False)
    with col1:
        fig2 = plot_correlation(data,FEATURE_COLUMN_NAMES[feature1])
        st.pyplot(fig2)

    with col2:
        fig3 = plot_correlation(data,FEATURE_COLUMN_NAMES[feature2])
        st.pyplot(fig3)
with col3[0]:
    if feature1 != feature2:
        with st.expander('Land Use Distribution Scatterplot'):
            plot = altair_plot(data,feature1,feature2)
            st.altair_chart(plot,use_container_width=True)
