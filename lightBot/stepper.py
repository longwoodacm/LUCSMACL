#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   When this script is run, the arm of a properly configured stepper motor will turn.
#   This is to be used for activating the motion sensor in Stevens 118.

from time import sleep
import RPi.GPIO as GPIO #Only works on Pi, workaround here for windows:  https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing
from sys import stderr
from datetime import datetime

#Tutorial for help understanding: https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/

import sqlite3

#Clear power output to pins, help reduce heat and energy waste
def clear_power(StepPins):
  for pin in StepPins:
    GPIO.output(pin, False)

#Rotate clockwise a number of steps
def step_forward(Seq,steps,StepPins):
  for step in range(steps):
    for pin in range(4):
      if Seq[step%8][pin] == 1:
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    sleep(0.00075)

#Rotate counter-clockwise a number of steps
def step_back(Seq,steps,StepPins):
  for step in range(steps):
    for pin in range(4):
      if Seq[7-step%8][pin] == 1:
        GPIO.output(StepPins[pin],True)
      else:
        GPIO.output(StepPins[pin],False)
    sleep(0.00075)


def log(source):
  conn = sqlite3.connect('/home/pi/LUCSMACL/lightBot/log.db')
  cur = conn.cursor()
  dt = datetime.now();
  stmt = """INSERT INTO lightLog(source,datetime) VALUES (?,?)"""
  cur.execute(stmt,(source,dt))
  conn.commit()
  conn.close()

def main():
  # 64 Steps per internal revolution * 63.684 gear ratio = aprox 4076 
  # https://42bots.com/tutorials/28byj-48-stepper-motor-with-uln2003-driver-and-arduino-uno/
  full_spin = 4076
  half_spin = int(full_spin/2)
  quar_spin = int(full_spin/4)
  

  #For additional GPIO documentation, visit: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  StepPins = [17,18,27,22]  #Board pins [11,12,13,15]
  for channel in StepPins:
    GPIO.setup(channel,GPIO.OUT)

  Seq = [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]

  clear_power(StepPins)
  step_forward(Seq,half_spin,StepPins)
  step_back(Seq,half_spin,StepPins)
  clear_power(StepPins)

  print('Step',file=stderr)


if __name__ == '__main__':
  main()
