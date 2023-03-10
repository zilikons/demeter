import geopandas as gpd
from construct_grid import make_grid

def gpd2grid_features(gdf,city_shape,grid_size=1000,urban_classification_switch=False,feature_name=None) -> gpd.GeoDataFrame:
    city_grid = make_grid(city_shape,grid_size)
    gdf = gpd.sjoin(city_grid,gdf,predicate='intersects').drop(columns='index_right')
    if urban_classification_switch:
        veg = gdf.apply(lambda x: 1 if x['Z']==1 else 2 if x['Z']==2 else 3 if x['Z']==3 else 0, axis=1)
        road = gdf.apply(lambda x: 1 if x['Z']==5 else 0, axis=1)
        water=gdf.apply(lambda x: 1 if x['Z']==4 else 0, axis=1)
        resi = gdf.apply(lambda x: 1 if x['Z']==11 else 2 if x['Z']==12 else 3 if x['Z']==13 else 4 if x['Z']==14 else 5 if x['Z']==15 else 0, axis=1)
        non_resi = gdf.apply(lambda x: 1 if x['Z']==21 else 2 if x['Z']==22 else 3 if x['Z']==23 else 4 if x['Z']==24 else 5 if x['Z']==25 else 0, axis=1)
        gdf = gdf.drop(gdf[gdf['Z']==255].index)
        gdf_proc = gpd.GeoDataFrame(list(zip(veg,road,water,resi,non_resi,gdf.geometry)),geometry=gdf.geometry,crs='ESRI:54009',
                                    columns = ['veg','road','water','resi','non_resi','geometry'])
        gdf_proc.columns = ['veg','road','water','resi','non_resi','geometry']
        return gdf_proc
    gdf = gdf.drop(columns = ['X','Y'])
    if feature_name == None:
        feature_name = 'Z'
    gdf.columns = [feature_name,'geometry']
    return gdf
