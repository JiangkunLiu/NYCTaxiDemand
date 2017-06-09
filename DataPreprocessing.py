import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from geopy import Nominatim
import time
from os import listdir

# Find all csv files in the specified directory
path = 'D:/TLC/'
suffix=".csv"
csv_files = [filename for filename in listdir(path) if filename.endswith( suffix )]
# Read a specified data set
file_number = 12
file_read = path + csv_files[file_number]
trips = pd.read_csv(file_read)

# Unify column namings, because yellow taxi and green taxi data have different names for some columns
trips.columns = map(str.lower, trips.columns)
column_name = list(trips.columns)
for i in range(len(column_name)):
    if 'pickup_datetime' in column_name[i]:
        column_name[i] = 'pickup_datetime'
    if 'dropoff_datetime' in column_name[i]:
        column_name[i] = 'dropoff_datetime'
trips.columns = column_name

# Only take those columns that are userful for this task to reduce table size
columns_useful = ['pickup_datetime', 'dropoff_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
                  'dropoff_latitude', 'passenger_count', 'total_amount']
trip = trips[columns_useful]

## Check the head and size of the data set
print(trip.head())
print(trip.shape)

## Check missing values in the data set
print("Percentage of available data for each parameter:")
print( trip.count() * 100 / len(trip) )
## Check the values of the data set
print(trip.describe())

# There are negative values for fare_amount, and ridiculously large values;
# There are 0 values for passenger count
# These unreasonable values should be removed
trip = trip.drop(trip.index[[True if value < 1 or value > 6 else False for value in trip['passenger_count']]])
trip = trip.drop(trip.index[[True if value <= 0 or value > 200 else False for value in trip['total_amount']]])
# Only consider the specified geometric area to reduce data size
# 40.702, -74.020
# 40.782, -73.851
trip = trip.drop(trip.index[[True if value < -74.020 or value > -73.851 else False for value in trip['pickup_longitude']]])
trip = trip.drop(trip.index[[True if value < -74.020 or value > -73.851 else False for value in trip['dropoff_longitude']]])
trip = trip.drop(trip.index[[True if value < 40.702 or value > 40.782 else False for value in trip['pickup_latitude']]])
trip = trip.drop(trip.index[[True if value < 40.702 or value > 40.782 else False for value in trip['dropoff_latitude']]])

# Round coordinates to 3 decimal places to reduce number of unique coordinates, thus work load of obtaining neighbourhood
# from geocoding service is reduced.
# The third decimal place is worth up to 111 m, the error caused by rounding is up to 55.5 m, which is not critical for this task
f = lambda x: round(x,3)
coordinate_columns = ['pickup_longitude', 'dropoff_longitude', 'pickup_latitude', 'dropoff_latitude']
trip[coordinate_columns] = trip[coordinate_columns].apply(f)
trip[coordinate_columns] = trip[coordinate_columns].astype(str)

# Create two new columns that hold pickup coordiante and dropoff coordiante with latitude and longitude concatenated
f = lambda x: ",".join(x)
trip["pickup_coordinate"]=trip[["pickup_latitude", "pickup_longitude"]].apply(f, axis=1)
trip["dropoff_coordinate"]=trip[["dropoff_latitude", "dropoff_longitude"]].apply(f, axis=1)
# Remove latitudes and longitudes
trip = trip.drop(coordinate_columns, axis=1)

# Save the cleaned data set
file_save = file_read[:-4] + '_cleaned' + file_read[-4:]
trip.to_csv(file_save)


