from gps_coordinates import Coordinates
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import config
import json
import urllib.request
from typing import Literal

from urllib.error import URLError
from exceptions import ApiServiceError
from json.decoder import JSONDecodeError

Celsius = int


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(frozen=True, slots=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """ Request weather from OpenWeather API and return it """
    open_weather_response = _get_openweather_response(
        longitude=coordinates.longitude,
        latitude=coordinates.latitude
    )
    weather = _parse_openweather_response(open_weather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    # ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(open_weather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(open_weather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(temperature=_parse_temperature(openweather_dict),
                   weather_type=_parse_weather_type(openweather_dict),
                   sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
                   sunset=_parse_sun_time(openweather_dict, 'sunset'),
                   city=_parse_city(openweather_dict))


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_sun_time(openweather_dict: dict, time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=59.9, longitude=30.3)))
