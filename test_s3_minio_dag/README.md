## DAG для тестирования подключения к S3

![image](https://github.com/user-attachments/assets/0ff141b7-ddd3-45f1-a313-215321a1879e)

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

## После запуска DAG, видно результат выполнения

![image](https://github.com/user-attachments/assets/bbaa6c28-3adb-45d9-982b-186f6fbddd9c)

Бакеты в MINIO

![image](https://github.com/user-attachments/assets/a25e9a1f-f4ba-4548-9d22-9d8a7861cc28)

И сам файл

![image](https://github.com/user-attachments/assets/deac4090-5fbb-4361-b755-e82718830cb1)

