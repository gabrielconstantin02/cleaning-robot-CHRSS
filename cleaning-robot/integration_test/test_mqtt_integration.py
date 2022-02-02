from flask_socketio import SocketIO

import pytest
import json
import status
from app import create_app, create_mqtt_app
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
)

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