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


def test_create_user(client):
    email = f"user_{int(time.time()*1000)}@test.com"
    res = client.post("/api/v1/users/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": email,
        "password": "1234"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data


def test_get_users(client):
    res = client.get("/api/v1/users/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/invalid-id")
    assert res.status_code == 404
