import subprocess
import copy
from flask import Flask, abort, request
app = Flask(__name__)

current_process = None

DEMO_ARGS = ['demo', '--led-cols=64', '--led-chain=2', '-D']

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
        args.append(request.args["f"])
        
    kill_current()
    current_process = subprocess.Popen(args)
    return ""
