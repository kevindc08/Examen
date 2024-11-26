# %%
import pandas as pd
from fastapi import FastAPI

# %%
app=FastAPI()

# %%
df = pd.read_csv('Data/co-emissions-per-capita new.csv')
df['Annual CO₂ emissions (per capita)']=df[('Annual CO₂ emissions (per capita)')].str.replace('.','')
df['Annual CO₂ emissions (per capita)']=df[('Annual CO₂ emissions (per capita)')].astype('float')
df['Annual CO₂ emissions (per capita)']=round(df[('Annual CO₂ emissions (per capita)')]/1000000,2)

# %%
@app.get('/')
def index():
    return{"message":"Bienvenido"}

# %%
index()

# %%
@app.get("/data")
def data():
    pais = list(df['Entity'].unique())
    dic = {}
    for i in pais:
        data = df[df['Entity'] == i].sort_values(ascending=False, by='Year')
        dic2 = {}
        for j in range(len(data)):
            dic2[int(data['Year'].iloc[j])] = float(data['Annual CO₂ emissions (per capita)'].iloc[j])
        dic[data['Entity'].iloc[0]] = dic2
    return dic

# %%
data()

# %%
@app.get("/data/country/{country}")
def country(country: str):
    if country not in df['Entity'].values:
        return {"Error": f"{country}not found"}
    data = df[df['Entity'] == country].sort_values(ascending=False, by='Year')
    dic = {}
    for i in range(len(data)):
        dic[int(data['Year'].iloc[i])] = float(data['Annual CO₂ emissions (per capita)'].iloc[i])
    return {country:dic}

# %%
country('Mexico')

# %%
@app.get("/data/year/{year}")
def year(year: int):
    if year not in df['Year'].values:
        return {"Error": f"{year}not found"}
    data = df[df['Year'] == year].sort_values(ascending=False, by='Entity')
    dic = {}
    for i in range(len(data)):
        dic[data['Entity'].iloc[i]] = float(data['Annual CO₂ emissions (per capita)'].iloc[i])
    return {country:dic}

# %%
year(1990)


