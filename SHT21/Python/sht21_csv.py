#!/usr/bin/env python3

import sht21
import datetime

sht21 = sht21.SHT21()
file = "log-sht21.txt"  # File for Datastorage

s = '{:%d.%m.%Y %H:%M}'.format(datetime.datetime.now())
try:
    (temp, humidity) = sht21.measure(1)
    s = s + "\t%s\t%d" % (temp, humidity)
except:
    s = s + "SHT21 I/O Error"
print(s)
with open(file, "a") as fp:
    s = s + "\r\n"
    fp.write(s)