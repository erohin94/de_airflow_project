from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from .operator import CurrencyScoopOperator


with DAG(
        dag_id='exchange_rate_usd_rub_dag',
        start_date=datetime(2025, 5, 1),
        schedule_interval='@daily',
) as dag:
    # Создание таблицы, если её нет
    create_table = PostgresOperator(
        task_id='create_table_task', # Название таска
        sql='sql/create_table.sql', # Путь до sql файла(необходимо указывать относительно директории, где лежит сам DAG.). Вместо пути можно написать SQL - запрос
        postgres_conn_id='postgres_default_db', # Connection Id из UI Airflow
    )

    get_rate = CurrencyScoopOperator(# Самописный кастомный оператор operator.py
        task_id='get_rate',
        base_currency='USD',
        currency='RUB',
        conn_id='cur_scoop_conn_id', # Connection Id из UI Airflow
        #dag=dag,
        do_xcom_push=True,
    )
    # Добавить запись о курсе валют в базу данных после успешного выполнения предыдущего таска get_rate.
    insert_rate = PostgresOperator(
        task_id='insert_rate',
        postgres_conn_id='postgres_default_db',
        sql='sql/insert_rate.sql',
        params={ # Позволяет передавать значения в SQL-шаблон. Конкретно в этом случае значения у нас статичные.
            'base_currency': 'USD',
            'currency': 'RUB',
        }
    )

    create_table >> get_rate >> insert_rate
