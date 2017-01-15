#!/usr/bin/python
import RPi.GPIO as gpio
import time
import sys

# Global Variables:
TRIG = 23
ECHO1 = 22
ECHO2 = 27
ECHO3 = 17
SENSOR_PAUSE = 0.5


def sense(trig_pin, echo_pin):

    # Send pulse signal
    gpio.output(trig_pin, True)
    time.sleep(0.1)
    gpio.output(trig_pin, False)

    # Record the last 'low' timestamp
    while gpio.input(echo_pin) == 0:
        pulse_start = time.time()

    while gpio.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Speed = distance / time mofo's
    # Speed of sound at sea level = 343m/s
    # And divide by 2, the sound has traveled there and back
    # so 17150 x time = distance

    distance = round(17150 * pulse_duration, 2)
    return distance


def setup():

    print "Initializing sensors"
    gpio.setmode(gpio.BCM)
    # Pi Output
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, False)
    # Pi Input
    gpio.setup(ECHO1, gpio.IN)
    gpio.setup(ECHO2, gpio.IN)
    gpio.setup(ECHO3, gpio.IN)

    print "Waiting for sensors to settle"
    time.sleep(2)


def start():

    setup()

    while True:
        try:
            print "ECHO1: " + str(sense(TRIG, ECHO1)) + "   -   ECHO2: " + \
                  str(sense(TRIG, ECHO2)) + "  -   ECHO3: " + str(sense(TRIG, ECHO3))

            #print "ECHO1: " + str(sense(TRIG, ECHO1)) + "   -   ECHO3: " + \
             #     str(sense(TRIG, ECHO3))
            time.sleep(SENSOR_PAUSE)

        except (KeyboardInterrupt, SystemExit):
            gpio.cleanup()
            print "\nExiting"
            sys.exit(0)

start()
