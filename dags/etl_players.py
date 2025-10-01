from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append("/opt/airflow/scripts")

import extract_basic, extract_advanced, transform, load_postgres

with DAG(
    "etl_players",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task_extract_basic = PythonOperator(
        task_id="extract_basic",
        python_callable=extract_basic.run
    )

    task_extract_advanced = PythonOperator(
        task_id="extract_advanced",
        python_callable=extract_advanced.run
    )

    task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform.run
    )

    task_load = PythonOperator(
        task_id="load_postgres",
        python_callable=load_postgres.run
    )

    [task_extract_basic, task_extract_advanced] >> task_transform >> task_load
