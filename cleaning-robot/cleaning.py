from flask import (
    Blueprint, request, jsonify
)

from .auth import login_required
from .db import get_db

bp = Blueprint('cleaning', __name__, url_prefix='/cleaning')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def set_cleaning():
    if request.method == 'POST':
        type = request.form['type']
        settings_v = request.form['settings_v']
        settings_m = request.form['settings_m']

        if not type:
            return jsonify({'status': 'Type is required.'}), 403
        if not settings_v:
            return jsonify({'status': 'Vacuuming settings are required.'}), 403
        if not settings_m:
            return jsonify({'status': 'Mop settings are required.'}), 403

        db = get_db()
        db.execute(
            'INSERT INTO cleaning (value)'
            ' VALUES (?)',
            (type, settings_v, settings_m)
        )
        db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, type, settings_v, settings_m'
        ' FROM cleaning'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Cleaning succesfully recorded/retrieved',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type': check['type'],
            'cleaning_v': check['cleaning_v'],
            'cleaning_m': check['cleaning_m'],
        }
    }), 200

# TODO:
# Create endpoint that allows to get and change model of headrests (models: cushioned, leather, plastic)