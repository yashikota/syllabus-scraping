"""
データを変換
"""
import pandas


def dataframe(enter: str) -> pandas.DataFrame:
    """htmlを読み込み、DataFrameに変換"""
    return pandas.read_html(enter, encoding="utf-8")


def csv(enter: pandas.DataFrame) -> list[str]:
    """DataFrameをcsvに変換"""
    dfs: list[str] = list()

    if len(enter) > 2:
        for i in range(1, len(enter)):
            if i == 1:
                df = (
                    (enter[i])
                    .dropna(how="all")
                    .dropna(how="all", axis=1)
                    .drop(enter[1].columns[0], axis=1)
                    .drop(enter[1].index[4])
                )
            else:
                df = (enter[i]).dropna(how="all").dropna(how="all", axis=1)
            df_text = (
                (df.to_csv(index=False, header=False, encoding="utf-8")).replace(
                    "\u3000", ""
                )
            ).splitlines()
            dfs.append(df_text)

    return dfs


def converter(enter: str) -> list[str]:
    return csv(dataframe(enter))
