# crossXwalk main app

import logging
import random
import os

from flask import Flask, abort, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from xwalk.core import CrossWalk
from xwalk.scene import Library


logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
library = Library('./static/img', './static/snd', 'config.yml')
crosswalk = CrossWalk(library)



# GET    /               index page

# GET    /state          get the current app state
# POST   /state          set a new state for the app
#   mode=off
#   mode=demo demo=n
#   mode=image path=p
#   mode=walk
#   mode=sync id=x [intro=y] [outro=z]

# POST   /button         trigger button press

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
    return render_template(
        'index.html',
        demos=crosswalk.demos,
        walks=library.walks,
        uploads=library.uploads,
        status=str(crosswalk.state()))


@app.route("/refresh", methods=['POST'])
def refresh_library():
    library.refresh()
    return "", 204


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
        # TODO:
        # check sync flag
        # kill demo controller
        # play walk images
        # play walk audio
        crosswalk.walk()
    else:
        return jsonify({'error': "Unknown mode: {}".format(mode)}), 400
    return jsonify(crosswalk.state())


@app.route("/button", methods=['POST'])
def push_button():
    body = request.get_json()
    hold = body.get('hold', 0.0)
    crosswalk.button(hold)
    return jsonify({ok: True})


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
    # TODO: implement
    raise Error("NYI")


@app.route("/queue/", methods=['POST'])
def add_queue():
    # TODO: implement
    raise Error("NYI")


@app.route("/queue/", methods=['DELETE'])
def clear_queue():
    # TODO: implement
    raise Error("NYI")
