import logging
from datetime import date, datetime, timedelta
import pandas as pd


def create_dataframe_for_x_days(num_of_days: int, start_date: date = None):
    if not start_date:
        start_date = date.today()
    end = start_date + timedelta(days=num_of_days)
    dates = pd.Series(pd.date_range(start_date, end, freq="D"))
    days = dates.diff().astype("timedelta64[D]").fillna("nan")
    df = pd.DataFrame({"year": dates.dt.year, "days": days})
    df = df.set_index(dates)
    logging.debug(df)
    return df