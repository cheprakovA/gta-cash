import asyncio
from functools import partial
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


from handlers.commands_handler import router as commands_router
from handlers.user_data_handler import router as user_data_router
from handlers.events_handler import successful_event, failed_event
from db.interaction import create_tables

from utils import BOT_TOKEN, WALLET_KEY
from wallet.webhook_manager import WebhookManager


async def main():
    create_tables()
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    wm = WebhookManager(api_key=WALLET_KEY)

    dp.include_router(commands_router)
    dp.include_router(user_data_router)

    wm.successful_handler(partial(successful_event, bot=bot))
    wm.failed_handler(partial(failed_event, bot=bot))

    logging.info('Bot has started')
    asyncio.create_task(wm.start())

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot is shutting down')
        sys.exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())