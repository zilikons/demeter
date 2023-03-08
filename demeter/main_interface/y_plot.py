import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def make_plotly_plot(filepath_to_grid_y,shapefile_gdf,city_name,colorscale='tealgrn'):
    url = "https://github.com/eurostat/Nuts2json/raw/master/2021/4326/20M/nutsrg_3.json"
    european_countries = gpd.read_file(url)
    gridded_y = gpd.read_file(filepath_to_grid_y)
    gridded_y_json = gridded_y.geometry.__geo_interface__
    shapefile_gdf = shapefile_gdf[shapefile_gdf['city_name']==city_name]
    location_name = shapefile_gdf['city_name']
    location_lat = shapefile_gdf['geometry'].centroid.y.values[0]
    location_lon = shapefile_gdf['geometry'].centroid.x.values[0]
    location_point = Point(location_lon, location_lat)
    location_country = european_countries[european_countries.contains(location_point)].iloc[0]
    location_data = pd.DataFrame({"Name": [location_name], "Latitude": [location_lat], "Longitude": [location_lon]})
    location_data['Name'] = location_data['Name'].astype(str)

    fig = px.choropleth_mapbox(location_data, geojson=location_country.geometry.__geo_interface__, color="Name",
    locations='Name', featureidkey="properties.NUTS_ID",
    mapbox_style="carto-positron", zoom=10, center={"lat": location_lat, "lon": location_lon},
    opacity=0.8, labels={'Name': 'Location'})
    trace = go.Choroplethmapbox(
        geojson=gridded_y_json,
        locations=gridded_y.index,
        z=np.round(gridded_y['num_points_inside'],2),
        colorscale=colorscale,
        marker_opacity=0.5,
        marker_line_width=0,
        name='Biodiversity',
        hovertemplate = 'Biodiversity Score: %{z}',
        hoverlabel= {'namelength':0}
    )

    fig.add_trace(trace)
    fig.update_layout(
        showlegend = False
    )
    return fig
