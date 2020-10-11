#!/usr/bin/python3
import datetime
import subprocess

import RPi.GPIO as GPIO

from lib import airly

R = 20
Y = 16
G = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(R, GPIO.OUT)
GPIO.setup(Y, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)


def on(d):
    if not is_night():
        GPIO.output(d, GPIO.HIGH)


def off(d):
    GPIO.output(d, GPIO.LOW)


def fan(speed):
    if is_night():
        speed = min(speed - 1, 2)
    subprocess.run(["ssh", "192.168.1.200", "./aqi_fan.py", str(speed)])


def is_night():
    current_hour = datetime.datetime.now().hour
    return not (6 < current_hour < 23);

# main
off(G)
off(R)
off(Y)

max_inside_current = airly.get_pollution_local()
previous_max_inside = airly.get_pollution_local_previous()
max_inside = max(max_inside_current, previous_max_inside)

if max_inside < 30:
    on(G)
    fan(0)
elif max_inside < 50:
    on(G)
    fan(1)
elif max_inside < 75:
    on(Y)
    fan(2)
elif max_inside < 100:
    on(Y)
    fan(3)
else:
    on(R)
    fan(4)
