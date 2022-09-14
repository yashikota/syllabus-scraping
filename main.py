import syllabus


def main():
    YEAR: str = "2022"

    # 学部/学科,URL,曜日,時限のリストを取得
    data: list[str] = list(syllabus.get_data(YEAR))

    # スクレイピング
    scraped_data: dict = syllabus.Scraping().scraper(YEAR, data)

    # 出力
    syllabus.output(YEAR, scraped_data)


if __name__ == "__main__":
    main()
