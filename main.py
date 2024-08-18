import os

import syllabus


def main():
    # スクレイピングする年度を取得
    year: str = os.getenv("YEAR")
    if year == "":
        print("スクレイピングする年度を指定してください")
        return

    # 学部/学科, URL, 曜日, 時限 のリストを取得
    data: list[str] = list(syllabus.get_data(year))

    # スクレイピング
    scraped_data: dict = syllabus.Scraping().scraper(year, data)

    # 一覧表示用と詳細表示用の出力
    syllabus.table_output(year, scraped_data)
    syllabus.output(year, scraped_data)


if __name__ == "__main__":
    main()
