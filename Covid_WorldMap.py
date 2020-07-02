# Import Packages
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mpimg
import matplotlib.colors as colors
import matplotlib.colorbar as mcb
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
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
from matplotlib.lines import Line2D
from matplotlib.widgets import Slider, Button, RadioButtons
import cartopy.feature as cfeature
#import ffmpeg
import imageio
pd.set_option("display.max_rows", None, "display.max_columns", None)

#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

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

# Get Data from John Hopkins GitHub Repository --> RAW very important
print("Get Worldwide data")
inputdata = urllib.request.urlopen(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
print("Got Worldwide data")
# df_world = dataframe worldwide
df_world = pd.read_csv(inputdata, sep=",")
df_world.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)

#print(df_world)
print("Worldwide data was put into dataframe")

# Create a list of all dates
# Create a header list
header_list = df_world.columns.tolist()
#print("This is the header_list: ", header_list)
date_list = header_list[4:]
#print("This is the date_list: ", date_list)
index_12thofApril = date_list.index("4/12/20")
index_13thofApril = date_list.index("4/13/20")
index_14thofApril = date_list.index("4/14/20")
transition_period_list = [index_12thofApril,index_13thofApril,index_14thofApril]
transition_period_list_dates = ['4/12/20','4/13/20','4/14/20']


#Get Data from 12th of April and append Dataframe World
print("Get US data from 12th of April")
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
    if 'Grand Princess' in df_us_daily.index:
        df_us_daily = df_us_daily.drop(index = ['Grand Princess'])
    #print(df_us_daily)
    #I have state-wide data from the 12th of April -> I can have a threeday-average from the 13th of April. --> And "new data with a ratio value from the 14th of April"
    #I need threeday-average of US until 13th of April -> I need raw data from US until 14th of April.
    #Set United States in df_world to zero
    column_number_date = df_world_columns_list.index(date)
    if date in transition_period_list_dates:
        print("Transition phase, let's keep all the data yay")
    else:
        united_states_index = df_world_country_list.index('US')
        #print(united_states_index)
        df_world.iat[united_states_index, column_number_date] = 0
    for state in state_list:
        index_number_state = df_world_province_list.index(state)
        df_world.iat[index_number_state, column_number_date] = df_us_daily.at[state,'Confirmed']

print("All data on board, let's continue")
# Have a country list
country_list_original = df_world['Country'].tolist()
country_list_unique_all = np.unique(country_list_original)
# remove countries that have numbers broken down to provinces
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

# Adjust date-list: remove first and last day to enable three day moving average
date_list_adjusted = date_list[1:-1]
#print(date_list_adjusted)

# Make new Dataframe with three day moving averages
print("Create new Dataframe for three day moving averages")
header_list_threedayaverage = ["Lat", "Lon"] + date_list_adjusted
#print(header_list_threedayaverage)
df_world_threedayaverage = pd.DataFrame(index=country_and_province, columns=header_list_threedayaverage)
#print(df_world_threedayaverage)

# fill lat and lon
for row in total_rows_list:
    lat = df_world.at[row, 'Lat']
    lon = df_world.at[row, 'Long']
    province = df_world.at[row, 'Province']
    if pd.isna(province):
        location = df_world.at[row, 'Country']
    else:
        location = df_world.at[row, 'Province']
    #print(location, lat, lon)
    df_world_threedayaverage.at[location, 'Lat'] = lat
    df_world_threedayaverage.at[location, 'Lon'] = lon

#print(df_world_threedayaverage)

for day in date_list_adjusted:
    date_fractions = day.split('/')
    month = date_fractions[0]
    day_of_month = date_fractions[1]
    year = "20" + date_fractions[2]
    #print("day = " + day, "year = " + year, "month = " + month, "day_of_the_month = " + day_of_month)
    day1 = datetime.date(int(year), int(month), int(day_of_month))
    day0 = day1 - datetime.timedelta(days=1)
    day2 = day1 + datetime.timedelta(days=1)
    #print(day0)
    #print(day1)
    #print(day2)
    #print("This is the day " + day)
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
        #print(location, confirmed_cases_days_0_1_2)

        confirmed_cases_three_day_average = statistics.mean(confirmed_cases_days_0_1_2)
        df_world_threedayaverage.at[location, day1_header] = confirmed_cases_three_day_average

df_world_threedayaverage.at['US','4/14/20']=0
df_world_threedayaverage.at['US','4/15/20']=0
for state in state_list:
    df_world_threedayaverage.at[state,'4/12/20']=0
    df_world_threedayaverage.at[state, '4/11/20'] = 0
#print(df_world_threedayaverage)
print("Three day moving average dataframe is created")
print("Make a dataframe to see newly infected each day (depending on three day average)")

