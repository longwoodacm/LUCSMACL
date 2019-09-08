import time
import RPi.GPIO as GPIO #Only works on Pi, workaround here:  https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing


def clear(StepPins):
  for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

def step_forward(Seq,steps):
  for step in range(steps):
    for pin in range(4):
      if Seq[step%8][pin] == 1:
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    time.sleep(0.00075)

def step_back(Seq,steps):
  for step in range(steps):
    for pin in range(4):
      if Seq[7-step%8][pin] == 1:
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    time.sleep(0.00075)

# 64 Steps per internal revolution * 63.684 gear ratio = aprox 4076 
# https://42bots.com/tutorials/28byj-48-stepper-motor-with-uln2003-driver-and-arduino-uno/
full_spin = 4076
half_spin = int(full_spin/2)
quar_spin = int(full_spin/4)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
StepPins = [17,18,27,22]
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]

clear(StepPins)
step_forward(Seq,half_spin)
step_forward(Seq,half_spin)
#step_back(Seq,half_spin)
clear(StepPins)
