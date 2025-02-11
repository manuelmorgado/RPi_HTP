#!/usr/bin/env python3

# Importing libraries
import sht21
import time
import datetime
import subprocess
import os.path
import json
import rpi_cpu

#
# Install a webserver with path to "/home/pi/www"
# Install rrdtool: "sudo apt-get install rrdtool"
# Copy "index.php" to "/home/pi/www"
# Use "crontab -e" and append the following line to call sht21_job.sh every 10 minutes:
# "*/10 * * * * /home/pi/sht21/sht21_job.sh"

rrd_file = "data.rrd"     # Database file
www_path = "/home/pi/www"  # Output (Chart)
json_file = "data.json"     # Output (JSON-Data)

def rrd_init():
    """Check if RRD Database ist available, if not, create it"""
    try:
        with open(rrd_file): pass
        print("RRD-Database [", rrd_file, "] found")
    except:
        print("Create RRD-Database: [", rrd_file, "]")
        cmd = [ "rrdtool", "create", "%s" % (rrd_file),
                "--step", '600',                    # 10min = 600
                "DS:temp:GAUGE:1800:U:U",           # Temperature, 30min Timeout,
                "DS:humidity:GAUGE:1800:U:U",       # Humidity, 30min Timeout,
                "DS:tcpu:GAUGE:1800:U:U",           # CPU-Temperature, 30min Timeout,
                "RRA:AVERAGE:0.5:1:288",         # 0.5 internal, store 48h @ 10min
                "RRA:AVERAGE:0.5:6:8760"]        # 0.5 internal, store 1 year @ 1hour
        subprocess.Popen(cmd)

def rrd_update(values):
    """Write values to RRD Database"""
    cmd = ["rrdtool", "update", rrd_file, "N:" + values]
    subprocess.Popen(cmd)

def rrd_graph(timespan,file):
    """Time in seconds (X-Axis) and Output-File"""
    print("Building graph from [%s], Timespan: %s Seconds" % (rrd_file,timespan))
    cmd = ["rrdtool", "graph", "%s/%s" % (www_path,file),
           "--start", "-%s" % (timespan),
           "--title=SHT21: %d Days of Temperature and Humidity " % (timespan/86400),
           "--vertical-label=Temperatur",
           "--watermark=www.emsystech.de",
           "--width=1000",
           "--height=500",
           "--alt-autoscale",
           "--lower-limit=-20",
           "--upper-limit=60",
           "--rigid",
           "--right-axis-label=Prozent",
           "--right-axis=1.25:25",
           "--slope-mode",
           "DEF:t=%s:temp:AVERAGE" % (rrd_file),
           "DEF:rh=%s:humidity:AVERAGE" % (rrd_file),
           "DEF:tcpu=%s:tcpu:AVERAGE" % (rrd_file),
           "CDEF:xrh=rh,0.8,*,20,-",
           "LINE2:t#FF0000:Temperatur",
           "LINE2:xrh#0000FF:Luftfeuchtigkeit",
           "LINE2:tcpu#00FF00:CPU-Temperatur"]
    subprocess.Popen(cmd)

sht21 = sht21.SHT21()
d = dict()
rrd_init()
d['time'] = '{:%d.%m.%Y %H:%M}'.format(datetime.datetime.now())
d['tcpu'] = rpi_cpu.get_temperature()
try:
    (d['temp'], d['humidity']) = sht21.measure(1)
except:
    d['temp']="-"
    d['humidity']="-"

rrd_update(str(d['temp'])+":"+str(d['humidity'])+":"+str(d['tcpu']))

# write measured data to data.json in webserver path
json = json.dumps(d)
print("Data: "+json)
with open(www_path+"/"+json_file, "w") as fp:
    fp.write(json)

# build charts if necessary
min = int(time.time() / 60)

# build day chart every 10 minutes or if not exist
if not (os.path.isfile(www_path+"/chart-day.png")) or ((min % 10) == 0):
    rrd_graph(1*24*60*60,"chart-day.png")
    
    # build week chart every hour or if not exist
    if not (os.path.isfile(www_path+"/chart-week.png")) or ((min % 60) == 0):
        rrd_graph(7*24*60*60,"chart-week.png")
