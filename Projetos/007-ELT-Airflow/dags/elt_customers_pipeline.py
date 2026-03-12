from airflow.decorators import dag, task
from datetime import datetime, timedelta
import logging

from scripts.extract_customers import extract_customers
from scripts.load_customers import load_customers
from scripts.validate_customers import validate_customers


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}


@dag(
    dag_id="elt_customers_pipeline",
    default_args=default_args,
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False,
    tags=["elt", "postgres", "data-engineering"]
)

def elt_customers_pipeline():

    @task
    def extract_task():

        logging.info("Starting extraction task")

        extract_customers()

        logging.info("Extraction completed")


    @task
    def load_task():

        logging.info("Starting load task")

        load_customers()

        logging.info("Load completed")


    @task
    def validate_task():

        logging.info("Starting validation task")

        validate_customers()

        logging.info("Validation completed")


    extract = extract_task()
    load = load_task()
    validate = validate_task()

    extract >> load >> validate


elt_customers_pipeline()