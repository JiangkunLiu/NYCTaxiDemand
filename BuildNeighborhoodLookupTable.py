import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from geopy import Nominatim
import time

# Part 1
# This part builds a coordinate-neighborhood lookup table
# Read cleaned data set
trip = pd.read_csv('trip_data_yellow+green_2016_1.csv')
# Get all coordinates appeared in both drop off and pickup locations
coordinates = trip['pickup_coordinate'].append(trip['dropoff_coordinate'])

# To further reduce the number of unique coordinates, remove rarely occurring coordinates
coordinates = coordinates.value_counts()
coordinate_series = pd.Series(coordinates.index[coordinates > 100])
print(coordinate_series.shape)

# coordinate_lookup = pd.read_csv('coordinate_lookup.csv')
# new_coor_green = []
# for val in coordinate_series:
#     if val not in coordinate_lookup.coordinate.values:
#         new_coor_green.append(val)
# coordinate_series = new_coor_green

# Use python library Geopy to obtain neighborhood from corresponding latitude and longitude.
geolocator = Nominatim()
def get_neighbourhood(coordinate):
    time.sleep(1)
    location = geolocator.reverse(coordinate, timeout=50)
    if location.address == None:
        return 'NaN'
    else:
        raw = location.raw['address']
        print(raw)
        if 'neighbourhood' in raw:
            return raw['neighbourhood']
        else:
            return raw['postcode']

# Build a list that holds neighborhood name for each coordinate
neighbourhood_series = ['NaN']*len(coordinate_series)
for i in range(0, len(coordinate_series)):
    print('%d ******************' % i)
    neighbourhood_series[i] = get_neighbourhood(coordinate_series[i])
# # Diagnose
# missing = coordinate_lookup[coordinate_lookup['neighbourhood']=='not found']
# for i in range(0, len(missing)):
#     print('%d ******************' % i)
#     print(missing['coordinate'].iloc[i])
#     missing['neighbourhood'].iloc[i] = get_neighbourhood(missing['coordinate'].iloc[i])

# Combine coordinate series and neighborhood series to form a lookup table
neighbourhood_series = pd.Series(neighbourhood_series)
coordinate_lookup = pd.DataFrame(data={'coordinate': coordinate_series, 'neighbourhood': neighbourhood_series})

# Somehow, for some coordinates, Geopy couldn't find neighbourhood name
# # Manual correction for yellow taxi lookup table
coordinate_lookup['neighbourhood'][2661]='Chelsea'
coordinate_lookup['neighbourhood'][2077]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2790]='Astoria'
coordinate_lookup['neighbourhood'][48]='Upper East Side'
coordinate_lookup['neighbourhood'][124]='Upper East Side'
coordinate_lookup['neighbourhood'][247]='Midtown East'
coordinate_lookup['neighbourhood'][337]='Upper East Side'
coordinate_lookup['neighbourhood'][357]='Upper East Side'
coordinate_lookup['neighbourhood'][446]='Upper East Side'
coordinate_lookup['neighbourhood'][451]='Upper East Side'
coordinate_lookup['neighbourhood'][481]='Upper East Side'
coordinate_lookup['neighbourhood'][517]='Upper East Side'
coordinate_lookup['neighbourhood'][633]='Upper East Side'
coordinate_lookup['neighbourhood'][636]='Upper East Side'
coordinate_lookup['neighbourhood'][653]='Upper East Side'
coordinate_lookup['neighbourhood'][718]='Garment District'
coordinate_lookup['neighbourhood'][909]='Upper East Side'
coordinate_lookup['neighbourhood'][954]='Upper East Side'
coordinate_lookup['neighbourhood'][966]='Midtown East'
coordinate_lookup['neighbourhood'][1034]='Upper East Side'
coordinate_lookup['neighbourhood'][1048]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][1092]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][1217]='Upper East Side'
coordinate_lookup['neighbourhood'][1330]='Garment District'
coordinate_lookup['neighbourhood'][1354]='Upper West Side'
coordinate_lookup['neighbourhood'][1519]='Upper East Side'
coordinate_lookup['neighbourhood'][1775]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][1844]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2090]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2128]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2148]='Greenwich Village'
coordinate_lookup['neighbourhood'][2186]='Lower East Side'
coordinate_lookup['neighbourhood'][2288]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2314]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2437]='Lower East Side'
coordinate_lookup['neighbourhood'][2460]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2465]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2638]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2652]='Greenwich Village'
coordinate_lookup['neighbourhood'][2715]='Stuyvesant Town'
coordinate_lookup['neighbourhood'][2740]='Stuyvesant Town'

