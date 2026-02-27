from app import create_app
import pytest
import time
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


@pytest.fixture
def user_id(client):
    email = f"owner_{int(time.time()*1000)}@test.com"
    res = client.post("/api/v1/users/", json={
        "first_name": "Owner",
        "last_name": "Test",
        "email": email,
        "password": "1234"
    })
    data = res.get_json()
    assert "id" in data
    return data["id"]


@pytest.fixture
def amenity_id(client):
    res = client.post("/api/v1/amenities/", json={"name": "WiFi"})
    data = res.get_json()
    assert "id" in data
    return data["id"]


def test_create_place(client, user_id, amenity_id):
    res = client.post("/api/v1/places/", json={
        "title": "My Apartment",
        "description": "Nice place",
        "price": 100,
        "latitude": 48.85,
        "longitude": 2.35,
        "owner_id": user_id,
        "amenities": [amenity_id]
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data


def test_get_places(client):
    res = client.get("/api/v1/places/")
    assert res.status_code == 200


def test_get_place_not_found(client):
    res = client.get("/api/v1/places/invalid")
    assert res.status_code == 404
