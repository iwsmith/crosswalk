from datetime import datetime
from gpiozero import LED, Button
import logging
import requests
import time

logging.warning("Starting button")
led = LED(24)
led.on()
button = Button(18, bounce_time=.1, hold_time=20)


def button_released():
    if led.value:
        requests.post("http://localhost/button")


def button_held():
    logging.warning("Long button press detected, resetting...")
    requests.posts("http://localhost/reset")


def button_pressed():
    led.off()


button.when_pressed = button_pressed
button.when_released = button_released
button.when_held = button_held

# TODO: spin and check /state to set button light
while True:
    state = requests.get("Http://localhost/state").json()
    if state["ready"]:
        led.on()
        time.sleep(1)
    else:
        delta = datetime.strptime(state["ready_at"], "%a, %d %b %Y %H:%M:%S %Z") - datetime.now()
        logging.warning("Ready in %d seconds", delta)
        if 600 > delta.seconds > 0:
            time.sleep(delta.seconds)
        else:
            logging.error("Delay to high (%d seconds), polling at 1 second intervals...", delta.seconds)
            time.sleep(1)
