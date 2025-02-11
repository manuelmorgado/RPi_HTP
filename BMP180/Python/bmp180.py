#!/usr/bin/env python
'''A Python class to access bmp180 based air pressure and temperature sensor.  The smbus module is
required.

Example:

import smbus
import bmp180
import sys, select
import os as os
import sensor
from sensor.util import Pressure, Temperature

bus = smbus.SMBus(1)
sensor = bmp180.bmp180(bus)
print sensor.pressure_and_temperature'''

# Importing libraries
import sensorbase
import struct
import time
import sys, select, os

# Default I2C address of bmp180
_DEFAULT_ADDRESS = 0x77

# Registers of sensor
_REG_AC1                 = 0xAA
_REG_AC2                 = 0xAC
_REG_AC3                 = 0xAE
_REG_AC4                 = 0xB0
_REG_AC5                 = 0xB2
_REG_AC6                 = 0xB4
_REG_B1                  = 0xB6
_REG_B2                  = 0xB8
_REG_MB                  = 0xBA
_REG_MC                  = 0xBC
_REG_MD                  = 0xBE
_REG_CALIB_OFFSET        = _REG_AC1
_REG_CONTROL_MEASUREMENT = 0xF4
_REG_DATA                = 0xF6

# Commands for conversion, temperature and pressure
_CMD_START_CONVERSION    = 0b00100000
_CMD_TEMPERATURE         = 0b00001110
_CMD_PRESSURE            = 0b00010100

# Oversampling mode (Affects the time of the measurament also the precision)
OS_MODE_SINGLE = 0b00
#OS_MODE_2      = 0b01
#OS_MODE_4      = 0b10
#OS_MODE_8      = 0b11

# Conversion time (in second)
_WAIT_TEMPERATURE = 0.0045
_WAIT_PRESSURE    = [0.0045, 0.0075, 0.0135, 0.0255]

# Define the Class of the sensor BMP180
class bmp180(sensorbase.SensorBase):
    
# Initialise the sensor
    def __init__(self, bus = None, addr = _DEFAULT_ADDRESS,
                 os_mode = OS_MODE_SINGLE):
        # Define the commands for measure the temperature or the pressure
        assert(bus is not None)
        assert(addr > 0b000111
               and addr < 0b1111000)

        super(bmp180, self).__init__(update_callback = self._update_sensor_data)

        # Define the coefficients of the calibrations
        self._bus = bus
        self._addr = addr
        self._ac0 = None
        self._ac1 = None
        self._ac2 = None
        self._ac3 = None
        self._ac4 = None
        self._ac5 = None
        self._ac6 = None
        self._b1 = None
        self._b2 = None
        self._mb = None
        self._mc = None
        self._md = None
        self._os_mode = os_mode
        self._pressure = None
        self._temperature = None
        self._read_calibration_data()

    # Pressure function
    @property
    def pressure(self):
        '''Returns a pressure value.  Returns None if no valid value is set
        yet.'''
        self._update()
        return (self._pressure)

    # Temperature function
    @property
    def temperature(self):
        '''Returns a temperature value.  Returns None if no valid value is
        set yet.'''
        self._update()
        return ( self._temperature)

    # OS mode function
    @property
    def os_mode(self):
        '''Gets/Sets oversampling mode.
        OS_MODE_SINGLE: Single mode.
        OS_MODE_2: 2 times.
        OS_MODE_4: 4 times.
        OS_MODE_8: 8 times.'''
        return (self._os_mode)

    @os_mode.setter
    # Set oversampling mode
    def os_mode(self, os_mode):
        assert(os_mode == OS_MODE_SINGLE
               or os_mode == OS_MODE_2
               or os_mode == OS_MODE_4
               or os_mode == OS_MODE_8)
        self._os_mode = os_mode

    @property
    # Pressure and temperature function
    def pressure_and_temperature(self):
        '''Returns pressure and temperature values as a tuple.  This call can
        save 1 transaction than getting a pressure and temperature
        values separetely.  Returns (None, None) if no valid values
        are set yet.'''
        self._update()
        return (self._pressure, self._temperature)    

