from flask import (
    Blueprint, request, jsonify
)

from .db import get_db
from .air_service import *

bp = Blueprint('vacuum_settings', __name__)

@bp.route('/vacuum_settings', methods=['POST'])
def set_vacuum_settings():
    frequency = request.form['frequency']
    power = request.form['power']
    error = None

    air = get_air()

    if not frequency and not power:
        if air is None:
            set_air_realtime()
            return jsonify({
                'status': 'No air quality record found; trying api...'
            }), 404
        frequency = air['value'] // 50 + 1
        power = frequency * 100
    elif not frequency:
        if air is None:
            set_air_realtime()
            return jsonify({
                'status': 'No air quality record found; trying api...'
            }), 404
        frequency = air['value'] // 50 + 1
    elif not power:
        if air is None:
            set_air_realtime()
            return jsonify({
                'status': 'No air quality record found; trying api...'
            }), 404
        power = (air['value'] // 50 + 1) * 100

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