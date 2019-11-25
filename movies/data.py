import requests
import pprint
import csv
from decouple import config

SECRET_KEY = '289ef966efc661f9b5c3a9943f43a88e'
api_url = f'https://api.themoviedb.org/3/movie/550?api_key={SECRET_KEY}&callback=test'

response = requests.get(api_url)
pprint.pprint(response)