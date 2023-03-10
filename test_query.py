from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from params import *

query = f"""
    SELECT veg
    FROM {PROJECT_ID}.{DATASET_ID}.{BASIC_TABLE}
    LIMIT 100
    """

client = bigquery.Client()
query_job = client.query(query)
result = query_job.result()
gdf = result.to_dataframe()
print(gdf)
