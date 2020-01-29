import os, urllib.parse, requests, re

from flask import render_template
from flask import current_app as app

from app.tv import bp, thetvdbclient


@bp.route('/tv/', methods=['GET'])
@bp.route('/tv/index', methods=['GET'])
def index():
    files = os.listdir(app.config['TV_IN'])
    for file in files:
        m = search_with_regex_for_tv_patterns(file)
        if m:
            thetvdbclient.search_series(m['seriesname'])

    return render_template('tv/index.html', title='TV', files=files)


def search_with_regex_for_tv_patterns(file):
    regs = app.config['tv_patterns']
    for reg in regs:
        m = re.search(reg['pattern'], file)
        if m:
            return m.groupdict()
