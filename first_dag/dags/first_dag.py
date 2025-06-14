import random
import datetime as dt

from airflow.models import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',                         # Владелец DAG — чаще для логирования и уведомлений
    'start_date': dt.datetime(2025, 5, 20),     # Дата, с которой начинается выполнение DAG
    'retries': 2,                               # Количество повторных попыток при неудаче задачи
    'retry_delay': dt.timedelta(seconds=10),    # Интервал между повторными попытками
}

def random_dice():
    '''
    Генерирует случайное число от 1 до 6 
    и выбрасывает исключение, если значение нечётное.
    '''
    val = random.randint(1, 6)
    if val % 2 != 0:
        raise ValueError(f'Odd {val}')

with DAG(
        dag_id='first_dag',
         schedule_interval='@daily',
         default_args=default_args
         ) as dag:

    dice = PythonOperator(
        task_id='random_dice',
        python_callable=random_dice,
        dag=dag,
    )