from datetime import datetime

import numpy as np
import pandas as pd


def postprocess_df(df):
    new_df = df.copy(deep=True)
    for column in new_df.columns[3:]:
        new_df[column] = new_df[column].fillna("").apply(lambda d: d[:10])

    start_date = new_df.apply(lambda item: np.min(item[3:]), axis=1)
    end_date = new_df.apply(lambda item: np.max(item[3:]), axis=1)
    uniq_dates = new_df.apply(lambda item: len(np.unique(item[3:])), axis=1)
    days = new_df.apply(
        lambda item: (datetime.strptime(np.max(item[3:]), "%Y-%m-%d")
        - datetime.strptime(np.min(item[3:]), "%Y-%m-%d")).days,
        axis=1,
    )
    new_df["uniq_dates"] = uniq_dates
    new_df["start_date"] = start_date
    new_df["end_date"] = end_date
    new_df["days"] = days
    new_df["date_joined"] = new_df["date_joined"].apply(lambda d: d[:10])
    new_df = new_df[
        [
            *new_df.columns[:3],
            "uniq_dates",
            "start_date",
            "end_date",
            "days",
            *new_df.columns[3:-2],
        ]
    ]

    return new_df


if __name__ == "__main__":
    df = pd.read_csv("res.csv", index_col=0)
    df = postprocess_df(df)
    df.to_csv("processed.csv")
