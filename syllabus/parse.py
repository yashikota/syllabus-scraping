"""
データを解析
"""
import re
import unicodedata

from syllabus.dow_period import DowPeriod


class Parser:
    def __init__(self):
        pass

    def main(self, enter: str, department: str, url: str) -> dict:
        try:
            """
            csvを読み込み、jsonに変換
            """

            value_list = list()
            lecture_list = list()
            lecture_value_list = list()
            lecture_key_list = list()
            big_dict = dict()
            correction = 0
            text = "\n".join(enter[1])
            key_list = [
                "lecture_title",
                "lecture_title_en",
                "year",
                "credit",
                "term",
                "person",
                "numbering",
                "department",
                "url",
                "aim",
                "cs",
                "spiral",
                "target",
                "method",
                "basis",
                "textbook",
                "reference_book",
                "knowledge",
                "office_hour",
                "practice",
            ]

            # 講義名等
            for i in range(len(enter[0])):
                value_list.append(enter[0][i])
            value_list[2] = str(value_list[2]).replace("年次", "")  # 年次を削除
            value_list[5] = (re.sub("\(.+?\)", "", value_list[5])).replace(
                "  ", " "
            )  # 担当者名のよみがな削除
            numbering = re.search(r"\w{8}(?=&value)", url).group()  # 講義コードをurlから抽出
            value_list.append(numbering)
            value_list.append(department)  # 学科名追加
            value_list.append(url)  # URL追加

            # 曜日と時限
            # dow, period = DowPeriod().main(numbering, value_list[1])
            # value_list.append(dow)
            # value_list.append(period)

            # 授業のねらい・概要
            value_list.append(enter[2][0])

            # CSコース
            if "CSコース" in text:
                spiral = re.search(r"CSコース,(.*)", text).group(1)
                if len(spiral) > 0:
                    value_list.append(spiral)
                    correction += 1  # 参照のズレを補正
                else:
                    value_list.append("記載なし")
            else:
                value_list.append("記載なし")

            # スパイラル型教育
            if "スパイラル型教育" in text:
                spiral = re.search(r"スパイラル型教育,(.*)", text).group(1)
                if len(spiral) > 0:
                    value_list.append(spiral)
                    correction += 1
                else:
                    value_list.append("記載なし")
            else:
                value_list.append("記載なし")

            # 授業計画
            for i in range(1, (len(enter[3 + correction]))):
                lecture_list.append(str(enter[3 + correction][i]).split(","))  # ","で分割
            for i in range(len(lecture_list)):
                # テーマ
                if len(lecture_list[i][1]) > 0:
                    lecture_key_list.append("theme" + str(i + 1))
                    lecture_value_list.append(lecture_list[i][1])
                # 内容・方法等
                if len(lecture_list[i][2]) > 0:
                    lecture_key_list.append("content" + str(i + 1))
                    lecture_value_list.append(lecture_list[i][2])
                # 予習/復習
                if len(lecture_list[i][3]) > 0:
                    lecture_key_list.append("preparation" + str(i + 1))
                    lecture_value_list.append(lecture_list[i][3])

            # 目標、評価方法、評価基準
            for i in range(3):
                value_list.append(enter[(4 + i) + correction][0])

            # 教科書
            if "教科書" in text:
                textbook = re.search(r"教科書,(.*)", text).group(1)
                if len(textbook) > 0:
                    value_list.append(
                        (re.search(r"出版社名(.*)", text).group(1)).replace("  ", "")
                    )
                    correction += 1  # 参照のズレを補正
                else:
                    value_list.append("記載なし")
            else:
                value_list.append("記載なし")

            # 参考書
            if "参考書" in text:
                reference_book = re.search(r"参考書,(.*)", text).group(1)
                if len(reference_book) > 0:
                    value_list.append(
                        (re.search(r"出版社名(.*)", text).group(1)).replace("  ", "")
                    )
                    correction += 1
                else:
                    value_list.append("記載なし")
            else:
                value_list.append("記載なし")

            # 受講心得
            value_list.append(enter[7 + correction][0])

            # オフィスアワー
            value_list.append(enter[8 + correction][0])

            # 実践的教育
            if len(enter[9 + correction]) > 0:
                value_list.append(enter[9 + correction][0])
            else:
                value_list.append("記載なし")

            # 正規化とダブルクオーテーションの削除
            for i in range(len(value_list)):
                value_list[i] = unicodedata.normalize(
                    "NFKC", str(value_list[i])
                ).replace('"', "")
            for i in range(len(lecture_value_list)):
                lecture_value_list[i] = unicodedata.normalize(
                    "NFKC", str(lecture_value_list[i])
                ).replace('"', "")

            # 辞書に変換
            df_dict = dict(zip(key_list, value_list))
            lecture_dict = dict(zip(lecture_key_list, lecture_value_list))
            if lecture_list != []:
                df_dict.update(lecture_dict)
            else:
                df_dict.update(
                    {"theme1": "記載なし", "content1": "記載なし", "preparation1": "記載なし"}
                )

            # 辞書に追加
            big_dict.update({numbering: df_dict})

            return big_dict

        except Exception as e:
            with open("error.log", "w") as f:
                f.write(f"{e}\n{url}")
            return big_dict
