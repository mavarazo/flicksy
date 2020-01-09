from flask import Blueprint

bp = Blueprint('tv', __name__)

from app.tv import routes