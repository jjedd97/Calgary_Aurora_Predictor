import logging

import geopy
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

