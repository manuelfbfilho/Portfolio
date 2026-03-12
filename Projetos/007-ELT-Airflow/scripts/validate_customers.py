from airflow.providers.postgres.hooks.postgres import PostgresHook


def validate_customers():

    hook = PostgresHook(postgres_conn_id="postgres_target")

    result = hook.get_first("SELECT COUNT(*) FROM customers")

    total_records = result[0]

    print(f"Total records in target table: {total_records}")

    if total_records == 0:
        raise ValueError("Data quality check failed: table is empty")

    print("Data quality check passed")