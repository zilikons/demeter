# Imports
import geopandas as gpd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt

#In: df including X and y
#Out: Model(Pipleine)

def get_model(df, score = False, save = False):

    # X, y separation
    X = df[['veg', 'roads', 'water', 'height_resid', 'height_nonresid', 'land_use_code', 'land_use_area', 'population']]
    y = df['log_y']

    # Define the columns to scale
    num_cols = ['veg', 'roads', 'water', 'height_resid', 'height_nonresid', 'land_use_area', 'population']

    # Define the columns to one-hot encode
    cat_cols = ['land_use_code']

    # Create the column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(), cat_cols)
        ])

    # Create the pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('xg_reg', xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                                    max_depth=7, alpha=10, n_estimators=200))
    ])

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = pipeline.predict(X_test)

    # Compute the mean squared error and R-squared of the predictions
    scores = {}

    mse = mean_squared_error(y_test, y_pred)
    scores['mse'] = mse

    r2 = r2_score(y_test, y_pred)
    scores['r2'] = r2

    if score == False:
        if save == False:
            return pipeline
        else:
            with open('../models/my_pipe.pkl', 'wb') as file:
                pickle.dump(pipeline, file)
            return pipeline
    else:
        if save == False:
            return pipeline, scores
        else:
            with open('../models/my_pipe.pkl', 'wb') as file:
                pickle.dump(pipeline, file)
            return pipeline, scores


def load_model_from_pickle_file(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def get_feature_importance(pipe):
    model = pipe.named_steps['xg_reg']
    results = pd.DataFrame([])
    results['feature'] = pipe.named_steps['preprocessor'].get_feature_names_out()
    results['importance'] = model.feature_importances_

    replacement_dict = {
        'cat__land_use_code_11100' : 'Continuous Urban Fabric (S.L. > 80%)',
        'cat__land_use_code_11210': 'Discontinuous Dense Urban Fabric (S.L. : 50% - 80%)',
        'cat__land_use_code_11220': 'Discontinuous Medium Density Urban Fabric (S.L. : 30% - 50%)',
        'cat__land_use_code_11230': 'Discontinuous Low Density Urban Fabric (S.L. : 10% - 30%)',
        'cat__land_use_code_11240': 'Discontinuous Very Low Density Urban Fabric (S.L. < 10%)',
        'cat__land_use_code_11300': 'Isolated Structures',
        'cat__land_use_code_12100': 'Industrial, commercial, public, military and private units',
        'cat__land_use_code_12210': 'Fast transit roads and associated land',
        'cat__land_use_code_12220': 'Other roads and associated land',
        'cat__land_use_code_12230': 'Railways and associated land',
        'cat__land_use_code_12300': 'Port areas',
        'cat__land_use_code_12400': 'Airports',
        'cat__land_use_code_13100': 'Mineral extraction and dump sites',
        'cat__land_use_code_13300': 'Construction sites',
        'cat__land_use_code_13400': 'Land without current use',
        'cat__land_use_code_14100': 'Green urban areas',
        'cat__land_use_code_14200': 'Sports and leisure facilities',
        'cat__land_use_code_21000': 'Arable land (annual crops)',
        'cat__land_use_code_22000': 'Permanent crops (vineyards, fruit trees, olive groves)',
        'cat__land_use_code_23000': 'Pastures',
        'cat__land_use_code_24000': 'Complex and mixed cultivation patterns',
        'cat__land_use_code_25000': 'Orchards at the fringe of urban classes',
        'cat__land_use_code_31000': 'Forests',
        'cat__land_use_code_32000': 'Herbaceous vegetation associations (natural grassland, moors...)',
        'cat__land_use_code_33000': 'Open spaces with little or no vegetations (beaches, dunes, bare rocks, glaciers)',
        'cat__land_use_code_40000': 'Wetland',
        'cat__land_use_code_50000': 'Water bodies',
        'num__veg' : 'Vegetation Intensity',
        'num__roads' : 'Road density',
        'num__water' : 'Water',
        'num__height_resid' : 'Residential Density',
        'num__height_nonresid' : 'Non-Residential Density',
        'num__land_use_area' : 'Land Use Area',
        'num__population': 'Population'
    }
    results['feature'] = results['feature'].replace(replacement_dict)
    return results


def plot_feature_importance(feature_importance):

    df = feature_importance.sort_values('importance', ascending=False)

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(12,8))
    ax.barh(df['feature'], df['importance'], color='lightblue')
    ax.set_xticks([])
    ax.tick_params(axis='y', labelsize=12)
    ax.set_xlabel('Feature Importance', fontsize=14)
    ax.set_title('XGBoost Feature Importance', fontsize=16)

    # Move the feature labels to the right side of the bars
    for i, v in enumerate(df['importance']):
        ax.text(v + 0.001, i, str(round(v, 4)), color='black', fontsize=12, va='center')

    plt.show()

def plot_from_model(pipe):
    plot_feature_importance(get_feature_importance(pipe))
