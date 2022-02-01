import pytest
from unit_test.client import client
from flask import jsonify
import json
import services.air_service as air_service
import services.cleaning_history_service as cleaning_history_service

type = 0
date = '01-02-2022'


def test_get_cleaning_history(client):
    request = client.get("/cleaning_history", data={"type": type, "date": date}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["data"]["type"] == type
    assert response["data"]["date"] == date