import flask
import RPi.GPIO as GPIO

app = flask.Flask(__name__)
app.config["DEBUG"] = True

red_pin   = 11
green_pin = 13
blue_pin  = 15

@app.route('/', methods=['GET'])
def led_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.output(red_pin, GPIO.LOW)

app.run()