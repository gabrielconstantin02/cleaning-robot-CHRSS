from flask import (
    Blueprint, request, jsonify
)
from db import get_db
import requests


def set_air(air_quality):
    db = get_db()
    db.execute("""INSERT INTO air_quality (value)
                  VALUES (?)""",
               (air_quality,))
    db.commit()


def get_air_realtime():
    api_key = "5886b8db8457d6883ef994cfd77a4779"
    api_url = "http://api.openweathermap.org/data/2.5/air_pollution?lat=44&lon=26&appid=" + api_key
    response = requests.get(api_url)
    air_quality = response.json()["list"][0]["components"]["pm10"]
    air_quality = float("{:.2f}".format(air_quality))
    return air_quality


def set_air_realtime():
    set_air(get_air_realtime())


def get_air():
    db = get_db()
    air_quality =  db.execute("""SELECT *
                                        FROM air_quality
                                        ORDER BY TIMESTAMP DESC
                                        LIMIT 1"""
                ).fetchone()
    return air_quality
