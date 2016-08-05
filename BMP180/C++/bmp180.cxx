#include <stdio.h>
#include <wiringPiI2C.h>
#include <iostream>
#include <vector>

// Address of the sensor (I2C).

int bmp = 0x40 ;

// Definine the registers of the sensor.

uint8_t _regAC1 = 0xAA ;
uint8_t _regAC2 = 0xAC ;
uint8_t _regAC3 = 0xAE ;
uint8_t _regAC4 = 0xB0 ;
uint8_t _regAC5 = 0xB2 ;
uint8_t _regAC6 = 0xB4 ;
uint8_t _regB1 = 0xB6 ;
uint8_t _regB2 = 0xB8 ;
uint8_t _regMB = 0xBA ;
uint8_t _regMC = 0xBC ;
uint8_t _regMD = 0xBE ;
uint8_t _regOffSet = 0xAA ;
uint8_t _regContMes = 0xF4 ;
uint8_t _regData = 0xF6 ;

// Comands for Conversion, Temperature and Pressure.

int _cmdConv = 0b00100000 ;
int _cmdTemp = 0b00001110 ;
int _cmdPres = 0b00010100;

// Oversampling mode (diferentes precission).
uint8_t _regB2 = 0xB8 ;
uint8_t _regMB = 0xBA ;
uint8_t _regMC = 0xBC ;
uint8_t _regMD = 0xBE ;
uint8_t _regOffSet = 0xAA ;
uint8_t _regContMes = 0xF4 ;
uint8_t _regData = 0xF6 ;

// Comands for Conversion, Temperature and Pressure.

int _cmdConv = 0b00100000 ;
int _cmdTemp = 0b00001110 ;
int _cmdPres = 0b00010100;

// Oversampling mode (diferentes precission).

int _osSingleMode = 0b00 ;
int _osMode_2 = 0b01 ;
int _osMode_4 = 0b10 ;
int _osMode_8 = 0b11 ;

// Convert sclae for temperature and preassure.

int _convTemp = 0.0045 ;
std::vector<int> v = {0.0045, 0.0075, 0.0135, 0.0255};
int data = 0 ;

init{

}
class bmp180:

//Function (Initialization, Read Calibration, Refresh Sensor and name).

init{

}

cal{

}

refresh{

}

// Properties (The posibility to measure the preasure, temperature or both).
preassure{

}

temperature{

}

preassure_temperature{

}

// OS mode
os_mode{

}