
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
from unicodedata import normalize
import re


# In[3]:


#cab_data = pd.read_csv("cab_data_p2.csv")


# In[2]:


# Get weather data for 2016 and returns dictionary of date features
def init_weather_features(start_date, end_date):
    date = start_date
    date_to_features = dict()
    # weather related features to extract
    feature_names = ["Mean Temperature",
                    "Max Temperature",
                    "Min Temperature",
                    "Dew Point",
                    "Average Humidity",
                    "Precipitation",
                    "Snow",
                    "Wind Speed",
                    "Visibility"]
    while (date <= end_date):
        # station: KNYC (Central Park, New York)
        (year, month, day) = (date.year, date.month, date.day)
        print(year, month, day)

        # Get the HTML of the weather webpage
        url_format_string = "http://www.wunderground.com/history/airport/KNYC/{year}/{month}/{day}/DailyHistory.html"
        url = url_format_string.format(year=year, month=month, day=day)
        response = requests.get(url)

        if response.status_code != 200:
            print("An error occurred while getting NYC weather data for {day}-{month}-{year}".format(
            year=year, month=month, day=day))
        else:
            features = dict()
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            table = soup.find_all(attrs={'id': 'historyTable'})[0]

            table_rows = table.find_all('tr')
            feature_list = []
            found_features = [False, False, False, False, False, False, False, False, False]
            # Loop through the entries of the table to find weather features
            for tr in table_rows:
                td = tr.find_all('td')
                # normalize the text to account for string encoding
                row = [normalize('NFKD', i.text) for i in td]

                # There are multiple rows named 'snow' and 'precipitation'
                # Use len(row) > 2 to get the "right" rows
                if len(row) > 2 and row[0] in feature_names:
                    data = row[1].strip() # remove extraneous whitespace
                    result = re.sub('[^0-9.]','', data) # remove all alphabetic characters
                    if result == "": # if there's no feature value (e.g.: T, for traces of precipitation/snow)
                        result = 0
                    features[row[0]] = result
                    found_features[feature_names.index(row[0])] = True
                    feature_list.append(result)

            # If a feature is not present in the table, set it to a default value: 0
            for found_feature, feature_name in zip(found_features, feature_names):
                if (not found_feature):
                    features[feature_name] = 0
            assert(len(features) == len(feature_names))
            date_to_features[date] = features
        date = date + datetime.timedelta(1)
        
    return date_to_features



# In[5]:


#start_date = datetime.datetime(2018, 5, 5)
#end_date = datetime.datetime(2018, 5, 5)
#date_features = init_weather_features(start_date, end_date)


# In[3]:


# insert method for dictionary (list of values for each key)
def dict_insert(d, key, val):
    if key in d:
        d[key].append(val)
    else:
        d[key] = [val]

# put the weather-related features into the dataframe
def create_weather_features(df, date_to_features):
    
    dt_format = '%Y-%m-%dT%H:%M:%S.%f'
    weather_features = dict()
    for time in df["tpep_dropoff_datetime"]:
        # Extract the datetime object from the timestamp
        dt = datetime.datetime.strptime(time, dt_format)
        y_m_d = datetime.datetime(dt.year, dt.month, dt.day)
        weather_dict = date_to_features[y_m_d]
        for feature_name in weather_dict:
            dict_insert(weather_features, feature_name, weather_dict[feature_name])
        
    for feature_name in weather_features:
        df[feature_name] = weather_features[feature_name]
    return df

#cab_data = create_weather_features(cab_data, date_features)


# In[90]:


# Inspect our newly created weather features
#print(cab_data.iloc[0])

