import requests as requests
from bs4 import BeautifulSoup
import json
import aiohttp
import pandas as pd
from .interfaces.nasa import Data
from .._models.nasa_data import gravar_bulk
import time
# from pandas.errors import 


async def get_history_date(latitude: str, longitude: str):
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
    json_string = await get_formated_dict('20100101', '20240101',latitude, longitude, PARAMETERS)    
    # json_raw = json.loads(json_string)
    # d=Data(data)
    # a = get_formated_dict(json_string)
    # j = Data.get_formated_dict()

    
    return json_string

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_request(url):
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, url)
    return data


async def get_formated_dict(START_DATE, END_DATE, latitude: str, longitude: str, parameters: list[str]):
    req = []
    for parameter in parameters:
       
        url = f'https://power.larc.nasa.gov/api/temporal/hourly/point?start={START_DATE}&end={END_DATE}&latitude={latitude}&longitude={longitude}&community=AG&parameters={parameter}&format=json&user=DAVE'

        try:
            
            response_json = await fetch_request(url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
        req.append(response_json['properties']['parameter'])

    d={}
    for r in req:
        for paramter in r.keys():
            print(paramter.lower(), len(r[paramter].keys()))
            d[paramter.lower()] =list( r[paramter].values())
    d['date'] = list(req[0][list(req[0].keys())[0]].keys())

    df = pd.DataFrame.from_dict(d)
    json_data = df.to_dict(orient='records')
    return json_data