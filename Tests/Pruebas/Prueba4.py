
import smbus
import time
bus = smbus.SMBus(1)
address = 0x40

def bearing255():
        bear = bus.read_byte_data(address, 1)
        return bear

def bearing3599():
        bear1 = bus.read_byte_data(address, 2)
        bear2 = bus.read_byte_data(address, 3)
        bear = (bear1 << 8) + bear2
        bear = bear/10.0
        return bear

while True:
        bearing = bearing3599()     #this returns the value to 1 decimal place in degrees$
        bear255 = bearing255()      #this returns the value as a byte between 0 and 255.
        print bearing
        print bear255
        time.sleep(1)

