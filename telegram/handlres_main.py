import logging

from aiogram import types, filters, Bot, Dispatcher
from aiogram.types import BotCommand, bot_command_scope
from aiogram.utils.exceptions import TelegramAPIError, MessageNotModified, CantParseEntities

from telegram.texts import Text
from .filters import AdminFilter, IsUserFilter
from .widgets import (
    main_dialogue,
    admin
)


async def set_bot_commands(bot: Bot):
    commands = [BotCommand(command=k.name, description=k.value) for k in Text.commands]
    await bot.set_my_commands(
        commands,
        scope=bot_command_scope.BotCommandScopeAllPrivateChats()
    )


async def cmd_help(message: types.Message):
    await message.answer(Text.general.help)


async def cmd_privacy(message: types.Message):
    await message.answer(Text.general.privacy)


async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, TelegramAPIError):  # MUST BE THE  LAST CONDITION
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    logging.exception(f'Update: {update} \n{exception}')


async def register_routers(dp: Dispatcher):
    await set_bot_commands(dp.bot)

    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsUserFilter)

    main_dialogue.register(dp)

    dp.register_message_handler(cmd_help, filters.CommandHelp())
    dp.register_message_handler(cmd_privacy, filters.CommandPrivacy())

    # await admin.register(dp)

    dp.register_message_handler(cmd_help, state=None)
    dp.register_errors_handler(errors_handler)
