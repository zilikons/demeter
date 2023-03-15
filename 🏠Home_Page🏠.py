import streamlit as st

st.set_page_config(page_title='DEMETER: Urban Assessment Platform',
                   page_icon=":sunflower:",
                   initial_sidebar_state='expanded')

st.title('DEMETER')
st.markdown('''
            ## Urban Assessment Platform
            Check the sidebar for our different views!
            ''')
with st.expander('Link to our data'):
    st.markdown('''Find all our processed data (in low and high resolution options) [here!](https://github.com/zilikons/demeter/tree/master/data)
                ''')
with st.expander('Link to our github repository'):
    st.markdown('''Check out all our processing pipelines and code in our [demeter github repo!](https://github.com/zilikons/demeter)
                ''')
with st.expander('Our collaborators!'):
    st.markdown('''[Anamaria Lukacs](https://github.com/nusero92)\
\
                [Basile Morel](https://github.com/Basile-73)\
\
                [Konstantinos Ziliaskopoulos](https://github.com/zilikons)\
\
                [Nico Hieke](https://github.com/sathustra)

                ''')
