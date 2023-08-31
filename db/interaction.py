import json
import sqlite3
from typing import Iterable, Optional
import aiosqlite

from wallet.entities import MoneyAmount

from .entities import OrderData, UserData
from utils import SCRIPT_PATH, DB_PATH, unpack


def adapt_user_data(user_data: UserData) -> str:
    return str(user_data)
    

def convert_user_data(s: str) -> UserData:
    return UserData(**json.loads(s))


def adapt_money_amount(money_amount: MoneyAmount) -> str:
    return str(money_amount)
    

def convert_money_amount(s: str) -> MoneyAmount:
    amount, currency_code = s.split()
    return MoneyAmount(amount=amount, currencyCode=currency_code)


sqlite3.register_adapter(UserData, adapt_user_data)
sqlite3.register_converter('userdata', convert_user_data)
sqlite3.register_adapter(MoneyAmount, adapt_money_amount)
sqlite3.register_converter('moneyamount', convert_money_amount)


def create_tables():
    with open(SCRIPT_PATH, 'r') as sql_file:
        sql_script = sql_file.read()

    with sqlite3.connect(DB_PATH, 
                         detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
        conn.cursor().executescript(sql_script)
        conn.commit()


async def get_user_orders(user_id: int) -> Iterable[sqlite3.Row]:
    query = 'select id, item_id, tmp from orders where user_id=?'
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(query, (user_id,)) as cursor:
            return await cursor.fetchall()


async def get_items() -> Iterable[sqlite3.Row]:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute('select * from items') as cursor:
            return await cursor.fetchall()


async def get_item(id: int) -> sqlite3.Row:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute('select title, price from items where id=?', (id,)) as cursor:
            return await cursor.fetchone()


async def get_users_ids() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute('select id from users') as cursor:
            return [row[0] for row in await cursor.fetchall()]


async def user_exists(user_id: int) -> bool:
    return user_id in await get_users_ids()
        

async def add_user(user_id: int, username: str, lang_code: str, ref: Optional[str]) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute('insert into users values (?, ?, ?, ?)', 
                           (user_id, username, lang_code, ref))
        await conn.commit()


async def add_order(order: OrderData) -> None:
    if not await user_exists(order.user_id):
        raise Exception('user not present in database')
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute('insert into orders values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                           tuple(order))
        await conn.commit()


async def update_order_payed(order_id: int, payed_ts: str) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("update orders set status='p' where id=?", (order_id,))
        await conn.execute('update orders set payed_ts=? where id=?', (payed_ts, order_id,))
        await conn.commit()


async def update_order_completed(order_id: int, completed_ts: str) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("update orders set status='c' where id=?", (order_id,))
        await conn.execute('update orders set completed_ts=? where id=?', 
                           (completed_ts, order_id,))
        await conn.commit()


# async def get_user_id_by_ext_id(external_id: str) -> int:
#     async with aiosqlite.connect(DB_PATH) as conn:
#         row = 
#         async with conn.execute('select user_id from orders where external_id=?', 
#                                 (external_id,)) as cursor:
#             return (await cursor.fetchone())[0]
