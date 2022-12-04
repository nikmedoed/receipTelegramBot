import typing

from aiogram.contrib.fsm_storage.redis import RedisStorage2


class RedisStorage2ext(RedisStorage2):
    async def get_key(self, key, *, chat: typing.Union[str, int, None] = None,
                      user: typing.Union[str, int, None] = None,
                      default: typing.Optional[dict] = None) -> typing.Optional[typing.Union[str, int, None]]:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, str(key))
        redis = await self._get_adapter()
        raw_result = await redis.get(key)
        return raw_result or default

    async def set_key(self, key, value, *, chat: typing.Union[str, int, None] = None,
                      user: typing.Union[str, int, None] = None):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, str(key))
        redis = await self._get_adapter()
        if value:
            await redis.set(key, str(value), ex=self._bucket_ttl)
        else:
            await redis.delete(key)

    async def get_all_users(self, key):
        key = self.generate_key("*", "*", str(key))
        redis = await self._get_adapter()
        keys = await redis.keys(key)
        return [k.split(":")[2] for k in keys]
