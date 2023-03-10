import geopandas as gpd
from construct_grid import make_grid

def gpd2grid_features(gdf,city_shape,grid_size=1000,urban_classification_switch=False,feature_name=None) -> gpd.GeoDataFrame:
    city_grid = make_grid(city_shape,grid_size)

    if urban_classification_switch:
        veg = gdf.Z.copy()
        veg[(gdf.Z!=1) & (gdf.Z!=2) & (gdf.Z!=3)] = 0
        veg = veg.replace({1:1,2:2,3:3})
        gdf['veg'] = veg
        road = gdf.Z.copy()
        road[(gdf.Z!=5)] = 0
        road = road.replace({5:1})
        gdf['road'] = road
        water = gdf.Z.copy()
        water[(gdf.Z!=4)] = 0
        water=water.replace({4:1})
        gdf['water'] = water
        resi = gdf.Z.copy()
        resi[(gdf.Z!=11) & (gdf.Z!=12) & (gdf.Z!=13) & (gdf.Z!=14) & (gdf.Z!=15)] = 0
        resi = resi.replace({11:1,12:2,13:3,14:4,15:5})
        gdf['resi'] = resi
        non_resi = gdf.Z.copy()
        non_resi[(gdf.Z!=21) & (gdf.Z!=22) & (gdf.Z!=23) & (gdf.Z!=24) & (gdf.Z!=25)] = 0
        non_resi = non_resi.replace({21:1,22:2,23:3,24:4,25:5})
        gdf['non_resi'] = non_resi
        gdf = gdf.drop(gdf[gdf['Z']==255].index).reset_index(drop=True)
        gdf = gdf.drop(columns=['X','Y','Z']).to_crs(epsg=3035)
        gdf_proc = gpd.sjoin(gdf,city_grid,predicate='within')
        gdf_proc_grouped = gdf_proc.groupby('index_right').sum()
        gdf_final = city_grid.merge(gdf_proc_grouped,left_index=True,right_index=True)
        return gdf_final
    gdf_proc = gpd.sjoin(gdf.to_crs(epsg=3035),city_grid,predicate='within')
    gdf_proc_grouped = gdf_proc.groupby('index_right').sum()
    gdf_final = city_grid.merge(gdf_proc_grouped,left_index=True,right_index=True)
    gdf_final = gdf_final.drop(columns = ['X','Y'])
    if feature_name == None:
        feature_name = 'Z'
    gdf_final.columns = ['geometry',feature_name]
    return gdf_final
