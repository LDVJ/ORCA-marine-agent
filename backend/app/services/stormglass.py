import httpx
from datetime import datetime, timezone, timedelta
from app.config import settings


async def get_tide_data(lat : float, lng : float):
    """Fetches raw tide extreme data from stormglass. Internal use  only"""

    url ='https://api.stormglass.io/v2/tide/extremes/point'

    now = datetime.now(timezone.utc)
    start = now.replace(hour=0,minute=0,second=0,microsecond=0)
    end = start + timedelta(days=1) 

    params = {
        "lat": lat,
        "lng" : lng,
        "start" : int(start.timestamp()),
        "end" :  int(end.timestamp())
    }

    headers = {
        "Authorization" : settings.STORMGLASS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()


    return data

def get_current_tide_summary(data : dict):
    """Extracts the next upcoming tide extreme from raw data. Internal use  only"""
    next_tide = data["data"][0]

    return {
        "type" : next_tide["type"],
        "height" : next_tide["height"],
        "time" : next_tide["time"]
    }

async def geT_tide_forecast(lat: float, lng : float):
    """Get upcoming tide information (next high/low tide time and height) for a coastal location"""
    raw_data = await get_tide_data(lat=lat, lng=lng)
    return get_current_tide_summary(raw_data)

import asyncio

if __name__ == "__main__":
    raw_data = asyncio.run(get_tide_data(9.9312, 76.2673))
    print(raw_data)