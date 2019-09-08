from flask import Flask, request
import serial

app = Flask(__name__)
app.config.from_object(__name__)

ard = serial.Serial('/dev/ttyACM0', 9600)

@app.route('/lights')
def lights():
  ard.write(bytes(str.encode('1')))
  return "Lights are turning on\n"

if __name__ == "__main__":
  app.run()
