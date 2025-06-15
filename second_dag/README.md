# **Про `start_date` и `execution_date`**

В Apache Airflow есть 2 ключевые даты, которые нужно понимать.

**Start Date** - `start_date`

**Execution Date** - `execution_date`

Start Date это дата начала от которой следует начинать запускать DAG согласно расписания `schedule_interval`.

Execution Date это дата выполнения конкретного запуска. В [примере](https://github.com/erohin94/de_airflow_project/tree/main/first_dag) у меня было 26 запусков. 26 запусков, а значит 26 `execution_date`, а именно:

```
1)20.05.2025
2)21.05.2025
3)22.05.2025
4)23.05.2025
5)24.05.2025
.....
.....
26)14.06.2025
```

Execution date можно получить, обратившись к контексту выполнения. Контекст можно получить, вызвав функцию `get_current_context`. Для примера работы с `execution_date` создал новый DAG по аналогии с предыдущим, но немного модифицировал код оператора.

```
import datetime as dt

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import get_current_context

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2025, 5, 25),
}


def even_only():
    context = get_current_context()
    execution_date = context['execution_date']

    if execution_date.day % 2 != 0:
        raise ValueError(f'Odd day: {execution_date}')


with DAG(dag_id='first_dag_execution_date',
         schedule_interval='@daily',
         default_args=default_args) as dag:

    even_only = PythonOperator(
        task_id='even_only',
        python_callable=even_only,
        dag=dag,
    )
```

![image](https://github.com/user-attachments/assets/11136422-89d5-490c-9153-822ce92f2b74)

Таски будут падать через день, т.е. каждый нечетный день.

![image](https://github.com/user-attachments/assets/91fd619c-3dad-40bd-923f-43b89fc40404)

Функция `get_current_context()` в Apache Airflow используется для получения контекста выполнения задачи (`task instance`) внутри Python-кода. 


**Что такое «контекст»?**

Контекст — это словарь (dict), который содержит множество полезных переменных, автоматически предоставляемых Airflow при исполнении задачи. Примеры:

| Ключ               | Значение                                                                |
| ------------------ | ----------------------------------------------------------------------- |
| `'execution_date'` | Дата, за которую выполняется DAG (не обязательно текущая дата)          |
| `'ds'`             | Строка даты исполнения в формате `'YYYY-MM-DD'`                         |
| `'dag'`            | Объект DAG                                                              |
| `'task'`           | Объект текущей задачи (`BaseOperator`)                                  |
| `'ts'`             | Метка времени исполнения (`'2024-12-25T00:00:00+00:00'`)                |
| `'run_id'`         | Идентификатор запущенного DAG Run (например, `'manual__...'`)           |
| `'ti'`             | Экземпляр задачи (`TaskInstance`) — даёт доступ к XCom и статусу задачи |



