#NewProject
#Information
#Import Packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib.request

#Get Data
inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/PyCharmProjects/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

#Downloading the CSV-Data
#inputdata = urllib.request.urlopen("http://cowid.netlify.com/data/full_data.csv")

print ("This is the inputdata: " + inputdata)


#What exactly is df?
df=pd.read_csv(inputdata, sep=",")
print (df)
#What is this for?
df_Switzerland = pd.DataFrame(data=df,index="Switzerland")
print (df_Switzerland)











#Still to do: Nicer showing of the graph, I just want enitre number ticks, I do not want to define the maximum and automated date creation! Otherwise very nice :D