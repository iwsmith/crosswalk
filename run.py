import subprocess
from flask import Flask
app = Flask(__name__)

current_process = None
DEMO_ARGS = ['--led-cols=64', '--led-chain=2', '-D']

@app.route("/kill")
def kill_current():
    if current_process:
        current_process.kill()
        current_process = None

@app.route("/demo/<int:n>")
def run_demo(n):
    kill_current()
    DEMO_ARGS.append(n)
    current_process = subprocess.Popen(DEMO_ARGS)
    DEMO_ARGS.pop()
