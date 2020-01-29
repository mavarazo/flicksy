import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    THETVDB_APIKEY = os.environ.get('THETVDB_APIKEY')
    TV_IN = os.path.join(basedir, 'tv_in')
    TV_OUT = os.path.join(basedir, 'tv_out')
    TV_REGEX = os.path.join(basedir, 'regex_tv.json')