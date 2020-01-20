import flask
import RPi.GPIO as GPIO
from flask import request
from flask import send_file
import cv2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

red_pin   = 11
green_pin = 13
blue_pin  = 15


def turn_on(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def turn_off(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def white_on():
    turn_on(red_pin)
    turn_on(green_pin)
    turn_on(blue_pin)

def all_off():
    turn_off(red_pin)
    turn_off(green_pin)
    turn_off(blue_pin)

def blue_on():
    turn_on(blue_pin)
    turn_off(red_pin)
    turn_off(green_pin)

def magenta_on():
    turn_on(red_pin)
    turn_on(blue_pin)
    turn_off(green_pin)

def green_on():
    turn_off(blue_pin)
    turn_off(red_pin)
    turn_on(green_pin)

@app.route('/led', methods=['POST'])
def led_on():
    content = request.json
    if(content["color"] == "white"):
        white_on()
    elif(content["color"] == "blue"):
        blue_on()
    elif(content["color"] == "green"):
        blue_on()
    elif(content["color"] == "magenta"):
        magenta_on()
    elif(content["color"] == "off"):
        all_off()
    return content["color"]
    
@app.route('/picture', methods=['GET'])
def take_picture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    name = 'img/geomsb.jpeg'
    picture = frame.copy()
    cv2.imwrite(name, frame)
    return send_file('../img/geomsb.jpeg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0')