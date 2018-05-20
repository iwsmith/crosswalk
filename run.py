from flask import Flask, abort, request, jsonify, render_template, redirect, url_for
from led_controller import LEDController

led = LEDController("./static/img")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html',
                           images=led.list_images(),
                           demos=led.list_demos(),
                           status=str(led))

@app.route("/kill")
def kill_current():
    led.kill()
    return redirect(url_for('index'))

@app.route("/demo/<int:n>")
def run_demo(n):
    led.demo(n, request.args.get("f"))
    return redirect(url_for('index'))

@app.route("/image/<string:filename>")
def display_image(filename):
    led.image(filename)
    return redirect(url_for('index'))

@app.route("/images")
def list_images():
    return jsonify(led.list_images())

@app.route("/random")
def random_image():
    return led.random_image()

@app.route("/status")
def status():
    return str(led)

