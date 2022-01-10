import conf
import asyncpraw
import asyncio
from aiogram import Bot, types
import sqlite3
from time import strftime

# ---------------------------------------------------------------------------
#              подключение к api
# ---------------------------------------------------------------------------
bot = Bot(token=conf.token, parse_mode=types.ParseMode.HTML)
reddit = asyncpraw.Reddit(client_id=conf.client_id,
                          client_secret=conf.secret,
                          user_agent='random_rabbit_bot/0.0.1')


# ----------------------------------------------------------------------------

def check_post(title, post_id):
    """
    Проверка на наличие поста
    :param title:
    :param post_id:
    :return: результат запроса
    """
    sqlite_connection = ''
    post = ''
    try:
        # ----------- подключение к бд ----------------------------
        sqlite_connection = sqlite3.connect('db/db_memes.db')
        cursor = sqlite_connection.cursor()
        # ------------ запрос к бд --------------------------------
        sqlite_select_query = """SELECT title, post_id 
                                 FROM memes 
                                 WHERE title=? AND post_id=? """
        data = [title, post_id]
        cursor.execute(sqlite_select_query, data)
        # ------------ получение запроса --------------------------
        post = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        text = f'Ошибка при подключении к sqlite, ' \
               f'{error}, TITLE = {title} ID = {post_id} ' \
               f'{strftime("%Y-%m-%d %H:%M:%S")}\n'
        # ----------- запись в файл при получении ошибки ----------
        with open('errors.txt', 'a', encoding='UTF-8') as f:
            f.write(text)
    finally:
        sqlite_connection.close()
        return post


def add_post(title, post_id):
    """
    Добавление поста в базу
    :param title:
    :param post_id:
    :return:
    """
    sqlite_connection = ''
    try:
        # ----------- подключение к бд ----------------------------
        sqlite_connection = sqlite3.connect('db/db_memes.db')
        cursor = sqlite_connection.cursor()
        # ------------ запрос к бд --------------------------------
        sqlite_insert_query = """INSERT INTO memes
                                  (title, post_id)  VALUES  (?, ?)"""
        data = [title, post_id]
        cursor.execute(sqlite_insert_query, data)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        text = f'Ошибка при подключении к sqlite, {error} {strftime("%Y-%m-%d %H:%M:%S")}\n'
        with open('errors.txt', 'a', encoding='UTF-8') as f:
            f.write(text)
    finally:
        sqlite_connection.close()
        text = f'Добавлено {title}, || {post_id} ' \
               f'{strftime("%Y-%m-%d %H:%M:%S")}\n'
        with open('logs.txt', 'a', encoding='UTF-8') as f:
            f.write(text)


async def send_message(channel_id, text):
    await bot.send_message(channel_id, text)


async def main():
    channel_id = conf.channel_id
    timeout = 10
    subreddit = 'memes'
    limit = 1

    while True:
        await asyncio.sleep(timeout)
        memes_sub = await reddit.subreddit(subreddit)
        memes_sub = memes_sub.new(limit=limit)
        item = await memes_sub.__anext__()

        if not check_post(item.title, item.id):
            add_post(item.title, item.id)
            post = f'{item.title} \n {item.url}'
            await send_message(channel_id, post)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
