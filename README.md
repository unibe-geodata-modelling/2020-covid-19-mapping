# The Spread of Corona Virus across the World

## Purpose of this Code
This code was written by Eva Ammann as seminar work for the seminar “Geodata Analysis and Modelling” at the University of Bern during the spring semester of 2020. 
It was written in using Python 3.8 in PyCharm Community 2019.3 and a Conda environment.

## Contact data
Name: Eva Ammann

E-Mail: Eva.ammann@students.unibe.ch

## About the Code
This code visualizes the global spread of lab-confirmed Covid-19 cases across the world from January 23rd on. It shows the confirmed cases per country, except for China, Australia and Canada where the data is broken down to Provinces. For the United States, the data is available on state-level from the 12th of April on. 
The data is retrieved from the John Hopkins University’s (JHU) GitHub repository (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data). During the Covid-19 pandemic, the Center for Systems Science and Engineering at the John Hopkins University in Baltimore, United States has emerged as trustworthy source for global data on the corona virus. It frequently and semi-automatically updates numbers of confirmed cases, deaths, recovered patients and where available tests conducted for all countries in the world. 

In this code, only the numbers on confirmed infections are used. The main datafile used from the JHU’s repository is the global time series on confirmed infections. In this file there is all the data needed for the countries, the overseas territories, the cruise ships and the provinces of Canada, China and Australia. From the 12th of April on, program code calls the daily reports of US states. The data on the confirmed cases is taken from each of them and appended to the global dataframe.

## Calculation and Dataframe Creation Method
The data collection takes place in several steps. Firstly, the global datafile is called, read as CSV and converted into a dataframe. Secondly, the US datafile for the 12th of April is called, read as CSV, formatted and appended to the global dataframe. Thirdly, the US datafile for every day since the 12th of April is called, read as CSV and the data filled into the global dataframe. 

Then a new dataframe is created which is two days shorter, one day at the beginning and one day at the end. This dataframe is used to calculate the three-day rolling average of confirmed infection cases in order to smoothen the numbers. Special attention has to be paid to the transition in the US from nationwide to statewide data. Since state-specific data is available from the 12th of April on, the first three-day average is calculated correctly on the 13th of April. 

The next dataframe calculates the new infections per day, based on the three-day moving average. Again, special attention has to be paid to the new infections when state data across the US is available. The problem is the calculation of the new cases per day. Usually, the total number of cases on day x-1 are subtracted from the total number of cases on day x. However, for the 13th of April, the first day on which all US states have a three-day moving average, there is no day x-1 so there is no knowledge about how many new cases were registered within one day. However, as long as this is taken into consideration for the next dataframe, this poses no further problem. 

The last dataframe calculates the infection rate compared to two days ago. It shows the quotient of the newly infected people today over the newly infected people of the day before yesterday. Considering the transition from country to statewide data in the US, the following has to be considered. Since the infection rate is based on new confirmed infections per day, the 13th of April cannot be used for this calculation. However, there is a solution: 
To calculate the infection rate of the 14th of April, the total amount of newly registered cases in the entire US on the 13th of April is divided by 50, the amount of states, and then every state compares its newly registered corona cases from the 14th of April to the national state average of the 13th of April. 

To calculate the individual infection rate of the 15th of April, the newly confirmed cases of the 15th of April are compared to the newly confirmed cases of the 14th of April, so there is only one day in between. From the 16th of April on, the comparison of the infection rate of the states is in accordance with all countries and provinces across the world. 
After the creation of all dataframes, the program loops through all available dates. For each day it loops through all locations, assesses the current state and trend of registered corona cases and plots it on a world map. There is even a special loop that checks for countries and provinces that have been corona-infection-free for at least 14 days, which is presumably the maximal incubation time of the virus (Lauer et al., 2020).

Each of the maps is displayed for half a second, creating an animation for the user. The map of the last available day remains visible and has to be closed with the cursor.

Each maps looks like this:

![Corona Map](https://github.com/unibe-geodata-modelling/2020-covid-19-mapping/blob/master/CoronaMap_159.png)


By deleting the hashtag in line 438 each map can be saved individually as .png.

## Possible improvements of the code
- Code could be made leaner by combining all information into one dataframe with several dimensions
- Creating an ArtistAnimation with all maps and export it as .mp4 video
- Adding a slider so that the user can manually move between the days
- Changing from a 3-day to a 7-day rolling average in order to account for weekly infection number fluctuation


## Acknowledgments
Many thanks to Dr. Pascal Horton and Dr. Andreas Zischg for this very interesting and insightful seminar!

## References
Lauer, S.A., Grantz, K.H., Bi, Q., Jones, F.K., Zheng, Q., Meredith, H.R., Azman, A.S., Reich, N.G. & Lessler, J. (2020): The Incubation Period of Coronavirus Disease 2019 (COVID-19) From Publicly Reported Confirmed Cases: Estimation and Application. Annals of Internal Medicine: Volume 172, Issue 9, pages 577-582.
