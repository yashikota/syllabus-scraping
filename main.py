import syllabus


def main():
    YEAR: str = "2024"

    # 学部/学科, URL, 曜日,時限 のリストを取得
    data: list[str] = list(syllabus.get_data(YEAR))

    # スクレイピング
    scraped_data: dict = syllabus.Scraping().scraper(YEAR, data)

    # 一覧表示用と詳細表示用の出力
    syllabus.table_output(YEAR, scraped_data)
    syllabus.output(YEAR, scraped_data)


if __name__ == "__main__":
    main()
