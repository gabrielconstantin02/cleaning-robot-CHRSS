from auth import login_required
from services.air_service import *

bp = Blueprint('air_api', __name__, url_prefix='/air')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def set_or_get_air_api():
    if request.method == 'POST':
        if 'air_quality' not in request.form:
            return jsonify({'status': 'Air quality is required.'}), 400
        air_quality = request.form['air_quality']
        set_air(air_quality)

    check = get_air()

    if check is None:
        return jsonify({
            'status': 'No air quality record found.'
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


@bp.route('/real', methods=['GET'])
@login_required
def get_air_realtime_api():
    set_air_realtime()
    check = get_air()

    if check is None:
        return jsonify({
            'status': 'No air quality record found.'
        }), 404

    return jsonify({
        'status': 'Realtime air quality successfully retrieved.',
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'air_quality': check['value']
        }
    }), 200
