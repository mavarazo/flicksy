from flask import render_template

from app.tv import bp


@bp.route('/tv/', methods=['GET'])
@bp.route('/tv/index', methods=['GET'])
def index():
    return render_template('tv/index.html', title='TV')
