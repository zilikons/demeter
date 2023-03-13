import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, Point

def create_square_polygon(size, centroid):
    half_size = size / 2
    x = centroid.x
    y = centroid.y
    points = [
        (x - half_size, y - half_size),
        (x + half_size, y - half_size),
        (x + half_size, y + half_size),
        (x - half_size, y + half_size)
    ]
    return Polygon(points)

def make_grid (polygon, cell_size):

    polygon_meter = polygon.set_crs(epsg=4326)  # Set the current CRS to WGS84
    polygon_meter = polygon.to_crs(epsg=3035)  # Convert to the desired CRS (UTM zone 33N)
    min_x, min_y, max_x, max_y = polygon_meter.bounds.values[0] #Retrieve extremes

    num_cols = int((max_x - min_x) / cell_size)
    num_rows = int((max_y - min_y) / cell_size)

    polygons = []
    for i in range(num_rows):
        for j in range(num_cols):
            x = min_x + j * cell_size + cell_size / 2
            y = min_y + i * cell_size + cell_size / 2
            centroid = Point(x, y)
            square = create_square_polygon(cell_size, centroid)
            polygons.append(square)

    grid = gpd.GeoDataFrame(geometry=polygons, crs='epsg:3035')
    grid_cut = gpd.sjoin(grid, polygon_meter)
    return grid_cut[['geometry']].reset_index(drop=True)


#outputs a tuple with squared grid polygons, and respective centroids
def make_grid_centroid(polygon, cell_size):
    polygon_meter = polygon.set_crs(epsg=4326, allow_override=True)  # Set the current CRS to WGS84
    polygon_meter = polygon.to_crs(epsg=3035)  # Convert to the desired CRS (UTM zone 33N)
    min_x, min_y, max_x, max_y = polygon_meter.bounds.values[0] #Retrieve extremes

    num_cols = int((max_x - min_x) / cell_size)
    num_rows = int((max_y - min_y) / cell_size)

    polygons = []
    centroids = []
    for i in range(num_rows):
        for j in range(num_cols):
            x = min_x + j * cell_size + cell_size / 2
            y = min_y + i * cell_size + cell_size / 2
            centroid = Point(x, y)
            centroids.append((centroid.x, centroid.y))
            square = create_square_polygon(cell_size, centroid)
            polygons.append(square)

    grid = gpd.GeoDataFrame(geometry=polygons, crs='epsg:3035')
    grid_cut = gpd.sjoin(grid, polygon_meter)
    return grid_cut[['geometry']].reset_index(drop=True), centroids

#First step in the Workflow: Create a centroid from the polygons in the given dataframe
def create_centroids_gdf(polygon, cell_size):
    # Create a grid of square polygons within the input polygon
    grid_cut_centroids = make_grid_centroid(polygon, cell_size)

    # Get the list of centroids from the output of make_grid_centroid()
    centroids = grid_cut_centroids[1]
    print(centroids)
    # Convert the list of centroids to a list of shapely Point objects
    points = [Point(x, y) for x, y in centroids]

    # Create a GeoDataFrame from the points
    centroids_gdf = gpd.GeoDataFrame({'geometry': points})

    # Set the CRS to epsg=3035
    centroids_gdf = centroids_gdf.set_crs(epsg=3035)

    return centroids_gdf

#Second step, join the city GDF and landuse GDF to yield the city area
def join_landuse_city(city_gdf, landuse_gdf):
    # Join the landuse feature with the city polygon
    landuse_joined = gpd.sjoin(landuse_gdf, city_gdf.to_crs(epsg=3035), predicate='within')

    if 'fua_name' in landuse_joined.columns:
        landuse_joined.drop(columns=['fua_name'], inplace=True)

    if 'fua_code' in landuse_joined.columns:
        landuse_joined.drop(columns=['fua_code'], inplace=True)

    if 'prod_date' in landuse_joined.columns:
        landuse_joined.drop(columns=['prod_date'], inplace=True)

    if 'perimeter' in landuse_joined.columns:
        landuse_joined.drop(columns=['perimeter'], inplace=True)

    if 'comment' in landuse_joined.columns:
        landuse_joined.drop(columns=['comment'], inplace=True)

    if 'index_right' in landuse_joined.columns:
        landuse_joined.drop(columns=['index_right'], inplace=True)

    if 'Pop2018' in landuse_joined.columns:
        landuse_joined.drop(columns=['Pop2018'], inplace=True)

        return landuse_joined

#Third step, join the centroids_gdf and the landuse_joined gdf from step 1 and 2
def join_landuse_centroid(centroid_gdf, landuse_gdf):
    # Match the input centroid point with the land use data
    landuse_centroid = gpd.sjoin(centroid_gdf, landuse_gdf, lsuffix='_left', rsuffix='_right')

    return landuse_centroid


#Fourth step, convert those centroids back into polygons
def points_to_squares(gdf, cell_size):
    polygons = []
    for point in gdf.geometry:
        x, y = point.x, point.y
        half_side = cell_size / 2
        square = Polygon([(x - half_side, y - half_side),
                          (x - half_side, y + half_side),
                          (x + half_side, y + half_side),
                          (x + half_side, y - half_side)])
        polygons.append(square)
    return gpd.GeoDataFrame(gdf.drop('geometry', axis=1), geometry=polygons, crs=gdf.crs)


#Fifth, join the squares (joined with land use) with the other features gdf
def sjoin_nearest(data, squares):
    data = data.to_crs(epsg=3035)
    squares = squares.to_crs(epsg=3035)
    joined_data = gpd.sjoin_nearest(data, squares, how='left')
    joined_data = joined_data.drop_duplicates(subset='geometry').reset_index(drop=True)
    joined_data = joined_data.drop(columns='index_right')

    columns_to_drop = ['index_right', 'country_left', 'class_2018', 'identifier', 'city_name', 'country_right']
    for column in columns_to_drop:
        if column in joined_data.columns:
            joined_data.drop(columns=[column], inplace=True)

    return joined_data



if __name__ == '__main__':
    df = gpd.read_file('../raw_data/gadm41_DEU_3.json')
    polygon_2 = gpd.GeoDataFrame(df[df['NAME_3']=='Dresden']['geometry'])
    my_grid = make_grid(polygon_2, 102)
    print(my_grid.head(2))
