from dataclasses import asdict
import time
from typing import Literal
import uuid
import ujson

from aiogram import F, Bot, Router
import aiohttp
import db.interaction
from db.entities import TempOrder, UserData
from states import InputOrderData
from utils import DATA_DIR, WALLET_KEY
from kb import payment_kb, platforms_kb

from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from WalletPay import AsyncWalletPayAPI

from wallet.entities import MoneyAmount, PaymentRequest
from wallet.interaction import send_payment_request
# from utils import send_payment_rq


router = Router()


@router.callback_query(Text(startswith='item-id-'))
async def item_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(item=int(callback.data[8:]))
    await callback.message.answer('Choose your platform:', reply_markup=platforms_kb())
    await state.set_state(InputOrderData.enter_platform)



@router.callback_query(InputOrderData.enter_platform)
async def get_username(callback: CallbackQuery, state: FSMContext):
    await state.update_data(platform=callback.data)
    await callback.message.answer('Enter your username:')
    await state.set_state(InputOrderData.enter_username)



@router.message(InputOrderData.enter_username)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Enter your password:')
    await state.set_state(InputOrderData.enter_password)



@router.message(InputOrderData.enter_password)
async def get_recovery_codes(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Enter your recovery codes:')
    await state.set_state(InputOrderData.enter_recovery_codes)



@router.message(InputOrderData.enter_recovery_codes, F.photo)
async def recovery_codes_as_image(message: Message, bot: Bot, state: FSMContext):
    largest = message.photo[-1]
    user_id = message.from_user.id
    await bot.download(largest, 
                       destination=DATA_DIR / f'{largest.file_unique_id}.jpg')
    data = await state.get_data()
    item_id = data['item']
    item = await db.interaction.get_item(item_id)

    request = PaymentRequest(amount=MoneyAmount(0.02), 
                             customerTelegramUserId=user_id, 
                             description=item[0],
                             customData='some custom data')
    
    response = await send_payment_request(request)

    print(response)
    
    # api = AsyncWalletPayAPI(api_key=WALLET_KEY)

    # order = await api.create_order(
    #     amount=0.05, # item[1]
    #     currency_code='USD',
    #     description=item[0],
    #     external_id=external_id,
    #     timeout_seconds=10800,    
    #     customer_telegram_user_id=user_id,
    #     return_url='https://t.me/MedellinCartelBoostBot',
    #     fail_return_url='https://t.me/wallet'
    # )

    # print(order.__dict__)
    # print(str(order))

    # ud = UserData(data['platform'], data['username'], 
    #               data['password'], image_nm)
    # to = TempOrder.from_dict()
    
    # await db.utils.add_order(user_id, item_id, external_id, ud, to)

    await message.answer('pls pay:', reply_markup=payment_kb(response.data.directPayLink))
    await state.clear()


@router.message(InputOrderData.enter_recovery_codes, F.text)
async def recovery_codes_as_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    order_dt = int(time.time())
    data = await state.get_data()
    recovery_codes = '|'.join(message.text.split('\n'))

    await db.interaction.add_order(user_id, 
                       data['platform'], 
                       UserData(data['username'], 
                                data['password'], 
                                recovery_codes),
                       data['item'], 
                       order_dt)

    print(data)
    await state.clear()
