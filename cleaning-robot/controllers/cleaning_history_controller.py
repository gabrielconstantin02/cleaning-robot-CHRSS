from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from services.cleaning_history_service import get_cleaning_history

bp = Blueprint('cleaning_history', __name__)


@bp.route('/cleaning_history', methods=['GET'])
@login_required
def get_cleaning_history_api():
    type = request.form['type']
    date = request.form['date']
    result = get_cleaning_history(type, date)
    return jsonify(result), 200