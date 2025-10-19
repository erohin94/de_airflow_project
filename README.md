# Airflow проекты

![1](https://github.com/user-attachments/assets/33bdc75a-4409-4aa7-9e62-009ab6b8b370)

Этот репозиторий содержит примеры DAG'ов (Directed Acyclic Graphs) для Apache Airflow, демонстрирующие различные сценарии загрузки и обработки данных.

## Содержание

### Простой DAG  
Базовый пример DAG'а с минимальной конфигурацией, предназначенный для знакомства с синтаксисом и базовыми возможностями Airflow.  

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/first_dag)

### Работа с execution_date
Пример DAG'а, демонстрирующий разницу между `start_date` и `execution_date`, а также способ получения `execution_date` из контекста выполнения.

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/second_dag)

### Зависимость тасков
Пример DAG с условным выполнением задач, где вторая задача (dummy_task) запускается только после успешного завершения первой (even_only), которая проверяет четность дня выполнения.

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/dag_with_two_tasks)

### TaskFlow API
Пример использования Taskflow API и интеграции с классическими операторами Airflow

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/taskflow_api)

### Тестовый DAG, для проверки подключения к S3  
Проверяет корректность настроек соединения с S3/MinIO, выводит список доступных бакетов и загружает тестовый файл для верификации доступа.  

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/test_s3_minio_dag)

### Загрузка природных событий из NASA EONET API
DAG, который ежедневно обращается к открытому API NASA EONET, проверяет доступность данных за текущую дату и, при наличии, загружает их в MinIO (или S3-хранилище).

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/eonet_nasa_api_dag)

### Конвертация данных NASA EONET из JSON.GZ в Parquet
Дополнение к DAG'у NASA EONET ("Загрузка природных событий из NASA EONET API"): после загрузки событий в формате .json.gz из NASA API, данные автоматически конвертируются в формат .parquet и сохраняются обратно в S3/MinIO. 
Это оптимизирует хранение и ускоряет последующую аналитику.

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/eonet_nasa_data_pipeline)

### Backfill и Catchup
В Airflow есть две важные концепции, которые необходимо хорошо понимать: Backfill и Catchup.

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/Backfill%20%D0%B8%20Catchup)


### Сенсоры
Сенсоры это разновидность операторов, используемых для организации событийно-ориентированных дата пайплайнов.

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/%D0%A1%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%8B)


### Загрузка курса валют из открытого API  
DAG, который ежедневно обращается к открытому API, получает актуальные курсы валют и сохраняет данные в хранилище. Подходит для интеграции с финансовыми или аналитическими системами.  

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/taskflow_api)

