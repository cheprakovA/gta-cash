import time
from pathlib import Path


WORK_DIR = Path.cwd() / 'bot'

DATA_DIR = WORK_DIR.parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

DB_NAME = 'db.sqlite'
SCRIPT_PATH = WORK_DIR / 'db' / 'init_db.sql'
DB_PATH = WORK_DIR  / 'db' / DB_NAME

BOT_TOKEN = '6599454857:AAHJvVwp3pTa7Grn5rPJMYNavfN3wJbHxjs'
WALLET_KEY = '0YzKF2xlOVXIxotj5EtF86APbFWMxhUtrbQw'

WEB_SERVER_HOST = '127.0.0.1'
WEB_SERVER_PORT = 8080

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "pivo-rearm-pivo"

BASE_WEBHOOK_URL = "https://medellincartel.pw"

APP_BASE_URL = ''

ALLOWED_IPS = {'172.255.248.29', '172.255.248.12', '127.0.0.1'}
ADMIN_IDS = (6379289072,)

WALLET_API_URL = 'https://pay.wallet.tg/wpay/store-api/v1'
BOT_TG_URL = 'https://t.me/MedellinCartelBoostBot'
WALLET_TG_URL = 'https://t.me/wallet'

HEADERS = {'Wpay-Store-Api-Key': WALLET_KEY,
           'Content-Type': 'application/json',
           'Accept': 'application/json'}



            

def dt_repr(dt_value: int | float) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dt_value))