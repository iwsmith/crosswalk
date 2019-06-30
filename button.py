from datetime import datetime
from gpiozero import LED, Button
import logging
import requests
import time

logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.warning("Starting button watcher")
led = LED(24)
button = Button(19, hold_time=20)
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


def button_held():
    logging.warning("Long button press detected, resetting...")
    requests.post("http://localhost/reset")


def button_pressed():
    logging.debug("Button pressed (ready: %s)", sign_ready)
    pressed_at = time.perf_counter()


button.when_pressed = button_pressed
button.when_released = button_released
button.when_held = button_held


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
            time.sleep(10)
        else:
            # Crosswalk is not ready yet
            sign_ready = False
            led.off()
            time.sleep(2)
    except Exception as ex:
        logging.error("Caught exception while checking crosswalk state: %s", ex)
        time.sleep(10)
