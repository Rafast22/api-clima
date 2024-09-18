import requests as requests
from bs4 import BeautifulSoup
import json
from rest_framework.parsers import JSONParser
from ..interfaces.nasa import Data
from ..helpers.helper import BASE_URL, START_DATE, END_DATE, COMMUNITY, PARAMETERS


#@async
def get_data_from_position(latitude: str, longitude: str, parameter: str) -> Data:
    request =  requests.get(BASE_URL + f'/point?start=${START_DATE}&end={END_DATE}&latitude={latitude}&longitude={longitude}&community={COMMUNITY}&parameters={parameter}&format=json&user=DAVE')
    #parse json
    
    return json.dumps(request.content)

def get_all_data(latitude: str, longitude: str):
    data: list = []
    for parameter in PARAMETERS:
       data.append(get_data_from_position(latitude, longitude, parameter))
       
#def prepare_data