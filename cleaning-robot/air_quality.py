from flask import (
    Blueprint, request, jsonify
)

from .auth import login_required
from .air_service import *

bp = Blueprint('air_api', __name__, url_prefix='/air')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def set_or_get_temperature():
    if request.method == 'POST':
        if 'air_quality' not in request.form:
            return jsonify({'status': 'Air quality is required.'}), 400
        air_quality = request.form['air_quality']
        set_air(air_quality)

    check = get_air()

    if check is None:
        set_air_realtime()
        return jsonify({
            'status': 'No air quality record found; trying api...'
        }), 404

    return jsonify({
        'status': 'Air quality successfully recorded.' if request.method == 'POST'
        else 'Air quality successfully retrieved.',
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'air_quality': check['value']
        }
    }), 200
