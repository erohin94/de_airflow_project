from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id='test_postgres_connection_dag',
    start_date=datetime(2025, 5, 15),
    schedule_interval=None,  # Запуск вручную
    catchup=False,
    tags=['test', 'postgres'],
) as dag:

    test_connection = PostgresOperator(
        task_id='test_postgres_query',
        postgres_conn_id='postgres_default_db',
        sql='SELECT 1;',
    )
