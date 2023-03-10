#If not already installed
#!pip install xgboost pandas scikit-learn matplotlib geopandas

import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


#In: df including X and y
#Out: Model(Pipleine) & Scores

def get_model(df):

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

    return pipeline, scores