#     Read Calibration function
#     def _read_calibration_data(self):
#         while True:
#                 try:
#                         calib = self._bus.read_i2c_block_data(self._addr,_REG_CALIB_OFFSET, 22)
#                         (self._ac1, self._ac2, self._ac3, self._ac4,self._ac5, self._ac6, self._b1, self._b2,self._mb, self._mc, self._md) = struct.unpack('>hhhHHHhhhhh', ''.join([chr(x) for x in calib]))
#                         break
#                 except IOError:
#                         pass
 # Read calibration function.
    def _read_calibration_data(self):
        while True:
                try:
                        calib = self._bus.read_i2c_block_data(self._addr,_REG_CALIB_OFFSET, 22)
                        (self._ac1, self._ac2, self._ac3, self._ac4,self._ac5, self._ac6, self._b1, self._b2,self._mb, self._mc, self._md) = struct.unpack('>hhhHHHhhhhh', ''.join([chr(x) for x in calib]))
                        break
                except IOError:
                        pass
    # Data
    def _update_sensor_data(self):

        # Read uncompensated temperature value
        cmd = _CMD_START_CONVERSION | _CMD_TEMPERATURE
        self._bus.write_byte_data(self._addr,
                                  _REG_CONTROL_MEASUREMENT, cmd)
        time.sleep(_WAIT_TEMPERATURE)
        vals = self._bus.read_i2c_block_data(self._addr,
                                             _REG_DATA, 2)
        ut = vals[0] << 8 | vals[1]

        # Read uncompensated pressure value
        cmd = _CMD_START_CONVERSION | self._os_mode << 6 | _CMD_PRESSURE
        self._bus.write_byte_data(self._addr,
                                  _REG_CONTROL_MEASUREMENT, cmd)
        time.sleep(_WAIT_PRESSURE[self._os_mode])
        vals = self._bus.read_i2c_block_data(self._addr,
                                             _REG_DATA, 3)
        up = (vals[0] << 16 | vals[1] << 8 | vals[0]) >> (8 - self._os_mode)

        # Calculating the true temperature
        x1 = ((ut - self._ac6) * self._ac5) >> 15
        x2 = (self._mc << 11) / (x1 + self._md)
        b5 = x1 + x2
        self._temperature = ((b5 + 8) / 2**4) / 10.0

        # Calculating the true temperature
        b6 = b5 - 4000
        x1 = self._b2 * ((b6 * b6) >> 12)
        x2 = self._ac2 * b6
        x3 = (x1 + x2) >> 11
        b3 = (((self._ac1 *4 + x3) << self._os_mode) + 2) >> 2
        x1 = (self._ac3 * b6) >> 13
        x2 = (self._b1 * (b6 * b6) >> 12) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self._ac4 * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> self._os_mode)
        if (b7 < 0x80000000):
            p = (b7 * 2) / b4
        else:
            p = (b7 / b4) * 2
        x1 = p**2 >> 16
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        self._pressure = (p + ((x1 + x2 + 3791) >> 4)) / 100.0

if __name__ == '__main__':

    import smbus
    from decimal import *

    bus = smbus.SMBus(1)
    sensor = bmp180(bus)

# Adquire the initial values of pressure and temperature.
(pres_init,temp_init) = sensor.pressure_and_temperature;
print "Initial value of temperature:",temp_init
print "Initial value of pressure:",pres_init
 
# Loop for the adquisition of temperature and pressure when the detects changes in one of them.
while True:

    # Save the data in a tuple.
    (pres,temp) = sensor.pressure_and_temperature;
    #print temp_init, temp

    # Check the change of pressure and temperature.
    (T,P) = (float(abs(Decimal(temp_init)-Decimal(temp))) , float(abs(Decimal(pres_init)-Decimal(pres))));

    # Show the temperature if it change equal or more than 0.2 Celsius degrees.    
    if T == 0.1 or P == 0.01:
        T = 0 ; P = 0;
    elif T >= 0.2 or P >= 0.08:
        T = 0 ; P = 0;
        temp_init = temp; pres_init = pres;
    print ("Temperature: ", temp ,"   Preassure: ", pres) 

    time.sleep(0.1)

    # End the process if you press any key + enter.
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break

# Measuring time of temperature and pressure function.
from timeit import Timer

prestime = Timer(lambda: sensor.pressure)
print prestime.timeit(number=1)

#temptime = Timer(lambda: sensor.temperature)
#print temptime.timeit(number=1)
