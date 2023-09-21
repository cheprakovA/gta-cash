import uuid

from aiogram import F, Bot, Router
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..db.interaction import add_order, get_item

from ..db.entities import OrderData
from ..states import InputOrderData
from ..utils import DATA_DIR, WALLET_KEY
from ..kb import payment_kb, platforms_kb
from ..wallet.entities import OrderPreview, PaymentRequest, WalletResponse
from ..wallet.interaction import send_payment_request
from ..wallet.webhook_manager import WebhookManager


wm = WebhookManager(api_key=WALLET_KEY)
router = Router()


@router.callback_query(Text(startswith='item-id-'))
async def item_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(item=int(callback.data[8:]))
    await callback.message.answer('Choose your platform:', reply_markup=platforms_kb())
    await state.set_state(InputOrderData.get_platform)



@router.callback_query(InputOrderData.get_platform)
async def get_username(callback: CallbackQuery, state: FSMContext):
    await state.update_data(platform=callback.data)
    await callback.message.answer('Enter your username:')
    await state.set_state(InputOrderData.get_username)



@router.message(InputOrderData.get_username)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Enter your password:')
    await state.set_state(InputOrderData.get_password)



@router.message(InputOrderData.get_password)
async def get_recovery_codes(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Enter your recovery codes:')
    await state.set_state(InputOrderData.get_recovery_codes)



@router.message(InputOrderData.get_recovery_codes, F.photo)
async def recovery_codes_as_image(message: Message, bot: Bot, state: FSMContext):
    largest = message.photo[-1]
    user_id = message.from_user.id
    file_nm = f'{largest.file_unique_id}.jpg'

    await bot.download(largest, destination=DATA_DIR / file_nm)
    await state.update_data(recovery_codes=file_nm)
    
    data = await state.get_data()
    item_id = data.pop('item')
    item = await get_item(item_id)
    external_id = uuid.uuid4()

    request = PaymentRequest(amount=0.01,
                             customerTelegramUserId=user_id, 
                             description=item[0],
                             externalId=external_id,
                             customData=str(user_id))
    
    response = await send_payment_request(request)

    order = OrderData(id=response.data.id,
                      user_id=user_id,
                      item_id=item_id,
                      externalId=external_id,
                      user_data=data,
                      status=response.data.status,
                      number=response.data.number,
                      amount=response.data.amount,
                      createdDateTime=response.data.createdDateTime,
                      expirationDateTime=response.data.expirationDateTime)
    
    print(order)
    print(tuple(order))
    
    await message.answer('pls pay:', reply_markup=payment_kb(response.data.directPayLink))
    await add_order(order)
    await state.clear()





@router.message(InputOrderData.get_recovery_codes, F.text)
async def recovery_codes_as_text(message: Message, state: FSMContext):
    await state.update_data(recovery_codes=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    item_id = data.pop('item')
    item = await get_item(item_id)
    external_id = uuid.uuid4()

    request = PaymentRequest(amount=0.01, 
                             customerTelegramUserId=user_id,
                             externalId=external_id,
                             description=item[0],
                             customData='some custom data')
    
    response: WalletResponse[OrderPreview] = await send_payment_request(request)

    order = OrderData(id=response.data.id,
                      user_id=user_id,
                      item_id=item_id,
                      externalId=external_id,
                      user_data=data,
                      status=response.data.status,
                      number=response.data.number,
                      amount=response.data.amount,
                      createdDateTime=response.data.createdDateTime,
                      expirationDateTime=response.data.expirationDateTime)
    
    print(order)
    print(tuple(order))
    
    await add_order(order)

    await state.set_state(InputOrderData.process_payment)

    await message.answer('pls pay:', reply_markup=payment_kb(response.data.directPayLink))
    await state.clear()