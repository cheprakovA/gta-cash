import time
import sqlite3


BOT_TOKEN = '6599454857:AAHJvVwp3pTa7Grn5rPJMYNavfN3wJbHxjs'
DB_NAME = 'db.sqlite'


PLATFORMS = {
    'ps4':     'PS4',
    'ps5':     'PS5',
    'xboxsex': 'Xbox Series X|S',
    'xboxone': 'Xbox One',
}


def dt_repr(dt_value: int | float) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt_value))



def create_users_table() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS users')
        conn.execute('''CREATE TABLE users(
                     id INTEGER PRIMARY KEY, 
                     username TEXT, 
                     lang_code TEXT,
                     platform TEXT)''')
        conn.commit()



def create_orders_table() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS orders')
        conn.execute('''CREATE TABLE orders(
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER,
                     item_id INTEGER,
                     created_dt INTEGER,
                     completed INTEGER)''')
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