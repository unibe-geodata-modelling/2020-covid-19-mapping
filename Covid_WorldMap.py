# NewProject

# Information
# Import Packages
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mpimg
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
import numpy as np
import numpy.ma as ma
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

#Find a solution for 11/12th of April for moving average

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
print("Get Worldwide data")
# Get Data from John Hopkins GitHub Repository --> RAW very important
inputdata = urllib.request.urlopen(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
print("Got Worldwide data")
# df_world = dataframe worldwide
df_world = pd.read_csv(inputdata, sep=",")
df_world.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

print(df_world)
print("Worldwide data was put into dataframe")

# Create a list of all dates
# Create a header list
header_list = df_world.columns.tolist()
#print("This is the header_list")
#print(header_list)
date_list = header_list[4:]
#print("This is the date_list")
#print(date_list)
index_12thofApril = date_list.index("4/12/20")
index_13thofApril = date_list.index("4/13/20")
transition_period_list = [index_12thofApril,index_13thofApril]
transition_period_list_dates = ['4/12/20','4/13/20']
print("Get US data from 12th of April")
#Get Data from 12th of April and append Dataframe World
us12april = urllib.request.urlopen(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/04-12-2020.csv")
print("Now append all US States to the World dataframe and remove double cruise ships")
df_us12april = pd.read_csv(us12april, sep=",")
df_us12april.rename(columns={'Province_State': 'Province', 'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)
df_us12april.set_index('Province', drop=False, inplace=True)
df_us12april = df_us12april.drop(
    columns=["Last_Update","Confirmed", "Deaths", "Recovered", "Active", "FIPS", "Incident_Rate", "People_Tested",
             "People_Hospitalized", "Mortality_Rate", "UID", "ISO3", "Testing_Rate", "Hospitalization_Rate"])
if 'Recovered' in df_us12april.index:
    df_us12april = df_us12april.drop(index=['Recovered'])
if 'Diamond Princess' in df_us12april.index:
    df_us12april = df_us12april.drop(index=['Diamond Princess'])
# Check for this one
if 'Grand Princess' in df_us12april.index:
    df_us12april = df_us12april.drop(index=['Grand Princess'])
#print(df_us12april)
df_world = df_world.append(df_us12april,ignore_index = True)
#print(df_world)
print("World Dataframe has now US states appended")
df_world_province_list = df_world['Province'].tolist()
df_world_country_list = df_world['Country'].tolist()
df_world_columns_list = df_world.columns.tolist()
#print(df_world_index_list)
#print(df_world_columns_list)
#Get a state list
state_list = df_us12april.index.tolist()
#print(state_list)
print("Prepare the World Dataframe properly")
# Fill with zeros before 12th of April
for date in date_list[:index_12thofApril]:
    for state in state_list:
        index_number_state = df_world_province_list.index(state)
        column_number_date = df_world_columns_list.index(date)
        df_world.iat[index_number_state, column_number_date] = 0
#print(df_world)


print("Now get the US data for every day since the 12th of April and immediately fill the data to the dataframe")
#Getting US-country-level data filling the dataframe after 12th of April and deleting US country number!
for date in date_list[index_12thofApril:]:
    #print('Date for the loop: ', date)
    date_fractions = date.split('/')
    day = date_fractions [1]
    month = date_fractions [0]
    year = "20" + date_fractions[2]
    #print("day: ", day, "month:", month)
    # Make US-Date-Format out of it
    if len(month) == 2:
        month_url = month
    else:
        month_url = '0'+ month
    if len(day) == 2:
        day_url = day
    else:
        day_url = '0'+ day

    date_url = month_url + '-' + day_url + '-' + year
    #print(date_url)

    usdailyreport = urllib.request.urlopen(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv".format(date_url))

    df_us_daily = pd.read_csv(usdailyreport, sep=",")
    df_us_daily.rename(columns={'Province_State':'Province','Country_Region':'Country','Long_':'Long'},inplace=True)
    df_us_daily.set_index('Province',drop=False, inplace=True)
    df_us_daily = df_us_daily.drop(columns=["Last_Update","Deaths","Recovered","Active","FIPS","Incident_Rate","People_Tested","People_Hospitalized","Mortality_Rate","UID","ISO3","Testing_Rate","Hospitalization_Rate"])
    if 'Recovered' in df_us_daily.index:
        df_us_daily = df_us_daily.drop(index=['Recovered'])
    if 'Diamond Princess' in df_us_daily.index:
        df_us_daily = df_us_daily.drop(index=['Diamond Princess'])
    #Check for this one in df_world
    if 'Grand Princess' in df_us_daily.index:
        df_us_daily = df_us_daily.drop(index = ['Grand Princess'])
    #print(df_us_daily)
    #I have state-wide data from the 12th of April -> I can have a threeday-average from the 13th of April.
    #I need threeday-average of US until 12th of April -> I need raw data from US until 13th of April.
    #Set United States in df_world to zero
    column_number_date = df_world_columns_list.index(date)
    if date in transition_period_list:
        print("Transition phase, let's keep all the data yay")
    else:
        united_states_index = df_world_country_list.index('US')
        #print(united_states_index)
        df_world.iat[united_states_index, column_number_date] = 0
    for state in state_list:
        index_number_state = df_world_province_list.index(state)
        df_world.iat[index_number_state, column_number_date] = df_us_daily.at[state,'Confirmed']

#print(df_world)
print("All data on board, let's continue")
# Have a country list
country_list_original = df_world['Country'].tolist()
country_list_unique_all = np.unique(country_list_original)
# remove countries that have numbers broken down to provinces -> Automation?
index_Canada = np.argwhere(country_list_unique_all == 'Canada')
index_Australia = np.argwhere(country_list_unique_all == 'Australia')
index_China = np.argwhere(country_list_unique_all == 'China')
country_list_unique = np.delete(country_list_unique_all, [index_Australia, index_Canada, index_China])
#print(country_list_unique)
# Have a Province list
province_list_original = df_world['Province'].tolist()
#print(province_list_original)
province_list_unique_with_nan = np.unique(province_list_original)
#print(province_list_unique_with_nan)
index_nan = np.argwhere(province_list_unique_with_nan == 'nan')
province_list_unique = np.delete(province_list_unique_with_nan, index_nan)
#print(province_list_unique)
# Bring lists together
country_and_province_appended = np.append(country_list_unique, province_list_unique)
country_and_province = np.unique(country_and_province_appended)
#print("Here is the final list:")
#print(country_and_province)

# Count the number of rows
total_rows = len(df_world.index)
total_rows_list = range(0, total_rows)
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

df_world_threedayaverage.at['US','4/13/20']=0
for state in state_list:
    df_world_threedayaverage.at[state,'4/12/20']=0
    df_world_threedayaverage.at[state, '4/11/20'] = 0
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

# Make new dataframe to calculate relative new infected cases
df_world_change_cases = pd.DataFrame(index=country_and_province, columns=date_list_adjusted)
value_for_change_from_zero_to_something = 999

for location in country_and_province:
    if df_world_threedayaverage.at[location, '1/23/20'] > 0:
        df_world_change_cases.at[location, '1/23/20'] = value_for_change_from_zero_to_something
    else:
        df_world_change_cases.at[location, '1/23/20'] = 0
for day in date_list_adjusted[1:]:
    print(day)
    column_number_day = date_list_adjusted.index(day)
    day_yesterday = date_list_adjusted[column_number_day - 1]
    for location in country_and_province:
        new_cases_today = df_world_new_cases.at[location,day]
        new_cases_yesterday = df_world_new_cases.at[location,day_yesterday]
        if new_cases_yesterday == 0:
            new_cases_ratio = value_for_change_from_zero_to_something
            if new_cases_today == 0:
                new_cases_ratio = 0
        else:
            new_cases_ratio = new_cases_today/new_cases_yesterday
        print("location: ", location, "today: ", day , "yesterday: ", day_yesterday, "new cases today: ", new_cases_today,
              "new cases yesterday: ", new_cases_yesterday, "new cases ratio: ", new_cases_ratio)
        df_world_change_cases.at[location, day] = new_cases_ratio

print(df_world_change_cases)


def corona_map_single_plot(date_map):
    date_map_index = date_list_adjusted.index(date_map)
    date_tomorrow_index = date_map_index + 1
    lat = df_world_threedayaverage['Lat']
    lon = df_world_threedayaverage['Lon']
    threedayaverage_map = df_world_threedayaverage[date_map]
    newly_infected_map = df_world_new_cases[date_map]
    new_infection_rate_map = df_world_change_cases[date_map]
    fig = plt.figure(num="Corona Map", figsize=(12.8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.coastlines()
    ax.set_global()
    ax.stock_img()
    ax.set_title("Confirmed Cases of Corona Patients on {} and trend per country or province".format(date_map))
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()
    plt.show()
# I need to create subplots instead of plots
#for date_now in date_list_adjusted:
    #date_now_index = date_list_adjusted.index(date_now)
    #date_tomorrow_index = date_now_index + 1
    #map_name = "map_" + date_now
    #fig = plt.figure(num=map_name, figsize=[12.8, 8])
    #ax = plt.axes(projection=ccrs.PlateCarree())
    #ax.set_global()
    #ax.add_feature(cfeature.LAND)
    #ax.add_feature(cfeature.OCEAN)
    #ax.add_feature(cfeature.COASTLINE)
    #ax.add_feature(cfeature.BORDERS, linestyle=":")
    #ax.set_title("Confirmed Cases of Corona Patients on {} and trend per country or province".format(date_now))

    #for location in country_and_province:
        #confirmed_cases_value = df_world_threedayaverage.at[location, date_now]
        #new_cases = df_world_new_cases.at[location, date_now]
        #new_cases_ratio = new_cases/confirmed_cases_value
        #new_change_cases = df_world_change_cases.at[location, date_now]
        #if confirmed_cases_value > 0:
            #marker_color = 'white'
            #marker_color = 'orange'
            #marker_size = math.log(confirmed_cases_value)
            #if marker_size < 1:
                #marker_size = 1
            #See changes in confirmed cases:
            #if new_change_cases < 0.9:
                #marker_color = 'yellow'
            #if new_change_cases > 1.1:
                #marker_color = 'red'
            #if new_cases == 0:
                #marker_color = 'greenyellow'
                #zero_infections_streak = 0
                #print("We have 0 new cases on {} in {}!".format(date_now,location))
                #for date_counter in date_list_adjusted[:date_tomorrow_index]:
                    #newly_infected = df_world_new_cases.at[location,date_counter]
                    #if newly_infected == 0:
                        #zero_infections_streak = zero_infections_streak + 1
                    #else:
                        #zero_infections_streak = 0
                #if zero_infections_streak >= 14:
                    #marker_color = "green"
            #plt.plot(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
                     #color=marker_color, marker='o', markersize=marker_size, transform=ccrs.PlateCarree())
    #subplot_row_number = (np.argwhere(date_list_adjusted == date_now))
    #plt.title(date_now)
    #print(date_now + " plot was created")
    #plt.show(block = False)
    #plt.pause(0.5)
    #plt.close()

    # plt.text(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
    # 'yay' , horizontalalignment='right', transform=ccrs.PlateCarree())

def corona_map(date_map):
    lat = df_world_threedayaverage['Lat']
    lon = df_world_threedayaverage['Lon']
    threedayaverage_map = df_world_threedayaverage[date_map]
    print(type(threedayaverage_map))
    s_linear = threedayaverage_map.astype('float64')
    print(type(s_linear))
    s_log = np.log(s_linear)
    s_square = np.square(s_log)
    print(type(s_square))
    masked_threedayaverage = ma.masked_equal(threedayaverage_map,0)
    #threedayaverage_map_log = float(math.log(threedayaverage_map))
    newly_infected_map = df_world_new_cases[date_map]
    new_infection_rate_map = df_world_change_cases[date_map]
    fig = plt.figure(num="Corona Map", figsize=(12.8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.coastlines()
    ax.set_global()
    ax.stock_img()
    #norming the colorbar
    divnorm = colors.DivergingNorm(vmin = 0, vcenter = 1, vmax = 2)
    #adding limegreen to the hot_r colormap
    hot_r = cm.get_cmap('hot_r', 256)
    newcolors = hot_r(np.linspace(0, 1, 256))
    #limegreen = np.array([0, 255 / 256, 0, 1])
    #newcolors[:5, :] = limegreen
    #newcolors2 = newcolors[:-10]
    #newcmp = ListedColormap(newcolors2)

    plt.scatter(lon, lat, transform=ccrs.PlateCarree(),
        label=None, s= s_square, c=new_infection_rate_map, cmap='YlOrRd',norm = divnorm,linewidth=0,zorder=3)
    #if 0 new cases make limegreen:
    for location in country_and_province:
        confirmed_cases_three_day_average = df_world_threedayaverage.at[location,date_map]
        new_cases_today = df_world_new_cases.at[location,date_map]
        if confirmed_cases_three_day_average > 0:
            if new_cases_today == 0:
                marker_size = math.log(confirmed_cases_three_day_average)
                marker_color = 'greenyellow'
                zero_infections_streak = 0
                print("We have 0 new cases on {} in {}!".format(date_map,location))
                date_now_index = date_list_adjusted.index(date_map)
                date_tomorrow_index = date_now_index + 1
                # if 14 days no new cases make dark green:
                #for date_counter in date_list_adjusted[:date_tomorrow_index]:
                    #newly_infected = df_world_new_cases.at[location,date_counter]
                    #if newly_infected == 0:
                        #zero_infections_streak = zero_infections_streak + 1
                    #else:
                        #zero_infections_streak = 0
                    #if zero_infections_streak >= 14:
                        #marker_color = "green"
                plt.plot(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
                         color=marker_color, marker='o', markersize=marker_size, transform=ccrs.PlateCarree(), zorder =5)

    plt.axis(aspect='equal')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.colorbar(label='Relative new Corona Cases on {}'.format(date_map))
    plt.show(block = False)
    plt.pause(0.5)
    plt.close()
    plt.show()

for date in date_list_adjusted:
    corona_map(date)

for date in date_list_adjusted:
    corona_map_single_plot(date)
#corona_map('4/10/20')
#corona_map('4/11/20')
#corona_map('4/12/20')
#corona_map('4/13/20')
#corona_map('4/14/20')
#corona_map('4/15/20')

