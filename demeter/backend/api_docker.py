from fastapi import FastAPI
import geopandas as gpd

app = FastAPI()

@app.get('/')
def index():
    return{'Welcome to my Docker API!':True}

@app.get('/berlin_data_1')
def cities_data1():
    data = gpd.read_file('raw_data/berlin_with_features.json')
    half_index = int(data.shape[0]/2)
    return data.iloc[:half_index,:].to_json()

@app.get('/berlin_data_2')
def cities_data2():
    data = gpd.read_file('raw_data/berlin_with_features.json')
    half_index = int(data.shape[0]/2)
    return data.iloc[half_index:,:].to_json()
