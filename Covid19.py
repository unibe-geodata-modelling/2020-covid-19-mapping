#Corona-Virus Pandas
#Downloading the CSV-Data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Slash vor USER ist wichtig!!
inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/full_data.csv"
#What exactly is df?
df=pd.read_csv(inputdata, sep=",")
#What is this for?
df.dtypes
#Define "date" column as string values
df["date"].astype('str')
#What are we doing here?
df.astype({'date':'str'}).dtypes

#constants: population numbers of each country
popIT=60480000
popCH=8570000
popDE=82790000
popFR=70000000
popAU=8822000

#Extract the country Dataframes
df_IT=df[df.location=="Italy"]
df_FR=df[df.location=="France"]
df_AU=df[df.location=="Austria"]
df_CH=df[df.location=="Switzerland"]
df_DE=df[df.location=="Germany"]

#IT add day counting from case no.100 -> I want the day where case no 100 appeared to be day 0

df_IT["countIT"]=0
daycounter=0
for index, row in df_IT.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_IT._set_value(index, "countIT", daycounter)


df_CH["countCH"]=0
daycounter=0
for index,row in df_CH.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_CH._set_value(index,"countCH",daycounter)

df_DE["countDE"]=0
daycounter=0
for index,row in df_DE.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_DE._set_value(index,"countDE",daycounter)

df_AU["countAU"]=0
daycounter=0
for index,row in df_AU.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_AU._set_value(index,"countAU",daycounter)

df_FR["countFR"]=0
daycounter=0
for index,row in df_FR.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_FR._set_value(index,"countFR",daycounter)


#plot the data
plt.plot(df_IT.countIT, df_IT.total_cases/popIT*1000000, label="IT", color="blue")
plt.plot(df_FR.countFR, df_FR.total_cases/popFR*1000000, label="FR", color="green")
plt.plot(df_CH.countCH, df_CH.total_cases/popCH*1000000, label="CH", color="red")
plt.plot(df_DE.countDE, df_DE.total_cases/popDE*1000000, label="DE", color="yellow")
plt.plot(df_AU.countAU, df_AU.total_cases/popAU*1000000, label="AU", color="black")
plt.legend(loc="best",frameon=False)

plt.ylabel("no. of cases per 1 mio. inhabitants")
plt.xlabel("days after 100th case")
plt.show()
