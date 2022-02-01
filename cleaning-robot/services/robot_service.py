import random
from db import get_db


def get_dirt_level():
    # This mocks the sensor of dirt detection
    dirt_level = random.random()
    return dirt_level


def get_battery_level():
    current_battery_level = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM battery_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    return {
        'status': 'Successfully got battery level',
        'data': {
            'id': current_battery_level['id'],
            'timestamp': current_battery_level['timestamp'],
            'value': current_battery_level['value'],
        }
    }


def get_bin_level():
    bin_level = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM bin_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if bin_level is None:
        return {
            'status': 'No bin level record found',
            'data': None
        }

    return {
        'status': 'Successfully got bin level',
        'data': {
            'id': bin_level['id'],
            'timestamp': bin_level['timestamp'],
            'value': bin_level['value'],
        }
    }
