from flask import (
    Blueprint, request, jsonify
)

from db import get_db
from services.cleaning_schedule_service import get_cleaning_schedule
from auth import login_required

bp = Blueprint('cleaning_schedule', __name__)

@bp.route('/cleaning_schedule', methods=['POST'])
@login_required
def set_cleaning_schedule_api():
    type = request.form['type']
    date = request.form['date']
    error = None

    if not type:
        return jsonify({'status': 'Type is required.'}), 403
    if not date:
        return jsonify({'status': 'Date is required.'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO cleaning_schedule (type, date)'
        ' VALUES (?, ?)',
        (type, date)
    )
    db.commit()

    check = get_db().execute(
        'SELECT timestamp, type, date'
        ' FROM cleaning_schedule'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Cleaning schedule successfully recorded',
        'data': {
            'type': check['type'],
            'date': check['date'],
            'timestamp': check['timestamp']
         }
         }), 200

@bp.route('/cleaning_schedule', methods=['GET'])
@login_required
def get_cleaning_schedule_api():
    type = request.form['type']
    date = request.form['date']
    result = get_cleaning_schedule(type, date)
    return jsonify(
        result
    ), 200