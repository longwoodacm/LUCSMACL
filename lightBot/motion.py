#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   When this script is run, a properly connected motion sensor will periodically check for motion.
#   This was created to test the motion sensor.

import time
import RPi.GPIO as GPIO
import stepper

#Set pin 14 as input for motion detection
pin = 14   #GPIO 14 -> Physical Pin 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)

i = 0
old = 1
while True:
  i = GPIO.input(pin)
  if i != old:
    print("State changed",i)
    if i == True:
      stepper.main()
  old = i
  time.sleep(0.01)
