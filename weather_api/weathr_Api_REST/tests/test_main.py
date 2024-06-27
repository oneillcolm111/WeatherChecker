import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_weather_entry(client):
    response = client.post("/weather/", json={"city": "New York", "day": "2022-01-01"})
    assert response.status_code == 201

def test_read_weather(client):
    response = client.get("/weather/2022-01-01")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0