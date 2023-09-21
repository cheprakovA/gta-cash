import asyncio
from functools import partial
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from .config import load_config

from .handlers.commands_handler import router as commands_router
from .handlers.user_data_handler import router as user_data_router
from .handlers.events_handler import successful_event, failed_event
from .db.interaction import create_tables

from .utils import BOT_TOKEN, WALLET_KEY
from .wallet.webhook_manager import WebhookManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():    
    # create_tables()
    config = load_config()
    
    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(
            url=f"redis://{config.redis.host}",
            connection_kwargs={
                "db": config.redis.db,
            },
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    
    # wm = WebhookManager(api_key=WALLET_KEY)

    dp.include_router(commands_router)
    dp.include_router(user_data_router)

    # wm.successful_handler(partial(successful_event, bot=bot))
    # wm.failed_handler(partial(failed_event, bot=bot))

    logger.info('starting bot')
    # asyncio.create_task(wm.start())

    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, config=config)
    finally:
        await dp.fsm.storage.close()
        await bot.session.close()
        


def launch():    
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('shutting down bot')


if __name__ == '__main__':
    launch()