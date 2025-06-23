from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from functions import download_dataset

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args,schedule_interval='@daily',start_date=datetime(2025, 6, 1),)
def eonet_nasa_api_dag():

    check_file = SimpleHttpOperator(
    method='GET',
    endpoint='start={{ execution_date.strftime("%Y-%m-%d") }}&end={{ execution_date.strftime("%Y-%m-%d") }}',
    #endpoint=f'start={{ ds }}&end={{ ds )}}', аналог execution_date.strftime("%Y-%m-%d")
    task_id='check_file',
    http_conn_id='nasa_eonet_id')

    @task
    def download_file():
        context = get_current_context()
        return download_dataset(context['execution_date'].strftime('%Y-%m-%d'))
    
    file_path = download_file()

    check_file >> file_path 

nyc_dag = eonet_nasa_api_dag()