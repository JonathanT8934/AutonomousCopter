#!/usr/bin/python
import RPi.GPIO as gpio
import time
import sys

def sense():
    # Send pulse signal

    gpio.output(TRIG, True)
    time.sleep(0.000001)
    gpio.output(TRIG, False)

    # Record the last 'low' timestamp
    while gpio.input(ECHO) == 0:
        pulse_start = time.time()

    while gpio.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Speed = distance / time mofo's
    # Speed of sound at sea level = 343m/s
    # And divide by 2, the sound has traveled there and back
    # so 17150 x time = distance

    distance = round(17150 * pulse_duration, 2)
    return distance


gpio.setmode(gpio.BCM)

TRIG = 23
ECHO = 22

print "Distance Measurement in progress"


gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)

gpio.output(TRIG, False)

print "Waiting for sensor to settle"

time.sleep(2)

while True:

    try:
        print sense()
        time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        gpio.cleanup()
        print "\nExiting"
        sys.exit(0);