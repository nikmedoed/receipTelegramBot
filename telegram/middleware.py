import datetime
import logging
from typing import Union

from aiogram import types, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.utils.exceptions import MessageError
from telegram.utils.aiogram_redis_ext import RedisStorage2ext
from telegram.utils.constants import StorageKeys


class ActivityMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update", "edited", "pool", "member"]

    async def pre_process(self, obj: Union[types.Message, types.CallbackQuery], data, *args):
        try:
            storage: RedisStorage2ext = obj.bot["storage"]
            await storage.set_key(
                key=StorageKeys.PREVIOUS_MESSAGE_DATE,
                user=obj.from_user.id,
                value=round(datetime.datetime.now().timestamp())
            )
            data["storage"] = storage
        except MessageError as e:  # MessageNotModified
            logging.error(f"ActivityMiddleware - {e.__class__}: {e.text}")


async def register_middleware(dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ActivityMiddleware())
