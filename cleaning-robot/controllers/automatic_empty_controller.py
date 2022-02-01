from flask import (
    Blueprint, jsonify
)
from services.robot_service import get_bin_level
from controllers.environment_controller import set_bin_level
from auth import login_required

bp = Blueprint('automatic_empty', __name__, url_prefix='/bin')


@bp.route('/', methods=['GET'])
@login_required
def automatic_empty_api():
    bin_data = get_bin_level()
    check = bin_data['data']
    status = bin_data['status']

    if check is None:
        return jsonify({
            'status': status
        }), 404

    print(check['value'])

    if check['value'] == 100:
        set_bin_level(0)
        bin_data = get_bin_level()
        check = bin_data['data']
        return jsonify({
            'status': 'Finished automatic bin empty',
            'data': {
                'id': check['id'],
                'timestamp': check['timestamp'],
                'value': check['value']
            }
        }), 200
    return jsonify({
        'status': 'Automatic empty not required. Bin is not full!',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200
