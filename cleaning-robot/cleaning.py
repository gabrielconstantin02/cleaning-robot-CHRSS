from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('cleaning', __name__)

@bp.route('/cleaning', methods=['POST'])
@login_required
def set_cleaning():
    if request.method == 'POST':
        type = request.form['type']
        settings_v = request.form['settings_v']
        settings_m = request.form['settings_m']

        if not type:
            return jsonify({'status': 'Type is required.'}), 403
        if type not in ['0', '1']:
            return jsonify({'status': 'Type should be 0 or 1.'}), 403
        if not settings_v:
            return jsonify({'status': 'Vacuuming settings are required.'}), 403
        if not settings_m:
            return jsonify({'status': 'Mop settings are required.'}), 403

        db = get_db()
        db.execute(
            'INSERT INTO cleaning (type, settings_v, settings_m)'
            ' VALUES (?, ?, ?)',
            (type, settings_v, settings_m)
        )
        db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, type, settings_v, settings_m'
        ' FROM cleaning'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Cleaning successfully recorded/retrieved',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type': check['type'],
            'cleaning_v': check['settings_v'],
            'cleaning_m': check['settings_m'],
        }
    }), 200

@bp.route('/cleaning', methods=['GET'])
@login_required
def get_cleaning():
    id = request.form['id']
    result = get_db().execute(
        'SELECT *'
        ' FROM cleaning'
        ' WHERE id=(?)',
        (id,)
    ).fetchone()
    return jsonify({
    'data': {
        'id': result['id'],
        'timestamp': result['timestamp'],
        'type': result['type'],
        'cleaning_v': result['settings_v'],
        'cleaning_m': result['settings_m'],
    }
}), 200