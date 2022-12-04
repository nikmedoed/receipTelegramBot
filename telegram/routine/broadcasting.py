from aiogram_broadcaster import MessageBroadcaster, TextBroadcaster
from aiogram import types
from typing import Union, List
from aiogram import Bot
import asyncio


from telegram.utils.aiogram_redis_ext import RedisStorage2ext
from telegram.utils.constants import StorageKeys


async def broadcast_message(message: types.Message, storage: RedisStorage2ext,
                            users: Union[None, List[int]] = None):
    if not users:
        users = await storage.get_all_users(StorageKeys.PREVIOUS_MESSAGE_DATE)
    try:
        if message.poll:
            for user in users:
                await message.forward(user)
                await asyncio.sleep(.05)
        else:
            await MessageBroadcaster(users, message).run()
    except Exception as e:
        await message.reply(f"Error in broadcasting for {len(users)} users: <code>{e}</code>")

    users_list = ",\n".join([str(u) for u in users])
    await message.reply(f"Broadcasting for {len(users)} users success, users list:\n<code>{users_list}</code>")


async def broadcast_admin(bot: Bot, text: str, **params):
    config = bot.get("config")
    return await bot.send_message(config.admin_id, text, **params)
