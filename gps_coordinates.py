from dataclasses import dataclass
from exceptions import CantGetCoordinates

import config
import requests
from requests.exceptions import RequestException


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    """ Return current coordinates  """
    ip = get_ip()
    coordinates = get_geo(ip)
    return _round_coordinates(coordinates)


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))


def get_ip() -> str:
    try:
        res = requests.get("https://api.ipify.org/?format=json")
        ip = res.json()['ip']
    except (ConnectionError, RequestException):
        raise CantGetCoordinates
    return ip


def get_geo(ip) -> Coordinates:
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        geo = res.json()
        print(f"Your ip is {ip}.Your city is {geo['city']}")
    except (ConnectionError, RequestException):
        raise CantGetCoordinates
    return Coordinates(latitude=geo['lat'], longitude=geo['lon'])


if __name__ == "__main__":
    print(get_gps_coordinates())
