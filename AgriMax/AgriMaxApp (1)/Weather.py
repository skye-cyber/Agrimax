import json
import os
import time

import requests
from datetim import datetime
from django.conf import settings
from get_coordinates import get_latitude_longitude


class Weather:
    def __init__(self, loc):
        self.loc = loc
        try:
            self.lat, self.lon = get_latitude_longitude(self.loc)
        except requests.ReadTimeout:
            pass

    def get_daily_forecast(self):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={
            self.lat}&longitude={self.lon}&current_weather=true"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            with open("test.json", 'w'):
                json.dump(data, indent=4)
            return data['current_weather']
        else:
            return None

    def get_weekly_forecast(self):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={
            self.lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,sunrise,sunset&timezone=auto"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            with open("test.json", 'w') as fp:
                json.dump(data, fp, indent=4)
            return data['daily']
        else:
            return None

    def get_weather_description(self, weather_code):
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Freezing fog",
            51: "Drizzle (light)",
            53: "Drizzle (moderate)",
            55: "Drizzle (heavy)",
            61: "Rain (light)",
            63: "Rain (moderate)",
            65: "Rain (heavy)",
            71: "Snow (light)",
            73: "Snow (moderate)",
            75: "Snow (heavy)",
            80: "Rain showers (light)",
            81: "Rain showers (moderate)",
            82: "Rain showers (heavy)",
            85: "Snow showers (light)",
            86: "Snow showers (heavy)",
            95: "Thunderstorm (light)",
            96: "Thunderstorm with hail (light)",
            99: "Thunderstorm (heavy)",
        }

        return weather_codes.get(weather_code, "Unknown weather code")

    def _3hrs_forecast(self):
        api_key = 'd1fce76f166b700e091ab7848af756db'

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        weather_root = settings.MEDIA_ROOT

        filename = f"weather/weather_data_{current_time}.json"

        # if os.path.exists(filename)

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={
            self.lat}&lon={self.lon}&appid={api_key}'

        response = requests.get(url, timeout=None)
        if response.status_code == 200:
            weather_data = response.json()

            json_file = os.path.join(weather_root, filename)

            with open(json_file, 'w') as json_file:
                json.dump(weather_data, json_file, indent=4)

            print(f"Data saved to {filename}")

            return weather_data
        else:
            return None


def entry_7_retry(loc, max_attempts=5):
    attempts = 0
    forecast = None

    while not forecast and attempts < max_attempts:
        init = Weather(loc)
        forecast = init.get_weekly_forecast()
        attempts += 1

        if not forecast:
            print("Failed to retrieve forecast, retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying

    if forecast:
        return forecast
    else:
        print("Max attempts reached. Unable to retrieve forecast.")
        return None


forecast = entry_retry("Nairobi")
init = Weather("jhh")

if forecast:
    for day in forecast['time']:
        index = forecast['time'].index(day)
        desc = init.get_weather_description(forecast['weathercode'][index])
        print(f"Date: {day}")
        print(f"Max Temperature: {forecast['temperature_2m_max'][index]}°C")
        print(f"Min Temperature: {forecast['temperature_2m_min'][index]}°C")
        print(f"Precipitation: {forecast['precipitation_sum'][index]} mm")
        print(f"Weather Code: {forecast['weathercode'][index]} {desc}")
        print(f"Sunrise: {forecast['sunrise'][index]}")
        print(f"Sunset: {forecast['sunset'][index]}")
        print("-" * 30)
else:
    print("Failed to retrieve weather data.")
