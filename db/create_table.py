import sqlite3

try:
    sqlite_connection = sqlite3.connect('db_memes.db')
    cursor = sqlite_connection.cursor()

    print("База данных создана и успешно подключена к SQLite")
    sqlite_create_table_query = '''CREATE TABLE  memes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    post_id text NOT NULL
                                    );'''

    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    print('таблица создана')

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

fok = 'df'