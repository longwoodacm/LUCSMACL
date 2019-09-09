#Author: Cameron Haddock
#Last Modified: 9 September 2019
#Purpose of File: 
#   This code is for running a flask server on acmpi in order to accept pings for activating lights

from flask import Flask
import subprocess

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/lights')
def lights():
  #subprocess.call("stepper.py",shell=True)
  return "Lights are turning on\n"

if __name__ == "__main__":
  app.run(host='localhost')
