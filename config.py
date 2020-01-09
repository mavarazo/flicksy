import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TV_IN = os.path.join(basedir, '/tv_in')
    TV_OUT = os.path.join(basedir, '/tv_out')
    MOVIE_IN = os.path.join(basedir, '/movie_in')
    MOVIE_OUT = os.path.join(basedir, '/movie_out')
    MUSIC_IN = os.path.join(basedir, '/music_in')
    MUSIC_OUT = os.path.join(basedir, '/music_out')
