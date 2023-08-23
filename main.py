import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import db

from utils import BOT_TOKEN, APP_BASE_URL, WALLET_KEY
from WalletPay import WalletPayAPI, WebhookManager, AsyncWalletPayAPI
from WalletPay.types import Event


manager = WebhookManager(client=WalletPayAPI(api_key=WALLET_KEY))
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)


# @manager.successful_handler
# async def handle_successful_event(event: Event):
#     user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
#     await bot.send_message(chat_id=user_id, 
#                            text=f'Your payment for order {event.payload.order_id} was successful!')
#     await db.utils.update_order(event.payload.order_id, event.payload.order_completed_datetime)



# @manager.failed_handler
# async def handle_failed_event(event: Event):
#     user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
#     await bot.send_message(chat_id=user_id, 
#                            text=f'Your payment for order {event.payload.order_id} timed out!')
#     # await db.utils.update_order(event.payload.order_id, event.payload.order_completed_datetime)


# @manager.successful_handler
# async def handle_successful_event(event: Event):
#     user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
#     await bot.send_message(chat_id=user_id, 
#                            text=f'Your payment for order {event.payload.order_id} was successful!')
#     await db.utils.update_order(event.payload.order_id, event.payload.order_completed_datetime)


# @manager.failed_handler
# async def handle_failed_event(event: Event):
#     user_id = await db.utils.get_user_id_by_ext_id(event.payload.external_id)
#     await bot.send_message(chat_id=user_id, 
#                            text=f'Your payment for order {event.payload.order_id} timed out!')
    # await db.utils.update_order(event.payload.order_id, event.payload.order_completed_datetime)


dispatcher = Dispatcher(storage=MemoryStorage())



# async def on_startup():
#     await bot.send_message(chat_id=637622249, text="Bot has started!")
#     # Start the webhook manager in the background
#     asyncio.create_task(manager.start())


# async def on_shutdown():
#     await bot.send_message(chat_id=637622249, text="Bot is shutting down!")



async def main():
    

    # dispatcher['base_url'] = APP_BASE_URL
    # dispatcher.startup.register(on_startup)
    # dispatcher.shutdown.register(on_shutdown)
    
    from handlers.commands_handlers import router
    dispatcher.include_router(router)
    
    # app = Application()
    # app['bot'] = bot

    # app.router.add_get('/payment_webhook', demo_handler)
    
    # SimpleRequestHandler(dispatcher=dispatcher, 
    #                      bot=bot).register(app, path='/webhook')
    # setup_application(app, dispatcher, bot=bot)

    # run_app(app, host='127.0.0.1', port=8081)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())