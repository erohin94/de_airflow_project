# **Описание**

**Граф**

![image](https://github.com/user-attachments/assets/22d864c4-4c76-4170-bd1b-ca6ed8a0fc01)

В пайплайне 3 таска:

1.`create_table`, отвечает за создание таблицы в базе данных PostgreSQL

2.`get_rate`, собственный Operator для работы с API сервиса курсов валют

3.`insert_rate`, укладывает полученный курс в таблицу, созданную в таске `create_table`
