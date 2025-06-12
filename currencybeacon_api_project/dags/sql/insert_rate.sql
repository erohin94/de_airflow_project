INSERT INTO currency_exchange_rates
VALUES ('{{ params.base_currency }}', '{{ params.currency }}', {{ ti.xcom_pull(task_ids="get_rate") }}, '{{ execution_date.strftime("%Y-%m-%d") }}')
ON CONFLICT (base, currency, date) 
DO UPDATE SET rate = EXCLUDED.rate;

/*
'{{ params.base_currency }}', '{{ params.currency }}' значения которые передаем из таска insert_rate

{{ ti.xcom_pull(task_ids="get_rate") }}
ti — это task instance (экземпляр задачи), доступен внутри шаблона.
xcom_pull() — метод для получения значения, которое была "вытолкнуто" (pushed) из другой задачи.
task_ids="get_rate" — указывает, из какой задачи брать результат (в данном случае — из get_rate).

Пример Задача 1: get_rate. Она находит курс доллара к евро (например, 0.923) и возвращает его.
def get_rate():
    return 0.923
Этот результат сохраняется во временное хранилище Airflow, которое называется XCom.

Задача 2: insert_to_db. Она вставляет данные в базу и хочет использовать тот курс, который вернула первая задача.

Образно:
get_rate() → вернула 0.923
xcom_pull(task_ids="get_rate") → взял 0.923
Вставил это число в SQL

-- '{{ execution_date.strftime("%Y-%m-%d") }}' в Airflow это дата и время запуска DAG'а для конкретной задачи
*/


/*
Вставка данных через UPSERT. 
Чтобы не допустить дублирования данных. 
При обнаружении дубля по 3-м колонкам: base, currency и date, произойдёт обновление колонки rate вместо добавления ещё одной.

ON CONFLICT (base, currency, date) — указываем, при каком конфликте (совпадении) сработает обновление.

DO UPDATE SET rate = EXCLUDED.rate — обновляем поле rate новым значением, если такая комбинация уже есть.

EXCLUDED — это специальное имя, которое PostgreSQL даёт той строке, которую пытались вставить. 
Можно использовать его, чтобы обратиться к значениям из этой строки при обновлении.
Это означает:
"Если строка с такими base, currency, date уже существует — обнови поле rate до значения rate(новое значение), которое мы пытались вставить."

INSERT INTO
    currency_exchange_rates
VALUES ('USD', 'RUB', 56.55, '2020-01-01')
ON CONFLICT (base, currency, date) DO
    UPDATE
        SET rate = excluded.rate;
Если в таблице currency_exchange_rates уже будет запись обменного курса USD/RUB за 1 января, 
то у этой строчки будет обновлена колонка rate на значение 56.55. 
Выражение excluded.rate ссылается на значение обменного курса, предложенного для вставки (новое значение).
*/
