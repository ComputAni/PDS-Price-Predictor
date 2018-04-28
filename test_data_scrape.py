#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
max_size = 50000
total_size = 1000000
num_chunks = total_size // max_size #Should be 200
total_data = []
print("Requesting: %d chunks" % num_chunks);
for i in range(num_chunks):
    curr_offset = max_size*i
    results = client.get("uacg-pexx", limit=50000, offset=curr_offset)
    total_data += results


# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(total_data)
print("Before scrubbing data size: ", len(results_df))
results_df = results_df[results_df.pickup_latitude != '0']
results_df = results_df[results_df.pickup_longitude != '0']
results_df = results_df[results_df.dropoff_latitude != '0']
results_df = results_df[results_df.dropoff_longitude != '0']
print("After scrubbing data size: ", len(results_df))

"""
dlen = len(results_df)
results_p1 = results_df.iloc[: dlen // 2]
results_p2 = results_df.iloc[dlen // 2:]

print(len(results_p1), len(results_p2))

#Write to csv file
results_p1.to_csv('cab_data_p1.csv')
results_p2.to_csv('cab_data_p2.csv')
"""
results_df.to_csv('cab_data.csv')


print("Finished writing to file!")