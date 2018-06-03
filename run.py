from flask import Flask, abort, request, jsonify, render_template, redirect, url_for
from led_controller import LEDController, MockController
from werkzeug.utils import secure_filename
from scene import from_yaml
import os

led = LEDController("./static/img")
#led = MockController("./static/img")
scenes = from_yaml("./static/scenes.yaml")
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

@app.route("/scene/<string:name>")
def play_scene(name):
    led.scene(scenes[name])
    return redirect(url_for('index'))

@app.route("/images")
def list_images():
    return jsonify(led.list_images())

@app.route("/random")
def random_image():
    led.random_image()
    return redirect(url_for('index'))

@app.route("/status")
def status():
    return led.status()

@app.route("/upload", methods=['POST'])
def upload_file():
    f = request.files['image']
    f.save(os.path.join(led.image_path, secure_filename(f.filename)))
    return redirect(url_for('index'))
