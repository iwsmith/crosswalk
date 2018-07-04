# crossXwalk main app

import random
import os

from flask import Flask, abort, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from xwalk.core import CrossWalk
from xwalk.scene import Library



app = Flask(__name__)
library = Library('./static/img', './static/snd', 'config.yml')
crosswalk = CrossWalk(library)


# GET  /                 index page
# POST /button           trigger button press

# GET  /state            get the current app state
# POST /state            set a new state for the app
#   mode=off
#   mode=demo demo=n
#   mode=image path=p
#   mode=walk
#   mode=sync id=x [intro=y] [outro=z]

# GET    /demos/         list available demos

# GET    /images/        list available images
# POST   /images/        upload a new image
# GET    /images/:id     fetch image by id
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
        # TODO: show image
        raise "NYI"
    elif mode == 'walk':
        # check sync flag
        # kill demo controller
        # play walk images
        # play walk audio
        raise "NYI"
    else:
        return jsonify({'error': "Unknown mode: {}".format(mode)}), 400
    return jsonify(crosswalk.state())


### Demo Handlers ###

@app.route("/demos/")
def list_demos():
    # TODO: implement
    raise "NYI"


### Image Handlers ###

@app.route("/images/")
def list_images():
    # TODO: implement
    raise "NYI"


@app.route("/images/", methods=['POST'])
def upload_image():
    # TODO: implement
    raise "NYI"


@app.route("/images/<string:id>")
def get_image(image_id):
    # TODO: implement
    raise "NYI"


@app.route("/images/<string:id>", methods=['DELETE'])
def delete_image(image_id):
    # TODO: implement
    raise "NYI"


### Queue Handlers ###

@app.route("/queue/")
def get_queue():
    # TODO: implement
    raise "NYI"


@app.route("/queue/", methods=['POST'])
def add_queue():
    # TODO: implement
    raise "NYI"


@app.route("/queue/", methods=['DELETE'])
def clear_queue():
    # TODO: implement
    raise "NYI"




### Old Code ###

#@app.route("/upload", methods=['POST'])
#def upload_file():
#    f = request.files['image']
#    f.save(os.path.join(led.image_path, secure_filename(f.filename)))
#    return redirect(url_for('index'))
