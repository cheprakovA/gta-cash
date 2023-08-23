import random
from typing import Literal
import time
import sqlite3
import requests
import aiohttp
import json
import ujson
from pathlib import Path
from WalletPay.types import OrderPreview




    




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

BOT_TOKEN = '6599454857:AAHJvVwp3pTa7Grn5rPJMYNavfN3wJbHxjs'
WALLET_KEY = '0YzKF2xlOVXIxotj5EtF86APbFWMxhUtrbQw'
APP_BASE_URL = ''
ALLOWED_IPS = {'172.255.248.29', '172.255.248.12', '127.0.0.1'}

async def send_payment_rq(
    user_id: int,
    item: tuple[str, float], 
    timeout: int = 10800, 
    currencyCode: Literal['TON', 'BTC', 'USDT', 'EUR', 'USD', 'RUB'] = 'USD'
) -> aiohttp.ClientResponse:
    data = {
        'amount': {
            'currencyCode': currencyCode,
            'amount': round(item[1]/1000, 2)
        },
        'description': item[0],
        # 'returnUrl': 'https://t.me/wallet',
        # 'failReturnUrl': 'https://t.me/wallet',
        'externalId': '7324-5355-' + ''.join([str(random.randint(0, 9)) for _ in range(4)]),
        'timeoutSeconds': timeout,
        'customerTelegramUserId': user_id
    }
    headers = {
        'Wpay-Store-Api-Key': '0YzKF2xlOVXIxotj5EtF86APbFWMxhUtrbQw',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post('https://pay.wallet.tg/wpay/store-api/v1/order', headers=headers, json=data) as resp:
            return await resp.json()
            

def dt_repr(dt_value: int | float) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt_value))