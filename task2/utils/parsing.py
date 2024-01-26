import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def parse_category(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
        ) as response:
            print(f"status:{response.status}")
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            books = soup.select("article", {"class": "product_pod"})
            print(f"Found {len(books)}")
            # название, цена, ссылка, наличие, инфа со страницы
            for book in books:
                # name and link
                name_h = book.select_one("h3")
                name = name_h.text



if __name__ == "__main__":
    asyncio.run(parse_category(""))
