import syllabus


def main():
    YEAR: str = "2022"

    # 学部・学科とURLのリストを取得
    department_url_list: list[str] = list(syllabus.get_department_url(YEAR))

    # スクレイピング
    data: dict = syllabus.Scraping().scraper(YEAR, department_url_list)

    # 出力
    syllabus.output(YEAR, data)


if __name__ == "__main__":
    main()
