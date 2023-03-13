import streamlit as st

st.set_page_config(page_title='DEMETER: Urban Assessment Platform',
                   menu_items={
                       'About': '#Hi',

                   },
                   initial_sidebar_state='expanded')
st.title('DEMETER')
st.markdown('''
            ## Urban Assessment Platform
            Check the sidebar for our options!
            ''')
