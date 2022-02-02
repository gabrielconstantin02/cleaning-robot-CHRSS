import pytest
from unit_test.client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.robot_service as robot_service

frequency = 1


def test_set_mop_settings(client):
    request = client.post("/mop_settings", data={"frequency": frequency}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == frequency
    assert response["status"] == "Mop setting successfully recorded"


def test_get_mop_settings(client):
    id = 1
    db_data = robot_service.get_mop_settings(id)
    request = client.get(f"/mop_settings?id={id}", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == db_data["data"]["frequency"]


def test_set_mop_settings_real(client):
    request = client.post("/mop_settings", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    air = air_service.get_air()['value']
    if air is None:
        air = air_service.get_air_realtime()

    assert request.status_code == 200
    assert response["data"]["frequency"] == air // 50 + 1