df_world_new_cases = pd.DataFrame(index=country_and_province, columns=date_list_adjusted)
#print(df_world_new_cases)

#Fill df_world_new_cases
# For the first day
for location in country_and_province:
    df_world_new_cases.at[location, '1/23/20'] = df_world_threedayaverage.at[location, '1/23/20']
#Loop for all following days
for day in date_list_adjusted[1:]:
    #print(day)
    column_number_day = date_list_adjusted.index(day)
    day_yesterday = date_list_adjusted[column_number_day - 1]
    for location in country_and_province:
        df_world_new_cases.at[location , day] = df_world_threedayaverage.at[location,day] - df_world_threedayaverage.at[location, day_yesterday]

#print(df_world_new_cases)
print("Newly infected dataframe was created")

print("Make dataframe to calculate relative new cases")
df_world_change_cases = pd.DataFrame(index=country_and_province, columns=date_list_adjusted)
value_for_change_from_zero_to_something = 999
#Special case for relative values for 23.01.2020 and 24.01.2020 because there are no two days before to compare
for location in country_and_province:
    if df_world_threedayaverage.at[location, '1/23/20'] > 0:
        df_world_change_cases.at[location, '1/23/20'] = value_for_change_from_zero_to_something
        df_world_change_cases.at[location,'1/24/20'] = df_world_new_cases.at[location,'1/24/20']/df_world_new_cases.at[location,'1/23/20']
    else:
        df_world_change_cases.at[location, '1/23/20'] = 0
        if df_world_threedayaverage.at[location,'1/24/20'] > 0:
            df_world_change_cases.at[location,'1/24/20'] = value_for_change_from_zero_to_something
        else:
            df_world_change_cases.at[location,'1/24/20'] = 0
for day in date_list_adjusted[2:]:
    #print(day)
    column_number_day = date_list_adjusted.index(day)
    day_yesterday = date_list_adjusted[column_number_day - 1]
    day_before_yesterday = date_list_adjusted[column_number_day-2]
    for location in country_and_province:
        new_cases_today = df_world_new_cases.at[location,day]
        new_cases_daybeforeyesterday = df_world_new_cases.at[location,day_before_yesterday]
        if new_cases_today == 0:
            new_cases_ratio = 0
        elif new_cases_daybeforeyesterday == 0:
            new_cases_ratio = value_for_change_from_zero_to_something
        else:
            new_cases_ratio = new_cases_today/new_cases_daybeforeyesterday
        #print("location: ", location, "today: ", day , "day before yesterday: ", day_before_yesterday, "new cases today: ", new_cases_today,
              #"new cases day before yesterday: ", new_cases_daybeforeyesterday, "new cases ratio: ", new_cases_ratio)
        df_world_change_cases.at[location, day] = new_cases_ratio


new_cases_per_average_state_13th_of_April = df_world_new_cases.at['US','4/13/20']/50
#print("per state average = ", new_cases_per_average_state_13th_of_April)

for state in state_list:
    new_cases_state_14th_of_April = df_world_new_cases.at[state,'4/14/20']
    new_cases_state_15th_of_April = df_world_new_cases.at[state, '4/15/20']
    new_cases_ratio_14 = new_cases_state_14th_of_April/new_cases_per_average_state_13th_of_April
    if new_cases_state_14th_of_April == 0:
        new_cases_ratio_15 = value_for_change_from_zero_to_something
    else:
        new_cases_ratio_15 = new_cases_state_15th_of_April/new_cases_state_14th_of_April
    df_world_change_cases.at[state, '4/14/20'] = new_cases_ratio_14
    df_world_change_cases.at[state,'4/15/20'] = new_cases_ratio_15
    #print (state, new_cases_per_average_state_13th_of_April, new_cases_state_14th_of_April, new_cases_state_15th_of_April, 'rates: ',
           #new_cases_ratio_14, df_world_change_cases.at[state,'4/15/20'])

#print(df_world_change_cases)
print("Datframe for new cases ratio was created")

for state in state_list:
    df_world_threedayaverage.at[state, '4/13/20'] = 0

fig = plt.figure(num="Corona Map", figsize=(12.8, 6.5))
corona_maps_list = []
colormap = cm.get_cmap('hot_r',9)
colors_list = colormap(np.linspace(0,1,9))
bounds = (0,0.33,0.67,1,1.33,1.67,2)
cmap = colors.ListedColormap(colors_list[1:7])
norm = colors.BoundaryNorm(bounds, cmap.N)
cmap.set_over(colors_list[7])

date_list_test = ('4/10/20','4/11/20','4/12/20','4/13/20','4/14/20','4/15/20')

