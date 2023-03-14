import altair as alt
from params import *

def altair_plot(data,feature1,feature2):
    column_names={
    'veg':'Vegetation Intensity',
    'road':'Road Density',
    'water':'Water',
    'resi':'Residential Density',
    'non_resi':'Non-Residential Density',
    'land_use_code':'Land Use',
    'code_2018':'Land Use',
    'pop':'Population',
    'log_y':'Biodiversity'
    }
    data1 = data.copy()
    if data1.shape[0] > 5000:
        data1 = data1.sample(5000)
    if 'land_use_code' in list(data1.columns):
        data1 = data1.rename(columns={'land_use_code':'code_2018'})
    data1 = data1.drop(columns='geometry')
    data1 = data1.rename(columns=column_names)
    data1['Land Use'] = data1['Land Use'].copy().astype(int).map(URBAN_ATLAS_LAND_USE)
    brush = alt.selection(type='interval')
    points = alt.Chart(data1).mark_point().encode(
        x=feature1,
        y=feature2,
        color = alt.condition(brush, 'Land Use', alt.value('lightgray'))
    ).add_selection(
        brush
    )
    bars = alt.Chart(data1).mark_bar().encode(
        y = 'Land Use',
        color = 'Land Use',
        x = 'count(Land Use)'
    ).transform_filter(
        brush
    )
    return points & bars
