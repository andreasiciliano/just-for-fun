# Code in this file closely follows tutorial available at
# http://stackabuse.com/using-machine-learning-to-predict-the-weather-part-1/
#
from datetime import datetime, timedelta  
import time
from collections import namedtuple
import pandas as pd  
import requests
import os
#import matplotlib.pyplot as plt

API_KEY = ''
STATE = ''
CITY = ''
DAYS = 300
BASE_URL = 'http://api.wunderground.com/api/{}/history_{}/q/{}/{}.json'

target_date = datetime(2016, 5, 16)
features = ["date", "meantempm", "meandewptm", "meanpressurem", "maxhumidity", "minhumidity",
"maxtempm", "mintempm", "maxdewptm", "mindewptm", "maxpressurem", "minpressurem", "precipm"]
DailySummary = namedtuple("DailySummary", features)

def extract_weather_data(url, api_key, target_date, state, city, days):  
    records = []
    for _ in range(days):
        request = BASE_URL.format(api_key, target_date.strftime('%Y%m%d'), 
            state, city)
        response = requests.get(request)
        if response.status_code == 200:
            data = response.json()['history']['dailysummary'][0]
            records.append(DailySummary(
                date=target_date,
                meantempm=data['meantempm'],
                meandewptm=data['meandewptm'],
                meanpressurem=data['meanpressurem'],
                maxhumidity=data['maxhumidity'],
                minhumidity=data['minhumidity'],
                maxtempm=data['maxtempm'],
                mintempm=data['mintempm'],
                maxdewptm=data['maxdewptm'],
                mindewptm=data['mindewptm'],
                maxpressurem=data['maxpressurem'],
                minpressurem=data['minpressurem'],
                precipm=data['precipm']))
        else:
            print(response.status_code)
        time.sleep(6)
        target_date += timedelta(days=1)
    return records


filename = 'weather_records_{}_{}.csv'.format(STATE, CITY)

# Look for csv file that stores weather info for the desired location
if os.path.isfile(filename):
    # if file exists, then load into into dataframe and set new target date
    # [Note: not handling the case where file exists but is empty]
    df = pd.read_csv(filename)
    target_date = datetime.strptime(df['date'].max(), '%Y-%m-%d') + timedelta(days=1)
    df = df.set_index('date')
else:
    # if file doesn't exist, then set target date to '2010-01-01' 
    # and create an empty dataframe
    df = pd.DataFrame()
    target_date = datetime(2010, 1, 1)

# Retrieve historical records and save them to a temporary DataFrame
records = extract_weather_data(BASE_URL, API_KEY, target_date, STATE, CITY, DAYS)
tmp_df = pd.DataFrame(records, columns=features)
tmp_df = tmp_df.set_index('date')

# Append new records to existing records (to an empty DataFrame if this is the
# first retrieval
df = df.append(tmp_df)

# Save records to csv file
df.to_csv(filename)
