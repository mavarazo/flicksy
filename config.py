import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    THETVDB_API_KEY = os.environ.get('THETVDB_API_KEY')
    THETVDB_API_URL = os.environ.get('THETVDB_API_URL', default = 'https://api.themoviedb.org/4')
    TV_IN = os.path.join(basedir, 'tv_in')
    TV_OUT = os.path.join(basedir, 'tv_out')
    TV_REGEX = os.path.join(basedir, 'regex_tv.json')