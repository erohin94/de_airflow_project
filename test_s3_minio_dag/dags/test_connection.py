from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def test_minio_connection():
    try:
        # 1. Подключение к MinIO
        s3_hook = S3Hook(aws_conn_id='aws_connection_id')
        s3 = s3_hook.get_conn()
        
        # 2. Простая проверка - список бакетов
        buckets = s3.list_buckets()
        print("Успешное подключение к MinIO!")
        print("Доступные бакеты:")
        for bucket in buckets['Buckets']:
            print(f"- {bucket['Name']}")
            
        # 3. Тест записи файла
        test_bucket = "test-bucket"
        test_content = b"Hello MinIO from Airflow!"
        
        s3.put_object(
            Bucket=test_bucket,
            Key="test_file.txt",
            Body=test_content
        )
        print(f"Файл успешно записан в {test_bucket}/test_file.txt")
        
    except Exception as e:
        print(f"Ошибка подключения к MinIO: {str(e)}")
        raise

# Создаем DAG
with DAG(
    dag_id='minio_connection_test',
    start_date=datetime(2025, 6, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    
    test_task = PythonOperator(
        task_id='test_minio_connection',
        python_callable=test_minio_connection
    )