import base64
import os
import re

import flask
from flask import (
    redirect, render_template, request, url_for,
    )

from findmydress.db import models
from findmydress.web import match, config
from findmydress.web.app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/match', methods=['GET', 'POST'])
def match_item():
    if request.method == 'GET':
        return flask.redirect(url_for('index'))

    file = request.files['query']
    uploads_root = os.path.join(config.STATIC_ROOT, 'uploads')
    save_path = os.path.join(uploads_root, file.filename)
    url_path = os.path.join('/static/uploads', file.filename)
    file.save(save_path)

    probability_list = match.find_similar_items(
        match.load_model(),
        match.extract_image_features(save_path),
        )

    metadata = match.load_item_records()

    dress_index = {item['dress_id']: item for item in metadata}

    for prob_result in probability_list:
        # get an item from dress_index for prob_result
        dress_result = dress_index.get(prob_result['dress_id'])
        if not dress_result:
            continue
        prob_result.update(dress_result)

    probability_list.sort(key=lambda x: x['probability'], reverse=True)

    return render_template(
        'match.html',
        filepath=url_path,
        matches=probability_list,
    )


@app.route('/images/')
def images():
    session = models.Session()
    images = session.query(models.ItemImage)[:30]
    
    result_obj = {
        'labels': config.STATIC_LABELS,
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
