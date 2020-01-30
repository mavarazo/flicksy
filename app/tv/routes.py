import os
import urllib.parse
import requests
import re

from flask import render_template
from flask import current_app as app

from app.tv import bp, thetvdbclient

class TvFile():

    def __init__(self, file_to_rename, extension, serie, episode):
        self._file_to_rename = file_to_rename
        self._extension = extension
        self._serie = serie
        self._episode = episode

    @property
    def file_to_rename(self):
        return self._file_to_rename

    @property
    def extension(self):
        return self._extension

    @property
    def serie(self):
        return self._serie

    @property
    def episode(self):
        return self._episode

    def __str__(self):
        return f"{self.file_to_rename}, {self._serie.seriesName, self._episode.episodeName})"


@bp.route('/tv/', methods=['GET'])
@bp.route('/tv/index', methods=['GET'])
def index():
    queue = []
    for f in os.listdir(app.config['TV_IN']):
        filename, extension = os.path.splitext(f)
        m = search_with_regex_for_tv_patterns(filename)
        if m:
            serie = thetvdbclient.search_series(m['seriesname'])[0]
            episode = thetvdbclient.search_episode(serie.id, int(
                m['seasonnumber']), int(m['episodenumber']))[0]
            queue.append(TvFile(os.path.abspath(f), extension, serie, episode))

    return render_template('tv/index.html', title='TV', queue=queue)


def search_with_regex_for_tv_patterns(file):
    regs = app.config['tv_patterns']
    for reg in regs:
        m = re.search(reg['pattern'], file)
        if m:
            return m.groupdict()
