import pytest
from client import client
from flask import jsonify
import json
import services.air_service as air_service

air_quality = 10


def test_set_air(client):
    request = client.post("/air", data={"air_quality": air_quality}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Air quality successfully recorded."
    assert response["data"]["air_quality"] == air_quality


def test_set_air_400(client):
    request = client.post('/air', data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 400
    assert response["status"] == "Air quality is required."


def test_get_air(client):
    request = client.get('/air', data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["air_quality"] == air_quality


def test_get_air_real(client):
    request = client.get("/air/real", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    real_data = air_service.get_air()[2]
    if real_data is None:
        real_data = air_service.get_air_realtime()

    assert request.status_code == 200
    assert response["status"] == "Realtime air quality successfully retrieved."
    assert response["data"]["air_quality"] == real_data
