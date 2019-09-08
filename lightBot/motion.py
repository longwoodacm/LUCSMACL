
import time
import RPi.GPIO as GPIO

#GPIO14 = Physical Pin 8
#Set as motion detection input
pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)

i = 0
while True:
  if i != GPIO.input(pin):
    i = GPIO.input(pin)
    print("State changed",i)
    if i == 1:
      time.sleep(2)
  time.sleep(0.001)
