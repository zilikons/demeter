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

if __name__ == '__main__':
    df = gpd.read_file('../raw_data/gadm41_DEU_3.json')
    polygon_2 = gpd.GeoDataFrame(df[df['NAME_3']=='Dresden']['geometry'])
    my_grid = make_grid(polygon_2, 102)
    print(my_grid.head(2))
