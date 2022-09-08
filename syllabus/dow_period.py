"""
開講曜日・時限を取得
"""
import asyncio
import re
import unicodedata

import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import Playwright, async_playwright, expect


class DowPeriod:
    def __init__(self):
        self.numbering: str = ""
        self.search_word: str = ""
        self.dow = list()
        self.period = list()

    async def _run(self, playwright: Playwright) -> "tuple[str, str]":
        """シラバス検索画面にて検索を行い、検索結果から講義コードと一致する講義の開講曜日・時限を取得する

        Parameters
        ----------
        playwright : Playwright
            Playwrightインスタンス

        Returns
        -------
        dow: str
            曜日
        period: str
            時限

        Raises
        ------
        Exception
            シラバス検索画面に移動できなかった場合
            検索の実行時間が許容値を超えた場合
        """

        try:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()

            # 検索ページを開く
            page = await context.new_page()
            await page.goto("https://www.portal.oit.ac.jp/CAMJWEB/slbssrch.do")

            # 検索
            await page.fill("#keywords", self.search_word)
            await page.click("#srch_skwr_search")
            await asyncio.sleep(1)

            # 検索結果からテーブルを取得
            html = (await page.content()).replace("<br>", "@")
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find_all(class_="list")
            df = (pd.read_html(str(table)))[0]

        except expect as e:
            # 例外処理
            print("Error: ", e)
            return None, None

        else:
            # 講義コードが一致する行を検索し、開講曜日と時限を取得
            lecture_column = df.iloc[:, 1]
            index = (lecture_column[lecture_column == self.numbering]).index[0]
            extract_dow_period = df.iloc[index, 3]

            normalized_dow_period = unicodedata.normalize("NFKC", extract_dow_period)
            splitted_dow_period = re.split("[@ ]", normalized_dow_period)

            # 曜日と時限を取得
            for i in range(1, len(splitted_dow_period), 3):
                self.dow.append((splitted_dow_period[i]).replace("曜日", ""))
            for i in range(2, len(splitted_dow_period), 3):
                self.period.append(splitted_dow_period[i].replace("時限", ""))

        finally:
            await page.close()
            await context.close()
            await browser.close()

    async def _get(self) -> None:
        async with async_playwright() as playwright:
            await self._run(playwright)

    def main(self, numbering: str, search_word: str) -> list[str]:
        self.numbering = numbering
        self.search_word = search_word

        asyncio.run(self._get())
        return self.dow, self.period
