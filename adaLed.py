import sys, time
import RPi.GPIO as GPIO

redPin   = 11
greenPin = 13
bluePin  = 15

def turn_on(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def turn_off(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def white_on():
    turn_on(redPin)
    turn_on(greenPin)
    turn_on(bluePin)

def white_off():
    turn_off(redPin)
    turn_off(greenPin)
    turn_off(bluePin)

def blue_on():
    turn_on(bluePin)

def blue_off():
    turn_off(bluePin)

def magenta_on():
    turn_on(redPin)
    turn_on(bluePin)

def magenta_off():
    turn_off(redPin)
    turn_off(bluePin)





