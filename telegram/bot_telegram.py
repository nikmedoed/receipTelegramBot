import logging
import asyncio
from aiogram import Bot, Dispatcher
from telegram.utils.aiogram_redis_ext import RedisStorage2ext

from .handlres_main import register_routers
from .middleware import register_middleware
from .utils.config_types import Config
from .utils.updatesworker import get_handled_updates_list
from telegram.routine.bot_startup_action import bot_startup_action


async def main(config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    storage = RedisStorage2ext(**config.redis_conf.__dict__)

    bot = Bot(config.bot_token, parse_mode="HTML")

    bot["config"]: Config = config
    bot["storage"] = storage

    loop = asyncio.get_running_loop()
    dp = Dispatcher(bot, loop=loop, storage=storage)

    await register_middleware(dp)
    await register_routers(dp)
    try:
        await bot_startup_action(dp)
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


def main_run(config):
    try:
        asyncio.run(main(config))
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
