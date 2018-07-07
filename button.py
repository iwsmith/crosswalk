from datetime import datetime
from gpiozero import LED, Button
from signal import pause
import logging
import requests

logging.warning("Starting button")
led = LED(24)
led.on()
button = Button(18, bounce_time=.1, hold_time=20)

def button_released():
    print("Button released")
    led.on()
    requests.post("http://localhost/button")

def button_held():
    print("Button held")

def button_pressed():
    print("button pressed")
    led.off()


button.when_pressed = button_pressed
button.when_released = button_released
button.when_held = button_held

# TODO: spin and check /state to set button light
pause()
