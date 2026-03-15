from sqlalchemy import create_engine
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_customers():

    print("Starting load into target database...")

    file_path = "/usr/local/airflow/include/customers.csv"

    df = pd.read_csv(file_path)

    postgres_hook = PostgresHook(postgres_conn_id="postgres_target")

    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # recriar tabela
    cursor.execute("DROP TABLE IF EXISTS customers")

    # criar estrutura baseada no dataframe
    columns = ", ".join([f"{col} TEXT" for col in df.columns])

    create_table_query = f"""
    CREATE TABLE customers (
        {columns}
    )
    """

    cursor.execute(create_table_query)

    # inserir dados
    for _, row in df.iterrows():

        values = "', '".join([str(v).replace("'", "") for v in row.values])

        insert_query = f"""
        INSERT INTO customers VALUES ('{values}')
        """

        cursor.execute(insert_query)

    conn.commit()

    cursor.close()
    conn.close()

    print("Load completed successfully")