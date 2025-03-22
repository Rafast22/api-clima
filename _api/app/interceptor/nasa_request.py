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
from datetime import datetime, timedelta

semaphore = asyncio.Semaphore(1)  

async def get_history_date(latitude: str, longitude: str):
    last_date = datetime.now()
    while True:
        r = await get_formated_dict(last_date.strftime("%Y%m%d"), last_date.strftime("%Y%m%d"), latitude, longitude)
        if len(r) == 0 or True in [any(value == -999.0 for value in obj.values()) for obj in r] :
            last_date = datetime(last_date.year, last_date.month-1, 1)
        else:
            del r
            break
    json_string = await get_formated_dict('20100101', last_date.strftime("%Y%m%d"),
                                          latitude, longitude)    
    return json_string

async def get_new_history_date(latitude: str, longitude: str, first_date: datetime):
    last_date = datetime.now()
    while True:
        r = await get_formated_dict(last_date.strftime("%Y%m%d"), last_date.strftime("%Y%m%d"), latitude, longitude)
        if len(r) == 0 or True in [any(value == -999.0 for value in obj.values()) for obj in r] :
            last_date -= timedelta(days=1)
        else:
            del r
            break
    json_string = await get_formated_dict(first_date.strftime("%Y%m%d"), 
                                          last_date.strftime("%Y%m%d"),
                                          latitude, longitude)    
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
    del years, counter, S_date, F_date, status, response_json, keys,first_date, last_date, url
    return prepare_object(req)

def insert_year_in_medium(data1:datetime, data2:datetime, year_list:list):
    new_date = data1 + (data2 - data1) / 2
    f_index = year_list.index(data2)
    year_list.insert(f_index, new_date)
    del new_date, f_index
    return year_list
def prepare_object(req):

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
    del timestamps
    return prepared_data

 