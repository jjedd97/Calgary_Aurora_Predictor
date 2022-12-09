import pandas as pd

from src.Geomagnetic.space_forecast import get_27_day_forecast
from src.LunarData.full_moon_finder import get_full_moons, days_to_full_moon
from src.SocialData.csv_manager import get_validation_dataframe_from_csv
from src.Weather.weather_file_reader import get_14_day_forecast

def cal_final_predictions(m,g, w,data):
    index = []
    prediction = []
    for i, values in data.iterrows():
        if not pd.isna(values["Geo"]) and not pd.isna(values["days_to_full_moon"]) and not pd.isna(values["avg_hourly_cloud_cover_8"]):
            index.append(i)
            # low cloud is good, further from moon good
            prediction.append(values["Geo"]*g+(100-(values["days_to_full_moon"]/31*100))*m+(100-values["avg_hourly_cloud_cover_8"])*w)
    print(pd.DataFrame(index=index, data={"Probability" :prediction}))

def cal_weights():
    grading = get_validation_dataframe_from_csv("./DataTrainer/grading.csv")
    num_catergories = 3
    moon_deviation = grading["days_to_full_moon"]["std"]
    geo_deviation = (grading["DOY"]["std"]+grading["MEAX"]["std"]+grading["MEAY"]["std"]+grading["MEAZ"]["std"])/4
    weather_deviation = (grading['avg_visibility']['std']+grading['avg_hourly_cloud_cover_8']["std"])/2

    total = moon_deviation*5 + geo_deviation/5 + weather_deviation*5
    moon_pie = (1-((moon_deviation*5)/total))
    geo_pie = (1-((geo_deviation/5) /total))
    weather_pie = (1- ((weather_deviation*5) /total))
    total_pie = moon_pie + geo_pie + weather_pie
    moon_weight = moon_pie/total_pie
    geo_weight = geo_pie/total_pie
    weather_weight = weather_pie/total_pie
    print("Weights being applied to data are as follows:")
    print(f"Geomagnetic: {geo_weight}")
    print(f"Lunar: {moon_weight}")
    print(f"weather: {weather_weight}")
    return moon_weight, geo_weight, weather_weight

weather_data = get_14_day_forecast()
geomatic_data = get_27_day_forecast()
geomatic_data = pd.DataFrame(index=geomatic_data["Date"]["Date"], data={"Geo" :geomatic_data.Zones["Sub-Auroral"].tolist()})
moons = get_full_moons()
moon_data = geomatic_data.index.to_series().apply(days_to_full_moon, moons=moons)
geomatic_data["days_to_full_moon"] = moon_data

all_data = geomatic_data.join(weather_data)
print(all_data)
m,g,w, = cal_weights()
cal_final_predictions(m,g,w, all_data)