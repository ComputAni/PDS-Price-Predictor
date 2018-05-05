
# coding: utf-8

# In[9]:


import pandas as pd
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar


# In[2]:


#cab_data = pd.read_csv("cab_data_p2.csv")


# In[3]:


#print(cab_data.iloc[0])


# In[4]:


# US Holidays Test Code
#cal = USFederalHolidayCalendar()
#us_holidays = cal.holidays(start='2016-01-01', end='2016-12-31').to_pydatetime()
#dt = datetime(2016, 1, 18)
#assert(dt in us_holidays)
#dt = datetime(2016, 1, 19)
#assert(dt not in us_holidays)


# In[10]:


def create_date_features(df, start_date, end_date):
    dt_format = '%Y-%m-%dT%H:%M:%S.000'
    # Get the list of US federal hollidays
    cal = USFederalHolidayCalendar()
    us_holidays = cal.holidays(start=start_date, end=end_date).to_pydatetime()
    
    date_feature_names = ["tpep_dropoff_datetime", "tpep_pickup_datetime"]
    date_feature_to_datetimes = {"tpep_dropoff_datetime" : [],
                                 "tpep_pickup_datetime" : []}
    for feature_name in date_feature_names:
        y, mo, d = [], [], [] # Year, Month, Day
        h, mi, s = [], [], [] # Hours, Minutes, Seconds
        day_of_week = [] # Day of the Week
        is_holiday = [] # Is the date a holiday?
        for time in df[feature_name]:
            # Extract the datetime object from the timestamp
            dt = datetime.strptime(time, dt_format)
            date_feature_to_datetimes[feature_name].append(dt)
            # Add the Year/Month/Day
            y.append(dt.year)
            mo.append(dt.month)
            d.append(dt.day)
            # Add Hour/Minute/Second
            h.append(dt.hour)
            mi.append(dt.minute)
            s.append(dt.second)
            # Add Day of the Week
            day_of_week.append(dt.weekday())
            # Add is_holiday
            y_m_d = datetime(dt.year, dt.month, dt.day)
            is_holiday.append(1 if y_m_d in us_holidays else 0)
        df[feature_name + "_years"] = y
        df[feature_name + "_months"] = mo
        df[feature_name + "_days"] = d
        df[feature_name + "_hours"] = h
        df[feature_name + "_minutes"] = mi
        df[feature_name + "_seconds"] = s
        df[feature_name + "_day_of_week"] = day_of_week
        df[feature_name + "_is_holiday"] = is_holiday
    durations = []
    for dropoff_time, pickup_time in zip(date_feature_to_datetimes["tpep_dropoff_datetime"],
                                         date_feature_to_datetimes["tpep_pickup_datetime"]):
        duration = (dropoff_time - pickup_time).total_seconds() / 60.0
        durations.append(round(duration))
    
    df["duration"] = durations
    return df
start = '2016-01-01'
end = '2016-12-31'
cab_data = create_date_features(cab_data, start, end)


# In[6]:


# Check Distribution of months and holidays
"""
print("Distribution of Months")
print(cab_data["tpep_dropoff_datetime_months"].value_counts())
print("Distribution of Holidays")
print(cab_data["tpep_dropoff_datetime_is_holiday"].value_counts())
"""


# In[7]:


#print(cab_data["dropoff_longitude"].value_counts())


# In[11]:


#cal = USFederalHolidayCalendar()
#us_holidays = cal.holidays(start='2016-01-01', end='2016-12-31').to_pydatetime()


# In[8]:


#print(us_holidays)

