from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from air_service import *
from db import get_db

bp = Blueprint('led', __name__, url_prefix='/led')

@bp.route('/', methods=['GET'])
@login_required
def get_vacuum_settings():
        db = get_db()
        result_cleaning= db.execute(
            """SELECT *
                FROM cleaning
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
        ).fetchone()
        result_resource_level = db.execute(
            """SELECT *
                FROM resource_level
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
        ).fetchone()
        result_battery_level = db.execute(
            """SELECT *
                FROM battery_level
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
        ).fetchone()
        result_bin_level = db.execute(
            """SELECT *
                FROM bin_level
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
        ).fetchone()
        result_air_quality = db.execute(
            """SELECT *
                FROM air_quality
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
        ).fetchone()
        if result_cleaning['type'] == 0: # 0 for vacuuming, 1 for mopping
            result_vacuum = db.execute(
            """SELECT *
                FROM vacuum_settings
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
            ).fetchone()
            return jsonify({
            'data': {
                'resource_level': result_resource_level['value'],
                'battery_level': result_battery_level['value'],
                'bin_level': result_bin_level['value'],
                'air_quality': result_air_quality['value'],
                'frequency': result_vacuum['frequency'],
                'power': result_vacuum['power']
            }
            }), 200
        else:
            result_mop = db.execute(
            """SELECT *
                FROM mop_settings
                ORDER BY TIMESTAMP DESC
                LIMIT 1"""
            ).fetchone()
            return jsonify({
            'data': {
                'resource_level': result_resource_level['value'],
                'battery_level': result_battery_level['value'],
                'bin_level': result_bin_level['value'],
                'air_quality': result_air_quality['value'],
                'frequency': result_mop['frequency']
            }
            }), 200