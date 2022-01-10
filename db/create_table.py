import sqlite3

try:
    sqlite_connection = sqlite3.connect('db_memes.db')
    cursor = sqlite_connection.cursor()
    print('table connect')
    sqlite_create_table_query = '''CREATE TABLE  memes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    post_id text NOT NULL
                                    );'''

    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    print('table create')

except sqlite3.Error as error:
    print("error sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print(" SQLite close")