for date_map in date_list_adjusted:
    date_map_index = date_list_adjusted.index(date_map)
    date_tomorrow_index = date_map_index + 1

    fig = plt.figure(num="Corona Map", figsize=(12.8, 6.5))

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.coastlines()
    ax.set_global()
    ax.stock_img()

    ax.set_title("Confirmed Cases of Corona Patients and Infection Rate on {} per Country or Province".format(date_map),
                 pad=22)


    for location in country_and_province:
        confirmed_cases_value = df_world_threedayaverage.at[location, date_map]
        new_cases = df_world_new_cases.at[location, date_map]
        relative_new_cases = df_world_change_cases.at[location, date_map]
        if confirmed_cases_value > 1:
            marker_color = 'white'
            marker_size_log = math.log(confirmed_cases_value,10)
            marker_size = marker_size_log*1.75
            if relative_new_cases > 0:
                marker_color = colors_list[1]
                if relative_new_cases > 0.33:
                    marker_color = colors_list[2]
                    if relative_new_cases > 0.67:
                        marker_color = colors_list[3]
                        if relative_new_cases > 1:
                            marker_color = colors_list[4]
                            if relative_new_cases > 1.33:
                                marker_color = colors_list[5]
                                if relative_new_cases > 1.67:
                                    marker_color = colors_list[6]
                                    if relative_new_cases > 2:
                                        marker_color = colors_list[7]

            if new_cases == 0:
                marker_color = 'limegreen'
                zero_infections_streak = 0
                for date_counter in date_list_adjusted[:date_tomorrow_index]:
                    newly_infected = df_world_new_cases.at[location,date_counter]
                    if newly_infected == 0:
                        zero_infections_streak = zero_infections_streak + 1
                    else:
                        zero_infections_streak = 0
                if zero_infections_streak >= 14:
                    marker_color = "green"
                #plt.text(df_world_threedayaverage.at[location,'Lon'], df_world_threedayaverage.at[location,'Lat'],
                         #zero_infections_streak, transform = ccrs.PlateCarree())


            plt.plot(df_world_threedayaverage.at[location, 'Lon'], df_world_threedayaverage.at[location, 'Lat'],
                     color=marker_color, marker='o', markersize=marker_size, transform=ccrs.PlateCarree())


    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, extend = 'max', extendfrac='auto', shrink=0.7, aspect=12, pad=0.05,
                 label='Infection Rate compared to two days ago')
    line1 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="limegreen",markersize= (math.log(100000,10))*1.75)
    line2 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="green",markersize= (math.log(100000,10))*1.75)
    line3 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="white",
                   markeredgecolor="black",markersize= (math.log(1000,10))*1.75)
    line4 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="white",
                   markeredgecolor="black",markersize= (math.log(10000,10))*1.75)
    line5 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="white",
                   markeredgecolor="black",markersize= (math.log(100000,10))*1.75)
    line6 = Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="white",
                   markeredgecolor="black",markersize= (math.log(1000000,10))*1.75)
    line7=Line2D(range(1), range(1), linewidth=0, color="white", marker='o', markerfacecolor="white",
                   markeredgecolor="white",markersize= 1)
    fig.legend((line1, line2), ('No new infections', 'No new infections for 14 days'), numpoints=1, ncol=1,
               loc='lower right',title='Infection-free locations',
               frameon=False)
    fig.legend((line3, line4, line5, line6), ('1000 infections', '10\'000 infections',
                                                            '100\'000 infections',
                                                            '1\'000\'000 infections'), numpoints=1, ncol=2,
               loc='lower center', bbox_to_anchor=(0.4,0),
               title='Absolute numbers of confirmed infections',
               frameon=False)

    plt.tight_layout(pad=1.08)
    #plt.savefig("/Users/evaammann/Desktop/Corona_Maps/CoronaMap_{}".format(date_map_index),dpi=300)
    #plt.savefig("CoronaMap_{}".format(date_map_index), dpi=100)
    #print("Image Saved for {}".format(date_map))
    #corona_map_png = mpimg.imread("CoronaMap_{}.png".format(date_map_index))
    #corona_map_imshow = plt.imshow(corona_map_png)

    #corona_maps_list.append(corona_map_imshow,)

    #plt.show()

    if date_map == date_list_adjusted[-1]:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(0.5)
        plt.close()


#print(corona_maps_list)
#print("Start the Animation")
#FFWriter = animation.FFMpegWriter(fps=20)
#fig_anim = plt.figure(num="Corona Map", figsize=(12.8, 6.5))
#anim = animation.ArtistAnimation(fig=fig, artists=corona_maps_list,interval=50, repeat_delay=3000,
                                   #blit=True)
#plt.show()


#anim.save('Corona Map Video.mp4', writer=writer)





