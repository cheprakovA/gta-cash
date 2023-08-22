from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_items
from utils import PLATFORMS



def menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='📑 catalog', callback_data='get_catalog'),
        InlineKeyboardButton(text='🛒 orders',  callback_data='get_orders')
    )
    builder.row(
        InlineKeyboardButton(text='💬 support', url='https://t.me/JorgeSupport'),
        InlineKeyboardButton(text='⭐ reviews', url='https://t.me/+7EdFvKHQhd8xZTli')
    )
    return builder.as_markup()


def platforms_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for alias, text in PLATFORMS.items():
        builder.add(InlineKeyboardButton(text=text, callback_data=alias))
    builder.add(InlineKeyboardButton(text='🎮 menu', callback_data='main_menu'))
    return builder.adjust(2, 2, 1).as_markup()


def platform_change_kb(platform: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='🕹️ change platform', callback_data='get_platforms')],
        [InlineKeyboardButton(text='🎮 continue with ' + PLATFORMS[platform], 
                              callback_data='hui_znaet')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



async def catalog_kb() -> InlineKeyboardMarkup:
    items = await get_items()
    buttons = [
        [InlineKeyboardButton(text=f'💰{item[1]} CASH     ${item[2]}',
                              callback_data=f'item-id-{item[0]}')]
        for item in items
    ]
    # buttons.append([InlineKeyboardButton(text='🕹️ change platform', 
    #                                      callback_data='get_platforms')])
    buttons.append([InlineKeyboardButton(text='🎮 back to menu', 
                                         callback_data='main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


