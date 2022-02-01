from db import get_db

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
