# The Spread of Corona Virus across the World

## Purpose of this Code
This code was written by Eva Ammann as seminar work for the seminar “Geodata Analysis and Modelling” at the University of Bern during the spring semester of 2020. 
It was written in using Python 3.8 in PyCharm Community 2019.3 and a Conda environment.

## Contact data
Name: Eva Ammann

E-Mail: Eva.ammann@students.unibe.ch

## About the Code
This code visualizes the global spread of lab-confirmed Covid-19 cases across the world from February 1st 2020 on and exports the visualization as a .gif animation to a specified directory. It shows the confirmed cases per country, except for China, Australia and Canada where the data is broken down to Provinces. For the United States, the data is available on state-level from the 12th of April on. 
The data is retrieved from the John Hopkins University’s (JHU) GitHub repository (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data). During the Covid-19 pandemic, the Center for Systems Science and Engineering at the John Hopkins University in Baltimore, United States has emerged as trustworthy source for global data on the corona virus. It frequently and semi-automatically updates numbers of confirmed cases, deaths, recovered patients and where available tests conducted for all countries in the world. 

In this code, only the numbers on confirmed infections are used. The main datafile used from the JHU’s repository is the global time series on confirmed infections. In this file there is all the data needed for the countries, the overseas territories, the cruise ships and the provinces of Canada, China and Australia. From the 12th of April on, the program code calls the daily reports of US states. The data on the confirmed cases is taken from each of them and appended to the global dataframe.

## Calculation and Dataframe Creation Method
The data collection takes place in several steps. Firstly, the global datafile is called, read as CSV and converted into a dataframe. Secondly, the US datafile for the 12th of April is called, read as CSV, formatted and appended to the global dataframe. Thirdly, the US datafile for every day since the 12th of April is called, read as CSV and the data filled into the global dataframe.

It is known that reported case numbers have a clear weekly variability with an oscillation minimum on the weekend (Bragato, 2020). Since the time series is long enough, a 7-day rolling average was chosen in order to always include every weekday when smoothing the case numbers and omit the weekly oscillation. This is why a new dataframe is created which is six days shorter, three days at the beginning and three days at the end. The 7-day rolling average is stored in this dataframe. Special attention has to be paid to the transition in the US from nationwide to statewide data. Since state-specific data is available from the 12th of April on, the first seven-day average is calculated correctly on the 15th of April. 

The next dataframe calculates the new infections per day, based on the seven-day moving average. Again, special attention has to be paid when state data across the US is available. The problem is the calculation of the new cases per day. Usually, the total number of cases on day x-1 are subtracted from the total number of cases on day x. However, for the 15th of April, the first day on which all US states have a seven-day moving average, there is no day  x-1 so there is no knowledge about how many new cases were registered within one day. So, the first day to have newly registered cases per state is the 16th of April. However, as long as this is taken into consideration for the next dataframe, this poses no further problem. 

The last dataframe calculates the infection rate compared to the same day a week ago. It shows the quotient of the newly infected people today over the newly infected people of seven days ago. Considering the transition from country to statewide data in the US, the following has to be considered: Since the infection rate is based on new confirmed infections per day, the 15th of April cannot be used for this calculation. Since the 16th of April is the first day with statewide data and the comparison time is one week, the first properly represented day is the 23rd of April for the states.

After the creation of all dataframes, the program loops through all available dates. For each day it loops through all locations, assesses the current state and trend of newly reported corona cases and plots it on a world map. There is even a special loop that checks for countries and provinces that have been corona-infection-free for at least 14 days, which is presumably the maximal incubation time of the virus (Lauer et al., 2020).

Each of the maps is displayed for half a second and saved to a previously defined directory. The map of the last available day remains visible and has to be closed with the cursor. After the last image is closed, all maps are compiled into a gif-animation and this is also saved in the previously defined directory. 

This is the .gif animation of the 11th of August 2020:

![Corona Map](https://github.com/unibe-geodata-modelling/2020-covid-19-mapping/blob/master/covid_animation.gif)


## Possible improvements of the code
- Code could be made leaner by combining all information into one dataframe with several dimensions
- Adding a slider so that the user can manually move between the days


## Acknowledgments
Many thanks to Dr. Pascal Horton and Dr. Andreas Zischg for this very interesting and insightful seminar!

## References
Bragato, P.L. (2020): Assessment of the weekly fluctuations of the Covid-19 cases in Italy and worldwide. Preprints. https://www.preprints.org/manuscript/202005.0202/v1 (accessed 02.07.2020)

Lauer, S.A., Grantz, K.H., Bi, Q., Jones, F.K., Zheng, Q., Meredith, H.R., Azman, A.S., Reich, N.G. & Lessler, J. (2020): The Incubation Period of Coronavirus Disease 2019 (COVID-19) From Publicly Reported Confirmed Cases: Estimation and Application. Annals of Internal Medicine: Volume 172, Issue 9, pages 577-582.
