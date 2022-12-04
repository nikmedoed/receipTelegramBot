from aiogram import types, filters, Bot, Dispatcher
from aiogram.types import BotCommand, bot_command_scope
from aiogram.utils.callback_data import CallbackData
from ..routine import broadcasting
from ..utils.aiogram_redis_ext import RedisStorage2ext
from ..utils.config_types import Config

from telegram.texts import Text


async def set_bot_commands(bot: Bot):
    commands = [BotCommand(command=k.name, description=k.value) for k in Text.commands]
    commands = [BotCommand(command=k, description=i) for k, i in Text.commands_admin] + commands
    await bot.set_my_commands(
        commands,
        scope=bot_command_scope.BotCommandScopeAllPrivateChats()
    )


async def forward_from_admin_reply(message: types.Message):
    await message.forward(message.reply_to_message.forward_from.id)


async def forward_to_admin(message: types.Message, storage: RedisStorage2ext):
    config: Config = message.bot.get("config")
    await message.answer(Text.general.forward_to_admin)
    await message.forward(config.admin_id)


AdminBrodCastConfirm = CallbackData("admin_broadcast_message_confirm", "message_id")


async def broadcast_message_confirm(message: types.Message, storage: RedisStorage2ext):
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(*[
        types.InlineKeyboardButton(
            a[0],
            callback_data=AdminBrodCastConfirm.new(message_id=a[1])
        ) for a in [("No", -1), ("Yes", message.message_id)]
    ])
    await message.reply(Text.admin.broadcast_message_confirm, reply_markup=keyboard)


async def admin_broadcast_message(query: types.CallbackQuery, storage: RedisStorage2ext, callback_data: dict):
    if callback_data["message_id"] == '-1':
        await query.answer(Text.admin.broadcast_message_confirm_no)
        await query.message.reply_to_message.delete()
    else:
        await query.answer(Text.admin.broadcast_message_confirm_yes)
        await broadcasting.broadcast_message(query.message.reply_to_message, storage)
    await query.message.delete()


async def register(dp: Dispatcher):
    await set_bot_commands(dp.bot)

    dp.register_message_handler(forward_from_admin_reply,
                                filters.IsReplyFilter(True),
                                content_types=types.ContentTypes.ANY,
                                admin=True)
    dp.register_message_handler(broadcast_message_confirm,
                                content_types=types.ContentTypes.ANY, admin=True)
    dp.register_callback_query_handler(admin_broadcast_message, AdminBrodCastConfirm.filter())
    dp.register_message_handler(forward_to_admin,
                                content_types=types.ContentTypes.ANY)
