from aiogram import types, Dispatcher, filters
from telegram.texts import Text
from ..utils.receip_parsers.receip_types import ReceipParser


async def good_link_processing(message: types.Message, parser: ReceipParser):
    receip = await parser.parse(message.text)
    await message.reply_document(
        (
            Text.main.filename.value.format(receip=receip),
            receip.save_virtual_xlsx()
        ),
        caption=Text.main.your_file.value.format(receip=receip)
    )


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
