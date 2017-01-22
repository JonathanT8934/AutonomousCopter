#!/usr/bin/python
import RPi.GPIO as gpio
import time
import sys
import os

# Global Variables:
TRIG = 23
ECHO1 = 22
ECHO2 = 27
ECHO3 = 17
SENSOR_PAUSE = 0.01


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




# Provides continous stream of readings.
# Also captures readings in lists complete with timngs
def start(readings):

    setup()
    starttime = round(time.time(), 3)
    histogram = []
    sense1 = []
    sense2 = []
    sense3 = []

    for i in range(readings):
        try:

            s1 = str(sense(TRIG, ECHO1))
            s2 = str(sense(TRIG, ECHO2))
            s3 = str(sense(TRIG, ECHO3))

            sense1.append(s1)
            sense2.append(s2)
            sense3.append(s3)

            histogram.append(round(time.time() - starttime, 3))

            print "ECHO1: " + str(s1) + "   -   ECHO2: " + \
                  str(s2) + "  -   ECHO3: " + str(s3)


            time.sleep(SENSOR_PAUSE)

        except (KeyboardInterrupt, SystemExit):
            gpio.cleanup()
            print "\nExiting"
            sys.exit(0)


    # Write arrays to log file.

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path ='Logs/SonarTestingOutput-' + str(time.time()) + '.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, 'w') as f:
        for h, s1, s2, s3 in zip(histogram, sense1, sense2, sense3):
            line = str(h) + ', ' + str(s1) + ', ' + str(s2) + ', ' + str(s3) +'\n'
            f.write(line)


if len(sys.argv) > 1:
    readings = sys.argv[1]

    start(int(readings))

else:
    start(999)
