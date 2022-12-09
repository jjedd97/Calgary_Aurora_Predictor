import datetime
import logging

import ephem


def get_full_moons(start_year=2015, end_year=2025):
    moons = []
    for year in range(start_year, end_year+1):
        date=ephem.Date(datetime.date(year,1,1))
        while date.datetime().year==year:
            date=ephem.next_full_moon(date)
            moons.append( (ephem.localtime(date).date(),'full') )
    return moons

def days_to_full_moon(date, moons):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if date > moons[-1][0]:
        logging.info("not enough moon data")
        return None
    for i in range(len(moons)):
        if moons[i][0] < date and moons[i+1][0]> date :
            delta = moons[i+1][0] - date
            return delta.days


