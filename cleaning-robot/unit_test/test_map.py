import pytest
from client import client
from flask import jsonify
import json
import services.map_service as map_service
import random


map_name = "test"
random.seed(13)
new_map_name = map_name + str(random.randint(0, 100000))

def test_set_map(client):
    request = client.post("/map", data={"map_name": new_map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Created new mapping"
    assert response["data"]["id"] == new_map_name


def test_set_map_405(client):
    request = client.post("/map", data={"map_name": map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 405
    assert response["status"] == "The mapping already exists"


def test_get_map(client):
    request = client.get("/map", data={"map_name": map_name}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Got the map"