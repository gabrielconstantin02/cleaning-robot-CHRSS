from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db
from services.map_service import *

bp = Blueprint('map', __name__)
bp_cells = Blueprint('map_cells', __name__)


@bp.route('/map', methods=['POST'])
@login_required
def set_map_api():
    # Generating a new map will imply to dynamically create a map by the robot going through the whole room
    db = get_db()
    database_script = ""
    map_name = request.form['map_name']
    check = get_db().execute(
        'SELECT *'
        ' FROM map'
        ' WHERE map_name=(?)',
        (map_name,)
    ).fetchone()

    if check is not None:
        return jsonify({
            'status': 'The mapping already exists'
        }), 405

    # mocking the map generation
    size = (32, 32)
    new_mapping, station_pos = generate_new_mapping(size)
    # creating the new mapping:
    map_connection = db.cursor()
    map_connection.execute(
        'INSERT INTO map (map_name, map_base_row, map_base_col, map_size_row, map_size_col)'
        ' VALUES (?, ?, ?, ?, ?)',
        (map_name, station_pos[0], station_pos[1], size[0], size[1])
    )
    map_id = map_connection.lastrowid

    for x_index, line in enumerate(new_mapping):
        for y_index, value in enumerate(line):
            database_script += f'INSERT INTO map_cells (map_id, row, col, value) VALUES ("{map_id}", {x_index}, {y_index}, {value});\n'

    # print(database_script)
    get_db().executescript(database_script)

    return jsonify({
        'status': 'Created new mapping',
        'data': {
            'id': map_name,
            'map_size_row': size[0],
            'map_size_col': size[1],
            'map': new_mapping
        }
    }), 200


@bp.route('/map', methods=['GET'])
@login_required
def get_map_api():
    return jsonify(get_map()), 200
