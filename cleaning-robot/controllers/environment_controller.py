
from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from services.robot_service import *
from db import get_db

bp = Blueprint('environment', __name__)


@bp.route('/resource_level', methods=['POST'])
def set_resource_level(base=-1):
    if base == -1:
        resource_level = request.form['resource_level']

        if not resource_level:
            return jsonify({'status': 'Resource level is required.'}), 403
    else:
        resource_level = base

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
def set_battery_level(base=-1):
    if base == -1:
        resource_level = request.form['battery_level']

        if not resource_level:
            return jsonify({'status': 'Battery level is required.'}), 403
    else:
        resource_level = 100

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
def set_bin_level(base=-1):
    if base == -1:
        bin_level = request.form['bin_level']
        if not bin_level:
            return jsonify({'status': 'Bin level is required.'}), 403

    else:
        bin_level = 0

    db = get_db()
    db.execute(
        'INSERT INTO bin_level (value)'
        ' VALUES (?)',
        (bin_level,)
    )
    db.commit()
    if base == -1:
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


@bp.route('/bin_level', methods=['GET'])
@login_required
def get_bin():
    return jsonify(get_bin_level()), 200


@bp.route('/battery_level', methods=['GET'])
@login_required
def get_battery():
    return jsonify(get_battery_level()), 200


@bp.route('/resource_level', methods=['GET'])
@login_required
def get_resource():
    return jsonify(get_resource_level()), 200
