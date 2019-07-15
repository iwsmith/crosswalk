from datetime import datetime
from gpiozero import LED, Button
import logging
import os
import requests
import time

logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

button_pin = int(os.getenv('XWALK_BUTTON_PIN', 19))
logging.warning("Starting button watcher on pin %d", button_pin)
led = LED(24)
button = Button(button_pin)
pressed_at = time.perf_counter()
sign_ready = False


def button_released():
    global sign_ready
    logging.debug("Button released: %s (LED: %s)", sign_ready, led.value)
    if sign_ready:
        sign_ready = False
        elapsed = time.perf_counter() - pressed_at
        requests.post("http://localhost/button", json={'hold': elapsed})
        led.off()


def button_pressed():
    global pressed_at
    logging.debug("Button pressed (ready: %s)", sign_ready)
    pressed_at = time.perf_counter()


button.when_pressed = button_pressed
button.when_released = button_released


# Spin and check /state to set button light.
while True:
    try:
        state = requests.get("http://localhost/state").json()
        now = datetime.now()
        if state["ready"]:
            # Crosswalk reports as ready
            if sign_ready == False:
                logging.info("Crosswalk is ready!")
            sign_ready = True
            led.on()
            time.sleep(5)
        else:
            # Crosswalk is not ready yet
            sign_ready = False
            led.off()
            time.sleep(2)
    except Exception as ex:
        logging.error("Caught exception while checking crosswalk state: %s", ex)
        time.sleep(10)
