import time

from aiogram import Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text, CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext

import db
import kb
from states import InputOrderData
import text

from utils import dt_repr, PLATFORMS


router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message):
    if not await db.user_exists(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.username, 
                          message.from_user.language_code)
    answ = text.SALUTATION_MESSAGE.format(name=message.from_user.first_name) + \
        '\n' + text.HELP_MESSAGE
    await message.answer(answ, reply_markup=kb.menu_kb())



@router.callback_query(Text('main_menu'))
async def catalog_handler(callback: CallbackQuery):
    await callback.message.answer(
        text.SALUTATION_MESSAGE.format(name=callback.from_user.first_name), 
        reply_markup=kb.menu_kb()
    )



# @router.message(Command('catalog'))
# async def cmd_catalog(message: Message):
#     catalog = await kb.catalog_kb()
#     await message.answer('Catalog:', reply_markup=catalog)



@router.callback_query(Text('get_catalog'))
async def catalog_handler(callback: CallbackQuery):
    # if not await db.user_platform_specified(callback.from_user.id):
    #     await platforms_handler(callback)
    catalog = await kb.catalog_kb()
    await callback.message.answer('Catalog:', reply_markup=catalog)



@router.callback_query(Text('get_platforms'))
async def platforms_handler(callback: CallbackQuery):
    await callback.message.answer('Choose your platform:', reply_markup=kb.platforms_kb())



# @router.message(Command('help'))
# async def cmd_help(message: Message):
#     await message.answer(text.HELP_MESSAGE)



# @router.callback_query(Text('help'))
# async def get_help(callback: CallbackQuery):
#     await callback.answer(text.HELP_MESSAGE)



# @router.message(Command('orders'))
# async def cmd_orders(message: Message):
#     orders = await db.get_user_orders(message.from_user.id)
#     pending = [_ for _ in orders if not _[2]]
#     completed = [_ for _ in orders if _[2]]
#     answ = ''
#     if pending:
#         pending_orders = '\n'.join([f'• {p[0]} since {dt_repr(p[1])}' 
#                                     for p in pending])
#         answ += text.PENDING_ORDERS_TEMPLATE.format(pending=pending_orders)
#     answ += '\n\n' if answ else ''
#     if completed:
#         completed_orders = '\n'.join([f'• {c[0]} at {dt_repr(c[2])}' 
#                                       for c in completed])
#         answ += text.COMPLETED_ORDERS_TEMPLATE.format(completed=completed_orders)
#     await message.answer(answ if answ else text.EMPTY_ORDER_LIST_MESSAGE)



@router.callback_query(Text('get_orders'))
async def orders_handler(callback: CallbackQuery):
    orders = await db.get_user_orders(callback.from_user.id)
    pending = [_ for _ in orders if not _[2]]
    completed = [_ for _ in orders if _[2]]
    answ = ''
    if pending:
        pending_orders = '\n'.join(
            ['<pre>{:<19}{:>19}</pre>'.format(p[0] + ' CASH', dt_repr(p[1]))
             for p in pending]
        )
        answ += text.PENDING_ORDERS_TEMPLATE.format(pending=pending_orders)
    answ += '\n\n' if answ else ''
    if completed:
        completed_orders = '\n'.join(
            ['<pre>{:<19}{:>19}</pre>'.format(c[0] + ' CASH', dt_repr(c[2]))
             for c in completed]
        )
        answ += text.COMPLETED_ORDERS_TEMPLATE.format(completed=completed_orders)
    await callback.message.answer(answ or text.EMPTY_ORDER_LIST_MESSAGE, 
                                  parse_mode=ParseMode.HTML)



@router.callback_query(Text(startswith='item-id-'))
async def item_handler(callback: CallbackQuery, state: FSMContext):
    await db.add_order(callback.from_user.id, 
                       int(callback.data[8:]),
                       int(time.time()))
    await callback.message.answer('Choose your platform:', reply_markup=kb.platforms_kb())
    await state.set_state(InputOrderData.enter_platform)



@router.callback_query(InputOrderData.enter_platform)
async def got_username(callback: CallbackQuery, state: FSMContext):
    # await db.update_user_platform(callback.from_user.id, callback.)
    await callback.message.answer('Enter your username:')
    await state.set_state(InputOrderData.enter_username)



@router.message(InputOrderData.enter_username)
async def got_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Enter your password:')
    await state.set_state(InputOrderData.enter_password)



@router.message(InputOrderData.enter_password)
async def got_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Enter your recovery codes:')
    await state.set_state(InputOrderData.enter_recovery_codes)



@router.message(InputOrderData.enter_recovery_codes)
async def got_recovery_codes(message: Message, state: FSMContext):
    data = await state.get_data()
    data['recovery_codes'] = message.text
    print(data)
    await state.clear()



@router.callback_query(Text(startswith='platform-'))
async def platform_handler(callback: CallbackQuery):
    await db.update_user_platform(callback.from_user.id, callback.data[9:])
    await callback.answer()



# @router.message()
# async def echo_message(message: Message):
#     await message.answer(message.from_user.id, message.text)