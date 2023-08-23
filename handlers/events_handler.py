import time
import uuid

from aiogram import F, Bot, Router
import db
from db.entities import TempOrder, UserData
from states import InputOrderData
from utils import DATA_DIR, WALLET_KEY

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from WalletPay import WalletPayAPI, WebhookManager, AsyncWalletPayAPI
from WalletPay.types import Event



router = Router()




