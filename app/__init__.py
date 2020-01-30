import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os, json
from flask import Flask, request, current_app
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with open(app.config['TV_REGEX']) as config_file:
        regex_tv = json.load(config_file)
    app.config.update(regex_tv)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tv import bp as tv_bp
    app.register_blueprint(tv_bp)

    from app.tv import thetvdbclient
    thetvdbclient.init_app(app.config['THETVDB_APIKEY'])

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/kidsbox.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flicksy startup')

    return app