# Manual correction for green taxi lookup table
coordinate_lookup['neighbourhood'][21]='Elmhurst'
coordinate_lookup['neighbourhood'][73]='Jackson Heights'
coordinate_lookup['neighbourhood'][75]='Jackson Heights'
coordinate_lookup['neighbourhood'][139]='DUMBO'
coordinate_lookup['neighbourhood'][152]='Jackson Heights'
coordinate_lookup['neighbourhood'][188]='Jackson Heights'
coordinate_lookup['neighbourhood'][207]='Jackson Heights'
coordinate_lookup['neighbourhood'][217]='Williamsburg'
coordinate_lookup['neighbourhood'][288]='Jackson Heights'
coordinate_lookup['neighbourhood'][305]='Astoria'
coordinate_lookup['neighbourhood'][335]='Astoria'
coordinate_lookup['neighbourhood'][346]='Astoria'
coordinate_lookup['neighbourhood'][359]='LIC'
coordinate_lookup['neighbourhood'][367]='Greenpoint'
coordinate_lookup['neighbourhood'][372]='Astoria'
coordinate_lookup['neighbourhood'][388]='Astoria'
coordinate_lookup['neighbourhood'][398]='Williamsburg'
coordinate_lookup['neighbourhood'][433]='Astoria'
coordinate_lookup['neighbourhood'][450]='Astoria'
coordinate_lookup['neighbourhood'][493]='Williamsburg'
coordinate_lookup['neighbourhood'][502]='Williamsburg'
coordinate_lookup['neighbourhood'][512]='Bushwick'
coordinate_lookup['neighbourhood'][565]='Jackson Heights'
coordinate_lookup['neighbourhood'][575]='East Elmhurst'
coordinate_lookup['neighbourhood'][577]='Williamsburg'
coordinate_lookup['neighbourhood'][580]='LIC'
coordinate_lookup['neighbourhood'][613]='Astoria'
coordinate_lookup['neighbourhood'][626]='Williamsburg'
coordinate_lookup['neighbourhood'][649]='Williamsburg'
coordinate_lookup['neighbourhood'][654]='Jackson Heights'
coordinate_lookup['neighbourhood'][656]='Woodside'
coordinate_lookup['neighbourhood'][669]='Jackson Heights'
coordinate_lookup['neighbourhood'][674]='Jackson Heights'
coordinate_lookup['neighbourhood'][677]='Woodside'
coordinate_lookup['neighbourhood'][684]='Astoria'
coordinate_lookup['neighbourhood'][691]='Bushwick'
coordinate_lookup['neighbourhood'][695]='Woodside'
coordinate_lookup['neighbourhood'][718]='Bushwick'
coordinate_lookup['neighbourhood'][768]='DUMBO'
coordinate_lookup['neighbourhood'][845]='Astoria'
coordinate_lookup['neighbourhood'][863]='Astoria'
coordinate_lookup['neighbourhood'][877]='Jackson Heights'
coordinate_lookup['neighbourhood'][887]='Astoria'
coordinate_lookup['neighbourhood'][903]='Jackson Heights'
coordinate_lookup['neighbourhood'][915]='Woodside'
coordinate_lookup['neighbourhood'][923]='Woodside'
coordinate_lookup['neighbourhood'][950]='Bushwick'
coordinate_lookup['neighbourhood'][1056]='East Elmhurst'

coordinate_lookup.to_csv('coordinate_lookup_green.csv')
# Merge lookup tables built from yellow and green taxi
# coordinate_lookup_yellow = pd.read_csv('coordinate_lookup_yellow.csv')
# coordinate_lookup_green = pd.read_csv('coordinate_lookup_green.csv')
# coordinate_lookup = coordinate_lookup_yellow.append(coordinate_lookup_green)
# coordinate_lookup.to_csv('coordinate_lookup.csv')

######################################################################################
# Part 2
# This part performs inner join between lookup table and trip data, so that we have a data set that contains
# neighborhood names for both pick up locations and drop off locations
coordinate_lookup = pd.read_csv('coordinate_lookup.csv')
# Merge trip data from yellow and green taxi, these data sets were cleaned
trip_yellow = pd.read_csv('D:/TLC/yellow_tripdata_2016-01_cleaned.csv')
trip_green = pd.read_csv('D:/TLC/green_tripdata_2016-01_cleaned.csv')
trip_data = trip_yellow.append(trip_green)

# Join the trip data with the lookup table to obtain pickup neighbourhood and dropoff neighbourhood
pickup_location = pd.DataFrame({'coordinate': coordinate_lookup['coordinate'], 'pickup_neighbourhood': coordinate_lookup['neighbourhood']})
dropoff_location = pd.DataFrame({'coordinate': coordinate_lookup['coordinate'], 'dropoff_neighbourhood': coordinate_lookup['neighbourhood']})

trip_data = pd.merge(trip_data, pickup_location, left_on='pickup_coordinate', right_on='coordinate', how='inner')
trip_data = pd.merge(trip_data, dropoff_location, left_on='dropoff_coordinate', right_on='coordinate', how='inner')

# Remove coordinate columns and save the table
trip_data = trip_data.drop(['Unnamed: 0', 'pickup_coordinate', 'dropoff_coordinate','coordinate_x', 'coordinate_y'], axis=1)
trip_data.to_csv('trip_data_yellow+green_2016_1.csv')

print(trip_data.shape)
print(trip_data.columns)
print(trip_data['pickup_neighbourhood'].unique().sort())