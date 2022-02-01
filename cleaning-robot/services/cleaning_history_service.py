from db import get_db
import datetime

def get_cleaning_history(type, date):
    result = get_db().execute(
        ' SELECT *'
        ' FROM cleaning_history'
        ' WHERE type=(?) AND strftime("%d-%m-%Y", date)=(?)',
        (type, date)
    ).fetchone()
    return {
        'data': {
            'id': result['id'],
            'timestamp': result['timestamp'],
            'type': result['type'],
            'date': result['date'].strftime("%d-%m-%Y"),
            'elapsed_time': result['elapsed_time']
        }
    }

def insert_cleaning_history(type, elapsed_time):
    db = get_db()
    date = datetime.datetime.now()
    print(date)
    db.execute("""INSERT INTO cleaning_history (elapsed_time, type, date)
                      VALUES (?, ?, ?)""",
               (elapsed_time, type, date))
    db.commit()