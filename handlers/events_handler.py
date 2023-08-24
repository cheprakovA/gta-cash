import time
import uuid

from aiogram import F, Bot, Router
import db.interaction
from db.entities import TempOrder, UserData
from states import InputOrderData
from utils import DATA_DIR, WALLET_KEY

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from WalletPay import WalletPayAPI, WebhookManager, AsyncWalletPayAPI
from WalletPay.types import Event


manager = WebhookManager(client=WalletPayAPI(api_key=WALLET_KEY))


@manager.successful_handler
async def handle_successful_event(event: Event):
    # user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
    # await bot.send_message(chat_id=user_id, 
    #                        text=f'Your payment for order {event.payload.order_id} was successful!')
    await db.interaction.update_order_payed(event.payload.order_id, 
                                      event.payload.order_completed_datetime)



@manager.failed_handler
async def handle_failed_event(event: Event):
    # user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
    # await bot.send_message(chat_id=user_id, 
    #                        text=f'Your payment for order {event.payload.order_id} timed out!')
    # await db.utils.update_order(event.payload.order_id, event.payload.order_completed_datetime)
    pass


