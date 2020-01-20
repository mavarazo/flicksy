import os, urllib.parse, requests

from flask import current_app, render_template

from app.tv import bp


@bp.route('/tv/', methods=['GET'])
@bp.route('/tv/index', methods=['GET'])
def index():
    headers = {"Authorization": "Bearer {}".format(current_app.config['THETVDB_API_KEY'])}
    files = os.listdir(current_app.config['TV_IN'])
    for file in files:
        query = '{}/search/tv?query={}'.format(current_app.config['THETVDB_API_URL'], urllib.parse.quote(file))
        print(query)
        print(requests.get(query, headers=headers).json())

    return render_template('tv/index.html', title='TV', files=files)
