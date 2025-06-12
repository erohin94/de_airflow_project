# **Описание**

**Граф**

![image](https://github.com/user-attachments/assets/22d864c4-4c76-4170-bd1b-ca6ed8a0fc01)

В пайплайне 3 таска:

1.`create_table_task`, отвечает за создание таблицы в базе данных PostgreSQL

2.`get_rate`, собственный Operator для работы с API сервисом курсов валют

3.`insert_rate`, укладывает полученный курс в таблицу, созданную в таске `create_table_task`

-----------------------------------------

**API от куда тянем данные**

[currencybeacon](https://currencybeacon.com/)

Для работы надо зарегистрироваться и получить ключ

![Снимок](https://github.com/user-attachments/assets/a9ecbeaa-90e3-41ac-96b8-0650ad547c4c)

-----------------------------------------

**Admin->Connections**

В подключениях прописываем следующие настройки.

Подключение к PostgreSQL

![image](https://github.com/user-attachments/assets/a07d0756-444b-4ee4-a8cc-dec93aec3d7f)

Подключение к API. В password передал API ключ currencybeacon

![image](https://github.com/user-attachments/assets/a5f3c1c7-a9db-4f43-a668-bf2d24db23a3)

-----------------------------------------

**Запуск**

![image](https://github.com/user-attachments/assets/7b5eda62-796d-487e-9e3c-37347a2e14c8)

Как видно, таблица появилась в БД

![image](https://github.com/user-attachments/assets/d676c644-7d9e-4a84-9045-799f9452ef40)



