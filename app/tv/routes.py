import os, urllib.parse, requests, re

from flask import current_app, render_template

from app.tv import bp


@bp.route('/tv/', methods=['GET'])
@bp.route('/tv/index', methods=['GET'])
def index():
    print(current_app.config)
    headers = {"Authorization": "Bearer {}".format(current_app.config['THETVDB_API_KEY'])}
    files = os.listdir(current_app.config['TV_IN'])
    for file in files:
        m = search_with_regex_for_tv_patterns(file)
        if m:
            query = '{}/search/tv?query={}'.format(current_app.config['THETVDB_API_URL'], urllib.parse.quote(m['seriesname']))
            print(query)
            print(requests.get(query, headers=headers).json())

    return render_template('tv/index.html', title='TV', files=files)


def search_with_regex_for_tv_patterns(file):
    regs = current_app.config['tv_patterns']
    for reg in regs:
        m = re.search(reg['pattern'], file)
        if m:
            return m.groupdict()
