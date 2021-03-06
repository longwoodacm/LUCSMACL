#!/usr/bin/env python3

#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   When this script is run, the arm of a properly configured stepper motor will turn.
#   This is to be used for activating the motion sensor in Stevens 118.

from time import sleep
import RPi.GPIO as GPIO #Only works on Pi, workaround here for windows:  https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing
from sys import stderr,argv
from datetime import datetime

#Tutorial for help understanding: https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/

import sqlite3

full_spin = 4076
half_spin = int(full_spin/2)
quar_spin = int(full_spin/4)



# 64 Steps per internal revolution * 63.684 gear ratio = aprox 4076 
# https://42bots.com/tutorials/28byj-48-stepper-motor-with-uln2003-driver-and-arduino-uno/

Seq = [[1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,1,1,0],
      [0,0,1,0],
      [0,0,1,1],
      [0,0,0,1],
      [1,0,0,1]]

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

#Determine if the current clock time falls between the given start and end times on the given day of the week
def valid_time(start,end,days):
  week = "MTWHFSU"
  today = week[datetime.today().weekday()]
  #print(today,days)
  if today not in days:
    return True
  
  startTime = datetime.strptime(start,'%H:%M')
  endTime = datetime.strptime(end,'%H:%M')
  now = datetime.now().replace(day=1,month=1,year=1900,microsecond=0)
  if startTime < now < endTime:
    return False
  return True

#Insert into the log the event that triggered the stepper motor
def log(source):
  conn = sqlite3.connect('/home/pi/LUCSMACL/lightBot/bot.db')
  cur = conn.cursor()
  dt = datetime.now();
  stmt = """INSERT INTO log(source,datetime) VALUES (?,?)"""
  cur.execute(stmt,(source,dt))
  conn.commit()
  conn.close()

#Empty the log to save space
def clearLog():
  conn = sqlite3.connect('/home/pi/LUCSMACL/lightbot/bot.db')
  cur = conn.cursor()
  stmt = """DELETE FROM log; 
            UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='log';
         """
  cur.execute(stmt)
  conn.commit()
  conn.close()

#Trigger to step forward
#Source is the source of the trigger
def step(source):
  conn = sqlite3.connect('/home/pi/LUCSMACL/lightBot/bot.db')
  cur = conn.cursor()
  request = """SELECT name,start,end,days,source FROM rules WHERE source = ? OR source = 'all';"""
  cur.execute(request,(source,))
  rules = cur.fetchall()
  conn.close()
  conflicts = [rule for rule in rules if not valid_time(rule[1],rule[2],rule[3])]
      
  #If there are conflicts, return them as a failure        
  if len(conflicts) > 0:
    string = "Failed to activate stepper motor due to time conflicts: ("
    for rule in conflicts:
      string = string + ' ' + rule[0] + ': ' + rule[4]
    string = string + ')'
    return string
 
  log(source)

  #For additional GPIO documentation, visit: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  StepPins = [17,18,27,22]  #Board pins [11,12,13,15]
  for channel in StepPins:
    GPIO.setup(channel,GPIO.OUT)


  clear_power(StepPins)
  step_forward(Seq,half_spin,StepPins)
  step_back(Seq,half_spin,StepPins)
  clear_power(StepPins)

  return "Stepped successfully"


if __name__ == '__main__':
  if len(argv) > 1 and argv[1] == "clearLog":
    clearLog();
  elif len(argv) > 1 and (argv[1].isdigit() or (argv[1].startswith('-') and argv[1][1:].isdigit())):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    StepPins = [17,18,27,22]  #Board pins [11,12,13,15]
    for channel in StepPins:
      GPIO.setup(channel,GPIO.OUT)
    if int(argv[1]) > 0:
      step_forward(Seq,int(full_spin/360*int(argv[1])),StepPins)
    else:
      step_back(Seq,int(full_spin/360*int(argv[1][1:])),StepPins)
    clear_power(StepPins)
  else:
    print(step('manual'));
