import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

def get_ua_on_square(polygon, urban_atlas):
    polygon_gdf = gpd.GeoDataFrame(geometry=[polygon])
    polygon_gdf.crs = 'epsg:3035'

    overlap_gdf = gpd.sjoin(urban_atlas, polygon_gdf,  predicate = 'intersects')

    if overlap_gdf.shape[0] == 0:
        print('No overlap in get_ua_on_square')
        return 0
    elif overlap_gdf.shape[0] == 1:
        return int(overlap_gdf.iloc[0]['code_2018'])
    else:
        return int(overlap_gdf.iloc[0]['code_2018']) # This part lacks accuracy



def get_urban_atlas(polygon, grid, urban_atlas):

    crs = 'epsg:3035'
    assert grid.crs == crs, f'CRS mismatch: expected {crs}, got {grid.crs}'
    assert urban_atlas.crs == crs, f'CRS mismatch: expected {crs}, got {urban_atlas.crs}'
    assert isinstance(grid, gpd.GeoDataFrame), f'Expected GeoDataFrame, got {type(grid)}'
    assert isinstance(urban_atlas, gpd.GeoDataFrame), f'Expected GeoDataFrame, got {type(urban_atlas)}'

    grid['urban_atlas'] = grid.apply(lambda row: get_ua_on_square(row['geometry'], urban_atlas), axis=1)

    return grid
