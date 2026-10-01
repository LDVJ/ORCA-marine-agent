import httpx
import asyncio
import pandas as pd
import random
import os

async def get_weather_data(lat : float, long : float):
    """Fetches raw weather forecast data from Open-Meteo. Internal use only — not given to Gemini directly."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : lat,
        "longitude" : long,
        "hourly" : "temperature_2m,wind_speed_10m,wind_direction_10m,precipitation,weather_code",
        "forecast_days" : 3
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url= url, params=params)
        response.raise_for_status()
        data = response.json()

    save_weather_data(data=data)
    return data

async def get_current_weather_data(lat: float, long : float):
    """Fetches the current weather forecast data from open-metro."""

    data = await get_weather_data(lat=lat, long=long)

    return {
        "temperature" : data["hourly"]["temperature_2m"][0],
        "wind_speed" : data["hourly"]["wind_speed_10m"][0],
        "wind_direction" : data["hourly"]["wind_direction_10m"][0],
        "precipitation" : data["hourly"]["precipitation"][0],
        "weather_code" : data["hourly"]["weather_code"][0],
    }

def save_weather_data(data : dict):
    """Takes weather raw weather data anndd saves in readable xlsx format"""

    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature":data["hourly"]["temperature_2m"],
        "wind_speed":data["hourly"]["wind_speed_10m"],
        "wind_direction":data["hourly"]["wind_direction_10m"],
        "precipitation":data["hourly"]["precipitation"],
        "weather_code":data["hourly"]["weather_code"],
    })

    os.makedirs("weather_data", exist_ok=True)

    while True:
        file_id  = random.randint(100000, 999999)
        file_path = f"weather_data/weather_data_{file_id}.xlsx"
        if not os.path.exists(file_path):
            break

    df.to_excel(file_path, index=False)
    print(f"file saved: {file_path}")

    return file_path
    

if __name__ == "__main__":
    data = asyncio.run(get_weather_data(9.9312, 76.2673))
    print(data)