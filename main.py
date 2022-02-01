import csv
from typing import Union
import requests
from os import environ

IP_API_URL = 'https://api.freegeoip.app/json/'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
IP_API_KEY = environ.get('API_key')
WEATHER_API_KEY = environ.get('W_API_key')
CSV_FILE = 'ip_data.csv'

test_ip_list = ['122.35.203.161',
                '174.217.10.111',
                '187.121.176.91',
                '176.114.85.116',
                '174.59.204.133',
                '54.209.112.174',
                '109.185.143.49',
                '176.114.253.216',
                '210.171.87.76',
                '24.169.250.142']


def get_city_and_country(ip_address: str) -> tuple:
    city_url = f'{IP_API_URL}{ip_address}?apikey={IP_API_KEY}'
    result = requests.get(city_url).json()
    return result['ip'], result['country_name'], result['city'], result['latitude'], result['longitude']


def get_weathers(lat: Union[int, float], lon: Union[int, float]) -> tuple:
    payload = {'latitude': lat, 'longitude': lon, 'units': 'metric', 'appid': WEATHER_API_KEY}
    weather_url = f'{WEATHER_URL}?lat={lat}&lon={lon}'
    r = requests.get(weather_url, params=payload)
    result = r.json()
    return result['main']['temp'], result['weather'][0]['main']


def get_all_data(ip_address: str) -> tuple:
    geographical_data = get_city_and_country(ip_address)
    meteorological_data = get_weathers(geographical_data[3], geographical_data[4])
    return geographical_data[:3] + meteorological_data


def make_csv_file(list_of_ips: list) -> None:
    with open(CSV_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'Country', 'City', 'Temp', 'Weather'])
        for ip in list_of_ips:
            writer.writerow(get_all_data(ip))


make_csv_file(test_ip_list)
