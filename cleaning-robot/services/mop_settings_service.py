from db import get_db

def get_mop_settings(ip):
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
