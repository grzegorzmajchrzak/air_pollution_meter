#!/usr/bin/python3

MAX_PM25 = 25
MAX_PM10 = 50
API_TOKEN = 'api_token'
URL_SLOMCZYNSKIEGO = 'https://airapi.airly.eu/v2/measurements/installation?apikey=%s&indexType=AIRLY_CAQI&installationId=9899' % API_TOKEN
URL_LUCZYCE = 'https://airapi.airly.eu/v2/measurements/installation?apikey=%s&indexType=AIRLY_CAQI&installationId=6628' % API_TOKEN
FILE = '/var/www/html/aqi.txt'