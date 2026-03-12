import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

CSV_PATH = "/usr/local/airflow/include/customers_extract.csv"


def load_customers():

    print("Starting load into target database...")

    df = pd.read_csv(CSV_PATH)

    hook = PostgresHook(postgres_conn_id="postgres_target")

    engine = hook.get_sqlalchemy_engine()

    df.to_sql(
        "customers",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} records into target_db")