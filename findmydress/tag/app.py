import base64
import os
import re

import flask
from flask import Flask, send_from_directory, send_file, request
from modscrape.tag import models

app = Flask(__name__)
app.debug = True


APP_ROOT = os.path.dirname(os.path.realpath(__file__))

# TODO: remove hard-coded facepalm here - move to config
IMAGE_FILES_ROOT = '/Users/dave/projects/modscrape/files/images'

STATIC_ROOT = os.path.join(APP_ROOT, 'static')

STATIC_LABELS = [
    "background",
    "mask",
    ]


@app.route('/images/')
def images():
    session = models.Session()
    images = session.query(models.ItemImage)[:30]
    
    result_obj = {
        'labels': STATIC_LABELS,
        'imageURLs': [flask.url_for('image_file', image_id=i.id) for i in images],
        'annotationURLs': [flask.url_for('image_annotation_file', image_id=i.id) for i in images],
        }
    return flask.jsonify(result_obj)


@app.route('/images/<int:image_id>')
def image_detail(image_id):
    session = models.Session()
    image = models.ItemImage.query.get(image_id)
    return "TODO: fill in image detail"


@app.route('/images/<int:image_id>/file')
def image_file(image_id):
    session = models.Session()
    image = session.query(models.ItemImage).get(image_id)
    return send_from_directory(IMAGE_FILES_ROOT, image.image_path)


@app.route('/images/<int:image_id>/annotation', methods=['GET', 'POST'])
def image_annotation_file(image_id):
    if request.method == 'GET':
        session = models.Session()
        image = session.query(models.ItemImage).get(image_id)
        return send_from_directory(IMAGE_FILES_ROOT, os.path.join('annotations', image.image_path))

    elif request.method == 'POST':
        mimetype, data = parse_data_url(flask.request.form['imgDataURL'])
        with open('/tmp/sample-tag.png', 'w') as f:
            f.write(data)

        return "TODO: fill in image detail"


DATA_URL_PATTERN = re.compile(r'data:(?P<mimetype>.+);(?P<encoding>base64),(?P<encoded_data>.+)$')
def parse_data_url(url):
    match = DATA_URL_PATTERN.match(url)
    if not match:
        raise ValueError("Couldn't parse data URL")

    mimetype = match.group('mimetype')
    data = base64.b64decode(match.group('encoded_data'))
    return mimetype, data


# Static routes serving basic js-segment-annotator files
@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/static/<path:path>')
def send_static_data(path):
    return send_from_directory(STATIC_ROOT, path)
