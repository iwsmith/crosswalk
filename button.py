from gpiozero import Button, LED
from signal import pause
import requests

led = LED(24)
led.on()

button = Button(18)

def btn():
    led.on()

    requests.get("http://localhost/random")

button.when_pressed = led.off
button.when_released =  btn

pause()
