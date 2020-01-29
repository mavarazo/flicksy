from flask import Blueprint
from flask import current_app as app

from . import thetvdbclient

bp = Blueprint('tv', __name__)
thetvdbclient = thetvdbclient.TheTvDbClient()

from app.tv import routes
