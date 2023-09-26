import asyncio
from functools import partial
import logging
import sys

from aiohttp import web

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from .config import load_config

from .handlers.commands_handler import router as commands_router
from .handlers.user_data_handler import router as user_data_router
from .handlers.events_handler import successful_event, failed_event
from .db.interaction import create_tables

from .utils import (
    BASE_WEBHOOK_URL, 
    BOT_TOKEN, 
    WEBHOOK_PATH, 
    WEBHOOK_SECRET,
    WEB_SERVER_HOST, 
    WEB_SERVER_PORT
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
    )



async def main():    
    # create_tables()
    config = load_config()
    
    # if config.tg_bot.use_redis:
    #     storage = RedisStorage.from_url(
    #         url=f"redis://{config.redis.host}",
    #         connection_kwargs={
    #             "db": config.redis.db,
    #         },
    #         key_builder=DefaultKeyBuilder(with_destiny=True),
    #     )
    # else:
    #     storage = MemoryStorage()
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(commands_router)
    dp.include_router(user_data_router)
    
    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    
    logger.info('starting bot')

    try:
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    finally:
        # await dp.fsm.storage.close()
        # await bot.session.close()
        pass
        


def launch():    
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('shutting down bot')


if __name__ == '__main__':
    launch()