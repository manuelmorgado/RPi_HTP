#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#Importing Lybraries
import time
import rpi_i2c

#Creating the class sht21
class sht21:
    """Interface Class for sht21 Temperture and Humidity Sensor from www.sensirion.com

    Hardware: Breakoutboard with sht21 Sensor for Raspberry Pi by www.emsystech.de

    The Class can be used in two ways.
    1. With the build in I2C Port from Raspberry Pi using I2C Driver
       I2C Driver must be enabled: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

    2. rpi_i2c can emulate an I2C Bus on any GPIO Pin. This is more flexible and more than one sensor can be used.
       But it needs Pullups für SCL and SDA und root for GPIO access. (sudo)

    The method "measure" does a complete cycle and returns a tupple with the values:

    (temperature, humidity) = SHT21.measure(1)      # I2C-1 Port

    If you want it more flexible e.g. multiple measurements, only humidity or temperature use:

    SHT21.open(1)
    ...
    temperature = SHT21.read_temperature()
    humidity = SHT21.read_humidity()
    ...
    SHT21.close()
    """

    i2c = rpi_i2c.I2C()     # I2C Wrapper Class
    
    def measure(self, dev=1, scl=3, sda=2):
        """Complete cycle including open, measurement und close, return tuple of temperature and humidity"""
        self.open(dev, scl, sda)
        t = self.read_temperature()
        rh = self.read_humidity()
        self.i2c.close()
        return (t, rh)

    def open(self, dev=1, scl=3, sda=2):
        """Hardware I2C Port, B,B+,Pi 2 = 1 the first Pi = 0"""
        self.i2c.open(0x40,dev, scl, sda)
        self.i2c.write([0xFE])  # execute Softreset Command  (default T=14Bit RH=12)
        time.sleep(0.050)

    def read_temperature(self):
        """ Temperature measurement (no hold master), blocking for ~ 88ms !!! """
        self.i2c.write([0xF3])
        time.sleep(0.036)  # wait, typ=66ms, max=85ms @ 14Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            t = ((data[0] << 8) + data[1]) & 0xFFFC  # set status bits to zero
            t = -46.82 + ((t * 175.72) / 65536)  # T = 46.82 + (175.72 * ST/2^16 )
            return round(t, 1)
        else:
            return None

    def read_humidity(self):
        """ RH measurement (no hold master), blocking for ~ 32ms !!! """
        self.i2c.write([0xF5])  # Trigger RH measurement (no hold master)
        time.sleep(0.03)  # wait, typ=22ms, max=29ms @ 12Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            rh = ((data[0] << 8) + data[1]) & 0xFFFC  # zero the status bits
            rh = -6 + ((125 * rh) / 65536)
            if (rh > 100): rh = 100
            return round(rh, 1)
        else:
            return None

    def close(self):
        """Closes the i2c connection"""
        self.i2c.close()

    def _check_crc(self, data, length):
        """Calculates checksum for n bytes of data and compares it with expected"""
        crc = 0
        for i in range(length):
            crc ^= (ord(chr(data[i])))
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x131  # CRC POLYNOMIAL
                else:
                    crc = (crc << 1)
        return True if (crc == data[length]) else False
i=1
while True:
	sensor = sht21()
	sensor.open
	temp = sensor.read_temperature
	print temp
#if __name__ == "__main__":
    #SHT21 = sht21()
    #while True:
        #try:
            ############################################################################################################
            # Example 1 Using the I2C Driver
            ############################################################################################################

            #(temperature, humidity) = SHT21.measure(1)      # I2C-1 Port
            #print("Temperature: %s °C  Humidity: %s %%" % (temperature, humidity))

            ############################################################################################################
            # Example 2 Using GPIOs on I2C Pins (without Driver), must be executed with sudo
            ############################################################################################################

            #(temperature, humidity) = SHT21.measure(None)   # No I2C-Port/Driver --> GPIO2, GPIO3
            #print("Temperature: %s °C  Humidity: %s %%" % (temperature, humidity))

            ############################################################################################################
            # Example 3 Using multiple Sensors (without Driver), must be executed with sudo, Pullups required
            ############################################################################################################

            #(t0, rh0) = SHT21.measure(None,25,8)  # Use GPIOs SCL=3, SDA=2
            #(t1, rh1) = SHT21.measure(None,7,11)  # Use GPIOs SCL=3, SDA=2
            #print("%s°C\t%s%%\t%s°C\t%s%%" % (t0,rh0,t1,rh1))

            ############################################################################################################
        #except:
            #print("sht21 I/O Error")
        #time.sleep(0.2)
