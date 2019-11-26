import requests
from decouple import config
from bs4 import BeautifulSoup as bts
from datetime import datetime, timedelta
import csv, requests, os, json
from pprint import pprint

with open('movie.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip().split(','))