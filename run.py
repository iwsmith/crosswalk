import subprocess
import copy
import os
from flask import Flask, abort, request
app = Flask(__name__)

current_process = None

DEMO_ARGS = ['demo', '--led-cols=64', '--led-chain=2', '-L', '-D']
IMG_VIEWER_ARGS = ['led-image-viewer', '--led-cols=64', '--led-no-hardware-pulse', '--led-chain=2', '--led-gpio-mapping=adafruit-hat', '-L', '-R 270']

IMAGES_PATH = os.getenv('CROSSWALK_IMAGES')


@app.route("/kill")
def kill_current():
    global current_process
    if current_process:
        current_process.kill()
        current_process = None
        return ""
    return ""

@app.route("/demo/<int:n>")
def run_demo(n):
    global current_process
    args = copy.copy(DEMO_ARGS)

    if n < 0 or n > 11:
        abort(400)

    args.append(str(n))
    if n is 1 or n is 2:
        args.append(os.path.join(IMAGES_PATH, request.args["f"]))
        
    kill_current()
    current_process = subprocess.Popen(args)
    return ""

@app.route("/image/<string:filename>")
def display_image(filename):
    global current_process
    args = copy.copy(IMG_VIEWER_ARGS)

    args.append(os.path.join(IMAGES_PATH, filename))

    kill_current()
    current_process = subprocess.Popen(args)
    return ""

