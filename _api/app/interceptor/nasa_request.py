import requests as requests
from bs4 import BeautifulSoup
import json
import aiohttp
import pandas as pd
from .interfaces.nasa import Data
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
import asyncio
from datetime import datetime
# from pandas.errors import 

semaphore = asyncio.Semaphore(1)  

async def get_history_date(latitude: str, longitude: str):
    today = datetime.now()
    json_string = await get_formated_dict('20100101', '20240101',latitude, longitude)    
    return json_string

async def fetch_data(session, url):
    async with semaphore:
        async with session.get(url) as response:
            return  response.status, await response.json()

async def fetch_request(url):
    async with aiohttp.ClientSession() as session:
        status, data = await fetch_data(session, url)
    return status, data


async def get_formated_dict(START_DATE, END_DATE, latitude: str, longitude: str):
    req = {}
    PARAMETERS = [
    #Relative Humidity at 2 Meters
        "RH2M",
    #Specific Humidity at 2 Meters
        "QV2M",
    #Temperature at 2 Meters
        "T2M",
    #
        "PRECTOTCORR",
    #    
        "WS2M"
    #add radiacion solar
] 
    S_date = datetime.strptime(START_DATE, "%Y%m%d")
    F_date = datetime.strptime(END_DATE, "%Y%m%d")
    # for parameter in PARAMETERS:
        # for year in range(S_date.year, f_date.year):
          
    counter = 0
    years:List[datetime] = [S_date, F_date]
    while True:
        first_date = years[counter].strftime('%Y%m%d')
        last_date = years[counter+1].strftime('%Y%m%d')
        url = f'https://power.larc.nasa.gov/api/temporal/hourly/point?start={first_date}&end={last_date}&latitude={latitude}&longitude={longitude}&community=AG&parameters={",".join(PARAMETERS)}&format=json&user=DAVE'
        try:
            
            status, response_json = await fetch_request(url)
            print(status)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            # return None
        
        try:
            keys = list(response_json['properties']['parameter'].keys())
            for key in keys:
                if key in req:
                    req[key].update(response_json['properties']['parameter'][key])
                else: 
                    req[key] = response_json['properties']['parameter'][key]

        except Exception as ex:
            print(ex)
            S_date = datetime.strptime(first_date, "%Y%m%d")
            F_date = datetime.strptime(last_date, "%Y%m%d")
            years = insert_year_in_medium(years[counter], years[counter+1], years)
            print(", ".join([str(year.year) for year in years]))
            continue
        counter +=1
        if len(years)-1 == counter:
            break
    return prepare_object(req)

def insert_year_in_medium(data1:datetime, data2:datetime, year_list:list):
    new_date = data1 + (data2 - data1) / 2
    f_index = year_list.index(data2)
    year_list.insert(f_index, new_date)
        #    medium = len(years) // 2  
        #         S_date = datetime.strptime(first_date, "%Y%m%d")
        #         F_date = datetime.strptime(last_date, "%Y%m%d")
        #         years.insert(medium, insert_year_in_medium(S_date, F_date))  
    # year_list.index(data2.year)
    return year_list
def prepare_object(req):
    # d={}
    # for r in req:
    #     print(r)
    #     d[r] = list(req[r].values())
    # d['date'] = list(req[0][list(req[0].keys())[0]].keys())

    # df = pd.DataFrame.from_dict(req)
    # json_data = df.to_dict(orient='records')

    timestamps = set(ts for subdict in req.values() for ts in subdict.keys())
    prepared_data = [
        {'Date': datetime.strptime(ts, "%Y%m%d%H"), 
         **{
             nome.lower(): req[nome][ts]
             for nome in req if ts in req[nome]
            }
        }
        for ts in sorted(timestamps)
    ]
    return prepared_data

 