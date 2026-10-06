import sys
from pathlib import Path
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.extract import (
    extract_weather_data,
    extract_air_quality_data
)

from src.transform import transform_data
from src.load import load_data


def extract_task():
    weather_data = extract_weather_data()
    air_quality_data = extract_air_quality_data()

    return {
        "weather": weather_data,
        "air_quality": air_quality_data
    }


def transform_task(**context):

    extracted_data = context["ti"].xcom_pull(
        task_ids="extract_data"
    )

    transformed_data = transform_data(
        extracted_data["weather"],
        extracted_data["air_quality"]
    )

    return transformed_data


def load_task(**context):

    transformed_data = context["ti"].xcom_pull(
        task_ids="transform_data"
    )

    load_data(transformed_data)


with DAG(
    dag_id="weather_air_quality_etl_pipeline",

    start_date=datetime(2026, 9, 22),

    schedule="*/5 * * * *",

    catchup=False,

    tags=[
        "weather",
        "air_quality",
        "etl",
        "open-meteo",
        "mysql"
    ],

) as dag:

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=extract_task,
    )

    transform_data_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_task,
    )

    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_task,
    )

    extract_data >> transform_data_task >> load_data_task