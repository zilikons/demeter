import streamlit as st
from pages import map_display
from PIL import Image

PAGES = {
    "Map Display Page": map_display,
}
st.title('DEMETER')
st.markdown('''
            ## Urban Assessment Dashboard
            Check the sidebar for our options!
            ''')
