import time
import sqlite3
from pathlib import Path
from aiogram.types import Message



class UserData:
    def __init__(self, username: str, password: str, recovery_codes: str):
        self.username = username
        self.password = password
        self.recovery_codes = recovery_codes
    

def adapt_user_data(data: UserData) -> str:
    return ';'.join([data.username, data.password, data.recovery_codes])
    

def convert_user_data(s: str) -> UserData:
    return UserData(*s.split(';'))


sqlite3.register_adapter(UserData, adapt_user_data)
sqlite3.register_converter('UDATA', convert_user_data)



BOT_TOKEN = '6599454857:AAHJvVwp3pTa7Grn5rPJMYNavfN3wJbHxjs'

WORK_DIR = Path.cwd()

DATA_DIR =  WORK_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)


DB_NAME = 'db.sqlite'

PLATFORMS = {
    'ps4':     'PS4',
    'ps5':     'PS5',
    'xboxsex': 'Xbox Series X|S',
    'xboxone': 'Xbox One',
}


# def img_title_repr(user_id: int, file_id: int, dt_value: int | float) -> str:
#     return DATA_DIR / f'{user_id}_{int(dt_value)}_{file_id}.jpg'


def dt_repr(dt_value: int | float) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt_value))



def create_users_table() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS users')
        conn.execute('CREATE TABLE users(\
                      id INTEGER PRIMARY KEY, \
                      username TEXT, \
                      lang_code TEXT)')
        conn.commit()



def create_orders_table() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS orders')
        conn.execute('CREATE TABLE orders(\
                      id INTEGER PRIMARY KEY, \
                      user_id INTEGER, \
                      platform TEXT, \
                      user_data UDATA, \
                      item_id INTEGER, \
                      created_dt INTEGER, \
                      completed INTEGER)')
        conn.commit()



def create_items_table() -> None:
    items = [
        (1,  '10 million',  17.99 ),
        (2,  '20 million',  19.99 ),
        (3,  '25 million',  23.99 ),
        (4,  '30 million',  27.99 ),
        (5,  '50 million',  34.99 ),
        (6,  '75 million',  49.99 ),
        (7,  '100 million', 59.99 ),
        (8,  '200 million', 79.99 ),
        (9,  '300 million', 99.99 ),
        (10, '500 million', 139.99),
        (11, '750 million', 159.99),
        (12, '1 billion',   199.99),
    ]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS items')
        conn.execute('CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT, price REAL)')
        conn.executemany('INSERT into items VALUES (?, ?, ?)', items)
        conn.commit()