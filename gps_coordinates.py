from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal
from exceptions import CantGetCoordinates
import re
import config
import requests
import json

@dataclass(slots=True, frozen=True)
class Coordinates():
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    """ Return current coordiantes  """
    coordinates = _get_whereami_coordinates()
    return _round_coordiantes(coordinates)


def _get_whereami_coordinates() -> Coordinates:
    whereami_output = _get_whereami_output()
    coordinates = _parse_coordinates(whereami_output)
    return coordinates


def _get_whereami_output() -> bytes:
    process = Popen(['whereami'], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates(wherami_output: bytes) -> Coordinates:
    try:
        output = wherami_output.decode().strip().split(',')
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(latitude=_parse_coord(output, 'latitude'),
                       longitude=_parse_coord(output, 'longitude'))


def _parse_coord(output: list[str], coord_type: Literal['latitude'] | Literal['longitude']) -> float:
    for line in output:
        x = re.search(r"\d+", line)
        print(x)
        if line.startswith(f"{coord_type}:"):
            return _parse_float_coordinate(line.split()[1])
        else:
            raise CantGetCoordinates


def _parse_float_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordiantes(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))

def get_ip() -> None:
    res = requests.get("https://api.ipify.org/?format=json")
    x = res.content.decode()
    res = json.loads(x)
    return res['ip']

def get_geo(ip):
    res = requests.get(f"http://ip-api.com/json/{ip}")
    x = res.content.decode()
    res = json.loads(x)
    print(res)

if __name__ == "__main__":
    print(get_geo(get_ip()))

