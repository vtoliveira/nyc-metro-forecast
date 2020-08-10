import re

import pandas as pd 

from constants import nyc_regions

def prepr_station(station):
    station = re.sub('[-/]', ' ', station)
    station = station.replace('AVE', 'AV')
    
    return station

def df_stations_to_regions():
    for key in nyc_regions.keys():
        nyc_regions[key] = [prepr_station(station.upper()) for station in nyc_regions[key]]
    
    df_station_regions = (
        pd.Series({value:key for key, l in nyc_regions.items() for value in l})
        .reset_index()
        .rename(columns={"index": "station", 0: "region"})
    )

    return df_station_regions