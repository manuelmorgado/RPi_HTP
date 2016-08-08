import time
import smbus
import RPi.GPIO
bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


addr = 0x00
while True:
   try:
    x = bus.read_byte_data(addr, 0x40)
    print x
    time.sleep(0.25)
   except:
    print 'exiting...'
    break


#DEVICE_ADDRESS = 0x00      #7 bit address (will be left shifted to add the read write bi$
#DEVICE_REG_MODE1 = 0x40
#DEVICE_REG_LEDOUT0 = 0x77

#Write a single register
#print bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
#print long read_byte(DEVICE_ADDRESS)

#Write an array of registers
#ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
#print bus.read_i2c_block_data(DEVICE_ADDRESS, DEVICE_REG_LEDOUT0)