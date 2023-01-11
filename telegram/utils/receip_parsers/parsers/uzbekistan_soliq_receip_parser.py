import asyncio
import aiohttp
import re
import datetime
import telegram.texts as Text
from telegram.utils.receip_parsers.receip_types import ReceipLine, Receip, ReceipParser
from urllib3 import disable_warnings, exceptions
from bs4 import BeautifulSoup

disable_warnings(exceptions.InsecureRequestWarning)


class ReceipUzSoliq(ReceipParser):
    templateRegStr = r'(https?:\/\/ofd\.soliq\.uz\/check([?&][trcs]=[UZ\d]+)+)'
    name = 'UZ – Savdo cheki/Sotuv'

    async def extract_link(self, message: str) -> str:
        return self.templateRegEx.search(message).group(0)

    def price_parser(self, price: str) -> float:
        return float(price.replace(',', ''))

    async def parser(self, link) -> Receip:
        reqLink = link
        async with aiohttp.ClientSession() as session:
            async with session.get(reqLink, verify_ssl=False) as resp:
                pageText = await resp.text()
        currency = 'Sʻ (so’m)'
        data = []
        soup = BeautifulSoup(pageText, 'lxml')
        for num, row in enumerate(soup.find_all("tr", {"class": "products-row"}), 1):
            item = [i.text.strip() for i in row.find_all('td')]
            cost = self.price_parser(item[2])
            quantity = self.price_parser(item[1])
            data.append(ReceipLine(
                num,
                item[0],
                cost / quantity,
                quantity,
                cost
            ))

        main = soup.find("div", {"class": "tickets"}).find_all('td')
        date = datetime.datetime.strptime(main[6].text.strip(), "%d.%m.%Y")

        extra = {
            'organization': main[1].contents[1].text,
            'adress': f"{main[1].contents[2].text.strip()}, {main[1].contents[3].text}",
            'receipt code': main[2].text.strip(),
            'receipt number': main[3].contents[1].contents[1].text,
            'SN': main[5].contents[1].contents[1].text
        }
        return Receip(
            date,
            link,
            currency,
            self.name,
            data,
            extra
        )


if __name__ == "__main__":
    link = 'sdf sdf sdf sd d\nhttps://ofd.soliq.uz/check?t=UZ210317238709&r=22051&c=20221222203700&s=159312926214'
    t = ReceipUzSoliq()
    link = asyncio.run(t.extract_link(link))

    receip = asyncio.run(t.parser(link))
    print(Text.Text.main.your_file.value.format(receip=receip))
    # receip.save_virtual_xlsx()
