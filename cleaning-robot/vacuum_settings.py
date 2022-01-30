from flask import (
    Blueprint, request, jsonify
)

from db import get_db

bp = Blueprint('vacuum_settings', __name__)

@bp.route('/vacuum_settings', methods=['POST'])
def set_vacuum_settings():
    frequency = request.form['frequency']
    power = request.form['power']
    error = None

    if not frequency:
        return jsonify({'status': 'Frequency level is required.'}), 403

    if not power:
        return jsonify({'status': 'Power level is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO vacuum_settings (frequency, power)'
        ' VALUES (?, ?)',
        (frequency, power, )
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, frequency, power'
        ' FROM vacuum_settings'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Vacuum setting successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'frequency': check['frequency'],
            'power': check['power']
         }
         }), 200

@bp.route('/vacuum_settings', methods=['GET'])
def get_vacuum_settings():
        id = request.form['id']
        result = get_db().execute(
            'SELECT *'
            ' FROM vacuum_settings'
            ' WHERE id=(?)',
            (id, )
        ).fetchone()
        return jsonify({
        'data': {
            'id': result['id'],
            'timestamp': result['timestamp'],
            'frequency': result['frequency'],
            'power': result['power'],
        }
    }), 200