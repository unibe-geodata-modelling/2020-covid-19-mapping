# NewProject
# Information
# Import Packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import statistics
from datetime import date
import urllib.request
# Ask how to import GDAL packages etc. cartopy
#import cartopy.crs as ccrs

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
    day_gregorian = gregorian_date_list [2]
    if day_gregorian.startswith("0"):
        day_header = day_gregorian[1]
    else:
        day_header = day_gregorian
    header_date = month_header + '/'+ day_header + '/' + year_header
    return header_date

# Get Data locally (2nd of April 2020)
#inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/PyCharmProjects/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

# Get Data from John Hopkins GitHub Repository --> RAW very important
inputdata = urllib.request.urlopen("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

#df_world = dataframe worldwide
df_world = pd.read_csv(inputdata, sep=",")
df_world.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

print(df_world)

#Create a list of all dates
#Create a header list
header_list = df_world.columns.tolist()
print("This is the header_list")
print(header_list)
date_list = header_list[4:]
print ("This is the date_list")
print(date_list)

#Have a country list
country_list_original = df_world['Country'].tolist()
country_list_unique_all = np.unique(country_list_original)
#remove countries that have numbers broken down to provinces -> Automation?
index_Canada = np.argwhere (country_list_unique_all == 'Canada')
index_Australia = np.argwhere (country_list_unique_all == 'Australia')
index_China = np.argwhere (country_list_unique_all == 'China')
country_list_unique = np.delete (country_list_unique_all, [index_Australia, index_Canada, index_China])
print (country_list_unique)
# Have a Province list
province_list_original = df_world['Province'].tolist()
print(province_list_original)
province_list_unique_with_nan = np.unique(province_list_original)
print (province_list_unique_with_nan)
index_nan = np.argwhere(province_list_unique_with_nan == 'nan')
province_list_unique = np.delete(province_list_unique_with_nan,index_nan)
print(province_list_unique)
#Bring lists together
country_and_province = np.append(country_list_unique,province_list_unique)
print("Here is the final list:")
print(country_and_province)


# Dataframe for Switzerland
#df_Switzerland = df_world[df_world.Country == "Switzerland"]
#print(df_Switzerland)

# Dataframes Europe
#df_France = df_world[df_world.Country == "France"]
#df_Germany = df_world[df_world.Country == "Germany"]
#df_Italy = df_world[df_world.Country == "Italy"]
#print (df_France)
#print(df_Germany)
#print(df_Italy)


#Count the number of rows
total_rows = len(df_world.index)
total_rows_list = range (1,total_rows)
print(total_rows)

print("All days All countries and regions")

#Loop over all columns (days)
for day in date_list:
    print ("This is the day " + day)
    #Loop over all rows (Countries and Provinces)
    for row in total_rows_list:
        province = df_world.at[row, 'Province']
        if pd.isna(province):
            country = df_world.at[row, 'Country']
            print(country)
        else:
            province = df_world.at[row, 'Province']
            print(province)
        confirmed_cases = df_world.at[row,day]
        print (confirmed_cases)



#Adjust date-list: remove first and last day to enable three day moving average
date_list_adjusted = date_list[1:-1]
print(date_list_adjusted)

#Make new Dataframe with three day moving averages
header_list_threedayaverage = ["Lat","Lon"] + date_list_adjusted
print(header_list_threedayaverage)
df_world_threedayaverage = pd.DataFrame(index=country_and_province ,columns=header_list_threedayaverage)
print(df_world_threedayaverage)
#fill lat and lon
for row in total_rows_list:
    lat = df_world.at[row,'Lat']
    lon = df_world.at[row,'Long']
    province = df_world.at[row, 'Province']
    if pd.isna(province):
        location = df_world.at[row, 'Country']
    else:
        location = df_world.at[row, 'Province']
    print(location, lat, lon)


for day in date_list_adjusted:
    date_fractions = day.split('/')
    month = date_fractions[0]
    day_of_month = date_fractions[1]
    year = "20" + date_fractions[2]
    print ("day = " + day,"year = " + year, "month = " + month, "day_of_the_month = " + day_of_month)
    day1 = datetime.date(int(year),int(month),int(day_of_month))
    day0 = day1 - datetime.timedelta(days=1)
    day2 = day1 + datetime.timedelta(days=1)
    print(day0)
    print(day1)
    print(day2)
    print ("This is the day " + day)
    #Loop over all rows (Countries and Provinces)
    for row in total_rows_list:
        province = df_world.at[row, 'Province']
        if pd.isna(province):
            country = df_world.at[row, 'Country']
            print(country)
        else:
            province = df_world.at[row, 'Province']
            print(province)
        day0_header = datetoheader(day0)
        day1_header = datetoheader(day1)
        day2_header = datetoheader(day2)
        confirmed_cases_day0 = df_world.at[row,day0_header]
        confirmed_cases_day1 = df_world.at[row,day1_header]
        confirmed_cases_day2 = df_world.at[row,day2_header]

        confirmed_cases_days_0_1_2 = [confirmed_cases_day0,confirmed_cases_day1,confirmed_cases_day2]
        print(confirmed_cases_days_0_1_2)

        confirmed_cases_three_day_average = statistics.mean(confirmed_cases_days_0_1_2)
        print(confirmed_cases_three_day_average)
        #print (confirmed_cases)

print(df_world_threedayaverage)

#for location in country_and_province:


#ax = plt.axes(projection =ccrs.PlateCarree())
#ax.coastlines()
#plt.show()
