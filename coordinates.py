from dataclasses import dataclass
import requests

from exceptions import CantGetCoordinates
from config import MAPS_URL


@dataclass(frozen=True)
class Coordinates:
    longitude: float
    latitude: float


def get_gps_coordinates() -> Coordinates:
    """Returns current coordinates using the entered address"""
    address = _get_address()
    return _get_maps_coordinates(address)


def _get_address() -> str:
    address = input("Введите адресс для которого хотите узнать погоду: ")

    while len(address) == 0:
        address = input("Вы не ввели адресс. Повторите попытку: ")

    validated = '+'.join(address.split())
    return validated


def _get_maps_coordinates(address: str) -> Coordinates:
    geocode = requests.get(MAPS_URL.format(address=address))

    if geocode.status_code != 200:
        raise CantGetCoordinates

    return _parse_coordinates(geocode)


def _parse_coordinates(maps_output) -> Coordinates:
    coordinates = maps_output.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    try:
        longitude = float(coordinates.split(' ')[0])
        latitude = float(coordinates.split(' ')[1])
    except ValueError:
        raise CantGetCoordinates

    return Coordinates(longitude=longitude, latitude=latitude)


if __name__ == '__main__':
    print(get_gps_coordinates())
