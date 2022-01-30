from flask import (
    Blueprint, request, jsonify
)

from .db import get_db


def get_bin_level():
    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM bin_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return check
