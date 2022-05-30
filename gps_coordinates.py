from dataclasses import dataclass
from subprocess import Popen, PIPE

from exceptions import CantGetCoordinates

@dataclass(slots=True, frozen=True)
class Coordinates():
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """ Return current coordiantes  """
    process = Popen(['whereami'], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    output_lines = output.decode().strip().lower().split("\n")
    print(output_lines)

get_coordinates()
