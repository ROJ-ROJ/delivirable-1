import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
import yaml


# Gathers the pasword from file passord.txt
with open("passord.txt") as tekst:
    for line in tekst:
        id=line

#gathers the data from the frost api a
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {'sources': 'SN17850','elements': 'mean(air_temperature P1D)','referencetime': '2025-01-01/2025-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))

#sets the data in to a dataframe
json = r.json()
data = json['data']
df = pd.DataFrame()
df = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)

#plots the data
plt.figure()
plt.plot(df['referenceTime'], df['value'])
plt.xlabel("Date")
plt.ylabel("Temperature")
#plt.show()

#sets data in to table and prints mean,median... table 
table=pd.DataFrame({"mean": [df["value"].mean()], "median": [df["value"].median()], "min": [df["value"].min()], "max": [df["value"].max()]})


print(f"""
mean  : {table["mean"][0]:.2f} 
median: {table["median"][0]:.2f}
min   :{table["min"][0]:.2f}
max   : {table["max"][0]:.2f}
""")

#task 2
#gathers data on rain and sets it intu a data frame
parameters = {'sources': 'SN17850','elements': "sum(precipitation_amount P1D)",'referencetime': '2025-01-01/2025-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))
json = r.json()
data = json["data"]
df2 = pd.DataFrame()
df2 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)

#plots the temprature and rain on the same graph 
temperature = df.set_index("referenceTime")["value"]
precipitation = df2.set_index("referenceTime")["value"]
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(temperature.index, temperature.values, color="red",label="temperature")
ax1.set_xlabel("Date")
ax1.set_ylabel("Temperature", color="red")
ax1.tick_params(axis="y", labelcolor="red")
ax2=ax1.twinx()
ax2.bar(precipitation.index, precipitation.values,color="blue",label="rain")
ax2.set_ylabel("rain", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")
plt.title("Temperature and Rain")
#plt.show()

#task 3

#gather dta from 1925 and sets it in to a data frame
parameters = {'sources': 'SN17850','elements': 'mean(air_temperature P1D)','referencetime': '1925-01-01/1925-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))
json = r.json()
data = json['data']
df3 = pd.DataFrame()
df3 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
df3["referenceTime"] = pd.to_datetime(df3["referenceTime"])

#plots the temprature from 1925 and 2025 on the same graph
df3["day"] = df3["referenceTime"].dt.dayofyear
df["referenceTime"] = pd.to_datetime(df["referenceTime"])
df["day"] = df["referenceTime"].dt.dayofyear
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df3["day"],df3["value"],color="blue",label="1925")
ax.plot(df["day"],df["value"],color="red",label="2025")
ax.set_xlabel("Time")
ax.set_ylabel("Temperature")
ax.set_title("Temperature 1925 and 2025")
ax.legend()
plt.show()


#sets data from 1925in to tavble and prints mean,median... from tble 1925 and 2025 
table2=pd.DataFrame({"mean": [df3["value"].mean()], "median": [df3["value"].median()], "min": [df3["value"].min()], "max": [df3["value"].max()]})
print(f"""
mean   2025: {table["mean"][0]:.2f} /  mean  1925: {table2["mean"][0]:.2f}
median 2025: {table["median"][0]:.2f} /  median 1925: {table2["median"][0]:.2f}
min    2025:{table["min"][0]:.2f} / min    1925: {table2["min"][0]:.2f}
max    2025: {table["max"][0]:.2f} / max    1925: {table2["max"][0]:.2f}
""")


#task 4

#funksjon for creating html file whith heatwaiwes
def HeatWave(id,year,station_name):
    #gather data and sets it in to a data frame
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {'sources': station_name,'elements': 'max(air_temperature P1D)','referencetime': f'{year}-01-01/{year}-12-31'}
    r = requests.get(endpoint, parameters, auth=(id,''))
    json = r.json()
    data = json['data']
    df4 = pd.DataFrame()
    df4 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
    #crates 5 vairiabels to store 5 days of temprature 
    t0=0
    t1=0
    t2=0
    t3=0
    t4=0
    #creates a file and writes dates: in the first line
    with open("heatwave_summary", "w") as file:
        file.write("dates:\n")
        heatwave="av"
        #lopps truhe the data 
        for i, temperatur in enumerate(df4["value"]):
               #sets the variabals to the last 5 tempratures
               t4=t3
               t3=t2
               t2=t1
               t1=t0
               t0=temperatur
               # if heatwave and hetwave er av sets hetwave on and  records start date 
               if t0>=27 and t1>=27 and t2>=27 and t3>=27 and t4>=27:
                   if heatwave=="av":
                       heatwave_start = df4['referenceTime'].iloc[i-4]
                       heatwave="på"
                # when the heatwave stops it writs the start date and end date. and sets hetwae of
               elif heatwave=="på":
                   file.write(f"- {heatwave_start}-{df4['referenceTime'].iloc[i-1]}\n")
                   heatwave="av"
        #writes the rest of the file 
        file.write(f'station_id: {id}\n')
        file.write(f'station_name: "{station_name}"\n')
        file.write(f'year: {year}\n')

HeatWave(id,2025,"SN17850")

#task 5
# Funksjon to plot the 7 day avrage temprature
def test(id,year,station_name):
    #henter data 
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {'sources': station_name,'elements': "mean(air_temperature P1D)",'referencetime': f'{year}-01-01/{year}-12-31'}
    r = requests.get(endpoint, parameters, auth=(id,''))
    json = r.json()
    data = json['data']
    df5 = pd.DataFrame()
    df5 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
    #makes variabels to savse the last seven tempraturs and a list to save the avrage temprature
    t0=0
    t1=0
    t2=0
    t3=0
    t4=0
    t5=0
    t6=0
    t_avrege=[]
    for i, temperatur in enumerate(df5["value"]):
        t6=t5
        t5=t4
        t4=t3
        t3=t2
        t2=t1
        t1=t0
        t0=temperatur
        t_avrege.append((t0+t1+t2+t3+t4+t5+t6)/7)
    #plots the 7 day avrage temprature and the scatter plots the daily tempratur
    plt.figure()
    plt.plot(df5["referenceTime"], t_avrege)
    plt.xlabel("Time")
    plt.ylabel("Temperature 7 day avrage")
    plt.scatter(df5["referenceTime"], df5["value"])
    plt.show()
    
print(test(id,2025,"SN17850"))
#shows the plots
plt.show()