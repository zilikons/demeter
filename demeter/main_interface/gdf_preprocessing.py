from construct_grid import *
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, Point


#Function that combines all the different steps from construct grid
def create_squares_and_join_data(city_gdf, landuse_gdf, other_features_gdf, cell_size):
    # Step 1: Create a grid of centroids within the city polygon
    polygon_meter = city_gdf.set_crs(epsg=4326, allow_override=True)
    polygon_meter = polygon_meter.to_crs(epsg=3035)
    centroids_gdf = create_centroids_gdf(polygon_meter, cell_size)

    # Step 2: Join the landuse feature with the city polygon
    landuse_joined = join_landuse_city(city_gdf, landuse_gdf)

    # Step 3: Match the input centroid point with the land use data
    landuse_centroid = join_landuse_centroid(centroids_gdf, landuse_joined)

    # Step 4: Convert the matched centroids back into squares
    squares_gdf = points_to_squares(landuse_centroid, cell_size)

    # Step 5: Join the squares with the other feature data
    joined_data = sjoin_nearest(other_features_gdf, squares_gdf)

    return joined_data
