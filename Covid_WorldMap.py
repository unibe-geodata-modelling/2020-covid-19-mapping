# NewProject
# Information
# Import Packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib.request
# Ask how to import GDAL packages etc. cartopy
#import cartopy.crs as ccrs


# Get Data
inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/PyCharmProjects/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

# Downloading the CSV-Data
# inputdata = urllib.request.urlopen("http://cowid.netlify.com/data/full_data.csv")

print("This is the inputdata: " + inputdata)

#df_world = dataframe worldwide
df_world = pd.read_csv(inputdata, sep=",")
df_world.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

print(df_world)

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
df_Switzerland = df_world[df_world.Country == "Switzerland"]
print(df_Switzerland)

# Dataframes Europe
df_France = df_world[df_world.Country == "France"]
df_Germany = df_world[df_world.Country == "Germany"]
df_Italy = df_world[df_world.Country == "Italy"]
print (df_France)
print(df_Germany)
print(df_Italy)


# Automated dataframe creation
total_rows = len(df_world.index)
total_rows_list = range (1,total_rows)
print(total_rows)

print("Test March Switzerland")
march = range(1,31)
Switzerland_040220 = df_world.at[206,'3/1/20']
print (Switzerland_040220)
for day in march:
    date = '3/' + str(day) + '/20'
    print (date)
    for row in total_rows_list:
        province = df_world.at[row, 'Province']
        if pd.isna(province):
            country = df_world.at[row, 'Country']
            print(country)
        else:
            province = df_world.at[row, 'Province']
            print(province)
        #naming = 'Switzerland' + date
        Switzerland_March = df_world.at[row,date]
        print (Switzerland_March)
#Maybe create loops for days and location?
#Data for 1/22/20
#for location in country_and_province:



#ax = plt.axes(projection =ccrs.PlateCarree())
#ax.coastlines()
#plt.show()
# Still to do: Nicer showing of the graph, I just want enitre number ticks, I do not want to define the maximum and automated date creation! Otherwise very nice :D
