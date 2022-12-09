from src.LunarData.full_moon_finder import get_full_moons, days_to_full_moon
from src.PastData.past_space_forecast import get_data_from_file, get_min_max_space_data
from src.SocialData.csv_manager import get_validation_dataframe_from_csv
from src.Weather.weather_file_reader import get_date_points_for_index, get_min_max_weather_values


def create_reported_sightings_data():
    # TODO get weather data
    sightings_df = get_validation_dataframe_from_csv("../SocialData/calgary-aurora-feed.csv")
    # selecting rows based on condition
    rslt_df = sightings_df.loc[(sightings_df['user-confirmed'] > 0) | (sightings_df['admin-confirmed'] > 0)]
    moons = get_full_moons()
    moon_data = rslt_df.index.to_series().apply(days_to_full_moon, moons=moons)
    rslt_df["days_to_full_moon"] = moon_data
    rslt_df = get_date_points_for_index(data=rslt_df, path="../Weather/weatherstats_calgary_daily.csv")
    # weather_data = rslt_df.index.to_series().apply(get_data_from_file,  folder="../PastData/Meanook")
    weather_data = None
    for i, _ in rslt_df.iterrows():
        if weather_data is not None:
            weather_data = weather_data.append(get_data_from_file(i, folder="../PastData/Meanook"))
        else:
            weather_data = get_data_from_file(i, folder="../PastData/Meanook")
    return rslt_df.join(weather_data)


def get_min_max_values():
    max_min_dict = {
        "moon": (0, 31),
        "weather": get_min_max_weather_values(path="../Weather/weatherstats_calgary_daily.csv"),
        "geomagnetic": get_min_max_space_data(folder="../PastData/Meanook")
    }
    return max_min_dict

def grade(sightings_data, min_max_data):
    sightings_data["days_to_full_moon"] = sightings_data["days_to_full_moon"].apply(lambda x: (x-min_max_data['moon'][0])/(min_max_data['moon'][1]-min_max_data['moon'][0])*10)
    sightings_data["avg_visibility"]= sightings_data["avg_visibility"].apply(lambda x: x / (min_max_data['weather']["avg_visibility"][1] - min_max_data['weather']["avg_visibility"][0])*10)
    sightings_data["DOY"] = sightings_data["DOY"].apply(lambda x: (x-min_max_data['geomagnetic']["DOY"][0]) / (min_max_data['geomagnetic']["DOY"][1] - min_max_data['geomagnetic']["DOY"][0])*10)
    sightings_data["MEAX"] = sightings_data["MEAX"].apply(
        lambda x: (x - min_max_data['geomagnetic']["MEAX"][0]) / (min_max_data['geomagnetic']["MEAX"][1] - min_max_data['geomagnetic']["MEAX"][0])*10)
    sightings_data["MEAY"] = sightings_data["MEAY"].apply(
        lambda x: (x - min_max_data['geomagnetic']["MEAY"][0]) / (min_max_data['geomagnetic']["MEAY"][1] - min_max_data['geomagnetic']["MEAY"][0])*10)
    sightings_data["MEAZ"] = sightings_data["MEAZ"].apply(
        lambda x: (x - min_max_data['geomagnetic']["MEAZ"][0]) / (min_max_data['geomagnetic']["MEAZ"][1] - min_max_data['geomagnetic']["MEAZ"][0])*10)
    sightings_data.to_csv("./grading.csv")
