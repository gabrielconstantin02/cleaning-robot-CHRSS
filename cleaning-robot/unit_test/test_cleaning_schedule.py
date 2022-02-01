import pytest
from client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.cleaning_schedule_service as cleaning_schedule_service
import random

random.seed(13)

type = random.randint(0, 100000)
date = '2022-02-01 15:59:46'

def test_set_cleaning_schedule(client):
    request = client.post("/cleaning_schedule", data={"type": type, "date": date}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Cleaning schedule successfully recorded"
    assert response["data"]["type"] == type
    assert response["data"]["date"] == 'Tue, 01 Feb 2022 21:59:46 GMT'


def test_set_cleaning_schedule_403_type(client):
    request = client.post("/cleaning_schedule", data={"type": "", "date": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Type is required."


def test_set_cleaning_schedule_403_date(client):
    request = client.post("/cleaning_schedule", data={"type": type, "date": ""}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 403
    assert response["status"] == "Date is required."


def test_get_cleaning_schedule(client):
    request = client.get("/cleaning_schedule", data={"type": type, "date": date}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response == date