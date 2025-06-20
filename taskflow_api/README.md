**Taskflow API** — это высокоуровневый интерфейс в Apache Airflow, который упрощает создание и выполнение задач в DAG (Directed Acyclic Graph). 
Он был введён в Airflow 2.0 для более интуитивного и лаконичного написания пайплайнов по сравнению с традиционным подходом.

Декоратор `@task`по умолчанию создаёт `PythonOperator`.

![image](https://github.com/user-attachments/assets/88d9e17e-d1e4-4e25-a502-9e13dd801ba7)

**Описание**

Чтобы сформировать объект DAG, необходимо обернуть функцию декоратором `@dag`. Этот декоратор принимает те же аргументы. 

Чтобы превратить функцию в `PythonOperator`, её необходимо обернуть в декоратор `@task`.

Инстанс DAG должен быть доступен в глобальном пространстве при импорте кода планировщиком. 
Именно поэтому вызываем функцию, обернутую в декоратор `@dag` и присваиваем переменной `main_dag`. Если этого не сделать, то планировщик не сможет найти DAG.

Явно не указываем `task_id`, он берётся из названия оборачиваемой функции.

Во всех примерах, где будет нужен `PythonOperator` можно будет использовать TaskFlow API. 

Также TaskFlow API позволяет "бесшовно" передавать возвращаемые значения из одного оператора в другой. До TaskFlow API необходимо было явно использовать XCom.

Подробный пост на тему TaskFlow API [TaskFlow API в Apache Airflow 2.0](https://startdatajourney.com/ru/course/apache-airflow-2/modules/11/36/1#:~:text=TaskFlow%20API%20%D0%B2%20Apache%20Airflow%202.0)
