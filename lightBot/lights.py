#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   When this script is run, a properly connected motion sensor will periodically check for motion.
#   When motion is detected, the arm of a properly configured stepper motor will turn.
#   This is to be used for activating the motion sensor in Stevens 118.

import time
import RPi.GPIO as GPIO


#Set all pin outputs to false to prevent step motor overheating
def clear_power(StepPins):
  for pin in StepPins:
    GPIO.output(pin, False)

#Move stepper motor clockwise
def step_forward(Seq,steps):
  for step in range(steps):
    for pin in range(4):
      if Seq[step%8][pin] == 1:
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    time.sleep(0.00075)

#Move stepper motor counter-clockwise
def step_back(Seq,steps):
  for step in range(steps):
    for pin in range(4):
      if Seq[7-step%8][pin] == 1: #Step in reverse order to step backwards
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    time.sleep(0.00075)


SensePin = 14 #Physical pin 8
StepPins = [17,18,27,22] #Physical pins [11,12,13,15]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SensePin,GPIO.IN)
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)


full_spin = 4096
half_spin = int(full_spin/2)
quar_spin = int(full_spin/4)

#Stepper motor step sequence
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]


while True:
  i = 0
  while True:
    active = GPIO.input(SensePin)
    if i != active:
      i = active
      #print("State changed",i)
      if i == 1:
        break
    time.sleep(1)

  clear_power(StepPins)
  step_forward(Seq,half_spin)
  step_back(Seq,half_spin)
  clear_power(StepPins)
#  print("Sleeping")
  time.sleep(300)
#  print("Awake")

