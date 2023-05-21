import pytest


def test_hello_world(client):
    response = client.get("/api/hello/", {}, format="json")

    assert response.status_code == 200
    assert response.json()["message"] == "Hello World!"
