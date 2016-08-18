#!/usr/bin/env python3

# Importing libraries
import sht21
import datetime

sht21 = sht21.SHT21()

# File for Datastorage
file = "log-sht21.txt"  

# Format of the data
s = '{:%d.%m.%Y %H:%M}'.format(datetime.datetime.now())

# Measuring
try:
    (temp, humidity) = sht21.measure(1)
    s = s + "\t%s\t%d" % (temp, humidity)
except:
    s = s + "SHT21 I/O Error"

# Showing the data
print(s)

# Saving the data in the file
with open(file, "a") as fp:
    s = s + "\r\n"
    fp.write(s)
