from fastapi import FastAPI
import pytest
from main import app
from fastapi.testclient import TestClient

app = FastAPI()
client = TestClient(app)

def test_create_weather_entry():
    response = client.post("/weather/", json={"city": "london", "day": "2022-01-01"})
    assert response.status_code == 201

def test_read_weather():
    response = client.get("/weather/2022-01-01")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0