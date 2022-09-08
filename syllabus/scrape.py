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
        self._limit: int = 5
        self._year: str = ""
        self._data: dict = dict()

    async def _get(self, client, department_url, semaphore):
        async with semaphore:
            department, url = department_url.split(",")
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
                self._data.update(Parser().main(res_csv, department, url))

    async def _request(self, department_url_list: list[str]):
        semaphore = asyncio.Semaphore(self._limit)
        client = httpx.AsyncClient()

        tasks = [
            self._get(client, department_url, semaphore)
            for department_url in department_url_list
        ]
        await asyncio.gather(*tasks)
        await client.aclose()

    def scraper(self, year: str, department_url_list: list[str]):
        self._year = year

        asyncio.run(self._request(department_url_list))
        return self._data
