import random
from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('map', __name__)


@bp.route('/map', methods=['POST'])
@login_required
def set_map():
    # Generating a new map will imply to dynamically create a map by the robot going through the whole room
    database_script = ""
    map_name = request.form['map_name']
    check = get_db().execute(
        'SELECT *'
        ' FROM map'
    ).fetchone()

    if check is not None:
        return jsonify({
            'status': 'An mapping already exists, delete it first'
        }), 404

    new_mapping = generate_new_mapping()
    for x_index, line in enumerate(new_mapping):
        for y_index, value in enumerate(line):
            database_script += f'INSERT INTO map (map_name, row, col, value) VALUES ("{map_name}", {x_index}, {y_index}, {value});\n'

    print(database_script)
    get_db().executescript(database_script)

    return jsonify({
        'status': 'Created new mapping',
        'data': {
            'id': map_name,
            'map': new_mapping
        }
    }), 200


@bp.route('/map', methods=['POST'])
@login_required
def get_map():
    pass


def generate_new_mapping():
    # This should be an algorithm for the robot to go around and generate a mapping
    map_size = 32
    random.seed(69)
    obstacle_numbers = 2
    obstacle_size = (2, 2)
    wall_size = 2
    mapping = [[0 for _ in range(map_size)] for _ in range(map_size)]
    ends = [0, 1, 30, 31]
    for i in ends:
        for j in range(map_size):
            mapping[i][j] = 1
    for i in range(wall_size, map_size - wall_size):
        for j in ends:
            mapping[i][j] = 1
    for obstacle in range(obstacle_numbers):
        obstacle_x = random.randint(wall_size, map_size - wall_size - obstacle_size[0])
        obstacle_y = random.randint(wall_size, map_size - wall_size - obstacle_size[1])
        for x in range(obstacle_size[0]):
            for y in range(obstacle_size[1]):
                mapping[obstacle_x + x][obstacle_y + y] = 1

    return mapping
