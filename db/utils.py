import json
import os
import sqlite3
from typing import Iterable, Optional
import aiosqlite

from entities import TempOrder, UserData



SCRIPT = 'init_db.sql'
DB_NAME = 'db.sqlite'


def adapt_user_data(udata: UserData) -> str:
    return repr(udata)
    

def convert_user_data(s: str) -> UserData:
    return UserData.from_dict(json.loads(s))


def adapt_temp_order(to: TempOrder) -> str:
    return repr(to)


def convert_temp_order(s: str) -> TempOrder:
    return TempOrder.from_dict(data=json.loads(s))


sqlite3.register_adapter(UserData, adapt_user_data)
sqlite3.register_converter('user_data', convert_user_data)
sqlite3.register_adapter(TempOrder, adapt_temp_order)
sqlite3.register_converter('incomplete_order', convert_temp_order)


def create_tables():
    with open(os.path.join('db', SCRIPT), 'r') as sql_file:
        sql_script = sql_file.read()
        print(sql_script)

    with sqlite3.connect(DB_NAME, 
                         detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
        conn.cursor().executescript(sql_script)
        conn.commit()


async def get_user_orders(user_id: int) -> Iterable[sqlite3.Row]:
    query = 'select id, item_id, tmp from orders where user_id=?'
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute(query, (user_id,)) as cursor:
            return await cursor.fetchall()



async def get_items() -> Iterable[sqlite3.Row]:
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute('select * from items') as cursor:
            return await cursor.fetchall()



async def get_item(id: int) -> sqlite3.Row:
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute('select title, price from items where id=?', (id,)) as cursor:
            return await cursor.fetchone()


async def get_users_ids() -> list[int]:
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute('select id from users') as cursor:
            return [row[0] for row in await cursor.fetchall()]



async def user_exists(user_id: int) -> bool:
    return user_id in await get_users_ids()
        


async def add_user(user_id: int, username: str, lang_code: str, ref: Optional[str]) -> None:
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute('insert into users values (?, ?, ?, ?)', 
                           (user_id, username, lang_code, ref))
        await conn.commit()



async def add_order(user_id: int, item_id: int, external_id: str, user_data: UserData, 
                    temp_order: TempOrder) -> None:
    if not await user_exists(user_id):
        raise Exception('user not present in database')
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute(
            'insert into orders(user_id, item_id, external_id, user_data, temp_order) \
             values (?, ?, ?, ?, ?)',
            (user_id, item_id, external_id, user_data, temp_order))
        await conn.commit()



async def update_order_payed(order_id: int, payed_ts: str) -> None:
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute("update orders set status='p' where id=?", (order_id,))
        await conn.execute('update orders set payed_ts=? where id=?', (payed_ts, order_id,))
        await conn.commit()


async def update_order_completed(order_id: int, completed_ts: str) -> None:
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute("update orders set status='c' where id=?", (order_id,))
        await conn.execute('update orders set completed_ts=? where id=?', 
                           (completed_ts, order_id,))
        await conn.commit()


async def get_user_id_by_ext_id(external_id: str) -> int:
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute('select user_id from orders where external_id=?', 
                                (external_id,)) as cursor:
            return (await cursor.fetchone())[0]

