# data from https://calgary.weatherstats.ca/download.html
import logging
from datetime import date, timedelta

import pandas as pd

columns_of_interest=["avg_visibility", "avg_hourly_cloud_cover_8"]
def get_14_day_forecast():
    url = "https://www.myweather2.com/City-Town/Canada/Alberta/Calgary/14-Day-Forecast.aspx"
    tables = pd.read_html(url)  # Returns list of all tables on page
    forecast_table = tables[1]
    logging.debug(f" forecast returned: {forecast_table}")
    index = []
    cloud_cover = []
    count = 0
    today = date.today()
    for i, data in forecast_table.iterrows():
        if isinstance(data["Day"], str):
            index.append(str(today+timedelta(days=count)))
            count = count + 1
            cloud_cover.append(get_cloud_cover_from_string(data["Cloud Amount"]))

    return pd.DataFrame(index=index, data={columns_of_interest[1]: cloud_cover})

def get_cloud_cover_from_string(data_string):
    shorter = data_string.split("High level cloud: ")[-1]
    shorter = shorter.split("%")[0]
    return float(shorter)


def get_date_points_for_index(data, path="./weatherstats_calgary_daily.csv"):
    df = pd.read_csv(path, index_col=0)
    df = df[columns_of_interest]
    data = data.join(df)
    return data


def get_min_max_weather_values(path="./weatherstats_calgary_daily.csv"):
    df = pd.read_csv(path, index_col=0)
    df = df[columns_of_interest]
    return df.agg(['min', 'max'])
