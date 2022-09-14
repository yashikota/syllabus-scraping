"""
非同期処理によるスクレイピング
"""
import asyncio

import httpx

from syllabus.convert import converter
from syllabus.parse import Parser
from syllabus.utility import normalize


class Scraping:
    def __init__(self):
        self._data = None
        self._limit: int = 5
        self._year: str = ""
        self._scraped_data: dict = dict()

    async def _get(self, client, data, semaphore):
        async with semaphore:
            department, url, dow, period = data.split(",")
            try:
                res = await client.get(url, timeout=10.0)
                print(department, url, res.status_code)
            except Exception as e:
                print(f"Error: {e}, {url}")
                res = await client.get(url, timeout=10.0)
            else:
                res_csv = converter(normalize(res.text))
                if len(res_csv) < 6:
                    return
                self._scraped_data.update(Parser().main(res_csv, department, url, dow, period))

    async def _request(self):
        semaphore = asyncio.Semaphore(self._limit)
        client = httpx.AsyncClient()

        tasks = [self._get(client, data, semaphore) for data in self._data]
        await asyncio.gather(*tasks)
        await client.aclose()

    def scraper(self, year: str, data: list[str]):
        self._year = year
        self._data = data

        asyncio.run(self._request())
        return self._scraped_data
