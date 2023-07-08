from typing import Generator
from app.helpers.postgres import PostgresDB
from app.helpers.fake_header import fake_header
from app.spiders.amazon import get_item
from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio
from asyncio import Semaphore


def get_failed_products_generator(
    pid_errors: str = "insertion_errors.log",
) -> Generator[str, None, None]:
    pids = []
    with open(pid_errors, "r", encoding="utf-8") as file:
        for product_id in file:
            product_id = product_id.strip()
            pids.append(product_id)

    return (pid for pid in pids)


def write_errors(line: str):
    print(line)
    with open("errors.log", "w", encoding="utf-8") as f:
        f.write(f"{line}\n")


async def scrap(pid: str, header: dict, limit: Semaphore) -> BeautifulSoup:
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
                    write_errors(pid)


async def main():
    limit = asyncio.Semaphore(8)
    tasks = []
    failed_pids = get_failed_products_generator()
    for pid in failed_pids:
        task = asyncio.create_task(scrap(pid, fake_header(), limit))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return result


if __name__ == "__main__":
    asyncio.run(main())
