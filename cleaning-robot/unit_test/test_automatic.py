from unit_test.client import client
import json

bin_lvl = 10
bin_full = 100

def test_get_automatic(client):
    request = client.get("/bin", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    environment.set_bin_level(bin_lvl)

    assert request.status_code == 200
    assert response["status"] == "Automatic empty not required. Bin is not full!"
    assert response["data"]["value"] == bin_lvl


def test_get_automatic_full(client):
    request = client.get("/bin", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    environment.set_bin_level(bin_full)

    assert request.status_code == 200
    assert response["status"] == "Finished automatic bin empty"
    assert response["data"]["value"] == bin_full

