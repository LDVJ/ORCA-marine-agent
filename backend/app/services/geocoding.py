import httpx
import asyncio

async def geocode_location(place_name : str):
    """convert a place name into latitude and longitude"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name" : place_name,
        "count" : 1,
        "format" : "json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"No Location found with the location name = {place_name}")

    result : dict = data["results"][0]

    return {
        "latitude" : result["latitude"],
        "longitude" : result["longitude"],
        "name" : result["name"],
        "country" : result.get("country")
    }


if __name__ == "__main__":
    result = asyncio.run(geocode_location("mumbai"))
    print(result)