## Пайплайн загрузки данных из API NASA

Использую открытое [API NASA](https://eonet.gsfc.nasa.gov/what-is-eonet), предоставляющее информацию о природных событиях по всему миру, таких как: вулканы, землетрясения, пожары, штормы, ураганы, циклоны, наводнения, пыльные бури и пр.

Пайплайн (DAG) будет состоять из следующих операторов:

`SimpleHttpOperator`, его буду использовать для проверки существования файла на сервере перед его загрузкой

`PythonOperator`: download_file — загрузка файла с сайта и перекладывание на S3 в виде json

![image](https://github.com/user-attachments/assets/1ba6df35-b7c8-4de2-a7d4-bc93ded0c6cf)

------------------------------------------------------

## Настройка подключений

В UI Airflow Connections прописать следующие параметры

```
{
  "endpoint_url": "http://host.docker.internal:9000",
  "region_name": "us-east-1"
}
```

`AWS Access Key ID` и `AWS Secret Access Key` создаю в Minio. На боковой панели выбрать `Access Keys` далее `Create access keys`.

![image](https://github.com/user-attachments/assets/2a3f9135-71ac-414b-afc8-2b9d460248f7)

Настройки в самом UI Airflow

![image](https://github.com/user-attachments/assets/bde10bf3-b2e6-4017-a3eb-014b40f4af47)

------------------------------------------------------
