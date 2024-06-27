from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional
import requests
import sqlite3

app = FastAPI()

# Define a function to store weather data in the database
async def store_weather(city: str, day: str) -> JSONResponse:
    try:
        # Fetch weather data from OpenWeatherMap API
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=38b75ff97a0a3045b462ffd7a77f9794")
        weather_data = response.json()
        
        # Store the data in the database
        conn = sqlite3.connect("weather.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO weather (city, date, min_temp, max_temp, avg_temp, humidity)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (city, day, weather_data["main"]["temp_min"], weather_data["main"]["temp_max"], weather_data["main"]["temp"], weather_data["main"]["humidity"]))
        conn.commit()
        conn.close()
        
        return JSONResponse(content={"message": "Weather data stored successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a function to retrieve weather data from the database
async def get_weather(day: str) -> JSONResponse:
    try:
        # Retrieve data from database
        conn = sqlite3.connect("weather.db")
        c = conn.cursor()
        c.execute("SELECT * FROM weather WHERE date=?", (day,))
        weather_data = c.fetchall()
        conn.close()
        
        if not weather_data:
            raise HTTPException(status_code=404, detail="No data found for the given day")
        
        # Convert rows to dictionaries
        weather_data = [{column_name: row[i] for i, column_name in enumerate(c.description)} for row in weather_data]
        
        return JSONResponse(content={"data": weather_data}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weather/")
async def create_weather_entry(city: str, day: str):
    return await store_weather(city, day)

@app.get("/weather/{day}")
async def read_weather(day: str):
    return await get_weather(day)