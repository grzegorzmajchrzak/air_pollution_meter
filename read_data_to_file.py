#!/usr/bin/python
import struct, sys, time, json
from lib import read_aqi, airly_config
import Adafruit_DHT

pm25, pm10 = read_aqi.read_pm_factors();
line = "%s   PM2.5: %s, PM10: %s\n" % (time.strftime("%Y.%m.%d %H:%M:%S"), pm25, pm10)
print(line)
	
with open(airly_config.FILE, 'a+') as outfile:
	outfile.write(line)
