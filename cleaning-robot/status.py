from db import get_db

def get_status():
    cleaning = get_db().execute(
        'SELECT id, timestamp, type, settings_v, settings_m'
        ' FROM cleaning'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if cleaning is None:
        return {'status': 'Please set a cleaning program'}

    return {
        'data': {
            "cleaning": "vacuuming" if cleaning['type'] == 0 else "mopping"
        }
    }
