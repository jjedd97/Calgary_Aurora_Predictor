import logging

import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from lxml import etree

from src.utils.dataframe_functions import create_dataframe_for_x_days


### This file will be used to fetch and parse data from: https://www.spaceweather.gc.ca
# In this data source Calgary is considered to be in the Sub-Auroral Zone

def get_27_day_forecast():
    '''
    url = "https://www.spaceweather.gc.ca/forecast-prevision/long/sflt-1-en.php"
    long_term_url="/forecast-prevision/long/sflt-en.php"
    response = requests.get(url)
    '''
    url = "https://www.spaceweather.gc.ca/forecast-prevision/long/sflt-1-en.php"
    long_term_url = "/forecast-prevision/long/sflt-en.php"
    tables = pd.read_html(url+long_term_url)  # Returns list of all tables on page
    forecast_table = tables[0]
    logging.debug(f" forecast returned: {forecast_table}")
    return forecast_table
