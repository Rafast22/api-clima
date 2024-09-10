import requests as re
from bs4 import BeautifulSoup
import json
from rest_framework.parsers import JSONParser
from interfaces import nasa

CONST_URL = "https://power.larc.nasa.gov/api/temporal/hourly/"
"point?start=20240128&end=20240128&latitude=43.0972&longitude=-99.5544&community=AG&parameters=PRECTOTCORR&format=json&user=DAVE"
