import logging
import os
from datetime import date

import pandas as pd

default_start = date(year=2015, day=1, month=1)
default_end = date(year=2025, day=31, month=12)

def create_csv(path: str ="./calgary-aurora-feed.csv", start_date=default_start, end_date=default_end):
    """
    Function that generates the csv, tracker of reported sights
    :param path: filepath of the csv to create
    :return:
    """
    if os.path.exists(path):
        logging.info(f"{path} already exists")
    else:
        dates = pd.Series(pd.date_range(start_date, end_date, freq="D"))
        df = pd.DataFrame(0, index=dates, columns=["user-confirmed", "admin-confirmed"])
        df = df.set_index(dates)
        df.to_csv(path)

def increase_csv(date_modified: date, path: str ="./calgary-aurora-feed.csv"):
    df = pd.read_csv(path, index_col=0)
    df.loc[[date_modified], ["user-confirmed"]] = df.loc[[date_modified], ["user-confirmed"]]+1
    df.to_csv(path)

def get_validation_dataframe_from_csv(path: str ="./calgary-aurora-feed.csv"):
    return pd.read_csv(path, index_col=0)
