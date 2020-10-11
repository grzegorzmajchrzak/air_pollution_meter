#!/usr/bin/python3
import re

import requests

from . import airly_config


def get_pollution_slomczynskiego() -> int:
    resp = requests.get(airly_config.URL_SLOMCZYNSKIEGO)
    if resp.status_code != 200:
        return 0
    pm25 = resp.json()['current']['values'][1]['value']
    pm10 = resp.json()['current']['values'][2]['value']
    return __pollution_in_percent(int(pm25), int(pm10))


def get_pollution_luczyce() -> int:
    resp = requests.get(airly_config.URL_LUCZYCE)
    if resp.status_code != 200:
        return 0
    pm25 = resp.json()['current']['values'][1]['value']
    pm10 = resp.json()['current']['values'][2]['value']
    return __pollution_in_percent(int(pm25), int(pm10))


def __pollution_in_percent(pm25: int, pm10: int) -> int:
    return int(100 * max(pm25 / airly_config.MAX_PM25, pm10 / airly_config.MAX_PM10))


def get_pollution_local() -> int:
    return __get_pollution_local_last(-1)


def get_pollution_local_previous() -> int:
    return __get_pollution_local_last(-2)


def __get_pollution_local_last(line_of_file: int):
    with open(airly_config.FILE) as myfile:
        lastline = (list(myfile)[line_of_file])
        result = re.search('.+ PM2.5: (\\d+), PM10: (\\d+)$', lastline, re.IGNORECASE)
        if result:
            pm25 = int(result.group(1))
            pm10 = int(result.group(2))
        return __pollution_in_percent(pm25, pm10)
