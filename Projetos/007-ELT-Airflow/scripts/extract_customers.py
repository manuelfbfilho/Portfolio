import pandas as pd
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook

output_path = "/usr/local/airflow/include/customers.csv"


def extract_customers():

    logging.info("Connecting to source database")

    hook = PostgresHook(postgres_conn_id="postgres_source")

    query = "SELECT * FROM customers"

    df = hook.get_pandas_df(query)

    logging.info(f"Extracted {len(df)} records")

    df.to_csv(output_path, index=False)

    logging.info(f"File saved at {output_path}")