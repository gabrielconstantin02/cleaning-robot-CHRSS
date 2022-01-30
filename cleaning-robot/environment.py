
from flask import (
    Blueprint, request, jsonify
)

from .db import get_db

bp = Blueprint('environment', __name__)


@bp.route('/resource_level', methods=['POST'])
def set_resource_level():
    resource_level = request.form['resource_level']
    error = None

    if not resource_level:
        return jsonify({'status': 'Resource level is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO resource_level (value)'
        ' VALUES (?)',
        (resource_level,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM resource_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Resource level successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
         }
         }), 200


@bp.route('/battery_level', methods=['POST'])
def set_battery_level():
    resource_level = request.form['battery_level']
    error = None

    if not resource_level:
        return jsonify({'status': 'Battery level is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO battery_level (value)'
        ' VALUES (?)',
        (resource_level,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM battery_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Battery level successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
         }
         }), 200


@bp.route('/bin_level', methods=['POST'])
def set_bin_level(automatic_empty=False):
    if not automatic_empty:
        resource_level = request.form['bin_level']
        if not resource_level:
            return jsonify({'status': 'Bin level is required.'}), 403

    if automatic_empty:
        resource_level = 0

    db = get_db()
    db.execute(
        'INSERT INTO bin_level (value)'
        ' VALUES (?)',
        (resource_level,)
    )
    db.commit()
    if not automatic_empty:
        check = get_db().execute(
            'SELECT id, timestamp, value'
            ' FROM bin_level'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        return jsonify({
            'status': 'Bin level successfully recorded',
            'data': {
                'id': check['id'],
                'timestamp': check['timestamp'],
                'value': check['value']
             }
             }), 200