import os

from flask import render_template, request

from findmydress.web import match
from findmydress.web.app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('master.html')


@app.route('/go', methods=['POST'])
def go():
    # import ipdb; ipdb.set_trace();
    file = request.files['query']
    uploads_root = '/Users/amyshapiro/flask_for_app/flaskexample/static/uploads'
    save_path = os.path.join(uploads_root, file.filename)
    url_path = os.path.join('/static/uploads', file.filename)
    file.save(save_path)
    best_match_image_url = match.find_best_match_image(save_path)
    return render_template(
        'go.html',
        filepath=url_path,
        best_match_image_url=best_match_image_url,
    )
