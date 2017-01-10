import RPi.GPIO as gpio
import time

GPIO.setmode(gpio.BCM)

TRIG = 23
ECHO = 24

print "Distance Measurement in progress"


gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)

gpio.output(TRIG, False)

print "Waiting for sensor to settle"

time.sleep(2)

