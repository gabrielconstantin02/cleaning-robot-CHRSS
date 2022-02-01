import pytest
from client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.cleaning_service as cleaning_service

type = 0
settings_v = 5
settings_m = 5

def test_set_cleaning(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": settings_v, "settings_m": settings_m}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Cleaning successfully recorded/retrieved"
    assert response["data"]["type"] == type
    assert response["data"]["cleaning_v"] == settings_v
    assert response["data"]["cleaning_m"] == settings_m


def test_set_cleaning_403_type(client):
    request = client.post("/cleaning", data={"type": "", "settings_v": "", "settings_m": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Type is required."


def test_set_cleaning_403_vacuuming(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": "", "settings_m": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Vacuuming settings are required."


def test_set_cleaning_403_type(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": settings_v, "settings_m": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Mop settings are required."


def test_get_vacuuming(client):
    request = client.get("/vacuuming", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Finished vacuuming"


def test_get_mopping(client):
    request = client.get("/mopping", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Finished mopping"
