import streamlit as st

st.set_page_config(page_title='DEMETER: Urban Assessment Platform',
                   menu_items={
                       'About': '#Hi',

                   },

                   initial_sidebar_state='expanded')
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Spectral:wght@300&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
st.title('DEMETER')
st.markdown('''
            ## Urban Assessment Platform
            Check the sidebar for our options!
            ''')
