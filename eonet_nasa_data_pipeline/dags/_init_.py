from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from functions import download_dataset, convert_to_parquet

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args,schedule_interval='@daily',start_date=datetime(2025, 6, 1),)
def eonet_nasa_api_dag():

    check_file = SimpleHttpOperator(
    method='GET',
    endpoint='start={{ execution_date.strftime("%Y-%m-%d") }}&end={{ execution_date.strftime("%Y-%m-%d") }}', #Всё, что есть в ссылке после указания домена
    #endpoint=f'start={{ ds }}&end={{ ds )}}', аналог
    task_id='check_file',
    http_conn_id='nasa_eonet_id') # Название ключа соединения, которое создадим через раздел Connections

    @task
    def download_file():
        '''
        Декорируемая функция вызывает get_current_context. 
        Эта функция возвращает контекст выполнения DAG, в нём хранится информация в том числе настройки, 
        текущая дата выполнения (execution_date) и многое другое. 
        Нам нужна текущая дата выполнения для передачи в функцию download_dataset. 
        Вызов get_current_context вне оператора вернёт ошибку, т.к. отсутствует контекст.
        '''
        context = get_current_context()
        return download_dataset(context['execution_date'].strftime('%Y-%m-%d'))
    
    @task
    def convert_file(s3_path: str):
        return convert_to_parquet(s3_path)  # вернёт s3://bucket/key.parquet
    
    file_path = download_file()
    parquet_path = convert_file(file_path)

    check_file >> file_path >> parquet_path

nyc_dag = eonet_nasa_api_dag()
