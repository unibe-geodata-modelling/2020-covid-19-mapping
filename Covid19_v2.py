#Corona-Virus Pandas
#Downloading the CSV-Data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib.request

dateoftoday= input("What is today's date? ")

#Inputdata aus Internet
inputdata = urllib.request.urlopen("http://cowid.netlify.com/data/full_data.csv")
#Slash vor USER ist wichtig!!
#inputdata = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/full_data.csv"
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
popJP=126200000
popUS=327350000
popCI=1400000000

#Extract the country Dataframes
df_IT=df[df.location=="Italy"]
df_FR=df[df.location=="France"]
df_AU=df[df.location=="Austria"]
df_DE=df[df.location=="Germany"]
df_CH=df[df.location=="Switzerland"]
df_JP=df[df.location=="Japan"]
df_CI=df[df.location=="China"]
df_US=df[df.location=="United States"]
#IT add day counting from case no.100 -> I want the day where case no 100 appeared to be day 0

df_IT["countIT"]=0
daycounter=0
for index, row in df_IT.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_IT._set_value(index, "countIT", daycounter)

df_US["countUS"]=0
daycounter=0
for index, row in df_US.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_US._set_value(index, "countUS", daycounter)

df_CI["countCI"]=0
daycounter=0
for index, row in df_CI.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_CI._set_value(index, "countCI", daycounter)

df_JP["countJP"]=0
daycounter=0
for index, row in df_JP.iterrows():
    if row["total_cases"]>=100:
        daycounter+=1
        df_JP._set_value(index, "countJP", daycounter)


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


#plot the absolute data
plt.subplot(1,2,1)
plt.plot(df_IT.countIT, df_IT.total_cases, label="IT", color="blue")
plt.plot(df_FR.countFR, df_FR.total_cases, label="FR", color="green")
plt.plot(df_DE.countDE, df_DE.total_cases, label="DE", color="yellow")
plt.plot(df_AU.countAU, df_AU.total_cases, label="AU", color="black")
plt.plot(df_JP.countJP, df_JP.total_cases, label="JP", color="grey")
plt.plot(df_CH.countCH, df_CH.total_cases, label="CH", color="red")
plt.plot(df_US.countUS, df_US.total_cases, label="US", color="purple")
#plt.plot(df_CI.countCI, df_CI.total_cases, label="CI", color="pink")

plt.legend(loc="best",frameon=False)
plt.ylabel("no. of cases")
#Ich hätte gerne, dass die Achse immer ganze Zahlen anzeigt!
plt. xlabel("days after 100th case")
plt.xticks(np.arange(0,31,5))


#plot the data per million inhabitants
plt.subplot(1,2,2)
plt.plot(df_IT.countIT, df_IT.total_cases/popIT*1000000, label="IT", color="blue")
plt.plot(df_FR.countFR, df_FR.total_cases/popFR*1000000, label="FR", color="green")
plt.plot(df_DE.countDE, df_DE.total_cases/popDE*1000000, label="DE", color="yellow")
plt.plot(df_AU.countAU, df_AU.total_cases/popAU*1000000, label="AU", color="black")
plt.plot(df_JP.countJP, df_JP.total_cases/popJP*1000000, label="JP", color="grey")
plt.plot(df_CH.countCH, df_CH.total_cases/popCH*1000000, label="CH", color="red")
plt.plot(df_US.countUS, df_US.total_cases/popUS*1000000, label="US", color="purple")
#plt.plot(df_CI.countCI, df_CI.total_cases/popCI*1000000, label="CI", color="pink")

plt.legend(loc="best",frameon=False)
plt.ylabel("no. of cases per million inhabitants")
plt. xlabel("days after 100th case")
plt.xticks(np.arange(0,31,5))

plt.tight_layout()
plt.suptitle("Data was retrieved on {}.".format(dateoftoday))
plt.show()

#Still to do: Nicer showing of the graph and automated date creation! Otherwise very nice :D