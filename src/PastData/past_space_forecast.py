import gzip
import logging
import os.path
from datetime import date, datetime, timedelta
from io import StringIO

import geopy
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from geopy import distance


def get_observatory_data(observatory_id: str = "MEA"):
    # MEA the default is located in northen alberta
    # The url here did not work :(
    pass


def find_closest_observatory(city_name: str = "Calgary"):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(city_name)

    observatories = requests.get('https://geomag.usgs.gov/ws/observatories/').json()
    closest = None
    smallest_distance = None
    for observatory in observatories["features"]:
        try:
            city = geolocator.geocode(observatory["properties"]["name"])
            # Note the returned value was long, lat and some other value
            distance_km = geopy.distance.geodesic([location.latitude, location.longitude],
                                                  [city.latitude, city.longitude]).km
            if not smallest_distance or distance_km < smallest_distance:
                smallest_distance = distance_km
                closest = observatory["id"]
        except:
            # most these names are not cities, using a good enough approach
            logging.debug("name wasn't a city")
    return closest

def get_data_from_file(desired_date: date, folder="./Meanook"):
    if isinstance(desired_date, str):
        desired_date = datetime.strptime(desired_date, '%Y-%m-%d').date()
    if desired_date.year < 2017:
        modifier = "dmin.min.gz"
    elif desired_date.year == 2017:
        modifier = "vmin.min.gz"
    else:
        modifier = "vmin.min"
    path = folder + "/" + str(desired_date.year) + "/" + "mea"+desired_date.strftime('%Y%m%d')+ modifier
    if os.path.exists(path):
        if modifier.split(".")[-1] == "gz":
            with gzip.open(path, 'r') as file:
                data = file.read().decode("utf-8")
                data = "DATE" + data.split("DATE")[1]
            data = StringIO(data)
        else:
            with open(path, 'r') as file:
                data = file.read()
                data = "DATE" + data.split("DATE")[1]
            data = StringIO(data)

        df = pd.read_csv(data, sep='\s+', index_col=0)
        averages = pd.DataFrame(index=[str(desired_date)], data={"DOY": df["DOY"].mean(), "MEAX": df["MEAX"].mean(), "MEAY": df["MEAY"].mean(),
                    "MEAZ":df["MEAZ"].mean()})
        return averages
    else:
        logging.warning("No observatory data")
        return pd.DataFrame(index=[str(desired_date)], data={"DOY": None, "MEAX": None, "MEAY": None,
                    "MEAZ": None})


def get_min_max_space_data(start_date=date(year=2015, month=1, day=1), end_date=date(year=2021,month=11, day=30), folder="./Meanook"):
    current_date = start_date
    all_data = None
    while current_date <= end_date:
        if all_data is not None:
            all_data = all_data.append(get_data_from_file(current_date, folder=folder))
        else:
            all_data = get_data_from_file(current_date, folder=folder)
        current_date = current_date + timedelta(days=1)

    return all_data.agg(['min', 'max'])


