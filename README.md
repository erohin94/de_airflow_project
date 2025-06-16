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

### Загрузка курса валют из открытого API  
DAG, который ежедневно обращается к открытому API, получает актуальные курсы валют и сохраняет данные в хранилище. Подходит для интеграции с финансовыми или аналитическими системами.  

🔗 [Смотреть пример](https://github.com/erohin94/de_airflow_project/tree/main/currencybeacon_api_project)

