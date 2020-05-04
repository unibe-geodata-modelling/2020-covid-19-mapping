# NewProject

# Information
# Import Packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import datetime
import math
import statistics
import gdal
import osgeo
import cartopy.crs as ccrs
from datetime import date
import urllib.request
from matplotlib.widgets import Slider, Button, RadioButtons
import cartopy.feature as cfeature
import imageio


def datetoheader(gregorian_date):
    gregorian_date_string = str(gregorian_date)
    gregorian_date_list = gregorian_date_string.split('-')
    year_gregorian = gregorian_date_list[0]
    year_header = year_gregorian[2:]
    month_gregorian = gregorian_date_list[1]
    if month_gregorian.startswith("0"):
        month_header = month_gregorian[1]
    else:
        month_header = month_gregorian
    day_gregorian = gregorian_date_list[2]
    if day_gregorian.startswith("0"):
        day_header = day_gregorian[1]
    else:
        day_header = day_gregorian
    header_date = month_header + '/' + day_header + '/' + year_header
    return header_date


# Get Data locally (2nd of April 2020)
# inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/PyCharmProjects/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

# Get Data from John Hopkins GitHub Repository --> RAW very important
inputdata = urllib.request.urlopen(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

# df_world = dataframe worldwide
df_world = pd.read_csv(inputdata, sep=",")
df_world.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

print(df_world)

# Create a list of all dates
# Create a header list
header_list = df_world.columns.tolist()
print("This is the header_list")
print(header_list)
date_list = header_list[4:]
print("This is the date_list")
print(date_list)

# Have a country list
country_list_original = df_world['Country'].tolist()
country_list_unique_all = np.unique(country_list_original)
# remove countries that have numbers broken down to provinces -> Automation?
index_Canada = np.argwhere(country_list_unique_all == 'Canada')
index_Australia = np.argwhere(country_list_unique_all == 'Australia')
index_China = np.argwhere(country_list_unique_all == 'China')
country_list_unique = np.delete(country_list_unique_all, [index_Australia, index_Canada, index_China])
print(country_list_unique)
# Have a Province list
province_list_original = df_world['Province'].tolist()
print(province_list_original)
province_list_unique_with_nan = np.unique(province_list_original)
print(province_list_unique_with_nan)
index_nan = np.argwhere(province_list_unique_with_nan == 'nan')
province_list_unique = np.delete(province_list_unique_with_nan, index_nan)
print(province_list_unique)
# Bring lists together
country_and_province_appended = np.append(country_list_unique, province_list_unique)
country_and_province = np.unique(country_and_province_appended)
print("Here is the final list:")
print(country_and_province)

# Count the number of rows
total_rows = len(df_world.index)
total_rows_list = range(1, total_rows)
print(total_rows)

print("All days All countries and regions")

# Loop over all columns (days)
for day in date_list:
    print("This is the day " + day)
    # Loop over all rows (Countries and Provinces)
    for row in total_rows_list:
        province = df_world.at[row, 'Province']
        if pd.isna(province):
            location = df_world.at[row, 'Country']
        else:
            location = df_world.at[row, 'Province']
        confirmed_cases = df_world.at[row, day]
        print(location, confirmed_cases)

# Adjust date-list: remove first and last day to enable three day moving average
date_list_adjusted = date_list[1:-1]
print(date_list_adjusted)

# Make new Dataframe with three day moving averages
header_list_threedayaverage = ["Lat", "Lon"] + date_list_adjusted
print(header_list_threedayaverage)
df_world_threedayaverage = pd.DataFrame(index=country_and_province, columns=header_list_threedayaverage)
print(df_world_threedayaverage)

# fill lat and lon
for row in total_rows_list:
    lat = df_world.at[row, 'Lat']
    lon = df_world.at[row, 'Long']
    province = df_world.at[row, 'Province']
    if pd.isna(province):
        location = df_world.at[row, 'Country']
    else:
        location = df_world.at[row, 'Province']
    print(location, lat, lon)
    df_world_threedayaverage.at[location, 'Lat'] = lat
    df_world_threedayaverage.at[location, 'Lon'] = lon

print(df_world_threedayaverage)

for day in date_list_adjusted:
    date_fractions = day.split('/')
    month = date_fractions[0]
    day_of_month = date_fractions[1]
    year = "20" + date_fractions[2]
    print("day = " + day, "year = " + year, "month = " + month, "day_of_the_month = " + day_of_month)
    day1 = datetime.date(int(year), int(month), int(day_of_month))
    day0 = day1 - datetime.timedelta(days=1)
    day2 = day1 + datetime.timedelta(days=1)
    print(day0)
    print(day1)
    print(day2)
    print("This is the day " + day)
    # Loop over all rows (Countries and Provinces)
    for row in total_rows_list:
        location = df_world.at[row, 'Province']
        if pd.isna(location):
            location = df_world.at[row, 'Country']
        else:
            location = df_world.at[row, 'Province']
        day0_header = datetoheader(day0)
        day1_header = datetoheader(day1)
        day2_header = datetoheader(day2)
        confirmed_cases_day0 = df_world.at[row, day0_header]
        confirmed_cases_day1 = df_world.at[row, day1_header]
        confirmed_cases_day2 = df_world.at[row, day2_header]

        confirmed_cases_days_0_1_2 = [confirmed_cases_day0, confirmed_cases_day1, confirmed_cases_day2]
        print(location, confirmed_cases_days_0_1_2)

        confirmed_cases_three_day_average = statistics.mean(confirmed_cases_days_0_1_2)
        df_world_threedayaverage.at[location, day1_header] = confirmed_cases_three_day_average

print(df_world_threedayaverage)

#Make a new dataframe to see newly infected (depending on three day average)
df_world_new_cases = pd.DataFrame(index=country_and_province, columns=date_list_adjusted)
print(df_world_new_cases)

#Fill df_world_new_cases
# For the first day
for location in country_and_province:
    df_world_new_cases.at[location, '1/23/20'] = df_world_threedayaverage.at[location, '1/23/20']
#Loop for all following days
for day in date_list_adjusted[1:]:
    print(day)
    column_number_day = date_list_adjusted.index(day)
    day_yesterday = date_list_adjusted[column_number_day - 1]
    for location in country_and_province:
        df_world_new_cases.at[location , day] = df_world_threedayaverage.at[location,day] - df_world_threedayaverage.at[location, day_yesterday]

print(df_world_new_cases)

# I need to create subplots instead of plots
for date_now in date_list_adjusted:
    map_name = "map_" + date_now
    map = plt.figure(num=map_name, figsize=[12.8, 8])
    #plt.title("Confirmed Cases on " + date_now)
    geo_axes = map.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    geo_axes.set_global()
    geo_axes.stock_img()
    geo_axes.coastlines()
    geo_axes.add_feature(cfeature.BORDERS, linestyle=':')
    geo_axes.grid(False)

    for location in country_and_province:
        confirmed_cases_value = df_world_threedayaverage.at[location, date_now]
        new_cases = df_world_new_cases.at[location, date_now]
        new_cases_ratio = new_cases/confirmed_cases_value
        if confirmed_cases_value > 0:
            #marker_color = 'white'
            marker_color = 'orange'
            marker_size = math.log(confirmed_cases_value)
            if marker_size < 1:
                marker_size = 1
            #See changes in confirmed cases:
            if new_cases_ratio < 0.1:
                marker_color = 'yellow'
            if new_cases_ratio > 0.2:
                marker_color = 'red'
            if new_cases == 0:
                marker_color = 'greenyellow'
            plt.plot(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
                     color=marker_color, marker='o', markersize=marker_size, transform=ccrs.PlateCarree())
    #subplot_row_number = (np.argwhere(date_list_adjusted == date_now))
    #plt.title(date_now)
    print(date_now + " plot was created")
    plt.show(block = False)
    plt.pause(1)
    plt.close()
    # plt.text(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
    # 'yay' , horizontalalignment='right', transform=ccrs.PlateCarree())
