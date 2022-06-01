from datetime import datetime
from pathlib import Path
from typing import Protocol

from weather_api_service import Weather
from weather_formatter import format_weather


class WeatherStorage(Protocol):
    """  Interface for storage  saving weather"""
    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage(WeatherStorage):
    """ Store weather in plain text format """
    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self._file, 'a') as file:
            file.write(f"{now} \n{formatted_weather}\n")


def save_weather(weather: Weather, my_storage: WeatherStorage) -> None:
    """ Save weather in storage """
    my_storage.save(weather)
