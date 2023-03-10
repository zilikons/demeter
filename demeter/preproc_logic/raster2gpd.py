import rasterio as rio
import rasterio.mask
import geopandas as gpd
from shapely import geometry
import numpy as np
import pandas as pd

def raster_cropping(path_to_raster,city_shape,exit_file_path,
                    crs_of_raster='ESRI:54009',crs_of_cityshape='epsg:4326') -> None:
    city_bounds = city_shape.total_bounds
    p1 = geometry.Point(city_bounds[2], city_bounds[1])
    p2 = geometry.Point(city_bounds[2], city_bounds[3])
    p3 = geometry.Point(city_bounds[0], city_bounds[3])
    p4 = geometry.Point(city_bounds[0], city_bounds[1])
    pointlist = [p1, p2, p3, p4]
    poly = geometry.Polygon([[p.x, p.y] for p in pointlist])
    poly = gpd.GeoDataFrame(crs=crs_of_cityshape, geometry=[poly]) #the crs of your points
    poly2 = poly.to_crs(crs_of_raster) #the crs of your raster file
    poly = poly.iloc[0]
    poly2 = poly2.iloc[0]
    poly = poly[0]
    poly2 = poly2[0]
    xx, yy = poly.exterior.coords.xy
    print(xx)
    print(yy)
    xx, yy = poly2.exterior.coords.xy
    print(xx)
    print(yy)
    p1 = geometry.Point(xx[0], yy[0])
    p2 = geometry.Point(xx[1], yy[1])
    p3 = geometry.Point(xx[2], yy[2])
    p4 = geometry.Point(xx[3], yy[3])
    pointlist = [p1, p2, p3, p4, p1]
    poly = geometry.Polygon([[p.x, p.y] for p in pointlist])
    polygons = [poly]
    with rio.open(path_to_raster) as src:
        out_image, out_transform = rasterio.mask.mask(src, polygons, crop = True)
    out_meta = src.meta
    out_meta.update({"driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform})
    with rio.open(exit_file_path, "w", **out_meta) as dest:
        dest.write(out_image)
    return None

def raster2gdf(raster_path):
    with rio.Env():
        with rio.open(raster_path) as src:
            crs = src.crs

            # create 1D coordinate arrays (coordinates of the pixel center)
            xmin, ymax = np.around(src.xy(0.00, 0.00), 9)  # src.xy(0, 0)
            xmax, ymin = np.around(src.xy(src.height-1, src.width-1), 9)  # src.xy(src.width-1, src.height-1)
            x = np.linspace(xmin, xmax, src.width)
            y = np.linspace(ymax, ymin, src.height)  # max -> min so coords are top -> bottom



            # create 2D arrays
            xs, ys = np.meshgrid(x, y)
            zs = src.read(1)

            # Apply NoData mask
            mask = src.read_masks(1) > 0
            xs, ys, zs = xs[mask], ys[mask], zs[mask]

    data = {"X": pd.Series(xs.ravel()),
            "Y": pd.Series(ys.ravel()),
            "Z": pd.Series(zs.ravel())}

    df = pd.DataFrame(data=data)
    geom = gpd.points_from_xy(df.X, df.Y)
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geom)

    return gdf

if __name__ == '__main__':
    berlin = gpd.read_file('../../raw_data/germany.json')
    berlin = berlin[berlin['NAME_3']=='Berlin']
    raster_path = '../../raw_data/raw_berlin/berlin_pop.tif'
    cropped_raster_path = '../../raw_data/raw_berlin/berlin_pop_proc.tif'
    raster_cropping(raster_path,berlin,cropped_raster_path)
    gdf = raster2gdf(cropped_raster_path)
    print(gdf.head(3))
