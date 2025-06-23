import json
from io import BytesIO
import requests
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def download_dataset(year_month: str):
    """
    Загружает данные из NASA EONET API и сохраняет в MinIO
    :param year_month: Дата в формате 'YYYY-MM-DD'
    """
    try:
        # 1. Получить данные от API
        url = f'https://eonet.gsfc.nasa.gov/api/v3/events/?start={year_month}&end={year_month}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json() # -> dict
        
        # 2. Подключение к MinIO
        s3_hook = S3Hook(aws_conn_id='aws_connection_id')
        s3 = s3_hook.get_conn()
        
        # 3. Проверка/создание бакета
        bucket_name = "eonet-nasa-bucket"
        buckets = s3.list_buckets()['Buckets']
        
        if not any(b['Name'] == bucket_name for b in buckets):
            print(f"Создаем бакет {bucket_name}...")
            s3.create_bucket(Bucket=bucket_name)
        
        # 4. Формируование имени файла
        file_key = f"eonet_data_{year_month}.json"
        
        # 5. Сохранение данных в MinIO
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(data, indent=2).encode('utf-8'),
            ContentType='application/json'
        )
        
        print(f"Данные успешно сохранены в {bucket_name}/{file_key}")
        return f"s3://{bucket_name}/{file_key}"
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA API: {str(e)}")
        raise
    except Exception as e:
        print(f"Ошибка при работе с MinIO: {str(e)}")
        raise