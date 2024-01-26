import asyncio
import csv
import os
from datetime import datetime

import aiofiles
import aiohttp
from aiogram.types import FSInputFile, Message
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from aiocsv import AsyncWriter


async def fetch_book_page(url, session):
    async with session.get(url) as response:
        return await response.text()


async def parse_book(book_html, base_link, writer, session):
    # getting name and link
    print(f"Parsing book from")
    book_info_row = []
    name_h = book_html.select_one("h3")
    rel_link = name_h.select_one("a")["href"]
    full_link = urljoin(base_link, rel_link)
    book_info_row.append(full_link)
    # book page info
    book_page_html = await fetch_book_page(full_link, session)
    book_soup = BeautifulSoup(book_page_html, "html.parser")
    # price and availability
    book_p = book_soup.select_one("div.product_main")
    # name
    name = book_p.select_one("h1").text
    # print(f"book name is {name}")
    book_info_row.insert(0, name)
    price = book_p.select_one("p.price_color").text
    book_info_row.append(price)
    availability = book_p.select_one("p.instock.availability").text.replace("\n", "")
    is_available = "In stock" in availability
    book_info_row.append(is_available)
    # other info from table
    info_table = book_soup.select_one("table")
    for row in info_table.find_all("td"):
        book_info_row.append(row.text)
    # print(f"writing book {name}, {book_info_row}")
    await writer.writerow(book_info_row)


async def parse_category(base_link, response, session):
    current_dir = os.path.dirname(__file__)
    file_path = f"{os.path.abspath(os.path.join(current_dir, '..'))}/data/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    async with aiofiles.open(
        file_path,
        mode="w",
    ) as csvfile:
        if response.status != 200:
            return False
        tasks = []
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        books = soup.select("article", {"class": "product_pod"})
        print(f"Found {len(books)}")
        writer = AsyncWriter(csvfile)
        book_info_columns = [
            "name",
            "link",
            "price",
            "is_available",
            "UPC",
            "Product Type",
            "Price (excl.tax)",
            "Price (incl.tax)",
            "Tax",
            "Availability",
            "Number of reviews",
        ]
        await writer.writerow(book_info_columns)
        for book in books:
            task = asyncio.create_task(parse_book(book, base_link, writer, session))
            tasks.append(task)
        await asyncio.gather(*tasks)
        return file_path


async def parse_and_send_file(base_link, message: Message):
    async with (aiohttp.ClientSession() as session):
        async with session.get(base_link) as response:
            if response.status != 200:
                await message.answer("Возникла ошибка: возсожно ссылка неверная")
                return False
            try:
                file_path = await parse_category(base_link, response, session)
                if file_path:
                    doc = FSInputFile(file_path)
                    await message.answer_document(doc)
                else:
                    await message.answer("Что то пошло не так")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    pass
    # asyncio.run(
    #     parse_category(
    #         "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    #     )
    # )
