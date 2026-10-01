import httpx
import pandas as pd
import os
import random

async def get_marine_condition(lat: float, long: float):
	"""Get current and forecasted sea condition (wave height, swell, sea temprature) for coastal location"""
	url = "https://marine-api.open-meteo.com/v1/marine"

	params = {
		"longitude": long,
		"latitude":lat,
		"hourly": "wave_height,wave_direction,wave_period,swell_wave_height,sea_surface_temperature",
		"forecast_days":3
	}

	async with httpx.AsyncClient() as client:
		response = await client.get(url=url, params=params)
		response.raise_for_status()
		data = response.json()

	return data


async def get_current_marine_condition(lat : float, long: float):

	data = await get_marine_condition(lat=lat, long=long)

	return {
		"wave_height" : data["hourly"]["wave_height"][0],
		"wave_direction" : data["hourly"]["wave_direction"][0],
		"sea_surface_temperature" : data["hourly"]["sea_surface_temperature"][0]
	}


def save_marine_data_excel(data : dict):
	"""Takes raw Open-Meteo JSON data and saves it as a readable Excel file with a random ID"""

	df = pd.DataFrame({
		"time" : data["hourly"]["time"],
		"wave_height_m" : data["hourly"]["wave_height"],
		"wave_direction_deg" : data["hourly"]["wave_direction"],
		"wave_period_s" : data["hourly"]["wave_period"],
		"swell_wave_height_m" : data["hourly"]["swell_wave_height"],
		"sea_surface_temperature_c": data["hourly"]["sea_surface_temperature"]
	})

	os.makedirs("marine_data",exist_ok=True)

	while True:
		file_id = random.randint(100000, 999999)
		file_path = f"marine_data/marine_data_{file_id}.xlsx"
		if not os.path.exists(file_path):
			break

	df.to_excel(file_path, index=False)
	print(f"File save : {file_path}")
	return file_path


import asyncio

if __name__ == "__main__":
	result = asyncio.run(get_marine_condition(9.9312, 76.2673)) #kochi
	save_marine_data_excel(result)