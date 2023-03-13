import streamlit as st
import plotly.express as px

import numpy as np
import pandas as pd
import pickle

st.set_page_config(
    layout='wide',
    page_title='Model Feature Importance',
    initial_sidebar_state='collapsed'
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""# Feature Importance for Biodiversity
## How to Make a Difference
In order to efficiently process the data volumes of up to 500,000 data points per city with 32 individual features, we opted for an XGBoost model.
In XGBoost (eXtreme Gradient Boosting), feature importance (plottet below) is a metric that measures the relevance of each feature in predicting the target variable. It indicates how useful or valuable each feature is in making predictions. The importance is calculated by the model during training and can be accessed after the model has been fitted. We display the ten most important features below.""")

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

model = load_model_from_pickle_file('models/berlin_pipeline_trained.pkl')
feature_importance = get_feature_importance(model)

df_top10 = feature_importance.sort_values('importance', ascending=False).iloc[:10]

# round to 4 digits not working:
df_top10['importance'] = df_top10['importance'].round(4)

fig = px.bar(df_top10, x='feature', y='importance',
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

with st.expander("See all features and importance"):
    st.write("""
        The features are sorted by importance in descending order.
    """)
    st.write(feature_importance.sort_values('importance', ascending=False))
    #st.image("https://static.streamlit.io/examples/dice.jpg")

with st.expander("See model explanation"):
    st.write("""
        XGBoost is a popular and efficient open-source implementation of the gradient boosted trees algorithm. Gradient boosting is a supervised learning algorithm, which attempts to accurately predict a target variable by combining the estimates of a set of simpler, weaker models.
        When using gradient boosting for regression, the weak learners are regression trees, and each regression tree maps an input data point to one of its leafs that contains a continuous score. XGBoost minimizes a regularized (L1 and L2) objective function that combines a convex loss function (based on the difference between the predicted and target outputs) and a penalty term for model complexity (in other words, the regression tree functions). The training proceeds iteratively, adding new trees that predict the residuals or errors of prior trees that are then combined with previous trees to make the final prediction. It's called gradient boosting because it uses a gradient descent algorithm to minimize the loss when adding new models.
        Below is a brief illustration on how gradient tree boosting works.
    """)
    st.image("https://docs.aws.amazon.com/images/sagemaker/latest/dg/images/xgboost_illustration.png")
    st.write("Source [link](https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost-HowItWorks.html)")


with st.expander("See balloons"):
    if st.button("Press this button"):
        st.balloons()
