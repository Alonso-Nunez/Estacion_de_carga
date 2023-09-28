import serial
import os, time

SERIAL_PORT = "/dev/ttyS0" # "/dev/ttyAMA0"
 # Enable Serial Communication
port = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
port.write("Información serial"+"\n\r")#Envia información
dato = port.read(10)#Lee 10 bytes
#port.readline() Lee toda una linea
print (dato)
port.close()

