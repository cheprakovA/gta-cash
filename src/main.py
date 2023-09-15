import asyncio
from functools import partial
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


from handlers.commands_handler import router as commands_router
from handlers.user_data_handler import router as user_data_router
from handlers.events_handler import successful_event, failed_event

from utils import BOT_TOKEN, WALLET_KEY
from wallet.webhook_manager import WebhookManager


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    wm = WebhookManager(api_key=WALLET_KEY)

    dp.include_router(commands_router)
    dp.include_router(user_data_router)

    wm.successful_handler(partial(successful_event, bot=bot))
    wm.failed_handler(partial(failed_event, bot=bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())