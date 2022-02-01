from db import get_db

def get_cleaning_history(type, date):
    result = get_db().execute(
        'SELECT *'
        ' FROM cleaning_history'
        ' WHERE type=(?) AND date=(?)',
        (type, date)
    ).fetchone()
    return {
        'data': {
            'id': result['id'],
            'timestamp': result['timestamp'],
            'type': result['type'],
            'date': result['date'],
            'elapsed_time': result['elapsed_time']
        }
    }
