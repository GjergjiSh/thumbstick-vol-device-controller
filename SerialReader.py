import serial
import time

ser = serial.Serial(port="COM3", baudrate=115200, timeout=0)
#ser.timeout = .1
ser.open()

while ser.is_open:
    line = ser.readline().decode("utf-8")
    print(line)