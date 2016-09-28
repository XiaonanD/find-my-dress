import base64
import os
import re

import flask
from flask import Flask, send_from_directory, send_file, request
from modscrape.tag import models

app = Flask(__name__)
app.debug = True


# Static routes serving basic js-segment-annotator files
@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/static/<path:path>')
def send_static_data(path):
    return send_from_directory(STATIC_ROOT, path)
