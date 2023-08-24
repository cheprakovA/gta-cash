from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, CommandStart
from aiogram.filters.command import CommandObject
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.deep_linking import create_start_link, decode_payload

import db.interaction
import kb
import text


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    reference = decode_payload(command.args or '') or None
    user = message.from_user
    if not await db.interaction.user_exists(user.id):
        await db.interaction.add_user(user.id, user.username, 
                                      user.language_code, reference)
    answ = text.SALUTATION_MESSAGE.format(name=message.from_user.first_name) + \
        '\n' + text.HELP_MESSAGE
    await message.answer(answ, reply_markup=kb.menu_kb())



@router.callback_query(Text('main_menu'))
async def main_menu_handler(callback: CallbackQuery):
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
    catalog = await kb.catalog_kb()
    await callback.message.answer('Catalog:', reply_markup=catalog)



@router.callback_query(Text('get_platforms'))
async def platforms_handler(callback: CallbackQuery):
    await callback.message.answer('Choose your platform:', reply_markup=kb.platforms_kb())


@router.callback_query(Text('get_referal_link'))
async def referal_link_handler(callback: CallbackQuery, bot: Bot):
    link = await create_start_link(bot, 
                                   payload=str(callback.from_user.id) or '', 
                                   encode=True)
    await callback.message.answer(f'Tap to copy your referal:\n\n`{link}`', 
                                  parse_mode=ParseMode.MARKDOWN_V2)



# @router.message(Command('help'))
# async def cmd_help(message: Message):
#     await message.answer(text.HELP_MESSAGE)



# @router.callback_query(Text('help'))
# async def get_help(callback: CallbackQuery):
#     await callback.answer(text.HELP_MESSAGE)



# @router.message(Command('orders'))
# async def cmd_orders(message: Message):
#     orders = await db.utils.get_user_orders(message.from_user.id)
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



# @router.callback_query(Text('get_orders'))
# async def orders_handler(callback: CallbackQuery):
#     orders = await db.utils.get_user_orders(callback.from_user.id)
#     pending = [_ for _ in orders if not _[2]]
#     completed = [_ for _ in orders if _[2]]
#     answ = ''
#     if pending:
#         pending_orders = '\n'.join(
#             ['<pre>{:<19}{:>19}</pre>'.format(p[0] + ' CASH', dt_repr(p[1]))
#              for p in pending]
#         )
#         answ += text.PENDING_ORDERS_TEMPLATE.format(pending=pending_orders)
#     answ += '\n\n' if answ else ''
#     if completed:
#         completed_orders = '\n'.join(
#             ['<pre>{:<19}{:>19}</pre>'.format(c[0] + ' CASH', dt_repr(c[2]))
#              for c in completed]
#         )
#         answ += text.COMPLETED_ORDERS_TEMPLATE.format(completed=completed_orders)
#     await callback.message.answer(answ or text.EMPTY_ORDER_LIST_MESSAGE, 
#                                   parse_mode=ParseMode.HTML)


# @router.callback_query(Text(startswith='platform-'))
# async def platform_handler(callback: CallbackQuery):
#     await db.utils.update_user_platform(callback.from_user.id, callback.data[9:])
#     await callback.answer()



# @router.message()
# async def echo_message(message: Message):
#     await message.answer(message.from_user.id, message.text)