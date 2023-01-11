from telegram.utils.receip_parsers import ReceipParser
from telegram.utils.texts_enum import EnumContent


class Commands(EnumContent):
    start = "запустить бота",
    help = "список команд",
    privacy = "о хранении данных"


class General(EnumContent):
    bot_started = "Бот запустился или перезапустился"
    help = (
               "Этот бот конвертирует ссылки на чеки в таблицу\n"
               "Просто перешли сюда ссылку из браузера. "
               "Лишний текст проигнорируется, важно наличие ссылки. "
               "Можно использовать функцию 'Поделиться' в браузере.\n"
               "\n"
               "На данный момент бот распознаёт чеки следующих вендоров:\n"
               "- {}\n"
               "\n"
               "Команды бота:\n"
               "{}\n"
               "\n"
               "Если бот работает некорректно, писать @nikmedoed\n\n"
               "<a href='https://gist.github.com/nikmedoed/119abe998466e2c05376768f97363e61'>"
               "Список способов поддержать проекты монетой</a>"
           ).format('\n- '.join(ReceipParser.get_all_vendors()),
                    '\n'.join([f'/{k.name} - {k}' for k in Commands])),
    privacy = ("Бот хранит только ваш id, чтобы понимать количество пользователей."
               ""),
    forward_to_admin = "Не получилось обработать сообщение, переслал @nikmedoed"


class Main(EnumContent):
    start = ("Привет!\n\n"
             "Бот конвертирует ссылки на чеки в таблицу.\n"
             "Подробнее о работе бота: /help")
    unknown = ("Не знаю как обработать эту ссылку.\n\n"
               "Подробнее о работе бота: /help")
    your_file = ("<b>Чек распознан</b>\n"
                 "<code>Вендор :: </code> {receip.vendor}\n"
                 "<code>Валюта :: </code> {receip.currency}\n"
                 "<code>Сумма :: </code> {receip.amount}\n"
                 "<code>Дата :: </code> {receip.date}\n"
                 "<code>Количество продуктов :: </code> {receip.volume}\n"
                 "<a href='{receip.link}'>Ссылка</a>\n")
    filename = ("{receip.date:%Y-%m-%d}"
                "_{receip.volume}шт"
                "_{receip.amount:.0f}"
                "_{receip.country}"
                "_{receip.vendor}"
                ".xlsx")
    error_parse = ("Не получилось загрузить данные")
    error_file = ("Не получилось создать файл")
    error_send = ("Не получилось отправить файл")


class CommandsAdmin(EnumContent):
    pass


class Admin(EnumContent):
    broadcast_message_confirm = "Разослать всем это сообщение?"
    broadcast_message_confirm_no = "Рассылка отменена"
    broadcast_message_confirm_yes = "Рассылка начата"


class Misc(EnumContent):
    eyes = "🧐 👀 👁 👁‍🗨 🙄".split()


class Text:
    general = General
    commands = Commands
    main = Main
    admin = Admin
    commands_admin = CommandsAdmin
    misc = Misc


if __name__ == "__main__":
    print(
        Text.general.help,
        sep="\n====\n"
    )
