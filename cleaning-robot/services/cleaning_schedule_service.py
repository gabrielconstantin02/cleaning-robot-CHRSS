from db import get_db


def get_cleaning_schedule(type, date):
    result = get_db().execute(
        'SELECT *'
        ' FROM cleaning_schedule'
        ' WHERE type=(?) AND date=(?)',
        (type, date)
    ).fetchone()
    return {
        'data': {
            'timestamp': result['timestamp'],
            'type': result['type'],
            'date': result['date'],
        }
    }
