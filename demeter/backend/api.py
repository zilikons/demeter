from fastapi import FastAPI
import geopandas as gpd

app = FastAPI()

@app.get('/')
def index():
    return{'Welcome to my API!':True}

@app.get('/eu_cities')
def cities_data():
    data = gpd.read_file('../../raw_data/eu_cities.json')
    return data.to_json()

@app.get('/berlin_grid')
def berlin_grid_data():
    data = gpd.read_file('../../raw_data/berlin_grid_y.json')
    return data.to_json()

@app.get('/berlin_data')
def berlin_data():
    data = gpd.read_file('../../raw_data/berlin_urban_class.json')
    return data.to_json()
