CREATE TABLE IF NOT EXISTS currency_exchange_rates (
    base VARCHAR(3) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12, 3) NOT NULL,
    date DATE NOT NULL,
    UNIQUE (base, currency, date)
);

/*
Таблица currency_exchange_rates:

base — хранится код базовой валюты
currency — хранится код конвертируемой валюты
rate — обменный курс между currency и base, т.е. стоимость base в currency
date — дата

Свойство UNIQUE по трём столбцам необходимо, чтобы делать вставку через UPSERT. 
Если по какой-то причине таск с одной и той же датой будет запущен несколько раз нужно не допустить дублирования. 
*/
