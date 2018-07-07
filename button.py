from datetime import datetime
from gpiozero import Button
from signal import pause
import requests

last_press = datetime.now()

def button_press():
    global last_press
    delta = datetime.now() - last_press
    if delta.total_seconds() < 0.5:
        print("debounced ({})".format(delta))
    else:
        print("button press")
        requests.post("http://localhost/button")
        last_press = datetime.now()

button = Button(18, bounce_time=0.5)

button.when_released = button_press

# TODO: spin and check /state to set button light
pause()
