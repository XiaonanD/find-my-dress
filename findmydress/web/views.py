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
    uploads_root = '/Users/amyshapiro/github/find-my-dress/findmydress/web/static/uploads'
    save_path = os.path.join(uploads_root, file.filename)
    url_path = os.path.join('/static/uploads', file.filename)
    file.save(save_path)

    probability_list = match.find_similar_items(match.load_model(),
        match.extract_image_features(save_path))

    metadata = match.load_item_records('/Users/amyshapiro/github/find-my-dress/data/dress_details.csv')

    dress_index = {item['dress_id']:item for item in metadata}

    for prob_result in probability_list:
        # get an item from dress_index for prob_result
        dress_result = dress_index.get(str(prob_result['dress_id']))
        if not dress_result:
            continue
        prob_result.update(dress_result)

    return render_template(
        'go.html',
        filepath=url_path,
        matches=probability_list,
    )
