from aiogram import Bot

from ..db.interaction import update_order_payed
from ..wallet.entities import Event


async def successful_event(event: Event, bot: Bot):
    await bot.send_message(chat_id=event.payload.customData, 
                           text=f'Your payment for order {event.payload.id} was successful')
    await update_order_payed(event.payload.id, event.payload.status, 
                                            event.payload.orderCompletedDateTime)


async def failed_event(event: Event, bot: Bot):
    await bot.send_message(chat_id=event.payload.customData, 
                           text=f'Your payment for order {event.payload.id} failed')
    await update_order_payed(event.payload.id, event.payload.status, 
                                            event.payload.orderCompletedDateTime)


