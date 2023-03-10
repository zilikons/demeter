import geopandas as gpd
from params import *
from shapely.geometry import Point
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def get_plotly_data(city_name):
    euro_url = "https://github.com/eurostat/Nuts2json/raw/master/2021/4326/20M/nutsrg_3.json"
    grid_url = "https://raw.githubusercontent.com/zilikons/demeter/master/data/berlin_1k.json"
    european_countries = gpd.read_file(euro_url)
    gridded_y = gpd.read_file(grid_url).to_crs(epsg=4326)
    gridded_y_json = gridded_y.geometry.__geo_interface__
    location_name = city_name
    location_lat = gridded_y.dissolve().centroid.y.values[0]
    location_lon = gridded_y.dissolve().centroid.x.values[0]
    #print(location_lat,location_lon)
    location_point = Point(location_lon, location_lat)
    location_country = european_countries[european_countries.contains(location_point)].reset_index(drop=True).iloc[0]
    location_data = pd.DataFrame({"Name": [location_name], "Latitude": [location_lat], "Longitude": [location_lon]})
    location_data['Name'] = location_data['Name'].astype(str)
    return [location_data, location_country, location_lat, location_lon, gridded_y_json, gridded_y]

def make_plotly_plot(location_datas,feature):
    colorbar_dict = {'Vegetation Intensity': 'Greens_r',
                 'Road Density': 'OrRd',
                 'Water': 'Blues_r',
                 'Residential Density': 'PuRd',
                 'Non-Residential Density': 'YlOrBr',
                 'Population': 'magma',
                 'Biodiversity': 'PRGn'}
    location_data, location_country, location_lat, location_lon, gridded_y_json, gridded_y = location_datas
    gridded_y['y'] = np.log1p(gridded_y['y'])
    fig = px.choropleth_mapbox(location_data, geojson=location_country.geometry.__geo_interface__, color="Name",
    locations='Name', featureidkey="properties.NUTS_ID",
    mapbox_style="carto-positron", zoom=8, center={"lat": location_lat, "lon": location_lon},
    opacity=0.8, labels={'Name': 'Location'})
    trace = go.Choroplethmapbox(
        geojson=gridded_y_json,
        locations=gridded_y.index,
        z=np.round(gridded_y[FEATURE_COLUMN_NAMES[feature]],2),
        colorscale=colorbar_dict[feature],
        marker_opacity=0.7,
        marker_line_width=0,
        name=feature,
        hovertemplate = feature+' Score: %{z}',
        hoverlabel= {'namelength':0}
    )

    fig.add_trace(trace)
    fig.update_layout(
        showlegend = False
    )
    return fig
