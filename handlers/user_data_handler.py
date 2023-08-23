import time
import uuid

from aiogram import F, Bot, Router
import db
from db.entities import TempOrder, UserData
from states import InputOrderData
from utils import DATA_DIR, WALLET_KEY
from kb import payment_kb, platforms_kb

from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from WalletPay import AsyncWalletPayAPI


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
    image_nm = f'{largest.file_unique_id}.jpg'
    await bot.download(largest, destination=DATA_DIR / image_nm)
    data = await state.get_data()
    external_id = str(uuid.uuid4())
    item_id = data['item']
    item = await db.utils.get_item(item_id)
    
    # response = await send_payment_rq(user_id, item)
    
    order = AsyncWalletPayAPI(api_key=WALLET_KEY).create_order(
        amount=item[1],
        currency_code='USD',
        description=item[0],
        external_id=external_id,
        timeout_seconds=10800,    
        customer_telegram_user_id=user_id,
        return_url='https://t.me/MedellinCartelBoostBot',
        fail_return_url='https://t.me/wallet'
    )

    ud = UserData(data['platform'], data['username'], 
                  data['password'], image_nm)
    to = TempOrder.from_dict(order.__dict__)
    
    await db.utils.add_order(user_id, item_id, external_id, ud, to)
    await message.answer('Pls pay:', reply_markup=payment_kb(to.direct_pay_link))
    await state.clear()


@router.message(InputOrderData.enter_recovery_codes, F.text)
async def recovery_codes_as_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    order_dt = int(time.time())
    data = await state.get_data()
    recovery_codes = '|'.join(message.text.split('\n'))

    await db.utils.add_order(user_id, 
                       data['platform'], 
                       UserData(data['username'], 
                                data['password'], 
                                recovery_codes),
                       data['item'], 
                       order_dt)

    print(data)
    await state.clear()