from automatic_empty_service import *
from environment import set_bin_level
from auth import login_required

bp = Blueprint('automatic_empty', __name__, url_prefix='/bin')


@bp.route('/', methods=['GET'])
@login_required
def automatic_empty():

    check = get_bin_level()

    if check is None:
        return jsonify({
            'status': 'No bin level record found'
        }), 404

    print(check['value'])

    if check['value'] == 100:
        set_bin_level(True)
        check = get_bin_level()
        return jsonify({
            'status': 'Finished automatic bin empty',
            'data': {
                'id': check['id'],
                'timestamp': check['timestamp'],
                'value': check['value']
            }
        }), 200
    return jsonify({
        'status': 'Automatic empty not required. Bin is not full !',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200