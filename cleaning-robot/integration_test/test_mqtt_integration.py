import pytest
from numpy import random
import status
from app import create_app, create_mqtt_app
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
)
from integration_test.client import client
import json
import services.air_service as air_service
from services import robot_service

type = 0
settings_v = 5
settings_m = 5
bin_lvl = 10
bin_full = 100
map_name = "test"
new_map_name = map_name + str(random.random() * 10000 // 10)
frequency = 1
power = 20

app = None
mqtt = None
socketio = None


@pytest.fixture
def client_mqtt():
    app = create_app()
    mqtt = create_mqtt_app()
    with app.test_client():
        with app.app_context():
            yield mqtt


@pytest.mark.integrationTest
def test_mqtt_status_publishing(client_mqtt):
    message = json.dumps(status.get_status(), default=str)
    print(message)
    res, mid = client_mqtt.publish('cleaning-robot', message)
    assert res == MQTT_ERR_SUCCESS


@pytest.mark.integrationTest
def test_set_map(client):
    request = client.post("/map", data={"map_name": new_map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Created new mapping"
    assert response["data"]["id"] == new_map_name


@pytest.mark.integrationTest
def test_set_map_405(client):
    request = client.post("/map", data={"map_name": map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 405
    assert response["status"] == "The mapping already exists"


@pytest.mark.integrationTest
def test_get_map(client):
    request = client.get("/map", data={"map_name": map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Got the map"


@pytest.mark.integrationTest
def test_set_cleaning(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": settings_v, "settings_m": settings_m},
                          follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Cleaning successfully recorded/retrieved"
    assert response["data"]["type"] == type
    assert response["data"]["cleaning_v"] == settings_v
    assert response["data"]["cleaning_m"] == settings_m


@pytest.mark.integrationTest
def test_get_automatic(client):
    client.post("/bin_level", data={"bin_level": bin_lvl})

    request = client.get("/bin/", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Automatic empty not required. Bin is not full!"
    assert response["data"]["value"] == bin_lvl


@pytest.mark.integrationTest
def test_set_cleaning_403_type(client):
    request = client.post("/cleaning", data={"type": "", "settings_v": "", "settings_m": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Type is required."


@pytest.mark.integrationTest
def test_set_cleaning_403_vacuuming(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": "", "settings_m": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Vacuuming settings are required."


@pytest.mark.integrationTest
def test_set_air_400(client):
    request = client.post('/air', data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 400
    assert response["status"] == "Air quality is required."


@pytest.mark.integrationTest
def test_set_vaccuming_settings(client):
    request = client.post("/vacuum_settings", data={"frequency": frequency, "power": power}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == frequency
    assert response["data"]["power"] == power
    assert response["status"] == "Vacuum setting successfully recorded"


@pytest.mark.integrationTest
def test_get_vaccuming_settings(client):
    id = 1
    db_data = robot_service.get_vacuum_settings(id)
    request = client.get("/vacuum_settings?id=1", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert response["data"]["frequency"] == db_data["data"]["frequency"]
    assert response["data"]["power"] == db_data["data"]["power"]


@pytest.mark.integrationTest
def test_set_vaccuming_settings_real(client):
    request = client.post("/vacuum_settings", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    air = air_service.get_air()["value"]
    if air is None:
        air = air_service.get_air_realtime()

    assert response["data"]["frequency"] == air // 50 + 1
    assert response["data"]["power"] == (air // 50 + 1) * 20


@pytest.mark.integrationTest
def test_get_air_real(client):
    request = client.get("/air/real", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    real_data = air_service.get_air()[2]
    if real_data is None:
        real_data = air_service.get_air_realtime()

    assert request.status_code == 200
    assert response["status"] == "Realtime air quality successfully retrieved."
    assert response["data"]["air_quality"] == real_data


@pytest.mark.integrationTest
def test_set_cleaning_403_type(client):
    request = client.post("/cleaning", data={"type": type, "settings_v": settings_v, "settings_m": ""},
                          follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Mop settings are required."


@pytest.mark.integrationTest
def test_get_vacuuming(client):
    request = client.get("/vacuuming", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Finished vacuuming"


@pytest.mark.integrationTest
def test_get_mopping(client):
    request = client.get("/mopping", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Finished mopping"
