import configparser
import json
import os
from datetime import datetime
import platform

# import time
from pathlib import Path

import requests

# from django.conf import settings
from .get_coordinates import get_latitude_longitude

# Create a configuration object
config = configparser.ConfigParser()


class Weather:
    def __init__(self, loc):
        def getCOORD():
            try:
                self.lat, self.lon = get_latitude_longitude(self.loc)
                if self.lat and self.lon:
                    # Add a new section and set latitude and longitude
                    section_name = f"{self.loc.lower()}coord"
                    config[section_name] = {
                        "lat": str(self.lat),
                        "lon": str(self.lon),
                    }

                directory = os.path.dirname(cfname)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                if not os.path.exists(cfname):
                    open(cfname, "a").close()

                # ...

                with open(cfname, "a") as config_file:
                    config.write(config_file)

            except requests.ReadTimeout:
                print("Coordinates Read Timeout")

        self.loc = loc
        cfname = (
            "weather\\coordCache.cfg"
            if platform.system().lower() == "windows"
            else "weather/coordCache.cfg"
        )
        coord_cache = Path(__file__).parent / cfname
        if os.path.exists(coord_cache):
            try:
                config.read(coord_cache)
                self.lat = config.get(f"{self.loc.lower()}coord", "lat")
                self.lon = config.get(f"{self.loc.lower()}coord", "lon")
            except configparser.NoSectionError:
                getCOORD()
        else:
            getCOORD()

    def get_daily_forecast(self):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={
            self.lat}&longitude={self.lon}&current_weather=true"

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return "ConnectionError"
        except Exception as e:
            print(e)
            return "RequestFailure"

        if response.status_code == 200:
            data = response.json()
            with open("test.json", "w"):
                json.dump(data, indent=4)
            return data["current_weather"]
        else:
            return None

    def get_weekly_forecast(self, cache_file):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={
            self.lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,sunrise,sunset&timezone=auto"

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return "ConnectionError"
        except Exception as e:
            print(e)
            return "RequestFailure"

        if response.status_code == 200:
            data = response.json()
            if not os.path.exists(os.path.dirname(cache_file)):
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            if not os.path.isfile(cache_file):
                parent_dir = os.path.dirname(cache_file)
                if not os.access(parent_dir, os.W_OK):  # Check access permission
                    raise PermissionError(
                        f"Cannot write to the parent directory '{parent_dir}'"
                    )
            try:
                with open(str(cache_file), "w") as fp:
                    json.dump(data, fp, indent=4)
            except Exception as e:
                print(f"Error saving to cache file '{cache_file}'. {e}")
            return data
        else:
            return None

    @staticmethod
    def get_weather_description(weather_code):
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

    def _3hrs_forecast(self, path):
        api_key = "d1fce76f166b700e091ab7848af756db"

        # weather_root = settings.MEDIA_ROOT

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={
            self.lat}&lon={self.lon}&appid={api_key}"

        try:
            response = requests.get(url, timeout=None)
        except requests.exceptions.ConnectionError:
            return "ConnectionError"
        except Exception as e:
            print(e)
            return "RequestFailure"

        if response.status_code == 200:
            weather_data = response.json()

            # json_file = os.path.join(weather_root, filename)

            with open(path, "w") as json_file:
                json.dump(weather_data, json_file, indent=4)

            print(f"Data saved to {path}")

            return weather_data
        else:
            return None


def main(loc, _type: str = "daily7", max_attempts: bool = 5):
    date = datetime.now().strftime("%Y-%m-%d")
    if _type == "daily7":
        filename = f"weather/weekly_{loc.lower()}_{date}.json"
        cache_file = os.path.join(Path(__file__).parent, filename)
        if os.path.exists(cache_file):
            print(f"Loading data from daily7 file {cache_file}")
            with open(cache_file, "r") as file:
                return json.load(file)

        else:
            init = Weather(loc)
            forecast = init.get_weekly_forecast(cache_file)

    elif _type == "hourly3":
        filename = f"weather/horly3_{loc.lower()}_{date}.json"
        cache_file = os.path.join(Path(__file__).parent, filename)
        if os.path.exists(cache_file):
            print(f"Loading data from horly3 file {cache_file}")
            with open(cache_file, "r") as json_file:
                return json.load(json_file)
        else:
            init = Weather(loc)
            forecast = init._3hrs_forecast(cache_file)

    if forecast:
        return forecast
    else:
        print("Unable to retrieve forecast.")
        return None


if __name__ == "__main__":
    url = "https://api.open-meteo.com/v1/forecast?latitude=-23.625&longitude=-46.875&current_weather=true"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        print("*" * 100)
        with open("test.json", "w") as fl:
            json.dump(data, fl, indent=4)
        print(data["current_weather"])

    """forecast = main("Nairobi")
    forecast = forecast['daily']
    if forecast:
        for day in forecast['time']:
            index = forecast['time'].index(day)
            desc = Weather.get_weather_description(forecast['weathercode'][index])
            print(f"Date: {day}")
            print(f"Max Temperature: {forecast['temperature_2m_max'][index]}°C")
            print(f"Min Temperature: {forecast['temperature_2m_min'][index]}°C")
            print(f"Precipitation: {forecast['precipitation_sum'][index]} mm")
            print(f"Weather Code: {forecast['weathercode'][index]} {desc}")
            print(f"Sunrise: {forecast['sunrise'][index]}")
            print(f"Sunset: {forecast['sunset'][index]}")
            print("-" * 30)
    else:
        print("Failed to retrieve weather data.")"""
