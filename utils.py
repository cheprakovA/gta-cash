from dataclasses import asdict
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

DATA_DIR = WORK_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

SCRIPT_PATH = WORK_DIR / 'db' / 'init_db.sql'
DB_PATH = WORK_DIR  / 'db' / 'db.sqlite'


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

WALLET_API_URL = 'https://pay.wallet.tg/wpay/store-api/v1'
BOT_TG_URL = 'https://t.me/MedellinCartelBoostBot'
WALLET_TG_URL = 'https://t.me/wallet'

HEADERS = {'Wpay-Store-Api-Key': '0YzKF2xlOVXIxotj5EtF86APbFWMxhUtrbQw',
           'Content-Type': 'application/json',
           'Accept': 'application/json'}



            

def dt_repr(dt_value: int | float) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt_value))