from app import create_app
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath
                (os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_create_amenity(client):
    res = client.post("/api/v1/amenities/", json={"name": "WiFi"})
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data


def test_get_amenities(client):
    res = client.get("/api/v1/amenities/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_get_amenity_not_found(client):
    res = client.get("/api/v1/amenities/invalid")
    assert res.status_code == 404
