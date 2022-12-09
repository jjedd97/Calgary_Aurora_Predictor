from src.LunarData.full_moon_finder import get_full_moons, days_to_full_moon
from src.PastData.past_space_forecast import get_data_from_file
from src.SocialData.csv_manager import get_validation_dataframe_from_csv
from src.Weather.weather_file_reader import get_date_points_for_index


def create_reported_sightings_data():
    #TODO get weather data
    sightings_df = get_validation_dataframe_from_csv("../SocialData/calgary-aurora-feed.csv")
    # selecting rows based on condition
    rslt_df = sightings_df.loc[(sightings_df['user-confirmed'] > 0) | (sightings_df['admin-confirmed'] >0) ]
    moons = get_full_moons()
    moon_data = rslt_df.index.to_series().apply(days_to_full_moon, moons=moons)
    rslt_df["days_to_full_moon"] = moon_data
    rslt_df = get_date_points_for_index(data=rslt_df, path="../Weather/weatherstats_calgary_daily.csv")
    #weather_data = rslt_df.index.to_series().apply(get_data_from_file,  folder="../PastData/Meanook")
    weather_data = None
    for i, _ in rslt_df.iterrows():
        if weather_data is not None:
            weather_data = weather_data.append(get_data_from_file(i, folder="../PastData/Meanook"))
        else:
            weather_data = get_data_from_file(i, folder="../PastData/Meanook")
    rslt_df = rslt_df.join(weather_data)
    print(rslt_df)

create_reported_sightings_data()