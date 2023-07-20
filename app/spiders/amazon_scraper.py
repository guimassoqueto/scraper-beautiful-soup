from app.helpers.database.postgres import PostgresDB
from app.spiders.amazon_item import get_item
from aiohttp import ClientSession
from asyncio import Semaphore
from bs4 import BeautifulSoup

from asyncio import run, Semaphore
from app.helpers.fake_header import fake_header

async def amazon_scraper(pid: str, header: dict, limit: Semaphore) -> BeautifulSoup:
    url = f"https://amazon.com.br/dp/{pid}"
    async with limit:
        async with ClientSession(headers=header) as session:
            async with session.get(url) as response:
                assert response.status == 200, "Status Code must be 200"
                try:
                    body = await response.text()
                    soup = BeautifulSoup(body, "html.parser")
                    item = get_item(pid, soup)
                    pg = PostgresDB()
                    await pg.upsert_item("products", item)
                    print("ok: ", pid)
                except Exception as e:
                    print(e)
                    print("Error:", pid)
