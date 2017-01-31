#!/usr/bin/python
"""
Code created for sonar, allows for specification of one trigger pin and multiple echo pins.
waits for all values to be collected from sonars before returning value. 
Limitations seem to include response to angular materials.
"""
import RPi.GPIO as gpio
import time
import sys

gpio.setmode(gpio.BCM)

class SonarSensor(object): 

    def __init__(self, TRIG, ECHO):
        self.TRIG=TRIG
        self.ECHO=ECHO  
        self.VAL={}
        self.FLAGS={}
        self.max_range=400

    def start_up(self):
        gpio.setup(self.TRIG,gpio.OUT)
        for i in self.ECHO:
            gpio.setup(i,gpio.IN)
            gpio.add_event_detect(i,gpio.BOTH,callback=self.get_time)
            self.VAL[i]=[0,0]
            self.FLAGS[i]=False

    def trigger_trig(self):
        for i in self.FLAGS.keys():
            self.FLAGS[i]=False
        gpio.output(self.TRIG,gpio.HIGH)
        time.sleep(0.000001)
        gpio.output(self.TRIG,gpio.LOW)

    def measure_vals(self):
        self.trigger_trig()
        time.sleep(0.1)
        conditional_statement=False
        print self.FLAGS.values()
        while not conditional_statement:
            if len([c for c in self.FLAGS.values() if c is True])==len(self.FLAGS.values()):
                conditional_statement=True
            else:
                print "Condition not met"
                time.sleep(0.05)
        output=''
        for channel, [time1,time2] in zip(self.VAL.keys(),self.VAL.values()):
            my_distance=round(17150 * (time2-time1),2)
            if my_distance>self.max_range:
                my_distance='>400'
            output+='%s: %s cm ,'%(channel,my_distance)
        return output

    def get_time(self,channel):
        if gpio.input(channel):
            #print "High %s @ %s"%(channel,time.time())
            self.VAL[channel][0]=time.time()
        else:
            #print "Low %s @ %s"%(channel,time.time())
            self.VAL[channel][1]=time.time()
            self.FLAGS[channel]=True
            


def run_func():
    a=SonarSensor(23,[22,24])
    a.start_up()
    while True:

        try:
            print str(a.measure_vals())+'m\n'
            time.sleep(0.2)
        except (KeyboardInterrupt, SystemExit):
            gpio.cleanup()
            print "\nExiting"
            sys.exit(0);
run_func()
