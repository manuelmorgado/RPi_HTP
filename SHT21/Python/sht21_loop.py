#!/usr/bin/env python3

# Importing libraries
import sht21
import time
import datetime


sht21 = sht21.SHT21()

# Intervall for measurement
interval = 5  

# File for Datastorage
file = "log_loop.txt"  

print("SHT21: Write measurement data every", interval, "seconds to", file)

# Getting data and measuring
while 1:
    if ((int(time.time()) % interval) == 0):
        try:
            (temp, humidity) = sht21.measure(1)
            timestamp = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.datetime.now())
            s = "%s\t%s\t%d" % (timestamp, temp, humidity)
        except:
            s = "SHT21 I/O Error"
        print(s)
        with open(file, "a") as fp:
            s = s + "\r\n"
            fp.write(s)
        time.sleep(1)
    time.sleep(0.5)
