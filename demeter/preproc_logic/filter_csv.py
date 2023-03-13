import geopandas as gpd
import pandas as pd
import numpy as np

def try_float(val):
    try:
        return np.float32(val)
    except ValueError:
        print(f'value error! {val}')
        return np.nan
def filter_csv(csv_path, bbox):
    """
    Filter the CSV file to include only the rows that are within the specified bounding box
    and save the result as a GeoJSON file.

    Parameters
    ----------
    csv_path : str
        The path to the CSV file.
    bbox : tuple
        A tuple of four float values representing the bounding box coordinates in the following order:
        (minimum longitude, minimum latitude, maximum longitude, maximum latitude)

    Returns
    -------
    gdf : GeoPandas GeoDataFrame
        The GeoPandas GeoDataFrame containing the filtered points.
    """
    # Read the CSV file into a Dask dataframe
    chunksize=1000000
    reader = pd.read_csv(csv_path,sep='\t',header=0, usecols=['decimalLongitude','decimalLatitude'],
                      converters={'decimalLongitude':try_float,'decimalLatitude':try_float},
                      on_bad_lines='skip',chunksize=chunksize)
    filtered_dfs = []
    for chunk in reader:
        bbox_mask = (chunk['decimalLongitude'] >= bbox[0]) & (chunk['decimalLatitude'] >= bbox[1]) & (chunk['decimalLongitude'] <= bbox[2]) & (chunk['decimalLatitude'] <= bbox[3])
        filtered_chunk = chunk[bbox_mask]
        filtered_dfs.append(filtered_chunk)

    filtered_df = pd.concat(filtered_dfs, ignore_index=True)

    # Filter the dataframe to include only the rows that are within the specified bounding box



    return filtered_df
