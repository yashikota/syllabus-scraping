"""
その他
"""
import json
import unicodedata
import urllib.request


def get_data(year: str) -> list:
    """
    学部/学科,URL,曜日,時限のリストを取得
    """
    return (
        urllib.request.urlopen(
            f"https://raw.githubusercontent.com/oit-tools/syllabus-extract/master/data/{year}.csv"
        )
        .read()
        .decode("utf-8")
        .splitlines()
    )


def output(year: str, data: dict) -> None:
    """
    jsonに出力
    """
    # ソート
    data: dict = dict(sorted(data.items()))
    # 保存
    with open(f"./data/{year}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def table_output(year: str, data: dict) -> None:
    """
    table表示用に出力
    """
    result = list()

    # ソート
    data: dict = dict(sorted(data.items()))
    # 抽出
    for key in data.keys():
        result.append({
            "lecture_title": data[key]["lecture_title"],
            "department": data[key]["department"],
            "year": data[key]["year"],
            "term": data[key]["term"],
            "dow": data[key]["dow"],
            "period": data[key]["period"],
            "credit": data[key]["credit"],
            "person": data[key]["person"],
            "numbering": data[key]["numbering"],
        })
    # 保存
    with open(f"./data/{year}table.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


def normalize(enter: str) -> str:
    """
    文字列を正規化
    """
    return unicodedata.normalize("NFKC", enter)
