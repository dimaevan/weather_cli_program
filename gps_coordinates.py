import json
from dataclasses import dataclass
from exceptions import CantGetCoordinates

import config
import urllib.request
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
    return Coordinates(*map(lambda c: round(c, 1),
                            [coordinates.latitude, coordinates.longitude]))


def get_ip() -> str:
    url = "https://api.ipify.org/?format=json"
    try:
        with urllib.request.urlopen(url) as resp:
            ip = resp.read().decode()
            result = json.loads(ip)['ip']
    except (ConnectionError, RequestException):
        raise CantGetCoordinates
    return result


def get_geo(ip) -> Coordinates:
    url = f"http://ip-api.com/json/{ip}"
    try:
        with urllib.request.urlopen(url) as resp:
            response = resp.read().decode()
            geo = json.loads(response)
        print(f"Your ip is {ip}. Your city is {geo['city']}")
    except (ConnectionError, RequestException):
        raise CantGetCoordinates
    return Coordinates(latitude=geo['lat'], longitude=geo['lon'])


if __name__ == "__main__":
    get_gps_coordinates()
