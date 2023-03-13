from demeter.preproc_logic.raster2gpd import raster_cropping, raster2gdf
from demeter.preproc_logic.gpd2grid_features import gpd2grid_features
from construct_grid import make_grid
from assign_y import assign_y
import geopandas as gpd
import pandas as pd

def raster2features(city_shapefile:gpd.GeoDataFrame,
                    city_y:gpd.GeoDataFrame,
                    built_tif_path:str,
                    pop_tif_path:str,
                    grid_size=100):
    city_name = city_shapefile['city_name'].values[0]
    city_grid = make_grid(city_shapefile,grid_size)
    city_y = city_y.to_crs(epsg=3035)
    city_grid_y = assign_y(city_grid,city_y)
    raster_cropping(built_tif_path,city_shapefile,f'../raw_data/cropped_tifs/{str(city_name).lower()}_class_proc.tif')
    raster_cropping(pop_tif_path,city_shapefile,f'../raw_data/cropped_tifs/{str(city_name).lower()}_pop_proc.tif')
    city_class = raster2gdf(f'../raw_data/cropped_tifs/{str(city_name).lower()}_class_proc.tif')
    city_pop = raster2gdf(f'../raw_data/cropped_tifs/{str(city_name).lower()}_pop_proc.tif')
    city_feat = gpd2grid_features(city_class,city_shapefile,grid_size=grid_size,urban_classification_switch=True)
    city_more_feat = gpd.sjoin(city_pop.to_crs(epsg=3035),city_feat,predicate='within').groupby('index_right').sum()
    cmf = city_more_feat.drop(columns=['X','Y']).rename(columns={'Z':'pop'})
    cff = pd.merge(city_grid,cmf,left_index=True,right_index=True)
    return cff
