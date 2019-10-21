#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   When this script is run, a properly connected motion sensor will periodically check for motion.
#   This was created to test the motion sensor.

import time
import RPi.GPIO as GPIO
import stepper
import sqlite3
from datetime import datetime, timedelta


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
      conn = sqlite3.connect('/home/pi/LUCSMACL/lightBot/log.db')
      cur = conn.cursor()
      request = """SELECT datetime FROM lightLog WHERE source='motion' ORDER BY datetime DESC;"""
      cur.execute(request)
      dt = cur.fetchone()

      conn.close()
      lastTime = datetime.strptime(dt[0].split('.',1)[0], '%Y-%m-%d %H:%M:%S') #2019-10-18 19:23:32.679844
      fiveMins = (datetime.now() - timedelta(minutes = 5)) > lastTime

      if fiveMins:
        stepper.log('motion')
        stepper.main()
  old = i
  time.sleep(0.01)
