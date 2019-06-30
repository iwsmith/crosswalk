# crossXwalk main app

import logging
import random
import os

from flask import Flask, abort, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from xwalk.animation import Library
from xwalk.core import CrossWalk
from xwalk.schedule import Schedule


logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
library = Library('config.yml', './static/img', './static/snd')
schedule = Schedule('config.yml')
crosswalk = CrossWalk(library, schedule)
crosswalk.walk()


# GET    /               index page
# POST   /refresh        reload the animation library
# POST   /button         trigger button press

# GET    /state          get the current app state
# POST   /state          set a new state for the app
# POST   /sync           synchronize the sign

# GET    /demos/         list available demos
# GET    /walks/         list available walk animations

# GET    /images/        list available uploaded images
# POST   /images/        upload a new image
# DELETE /images/:id     delete an image by id

# GET    /queue/         list the queued scenes
# POST   /queue/         enqueue a scene to play
# DELETE /queue/         empty the queued scenes


### State Handlers ###

@app.route("/")
def index():
    recent = {}
    for animation in crosswalk.history:
        count = recent.get(animation.name, 0)
        recent[animation.name] = count + 1
    recent = sorted(recent.items(), key=lambda e: e[1], reverse=True)
    return render_template(
        'index.html',
        recent=recent,
        demos=crosswalk.demos,
        walks=library.walks,
        uploads=library.uploads,
        status=str(crosswalk.state()))


@app.route("/refresh", methods=['POST'])
def refresh_library():
    library.refresh()
    return "", 204


@app.route("/ready")
def set_ready():
    crosswalk.make_ready()
    return "", 200


@app.route("/button", methods=['POST'])
def push_button():
    body = request.get_json() or {}
    hold = body.get('hold', 0.0)
    crosswalk.button(hold)
    return jsonify({'ok': True})


@app.route("/state")
def get_state():
    return jsonify(crosswalk.state())


@app.route("/state", methods=['POST'])
def set_state():
    body = request.get_json()
    mode = body.get('mode')
    if mode == 'off':
        crosswalk.off()
    elif mode == 'demo':
        demo_id = body.get('demo')
        if demo_id is None:
            return jsonify({'error': "No demo id provided"}), 400
        crosswalk.demo(demo_id)
    elif mode == 'image':
        name = body.get('image')
        if name is None:
            return jsonify({'error': "No image name provided"}), 400
        image = library.find_image(name)
        if image is None:
            return jsonify({'error': "No image with name {}".format(name)}), 404
        crosswalk.show(image)
    elif mode == 'walk':
        crosswalk.walk()
    else:
        return jsonify({'error': "Unknown mode: {}".format(mode)}), 400
    return jsonify(crosswalk.state())


@app.route("/sync", methods=['POST'])
def sync_state():
    body = request.get_json() or {}
    scene = body.get('scene')
    if not scene:
        return jsonify({'error': "Missing scene to synchronize"}), 400
    crosswalk.sync(scene)
    return jsonify(crosswalk.state())



### Demo Handlers ###

@app.route("/demos/")
def list_demos():
    demos = [
        {
            'id': demo.demo_id,
            'description': demo.description,
            'ppm_required': demo.ppm_required,

        }
        for demo in crosswalk.demos
    ]
    return jsonify(demos)


### Image Handlers ###

@app.route("/walks/")
def list_walks():
    walks = []
    for image in library.walks:
        data = {
            'name': image.name,
            'image_path': image.image_path,
        }
        if image.audio_path:
            data['audio_path'] = image.audio_path
        if image.loops:
            data['loops'] = image.loops
        if image.frame_delay:
            data['frame_delay'] = image.frame_delay
        walks.append(data)
    return jsonify(walks)


@app.route("/images/")
def list_images():
    images = []
    for image in library.uploads:
        data = {
            'name': image.name,
            'image_path': image.image_path,
        }
        if image.audio_path:
            data['audio_path'] = image.audio_path
        if image.loops:
            data['loops'] = image.loops
        if image.frame_delay:
            data['frame_delay'] = image.frame_delay
        images.append(data)
    return jsonify(images)


@app.route("/images/", methods=['POST'])
def upload_image():
    f = request.files['image']
    if not f:
        return jsonify({'error': "No image file provided"}), 400
    f.save(os.path.join(library.image_dir, 'uploads', secure_filename(f.filename)))
    library.refresh()
    return redirect(url_for('index'))


@app.route("/images/<string:name>", methods=['DELETE'])
def delete_image(name):
    if name is None:
        return jsonify({'error': "No image name provided"}), 400
    image = library.find_image(name)
    if image is None:
        return jsonify({'error': "No image with name {}".format(name)}), 404
    if image not in library.uploads:
        return jsonify({'error': "Image {} is not an upload and cannot be deleted".format(name)}), 400
    os.remove(os.path.join(library.image_dir, secure_filename(filename)))
    library.refresh()
    return "", 204


### Queue Handlers ###

@app.route("/queue/")
def get_queue():
    return jsonify([walk.name for walk in crosswalk.queue])


@app.route("/queue/", methods=['POST'])
def add_queue():
    body = request.get_json() or {}
    name = body.get('walk')
    if not name:
        return jsonify({'error': "Missing walk animation name"}), 400
    walk = crosswalk.library.find_image(name)
    if not walk:
        return jsonify({'error': "Walk animation {} not found".format(name)}), 404
    crosswalk.queue.append(walk)
    return get_queue()


@app.route("/queue/", methods=['DELETE'])
def clear_queue():
    crosswalk.queue = []
    return "", 204
