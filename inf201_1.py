import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
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

plt.plot(df['referenceTime'], df['value'])
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
#plt.show()
table=pd.DataFrame({"mean": [df["value"].mean()], "median": [df["value"].median()], "min": [df["value"].min()], "max": [df["value"].max()]})
print(f"""
mean  : {table["mean"][0]:.2f} 
median: {table["median"][0]:.2f}
min   : {table["min"][0]:.2f}
max   : {table["max"][0]:.2f}
""")