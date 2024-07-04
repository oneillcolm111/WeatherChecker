from fastapi import FastAPI
import pytest
from main import app
from fastapi.testclient import TestClient
import requests
import sqlite3

app = FastAPI()
client = TestClient(app)

@pytest.fixture()

def test_data():
    return {"city": "london", "date": "2024-06-01"}

def test_create_weather_entry2(test_data):
    response = client.post("/weather/", json=test_data)
    assert response.status_code == 201
    assert response.json()["city"] == test_data["city"]
    assert response.json()["date"] == test_data["date"]

def test_read_weather2(test_data):
    response = client.post("/weather/", json=test_data)
    response = client.get(f"/weather/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json()["city"] == test_data["city"]
    assert response.json()["date"] == test_data["date"]

def test_read_non_existent_weather2():
    response = client.get("/weather/2022-01-01")
    assert response.status_code == 404

def test_invalid_date2():
    response = client.post("/weather/", json={"city": "london", "day": " invalid date"})
    assert response.status_code == 422

def test_create_weather_entry(test_data):
    response = client.post("/weather/", json=test_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Weather data stored successfully"
    try:
        # Fetch weather data from OpenWeatherMap API
        response = requests.get(F"http://api.openweathermap.org/data/2.5/weather?q={test_data['city']}&appid=38b75ff97a0a3045b462ffd7a77f9794")
        weather_data = response.json()
        
        # Store the data in the database
        conn = sqlite3.connect("weather.db")
        c = conn.cursor()
        c.execute("""
            SELECT * FROM weather WHERE city=? AND date=?
        """, (test_data["city"], test_data["date"]))
        stored_data = c.fetchall()
        conn.close()
        
        assert len(stored_data) == 1
        assert stored_data[0][1] == test_data["date"]
    except Exception as e:
        assert False

def test_read_weather(test_data):
    try:
        response = client.post("/weather/", json=test_data)
        response = client.get(f"/weather/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["city"] == test_data["city"]
        assert response.json()["date"] == test_data["date"]
    except Exception as e:
        assert False

def test_read_weather_with_valid_date(test_data):
    response = client.post("/weather/", json=test_data)
    try:
        response = client.get(f"/weather/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["city"] == test_data["city"]
        assert response.json()["date"] == test_data["date"]
    except Exception as e:
        assert False

def test_read_non_existent_weather():
    try:
        response = client.get("/weather/2022-01-01")
        assert response.status_code == 404
    except Exception as e:
        assert False

def test_invalid_date():
    try:
        response = client.post("/weather/", json={"city": "london", "day": " invalid date"})
        assert response.status_code == 422
    except Exception as e:
        assert False