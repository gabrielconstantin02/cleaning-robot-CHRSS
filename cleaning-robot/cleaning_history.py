from flask import (
    Blueprint, request, jsonify
)

from db import get_db

bp = Blueprint('cleaning_history', __name__)

@bp.route('/cleaning_history', methods=['GET'])
def get_cleaning_history():
    type = request.form['type']
    date = request.form['date']
    result = get_db().execute(
        'SELECT *'
        ' FROM cleaning_history'
        ' WHERE type=(?) AND date=(?)',
        (type, date)
    ).fetchone()
    return jsonify({
    'data': {
        'id': result['id'],
        'timestamp': result['timestamp'],
        'type': result['type'],
        'date': result['date'],
        'elapsed_time': result['elapsed_time']
    }
}), 200