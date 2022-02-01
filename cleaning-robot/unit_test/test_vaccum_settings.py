import pytest
from client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.robot_service as robot_service


frequency = 5
power = 5


def test_set_vaccuming_settings(client):
    request = client.post("/vacuum_settings", data={"frequency": frequency, "power": power}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == frequency
    assert response["data"]["power"] == power
    assert response["status"] == "Vacuum setting successfully recorded"


def test_get_vaccuming_settings(client):
    id = 1
    db_data = robot_service.get_vacuum_settings(id)
    request = client.get("/vacuum_settings", data={"id": 1}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == db_data["data"]["frequency"]
    assert response["data"]["power"] == db_data["data"]["power"]


# def test_set_vaccuming_settings_real(client):
#     request = client.post("/vacuum_settings", data={"frequency": "", "power": ""}, follow_redirects=True)
#     response = json.loads(request.data.decode())
#
#     air = air_service.get_air()[2]
#     if air is None:
#         air = air_service.get_air_realtime()
#
#     assert response["data"]["frequency"] == air // 50 + 1
#     assert response["data"]["power"] == (air // 50 + 1) * 100



