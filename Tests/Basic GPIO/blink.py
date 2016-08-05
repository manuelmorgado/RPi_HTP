# Blink test for Raspberry Pi B, using the port 15(wiringPi) or GPIO14 in the board.
# Connect to the General Purpose I/O (port IO14) the correct resistors and then one LED
# and finally to the GND. (Python version)
# Date: 28/07/2016


# Importing Raspberry libraries.
import RPi.GPIO as gpio         #Library for pins GPIO.
import time

#Setting up the Raspberry as BOARD mode and pins (IN/OUT/PWM/UP/DOWN/TREE etc).
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)         #LED output pin.

Set up counter.
i=0;

while i!=2:
    if i==0:                    #When output from motion sensor is LOW.
        print "OFF",i
        gpio.output(14, 0)       #Turn OFF LED.
        time.sleep(0.5)
        i+=1
    elif i==1:                  #When output from motion sensor is HIGH.
        print "ON",i
        gpio.output(14, 1)       #Turn ON LED.
        time.sleep(0.5)
        i-=1