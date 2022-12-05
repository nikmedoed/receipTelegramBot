import asyncio
import aiohttp
import re
import datetime
import telegram.texts as Text
from telegram.utils.receip_parsers.receip_types import ReceipLine, Receip, ReceipParser
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

KAZ_EXTRA_FIELDS = [
    'orgTitle',
    'retailPlaceAddress',
    'orgId',
    'kkmSerialNumber',
    'kkmFnsId'
]
KAZ_EXTRA_FIELDS_TICKET = ['transactionId', 'fiscalId', ]


class ReceipKazakhtelecom(ReceipParser):
    templateRegStr = r'https:\/\/consumer\.oofd\.kz\/ticket\/[-a-z0-9]+'
    name = 'Казахтелеком'

    def extract_link(self, message: str) -> str:
        return str(max(self.templateRegEx.findall(message), key=len))

    async def parser(self, link) -> Receip:
        if not self.templateRegEx.match(link):
            raise AssertionError("Link incorrect")
        reqLink = link.replace('ticket', r'api/tickets/ticket')
        async with aiohttp.ClientSession() as session:
            async with session.get(reqLink) as resp:
                ticket = await resp.json()
        currency = '₸'
        data = []
        for n, item in enumerate(ticket['ticket']['items']):
            item = item['commodity']
            data.append(ReceipLine(
                n,
                re.sub(r'\d{5,} ', '', item['name']),
                item['price'],
                item['quantity'],
                item['sum']
            ))
        extra = {i: ticket[i] for i in KAZ_EXTRA_FIELDS if ticket[i]}
        for i in KAZ_EXTRA_FIELDS_TICKET:
            ti = ticket['ticket'].get(i)
            if ti:
                extra[i] = ti
        return Receip(
            datetime.datetime.fromisoformat(ticket['ticket']['transactionDate']),
            link,
            currency,
            self.name,
            data,
            extra
        )


if __name__ == "__main__":
    t = ReceipKazakhtelecom()
    link = 'Казахтелеком\nhttps://consumer.oofd.kz/ticket/aadb79f8-a8cf-4b02-bc1e-8d8361575bd0'
    link = max(t.templateRegEx.findall(link), key=len)
    receip = asyncio.get_event_loop().run_until_complete(t.parser(link))
    print(Text.Text.main.your_file.value.format(receip=receip))
    receip.save_virtual_xlsx()
