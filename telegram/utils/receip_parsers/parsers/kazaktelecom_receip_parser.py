from datetime import datetime
import asyncio
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from telegram.utils.receip_parsers.receip_types import ReceipLine, Receip, ReceipParser


class ReceipKazakhtelecom(ReceipParser):
    templateRegStr = r'https:\/\/consumer\.oofd\.kz\/ticket\/[-a-z0-9]+'
    name = 'Казахтелеком'

    @staticmethod
    def price_parser(text: str) -> float:
        return float("".join(text.split()[:-1]).replace(',', '.'))

    def extract_link(self, message: str) -> str:
        return str(max(self.templateRegEx.findall(message), key=len))

    async def parser(self, link) -> Receip:
        if not self.templateRegEx.match(link):
            raise AssertionError("Link incorrect")

        async with async_playwright() as p:
            for browser_type in [p.chromium, p.firefox, p.webkit]:
                browser = await browser_type.launch()
                page = await browser.new_page()
                await page.goto(link)
                text = await page.content()
                await browser.close()
                soup = BeautifulSoup(text, 'lxml')
                currency = ''
                data = []
                for row in soup.find('app-ticket-items').contents[2:]:
                    items = row.div.div.div.contents
                    if not currency: currency = items[3].string.split()[-1]
                    data.append(ReceipLine(
                        int(items[0].string[:-1]),
                        re.sub(r'\d{5,} ', '', items[1].string),
                        self.price_parser(items[3].string),
                        float(items[4].string.replace(',', '.')),
                        self.price_parser(items[5].string)
                    ))
                date = re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}', soup.find('span', text='Дата').next_sibling)
                date = datetime.strptime(date.group(), "%d.%m.%Y %H:%M")
                return Receip(
                    date,
                    link,
                    currency,
                    self.name,
                    data
                )


if __name__ == "__main__":
    t = ReceipKazakhtelecom()
    link = 'Казахтелеком\nhttps://consumer.oofd.kz/ticket/aadb79f8-a8cf-4b02-bc1e-8d8361575bd0'
    link = max(t.templateRegEx.findall(link), key=len)
    t = asyncio.get_event_loop().run_until_complete(t.parser(link))
    print("Чек распознан"
          "<code>Вендор :: </code> {receip.vendor}\n"
          "<code>Валюта :: </code> {receip.currency}\n"
          "<code>Сумма :: </code> {receip.amount}\n"
          "<code>Дата :: </code> {receip.date}\n"
          "<code>Количество продуктов :: </code> {receip.volume}\n"
          "<code>Ссылка :: </code> {receip.link}\n".format(receip=t))
    t.save_xlsx()
