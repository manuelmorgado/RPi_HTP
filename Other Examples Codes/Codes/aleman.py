#!/usr/bin/python

import smbus
import time
import math
import RPi.GPIO as GPIO

# Adressen
BMP085 = 0x77

# Variablen
Kalibrationswerte = {}

# Modus (1 ist der Standardmodus)
oss = 3

# EOC Pin
EOC = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO als Eingang schalten
GPIO.setup(EOC, GPIO.IN)

# Signed Integer auslesen
def ReadSInt(Device, Adresse):

	# Auslesen der beiden Bytewerte
	MSB = Bus.read_byte_data(Device, Adresse)
	LSB = Bus.read_byte_data(Device, Adresse + 1)

	# Wenn Vorzeichen vorhanden, den Wert umwandeln
	if(MSB > 127):
		MSB = MSB - 256
	
	# Datenbytes zusammenfuegen
	Data = (MSB << 8) + LSB
	
	return Data
	
# Unsigned Integer auslesen
def ReadUInt(Device, Adresse):

	# Auslesen der beiden Bytewerte
	MSB = Bus.read_byte_data(Device, Adresse)
	LSB = Bus.read_byte_data(Device, Adresse + 1)
	
	# Datenbytes zusammenfuegen
	Data = (MSB << 8) + LSB
	
	return Data

# Kalibrationswerte auslesen	
def ReadCal(Device):

	Data = {}
	
	# Kalibrationswerte auslesen
	AC1 = ReadSInt(Device, 0xAA)
	AC2 = ReadSInt(Device, 0xAC)
	AC3 = ReadSInt(Device, 0xAE)
	AC4 = ReadUInt(Device, 0xB0)
	AC5 = ReadUInt(Device, 0xB2)
	AC6 = ReadUInt(Device, 0xB4)
	B1 = ReadSInt(Device, 0xB6)
	B2 = ReadSInt(Device, 0xB8)
	MB = ReadSInt(Device, 0xBA)
	MC = ReadSInt(Device, 0xBC)
	MD = ReadSInt(Device, 0xBE)
	
	# Werte einem Dictionary anhaengen
	Data.update({"AC1": AC1})
	Data.update({"AC2": AC2})
	Data.update({"AC3": AC3})
	Data.update({"AC4": AC4})
	Data.update({"AC5": AC5})
	Data.update({"AC6": AC6})
	Data.update({"B1": B1})
	Data.update({"B2": B2})
	Data.update({"MB": MB})
	Data.update({"MC": MC})
	Data.update({"MD": MD})
	
	return Data
	
def ReadTemp(Device):

	Temp = 0
	
	# Temperaturmessung starten
	Bus.write_byte_data(Device, 0xF4, 0x2E)
	
	# Warten bis ein High-Pegel anliegt
	while GPIO.input(EOC) == 0:			
		pass

	# Temperaturwerte auslesen
	Temp = ReadUInt(Device, 0xF6)
	
	return Temp
	
def ReadPres(Device, oss):

	Pressure = 0

	# Druckmessung starten
	Bus.write_byte_data(Device, 0xF4, (0x34 + (oss << 6)))

	# Warten bis ein High-Pegel anliegt
	while GPIO.input(EOC) == 0:			
		pass

	# Druckwerte auslesen und verarbeiten
	MSB = Bus.read_byte_data(Device, 0xF6)
	LSB = Bus.read_byte_data(Device, 0xF7)
	XLSB = Bus.read_byte_data(Device, 0xF8)
	Pressure = ((MSB << 16) + (LSB << 8) + XLSB) >> (8 - oss)
	
	return Pressure

def CalTemp(rawTemp):

	# Fuer die Formel siehe Datenblatt
	X1 = (rawTemp - Kalibrationswerte["AC6"]) * Kalibrationswerte["AC5"] / math.pow(2, 15)
	X2 = Kalibrationswerte["MC"] * math.pow(2, 11) / (X1 + Kalibrationswerte["MD"])
	B5 = X1 + X2
	Temp = (B5 + 8.0) / float(math.pow(2, 4))

	# Temperatur in Grad Celsius umrechen
	Temp = Temp * 0.1
	Temp = round(Temp, 2)

	return Temp
	
def CalPres(rawPres, rawTemp, oss):

	# Benoetigten Werte berechnen
	X1 = (rawTemp - Kalibrationswerte["AC6"]) * Kalibrationswerte["AC5"] / math.pow(2, 15)
	X2 = Kalibrationswerte["MC"] * math.pow(2, 11) / (X1 + Kalibrationswerte["MD"])
	B5 = X1 + X2

	# Fuer Formel siehe Datenblatt
	B6 = B5 - 4000
	X1 = (Kalibrationswerte["B2"]  * (B6 * B6 / math.pow(2, 12))) / math.pow(2, 11)
	X2 = Kalibrationswerte["AC2"] * B6 / math.pow(2, 11)
	X3 = X1 + X2
	B3 = ((long(Kalibrationswerte["AC1"] * 4 + X3) << oss) + 2) /  4
	X1 = Kalibrationswerte["AC3"] * B6 / math.pow(2, 13)
	X2 = (Kalibrationswerte["B1"] * (B6 * B6 / math.pow(2, 12))) / math.pow(2, 16)
	X3 = ((X1 + X2) + 2) / math.pow(2, 2)
	B4 = Kalibrationswerte["AC4"] * long(X3 + 32768) / math.pow(2, 15)
	B7 = (long(rawPres) - B3) * (50000 >> oss)
	
	if(B7 < 0x80000000):
		p = (B7 * 2) / B4
	else:
		p = (B7 / B4) * 2
	
	X1 = (p / math.pow(2, 8)) * (p / math.pow(2, 8))
	X1 = (X1 * 3038) / math.pow(2, 16)
	X2 = (-7357 * p) / math.pow(2, 16)
	Pressure = p + (X1 + X2 + 3791) / math.pow(2, 4)
	
	# Ergebnis umrechnen (hPa) und runden
	Pressure = Pressure / 100
	Pressure = round(Pressure, 3)
	
	return Pressure
	
def CalAltitude(Pressure):

	# Druck auf Meereshoehe
	p0 = 1013.25
	
	# Fuer Formel siehe Datenblatt
	Exp = 1 / 5.255
	Altitude = math.pow((Pressure / p0), Exp)
	Altitude = 44330 * (1 - Altitude)
	
	# Ergebnis runden
	Altitude = round(Altitude, 2)

	return Altitude


while True:	

	# I2C Bus 0 oeffnen
	Bus = smbus.SMBus(0)

	# Kalibrationswerte auslesen
	Kalibrationswerte = ReadCal(BMP085)

	# Rohdaten einlesen
	UT = ReadTemp(BMP085)
	UP = ReadPres(BMP085, oss)

	# Daten errechnen
	Temperatur = CalTemp(UT)
	Pressure = CalPres(UP, UT, oss)
	Altitude = CalAltitude(Pressure)

	# Ausgabe
	print "----------------------------------------"
	print "Temperatur: " + str(Temperatur) + " C"
	print "Luftdruck: " + str(Pressure) + " hPa"
	print "Altitude: " + str(Altitude)
	print "----------------------------------------"

	Bus.close()
	
	time.sleep(1)
