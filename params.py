import os

PROJECT_ID=os.getenv('PROJECT_ID')
BASIC_TABLE=os.getenv('BASIC_TABLE')
DATASET_ID=os.getenv('DATASET_ID')
DOCKER_URL=os.getenv('DOCKER_URL')
URBAN_ATLAS_LAND_USE={
    11100: 'Continuous Urban Fabric (S.L. > 80%)',
    11210: 'Discontinuous Dense Urban Fabric (S.L. : 50% - 80%)',
    11220: 'Discontinuous Medium Density Urban Fabric (S.L. : 30% - 50%)',
    11230: 'Discontinuous Low Density Urban Fabric (S.L. : 10% - 30%)',
    11240: 'Discontinuous Very Low Density Urban Fabric (S.L. < 10%)',
    11300: 'Isolated Structures',
    12100: 'Industrial, commercial, public, military and private units',
    12210: 'Fast transit roads and associated land',
    12220: 'Other roads and associated land',
    12230: 'Railways and associated land',
    12300: 'Port areas',
    12400: 'Airports',
    13100: 'Mineral extraction and dump sites',
    13300: 'Construction sites',
    13400: 'Land without current use',
    14100: 'Green urban areas',
    14200: 'Sports and leisure facilities',
    21000: 'Arable land (annual crops)',
    22000: 'Permanent crops (vineyards, fruit trees, olive groves)',
    23000: 'Pastures',
    24000: 'Complex and mixed cultivation patterns',
    25000: 'Orchards at the fringe of urban classes',
    31000: 'Forests',
    32000: 'Herbaceous vegetation associations (natural grassland, moors...)',
    33000: 'Open spaces with little or no vegetations (beaches, dunes, bare rocks, glaciers)',
    40000: 'Wetland',
    50000: 'Water bodies'
}
FEATURE_COLUMN_NAMES={
    'Vegetation Intensity':'veg',
    'Road density':'roads',
    'Water':'water',
    'Residential Density':'height_resid',
    'Non-Residential Density':'height_nonresid',
    'Land Use':'land_use_code',
    'Population':'population',
    'Biodiversity':'log_y'
}
