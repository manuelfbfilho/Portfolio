import pandas as pd
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook

CSV_PATH = "/usr/local/airflow/include/customers_extract.csv"


def extract_customers():

    logging.info("Connecting to source database")

    hook = PostgresHook(postgres_conn_id="postgres_source")

    query = "SELECT * FROM customers"

    df = hook.get_pandas_df(query)

    logging.info(f"Extracted {len(df)} records")

    df.to_csv(CSV_PATH, index=False)

    logging.info(f"File saved at {CSV_PATH}")