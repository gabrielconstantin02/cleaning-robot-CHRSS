import random
from db import get_db
random.seed(42)


def get_dirt_level():
    # This mocks the sensor of dirt detection
    dirt_level = random.random() / 3
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


def get_resource_level():
    current_resource_level = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM resource_level'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    return {
        'status': 'Successfully got resource level',
        'data': {
            'id': current_resource_level['id'],
            'timestamp': current_resource_level['timestamp'],
            'value': current_resource_level['value'],
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

def get_cleaning_settings(type):
    cleaning_settings = get_db().execute(
        'SELECT settings_v, settings_m'
        ' FROM cleaning'
        ' WHERE type=(?)'
        ' ORDER BY timestamp DESC',
        (type,)
    ).fetchone()
    if type == 0:
        return get_vacuum_settings(cleaning_settings['settings_v'])
    else:
        return get_mop_settings(cleaning_settings['settings_m'])


def get_vacuum_settings(id):
    result = get_db().execute(
        'SELECT *'
        ' FROM vacuum_settings'
        ' WHERE id=(?)',
        (id,)
    ).fetchone()
    return {
        'data': {
            'id': result['id'],
            'timestamp': result['timestamp'],
            'frequency': result['frequency'],
            'power': result['power'],
        }
    }


def get_mop_settings(id):
    result = get_db().execute(
        'SELECT *'
        ' FROM mop_settings'
        ' WHERE id=(?)',
        (id, )
    ).fetchone()
    return {
        'data': {
            'id': result['id'],
            'timestamp': result['timestamp'],
            'frequency': result['frequency']
        }
    }
