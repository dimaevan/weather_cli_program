from gps_coordinates import Coordinates
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

Celsium = int


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
    temperature: Celsium
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordiantes: Coordinates) -> Weather:
    """ Request weather from OpenWeather API and return it """
    return Weather(temperature=20,
                   weather_type=WeatherType.CLEAR,
                   sunrise=datetime.fromisoformat("2022-05-04 04:00:00"),
                   sunset=datetime.fromisoformat("2022-05-04 04:00:00"),
                   city="Saint-Petersburg")

