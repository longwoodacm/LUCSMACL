import serial
from time import sleep

ard = serial.Serial('/dev/ttyACM0', 9600)
sleep(2)
while True:
  print("High")
  print(ard.write(bytes(str.encode('1'))))
  sleep(7)
ard.close()
