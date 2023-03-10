import streamlit as st
import plotly.express as px

import numpy as np
import pandas as pd

st.set_page_config(
    layout='wide'
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""# Feature Importance for Biodiversity
## Have a look at this
The plot below shows the importance of features for biodiversity""")

#df = pd.DataFrame({
#    'first column': list(range(1, 11)),
#    'second column': np.arange(10, 101, 10)
#})

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# # and used to select the displayed lines
# head_df = df.head(line_count)

# head_df


from modelv1 import get_model, load_model_from_pickle_file, get_feature_importance, plot_feature_importance, plot_from_model, plot_feature_importance_v2

model = load_model_from_pickle_file('../models/berlin_pipeline_trained.pkl')
feature_importance = get_feature_importance(model)

fig = px.bar(feature_importance.sort_values('importance', ascending=True), x='feature', y='importance',
                 hover_data=['feature', 'importance'], color='importance', color_continuous_scale=['blue', 'grey', 'green', 'green'],
                 labels={'importance':'Feature Importance'}, height=400)


fig.update_layout(
    plot_bgcolor='rgba(240,240,240,1)',
    paper_bgcolor='rgba(240,240,240,1)',
    font=dict(color='black')
)
#fig.show()
st.plotly_chart(fig,use_container_width=True, theme = 'streamlit')
#st.write(fig)
