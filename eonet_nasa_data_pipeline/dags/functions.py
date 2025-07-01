import json
import gzip
import pandas as pd
from io import BytesIO
from tempfile import NamedTemporaryFile
import requests
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def download_dataset(year_month: str):
    """
    Загружает данные из NASA EONET API и сохраняет в MinIO
    
    :param year_month: Дата в формате 'YYYY-MM'
    """
    try:
        # 1. Получаем данные от API
        url = f'https://eonet.gsfc.nasa.gov/api/v3/events/?start={year_month}&end={year_month}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 2. Подключаемся к MinIO
        s3_hook = S3Hook(aws_conn_id='aws_connection_id')
        s3 = s3_hook.get_conn()
        
        # 3. Проверяем/создаем бакет
        bucket_name = "eonet-nasa-bucket"
        buckets = s3.list_buckets()['Buckets']
        
        if not any(b['Name'] == bucket_name for b in buckets):
            print(f"Создаем бакет {bucket_name}...")
            s3.create_bucket(Bucket=bucket_name)
        
        # 4. Формируем имя файла
        file_key = f"eonet_data_{year_month}.json.gz"
        
        # 5. Сохраняем данные в MinIO - Было
        #s3.put_object(
        #    Bucket=bucket_name,
        #    Key=file_key,
        #    Body=json.dumps(data, indent=2).encode('utf-8'),
        #    ContentType='application/json'
        #)

        # 5. Сохраняем данные во временный gzip-файл
        with NamedTemporaryFile(mode='wb+', suffix='.json.gz', delete=True) as temp_file:
            with gzip.GzipFile(fileobj=temp_file, mode='wb') as gz_file:
                gz_file.write(json.dumps(data, indent=2).encode('utf-8'))
            temp_file.flush()

             # 6. Загружаем файл в MinIO
            s3_hook.load_file(
                filename=temp_file.name,
                key=file_key,
                bucket_name=bucket_name,
                replace=True,
                encrypt=False
            )
        
        print(f"Данные успешно сохранены в {bucket_name}/{file_key}")
        return f"s3://{bucket_name}/{file_key}"
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA API: {str(e)}")
        raise
    except Exception as e:
        print(f"Ошибка при работе с MinIO: {str(e)}")
        raise

def convert_to_parquet(s3_path: str) -> str:
    """
    Конвертирует JSON.GZ файл из S3 (загруженный ранее) в Parquet и загружает обратно в тот же бакет.

    :param s3_path: s3-путь к файлу формата 's3://bucket/key.json.gz'
    :return: s3-путь к сохранённому .parquet
    """
    try:
        # 1. Разбор пути s3://bucket/key
        if not s3_path.startswith("s3://"):
            raise ValueError("Некорректный путь S3")

        bucket_name, key = s3_path.replace("s3://", "").split("/", 1)

        # 2. Подключение к MinIO
        s3_hook = S3Hook(aws_conn_id='aws_connection_id')
        s3 = s3_hook.get_conn()

        # 3. Скачивание gzip-файла
        response = s3.get_object(Bucket=bucket_name, Key=key)
        compressed_data = response['Body'].read()

        # 4. Распаковка и загрузка JSON
        with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as gz:
            json_data = json.load(gz)

        # 5. Преобразование в DataFrame
        df = pd.json_normalize(json_data["events"])

        # 6. Сохраняем как .parquet во временный файл
        with NamedTemporaryFile(mode='wb+', suffix='.parquet', delete=True) as tmp_parquet:
            df.to_parquet(tmp_parquet.name, engine='pyarrow', index=False)

            # 7. Генерируем новое имя файла
            parquet_key = key.replace(".json.gz", ".parquet")

            # 8. Загрузка .parquet в S3
            s3_hook.load_file(
                filename=tmp_parquet.name,
                key=parquet_key,
                bucket_name=bucket_name,
                replace=True
            )

        print(f"Parquet сохранён в {bucket_name}/{parquet_key}")
        return f"s3://{bucket_name}/{parquet_key}"

    except Exception as e:
        print(f"Ошибка при конвертации в Parquet: {e}")
        raise

    #Добавлено сохранение во врееменный файл перед загрузкой в S3 with NamedTemporaryFile
    #Функция возвращает путь до S3 объекта return f"s3://{bucket_name}/{file_key}", которым воспользуется следующий оператор.
    #Добавлен to_parquet — оператор скачивает файл, загруженный предыдущим оператором, и трансформирует его в формат Parquet, сохраняя результат в S3.