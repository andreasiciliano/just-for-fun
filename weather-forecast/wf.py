# Code in this file closely follows tutorial available at
# http://stackabuse.com/using-machine-learning-to-predict-the-weather-part-1/
#
from datetime import datetime, timedelta  
import time
from collections import namedtuple
import pandas as pd  
import requests  
#import matplotlib.pyplot as plt

API_KEY = ''
STATE = ''
CITY = ''
BASE_URL = "http://api.wunderground.com/api/{}/history_{}/q/{}/{}.json"

target_date = datetime(2016, 5, 16)
features = ["date", "meantempm", "meandewptm", "meanpressurem", "maxhumidity", "minhumidity",
"maxtempm", "mintempm", "maxdewptm", "mindewptm", "maxpressurem", "minpressurem", "precipm"]
DailySummary = namedtuple("DailySummary", features)

def extract_weather_data(url, api_key, target_date, state, city, days):  
    records = []
    for _ in range(days):
        request = BASE_URL.format(API_KEY, state, city, target_date.strftime('%Y%m%d'))
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

records = extract_weather_data(BASE_URL, API_KEY, STATE, CITY, target_date, 3)
df = pd.DataFrame(records, columns=features).set_index('date')
df.to_csv('records.csv')
