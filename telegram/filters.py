import typing
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from telegram.utils.aiogram_redis_ext import RedisStorage2ext
from telegram.utils.constants import StorageKeys


class AdminFilter(BoundFilter):
    key = 'admin'

    def __init__(self, admin: typing.Optional[bool] = None):
        self.admin = admin

    async def check(self, message: types.Message) -> bool:
        if self.admin is None:
            return True
        return message.bot.get("config").admin_id == message.from_user.id
        # ) == self.admin


class IsUserFilter(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, message: types.Message) -> bool:
        if self.is_user is None:
            return True
        storage: RedisStorage2ext = message.bot.get("storage")
        user_url = await storage.get_key(StorageKeys.PREVIOUS_MESSAGE_DATE, user=message.from_user.id)
        return self.is_user == bool(user_url)
