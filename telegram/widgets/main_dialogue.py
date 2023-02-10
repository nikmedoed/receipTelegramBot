import asyncio
import logging

from aiogram import types, Dispatcher, filters
from telegram.texts import Text
from ..utils.receip_parsers.receip_types import ReceipParser


# TODO если ошибки парсинга будут не из-за скорости скана, то добавить кнопку повторить,
# которая будет перебирать шаблоны для текста из сообщения реплая.
async def good_link_processing(message: types.Message, parser: ReceipParser):
    err = Text.main.error_parse
    attempts = 0
    try:
        while 1:
            try:
                receip = await parser.parse(message.text)
                break
            except Exception as error:
                attempts += 1
                await asyncio.sleep(5)
                if attempts > 5:
                    raise error
        err = Text.main.error_file
        file = receip.save_virtual_xlsx()
        err = Text.main.error_send
        mess = await message.reply_document(
            (Text.main.filename.value.format(receip=receip), file),
            caption=Text.main.your_file.value.format(receip=receip)
        )
        await mess.reply("\n".join(
            [f'{item.name} - {item.cost}' +
             ("" if item.quantity == 1 else f" ({item.price}*{item.quantity:.2f})") for
             item in receip.items]))
    except Exception as error:
        await message.reply(err)
        logging.error(error)


def processor_generator(parser: ReceipParser):
    async def temp(message: types.Message):
        return await good_link_processing(message, parser)

    return temp


async def unknown_link(message: types.Message):
    await message.reply(Text.main.unknown)


async def start_dialogue(message: types.Message):
    await message.answer(Text.main.start)
    await message.answer(Text.general.help)


def register(dispatcher: Dispatcher):
    for parser in ReceipParser.parsers():
        dispatcher.register_message_handler(
            processor_generator(parser()),
            # filters.Regexp(rf'.*{parser.templateRegStr}*' )
            filters.Regexp(parser.templateRegStr)
        )

    dispatcher.register_message_handler(
        unknown_link,
        filters.Regexp(r'https:\/\/\S+')
    )
    dispatcher.register_message_handler(
        start_dialogue,
        filters.CommandStart()
    )
