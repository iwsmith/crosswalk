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
button = Button(18, hold_time=20)
sign_ready = False


def button_released():
    global sign_ready
    logging.debug("Button released: %s (LED: %s)", sign_ready, led.value)
    if sign_ready:
        sign_ready = False
        requests.post("http://localhost/button")
        led.off()


def button_held():
    logging.warning("Long button press detected, resetting...")
    requests.post("http://localhost/reset")


def button_pressed():
    logging.debug("Button pressed (ready: %s)", sign_ready)
    #led.off()


button.when_pressed = button_pressed
button.when_released = button_released
button.when_held = button_held

# Spin and check /state to set button light.
while True:
    try:
        state = requests.get("http://localhost/state").json()
        ready_at = datetime.strptime(state["ready_at"], "%a, %d %b %Y %H:%M:%S %Z")
        now = datetime.now()
        if state["ready"]:
            # Crosswalk reports as ready
            if sign_ready == False:
                logging.info("Crosswalk is ready!")
            sign_ready = True
            led.on()
            time.sleep(1)
        elif ready_at <= now:
            # Crosswalk just became ready.
            logging.debug("Wait for it...")
            time.sleep(1)
        else:
            # Crosswalk is not ready yet
            sign_ready = False
            led.off()
            delta = ready_at - now
            if delta.seconds >= 60:
                naptime = 30
            elif delta.seconds >= 1:
                naptime = delta.seconds/2
            else:
                naptime = delta.total_seconds() + 0.25
            logging.debug("Crosswalk ready in %s (sleeping %.2f)", delta, naptime)
            time.sleep(naptime)
    except Exception as ex:
        logging.error("Caught exception while checking crosswalk state: %s", ex)
        time.sleep(1)
