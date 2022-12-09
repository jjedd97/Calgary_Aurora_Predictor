# data from https://calgary.weatherstats.ca/download.html
import pandas as pd

columns_of_interest=["avg_visibility", "avg_hourly_cloud_cover_8"]

def get_date_points_for_index(data, path="./weatherstats_calgary_daily.csv"):
    df = pd.read_csv(path, index_col=0)
    df = df[columns_of_interest]
    data = data.join(df)
    return data
