# Demeter: Urban Assessment Platform

## Link to the platform

[Demeter on Streamlit](https://zilikons-demeter-home-page-noxs3y.streamlit.app/)

## Collaborators
[Anamaria Lukacs](https://github.com/nusero92)\
\
[Basile Morel](https://github.com/Basile-73)\
\
[Konstantinos Ziliaskopoulos](https://github.com/zilikons)\
\
[Nico Hieke](https://github.com/sathustra)

## Description

Demeter is an urban assessment platform, focused on urban biodiversity, using exclusively remote sensing and satellite data for assessing, visualizing and modeling different urban features and their impact on biodiversity.

Our goal was to create a simple yet informative platform that could easily communicate satellite data to stakeholders, while simultaneously creating the pipelines to bring together different satellite and remote sensing data sources into a unified dataframe format.

## Data Sources

For the land use data, we used the [Urban Atlas 2018 Land Use data](https://land.copernicus.eu/local/urban-atlas/urban-atlas-2018) from Copernicus. Data format was in vector form (.gpkg).

For the population and urban classification data, we used the [Global Human Settlement Layer 2020 Data](https://ghsl.jrc.ec.europa.eu/download.php?ds=pop), with a 100m and 10m resolution respectively. Data format was in raster form (.tif).

For the city shapefiles, we used the [GADM Global Country Dataset](https://gadm.org/index.html). Data format was in GeoJSON (.json).

For the biodiversity data, we used the [GBIF occurences dataset](https://www.gbif.org/occurrence/search), filtered for observations with a coordinate uncertainty below 500m and after the year 2010, filtered for each city shape polygon. Data format was in tab delimited values format (.tsv).

## Data

All processed data is available in the /data folder, with files ending in 'with_features' being high resolution and files ending in '1k' being low resolution. All data is available as newline delimited geojson files (.json).
