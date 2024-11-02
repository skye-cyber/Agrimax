'''import requests
from .get_cordinates impor

class Weather:
    def __init__(self, loc):
        self.loc = loc

    def get_weather_open_meteo(latitude, longitude):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={
            latitude}&longitude={longitude}&current_weather=true"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['current_weather']
        else:
            return None

    def get_weekly_forecast(latitude, longitude):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={
            longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,sunrise,sunset&timezone=auto"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['daily']
        else:
            return None


# Example usage
latitude = 40.7128  # Latitude for New York City
longitude = -74.0060  # Longitude for New York City

forecast = get_weekly_forecast(latitude, longitude)

if forecast:
    for day in forecast['time']:
        index = forecast['time'].index(day)
        print(f"Date: {day}")
        print(f"Max Temperature: {forecast['temperature_2m_max'][index]}°C")
        print(f"Min Temperature: {forecast['temperature_2m_min'][index]}°C")
        print(f"Precipitation: {forecast['precipitation_sum'][index]} mm")
        print(f"Weather Code: {forecast['weathercode'][index]}")
        print(f"Sunrise: {forecast['sunrise'][index]}")
        print(f"Sunset: {forecast['sunset'][index]}")
        print("-" * 30)
else:
    print("Failed to retrieve weather data.")

# Example usage
latitude = 40.7128  # Latitude for New York City
longitude = -74.0060  # Longitude for New York City

weather = get_weather_open_meteo(latitude, longitude)

if weather:
    print(f"Current temperature: {weather['temperature']}°C")
    print(f"Wind speed: {weather['windspeed']} km/h")
else:
    print("Failed to retrieve weather data.")'''

print(f'2024-10-{str(1).zfill(8)}')
