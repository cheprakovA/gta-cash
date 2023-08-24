from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.enums import Platform

from db.interaction import get_items



def menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='📑 Catalog', callback_data='get_catalog'),
        InlineKeyboardButton(text='🛒 Orders',  callback_data='get_orders')
    )
    builder.row(
        InlineKeyboardButton(text='💬 Support', url='https://t.me/JorgeSupport'),
        InlineKeyboardButton(text='⭐ Reviews', url='https://t.me/+7EdFvKHQhd8xZTli')
    )
    builder.row(InlineKeyboardButton(text='🤝🏻 Referral',
                                     callback_data='get_referal_link'))
    return builder.as_markup()


def platforms_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=Platform.PS4, callback_data='ps4'))
    builder.add(InlineKeyboardButton(text=Platform.PS5, callback_data='ps5'))
    builder.add(InlineKeyboardButton(text=Platform.XBOXONE, callback_data='xboxone'))
    builder.add(InlineKeyboardButton(text=Platform.XBOXSEX, callback_data='xboxsex'))
    builder.add(InlineKeyboardButton(text='🎮 Menu', callback_data='main_menu'))
    return builder.adjust(2, 2, 1).as_markup()


def payment_kb(link: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='👛 Pay via Wallet', url=link)],
        [InlineKeyboardButton(text='🎮 Menu', callback_data='main_menu')],
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
    buttons.append([InlineKeyboardButton(text='🎮 Menu', 
                                         callback_data='main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


