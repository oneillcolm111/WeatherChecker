from fastapi import FastAPI
import pytest
from main import app
from fastapi.testclient import TestClient

app = FastAPI()
client = TestClient(app)

@pytest.fixture()
def test_data():
    return {"city": "london", "date": "2024-06-01"}

def test_create_weather_entry(test_data):
    response = client.post("/weather/", json=test_data)
    assert response.status_code == 201
    assert response.json()["city"] == test_data["city"]
    assert response.json()["date"] == test_data["date"]

def test_read_weather(test_data):
    response = client.post("/weather/", json=test_data)
    response = client.get(f"/weather/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json()["city"] == test_data["city"]
    assert response.json()["date"] == test_data["date"]

def test_read_non_existent_weather():
    response = client.get("/weather/2022-01-01")
    assert response.status_code == 404

def test_invalid_date():
    response = client.post("/weather/", json={"city": "london", "day": " invalid date"})
    assert response.status_code == 422