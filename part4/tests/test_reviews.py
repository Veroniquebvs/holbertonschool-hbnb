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
    email = f"reviewer_{int(time.time()*1000)}@test.com"
    res = client.post("/api/v1/users/", json={
        "first_name": "Reviewer",
        "last_name": "Test",
        "email": email,
        "password": "1234"
    })
    data = res.get_json()
    assert "id" in data
    return data["id"]


@pytest.fixture
def place_id(client, user_id):
    amenity_res = client.post("/api/v1/amenities/", json={"name": "WiFi"})
    amenity_id = amenity_res.get_json()["id"]
    res = client.post("/api/v1/places/", json={
        "title": "My Place",
        "description": "Nice",
        "price": 100,
        "latitude": 48.85,
        "longitude": 2.35,
        "owner_id": user_id,
        "amenities": [amenity_id]
    })
    data = res.get_json()
    assert "id" in data
    return data["id"]


def test_create_review(client, user_id, place_id):
    res = client.post("/api/v1/reviews/", json={
        "text": "Excellent!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data


def test_get_review_not_found(client):
    res = client.get("/api/v1/reviews/invalid")
    assert res.status_code == 404


def test_update_and_delete_review(client, user_id, place_id):
    res = client.post("/api/v1/reviews/", json={
        "text": "Good",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = res.get_json()["id"]

    # Update
    res = client.put(f"/api/v1/reviews/{review_id}", json={
        "text": "Updated",
        "rating": 3,
        "user_id": user_id,
        "place_id": place_id
    })
    assert res.status_code == 200
    assert res.get_json()["rating"] == 3

    # Delete
    res = client.delete(f"/api/v1/reviews/{review_id}")
    assert res.status_code == 200
