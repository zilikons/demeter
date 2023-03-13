
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


def count_points(polygon, y_meter_data):

    #write Square to GeoDataFrame
    polygon_gs = gpd.GeoSeries([polygon])
    polygon_gpd = gpd.GeoDataFrame(geometry = polygon_gs)

    #To avoid error message, assert in assign_y makes sure this is true
    polygon_gpd.crs = 'epsg:3035'
    y_meter_data.crs = 'epsg:3035'

    # Perform a spatial join to get the points inside the polygon
    gdf_join = gpd.sjoin(y_meter_data, polygon_gpd)

    # Count the number of points inside the polygon
    return len(gdf_join)

def assign_y(grid, y_meter_data):

    # Check Inputs
    crs = 'epsg:3035'
    assert grid.crs == crs, f'CRS mismatch: expected {crs}, got {grid.crs}'
    assert y_meter_data.crs == crs, f'CRS mismatch: expected {crs}, got {y_meter_data.crs}'
    assert isinstance(grid, gpd.GeoDataFrame), f'Expected GeoDataFrame, got {type(grid)}'
    assert isinstance(y_meter_data, gpd.GeoDataFrame), f'Expected GeoDataFrame, got {type(y_meter_data)}'

    grid['y'] = grid.apply(lambda row: count_points(row['geometry'], y_meter_data), axis=1)

    return grid
