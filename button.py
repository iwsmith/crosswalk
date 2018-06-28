from gpiozero import Button
from signal import pause
import requests

def button_press():
    print("button")
    requests.get("http://localhost/random")

button = Button(18)

button.when_released = button_press

pause()
