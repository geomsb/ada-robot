import requests

def set_led(color):
    led_api_url = 'http://georginapi:5000/led'
    api_response = requests.post(led_api_url,  json={"color": color})

def white_on():
    set_led("white")

def blue_on():
    set_led("blue")

def green_on():
    set_led("green")

def magenta_on():
    set_led("magenta")

def all_off():
    set_led("off")




