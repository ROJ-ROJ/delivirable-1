import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
import yaml

with open("passord.txt") as tekst:
    for line in tekst:
        id=line

endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {'sources': 'SN17850','elements': 'mean(air_temperature P1D)','referencetime': '2025-01-01/2025-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))
json = r.json()
data = json['data']
df = pd.DataFrame()
df = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)

plt.figure()
plt.plot(df['referenceTime'], df['value'])
plt.xlabel("Date")
plt.ylabel("Temperature")
#plt.show()
table=pd.DataFrame({"mean": [df["value"].mean()], "median": [df["value"].median()], "min": [df["value"].min()], "max": [df["value"].max()]})

print(f"""
mean  : {table["mean"][0]:.2f} 
median: {table["median"][0]:.2f}
min   :{table["min"][0]:.2f}
max   : {table["max"][0]:.2f}
""")

#task 2
parameters = {'sources': 'SN17850','elements': "sum(precipitation_amount P1D)",'referencetime': '2025-01-01/2025-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))
json = r.json()
data = json["data"]
df2 = pd.DataFrame()
df2 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)


temperature = df.set_index("referenceTime")["value"]
precipitation = df2.set_index("referenceTime")["value"]

fig, ax1 = plt.subplots(figsize=(12, 6))

# Temperature
ax1.plot(temperature.index, temperature.values, color="red",label="temperature")
ax1.set_xlabel("Date")
ax1.set_ylabel("Temperature", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# Precipitation
ax2=ax1.twinx()
ax2.bar(precipitation.index, precipitation.values,color="blue",label="rain")
ax2.set_ylabel("rain", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

plt.title("Temperature and Rain")
#plt.show()
#task 3

parameters = {'sources': 'SN17850','elements': 'mean(air_temperature P1D)','referencetime': '1925-01-01/1925-12-31'}
r = requests.get(endpoint, parameters, auth=(id,''))
json = r.json()
data = json['data']
df3 = pd.DataFrame()
df3 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
df3["referenceTime"] = pd.to_datetime(df3["referenceTime"])

# Convert dates to day of year
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

plt.tight_layout()
plt.show()



table2=pd.DataFrame({"mean": [df3["value"].mean()], "median": [df3["value"].median()], "min": [df3["value"].min()], "max": [df3["value"].max()]})
print(f"""
mean   2025: {table["mean"][0]:.2f} /  mean  1925: {table2["mean"][0]:.2f}
median 2025: {table["median"][0]:.2f} /  median 1925: {table2["median"][0]:.2f}
min    2025:{table["min"][0]:.2f} / min    1925: {table2["min"][0]:.2f}
max    2025: {table["max"][0]:.2f} / max    1925: {table2["max"][0]:.2f}
""")


#task 4

def HeatWave(id,year,station_name):
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {'sources': station_name,'elements': 'max(air_temperature P1D)','referencetime': f'{year}-01-01/{year}-12-31'}
    r = requests.get(endpoint, parameters, auth=(id,''))
    json = r.json()
    data = json['data']
    df4 = pd.DataFrame()
    df4 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
    t0=0
    t1=0
    t2=0
    t3=0
    t4=0
    with open("heatwave_summary", "w") as file:
        file.write("dates:\n")
        heatwave="av"
        for i, temperatur in enumerate(df4["value"]):
               t4=t3
               t3=t2
               t2=t1
               t1=t0
               t0=temperatur
              
               if t0>=27 and t1>=27 and t2>=27 and t3>=27 and t4>=27:
                   if heatwave=="av":
                       heatwave_start = df4['referenceTime'].iloc[i-4]
                       heatwave="på"
               elif heatwave=="på":
                   file.write(f"- {heatwave_start}-{df4['referenceTime'].iloc[i-1]}\n")
                   heatwave="av"
        file.write(f'station_id: {id}\n')
        file.write(f'station_name: "{station_name}"\n')
        file.write(f'year: {year}\n')


HeatWave(id,2025,"SN17850")

#task 5

def test(id,year,station_name):
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {'sources': station_name,'elements': "mean(air_temperature P1D)",'referencetime': f'{year}-01-01/{year}-12-31'}
    r = requests.get(endpoint, parameters, auth=(id,''))
    json = r.json()
    data = json['data']
    df5 = pd.DataFrame()
    df5 = pd.concat([pd.DataFrame(item['observations']).assign(referenceTime=item['referenceTime'],sourceId=item['sourceId'])for item in data],ignore_index=True)
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
    plt.figure()
    plt.plot(df5["referenceTime"], t_avrege)
    plt.xlabel("Time")
    plt.ylabel("Temperature 7 day avrage")
    plt.scatter(df5["referenceTime"], df5["value"])
    plt.show()
    
print(test(id,2025,"SN17850"))

plt.show()