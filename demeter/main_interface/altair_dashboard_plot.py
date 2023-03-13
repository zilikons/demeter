import altair as alt
from params import *

def altair_plot(data,feature1,feature2):
    data['code_2018'] = data['code_2018'].copy().astype(int).map(URBAN_ATLAS_LAND_USE)
    brush = alt.selection(type='interval')
    points = alt.Chart(data).mark_point().encode(
        x=FEATURE_COLUMN_NAMES[feature1],
        y=FEATURE_COLUMN_NAMES[feature2],
        color = alt.condition(brush, 'code_2018', alt.value('lightgray'))
    ).add_selection(
        brush
    )
    bars = alt.Chart(data).mark_bar().encode(
        y = 'code_2018',
        color = 'code_2018',
        x = 'count(code_2018)'
    ).transform_filter(
        brush
    )
    return points & bars
