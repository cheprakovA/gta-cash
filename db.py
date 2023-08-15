import sqlite3
import time
from typing import Iterable, Optional

import aiosqlite

import utils


async def get_user_orders(user_id: int) -> Iterable[sqlite3.Row]:
    query = '''SELECT items.name, orders.created_dt, orders.completed
               FROM orders JOIN items
               ON orders.item_id=items.id
               WHERE orders.user_id=?'''
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        async with conn.execute(query, (user_id,)) as cursor:
            return await cursor.fetchall()



async def get_items() -> Iterable[sqlite3.Row]:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        async with conn.execute('SELECT * FROM items') as cursor:
            return await cursor.fetchall()



async def get_users_ids() -> list[int]:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        async with conn.execute('SELECT id FROM users') as cursor:
            return [row[0] for row in await cursor.fetchall()]



async def user_exists(user_id: int) -> bool:
    return user_id in await get_users_ids()



async def user_platform_specified(user_id: int) -> Optional[str]:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        async with conn.execute('SELECT platform FROM users WHERE id=?', (user_id,)) as cursor:
            return (await cursor.fetchone())[0]



async def update_user_platform(user_id: int, platform: str) -> None:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        await conn.execute('UPDATE users SET platform=? WHERE id=?', 
                           (platform, user_id,))
        await conn.commit()
        


async def add_user(user_id: int, username: str, lang_code: str) -> None:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        await conn.execute('INSERT INTO users VALUES (?, ?, ?, ?)', 
                           (user_id, username, lang_code, None))
        await conn.commit()



async def add_order(user_id: int, item_id: int, created_dt: int) -> None:
    if not await user_exists(user_id):
        raise Exception('user not present in database')
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        await conn.execute(
            'INSERT INTO orders(user_id, item_id, created_dt, completed) VALUES (?, ?, ?, ?)',
            (user_id, item_id, created_dt, 0,))
        await conn.commit()



async def complete_order(order_id: int) -> None:
    async with aiosqlite.connect(utils.DB_NAME) as conn:
        await conn.execute('UPDATE orders SET completed=? WHERE id=?', 
                         (int(time.time()), order_id,))
        await conn.commit()
