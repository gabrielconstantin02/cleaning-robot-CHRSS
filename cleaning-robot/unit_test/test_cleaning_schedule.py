import pytest
from unit_test.client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.cleaning_schedule_service as cleaning_schedule_service
from numpy import random

type = 0
hours = str(random.randint(10,23)) + ":" + str(random.randint(10,59)) + ":" + str(random.randint(10,59))
date = '2022-02-01 ' + hours

def test_set_cleaning_schedule(client):
    request = client.post("/cleaning_schedule", data={"type": type, "date": date}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Cleaning schedule successfully recorded"
    assert response["data"]["type"] == type
    assert response["data"]["date"] == 'Tue, 01 Feb 2022 ' + hours + ' GMT'


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
    request = client.get(f"/cleaning_schedule?type={type}&date={date}", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["data"]["date"] == 'Tue, 01 Feb 2022 ' + hours + ' GMT'
