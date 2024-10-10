import requests as requests
from bs4 import BeautifulSoup
import json
import asyncio
from interfaces.nasa import Data
from helpers.helper import BASE_URL, START_DATE, END_DATE, COMMUNITY, PARAMETERS


#@async
def _get_data_from_position(latitude: str, longitude: str, parameter: str) -> Data:
    request =  requests.get(BASE_URL + f'/temporal/hourly/point?start={START_DATE}&end={END_DATE}&latitude={latitude}&longitude={longitude}&community={COMMUNITY}&parameters={parameter}&format=json&user=DAVE')
    #parse json
    data = json.loads(request.content)
    d=Data(data)
    return d

async def _get_all_data(latitude: str, longitude: str):
    data: list = []
    # for parameter in PARAMETERS:
    #    data.append(get_data_from_position(latitude, longitude, parameter))
       
data = _get_data_from_position("-25.65", "-54.716666666667", ",".join(PARAMETERS))
s = data.get_formated_dict()

async def get_history_date():
    
    pass