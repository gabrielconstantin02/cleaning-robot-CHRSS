from unit_test.client import client
import controllers.environment_controller as environment
import json

bin_lvl = 10
bin_full = 100

def test_get_automatic(client):
    client.post("/bin_level", data={"bin_level": bin_lvl})

    request = client.get("/bin/", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())

    assert request.status_code == 200
    assert response["status"] == "Automatic empty not required. Bin is not full!"
    assert response["data"]["value"] == bin_lvl


# def test_get_automatic_full(client):
#     client.post("/bin_level", data={"bin_level": bin_full})
#
#     request = client.get("/bin/", data={}, follow_redirects=True)
#     response = json.loads(request.data.decode())
#
#     assert request.status_code == 200
#     assert response["status"] == "Finished automatic bin empty"
#     assert response["data"]["value"] == bin_full

