import random
from db import get_db

def get_map():
    map_db = get_db().execute(
        'SELECT *'
        ' FROM map'
        ' ORDER BY map_id DESC'
    ).fetchone()

    map_cells_db = get_db().cursor().execute(
        'SELECT *'
        ' FROM map_cells'
        ' WHERE map_id=(?)',
        (map_db['map_id'],)
    )

    size = (map_db['map_size_row'], map_db['map_size_col'])
    mapping = convert_map_from_sql(map_cells_db, size)

    return {
        'status': 'Created new mapping',
        'data': {
            'id': map_db['map_name'],
            'map_size_row': size[0],
            'map_size_col': size[1],
            'map': mapping
        }
    }


def convert_map_from_sql(cursor, size):
    mapping = [[0 for _ in range(size[1])] for _ in range(size[0])]
    for cell in cursor:
        row = cell['row']
        col = cell['col']
        mapping[row][col] = cell['value']
    return mapping


def generate_new_mapping(map_size):
    # This should be an algorithm for the robot to go around and generate a mapping
    random.seed(69)
    station_pos = None
    obstacle_numbers = 2
    obstacle_size = (2, 2)
    wall_size = 2
    mapping = [[0 for _ in range(map_size[1])] for _ in range(map_size[0])]
    ends = [0, 1, 30, 31]
    for i in ends:
        for j in range(map_size[1]):
            mapping[i][j] = 1
    for i in range(wall_size, map_size[0] - wall_size):
        for j in ends:
            mapping[i][j] = 1
    for obstacle in range(obstacle_numbers):
        obstacle_x = random.randint(wall_size, map_size[0] - wall_size - obstacle_size[0])
        obstacle_y = random.randint(wall_size, map_size[1] - wall_size - obstacle_size[1])
        for x in range(obstacle_size[0]):
            for y in range(obstacle_size[1]):
                mapping[obstacle_x + x][obstacle_y + y] = 1

    for i in range(map_size[0]):
        if station_pos is None:
            for j in range(map_size[1]):
                if mapping[i][j] != 1:
                    station_pos = (i, j)
                    mapping[i][j] = 2
                    break
    return mapping, station_pos
