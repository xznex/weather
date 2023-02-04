import json
from json import JSONDecodeError
from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias, Literal
from enum import Enum
import requests

from coordinates import Coordinates
from config import WEATHER_URL, WEATHER_API
from exceptions import ApiServiceError


Celsius: TypeAlias = int

YANDEX_WEATHER_HEADERS = {
    "X-Yandex-API-Key": WEATHER_API
}


class WeatherType(str, Enum):
    CLEAR = "ясно"
    PARTLY_CLOUDY = "малооблачно"
    CLOUDY = "облачно"
    OVERCAST = "пасмурно"
    DRIZZLE = "морось"
    LIGHT_RAIN = "небольшой дождь"
    RAIN = "дождь",
    MODERATE_RAIN = "умеренно сильный дождь",
    HEAVY_RAIN = "сильный дождь",
    CONTINUOUS_HEAVY_RAIN = "длительный сильный дождь",
    SHOWERS = "ливень",
    WET_SNOW = "дождь со снегом",
    LIGHT_SNOW = "небольшой снег",
    SNOW = "снег",
    SNOW_SHOWERS = "снегопад",
    HAIL = "град",
    THUNDERSTORM = "гроза",
    THUNDERSTORM_WITH_RAIN = "дождь с грозой",
    THUNDERSTORM_WITH_HAIL = "гроза с градом",


@dataclass(frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    yandex_weather_response = _get_yandex_weather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_yandex_weather_response(yandex_weather_response)
    return weather


def _get_yandex_weather_response(longitude: float, latitude: float) -> str:
    url = WEATHER_URL.format(longitude=longitude, latitude=latitude)
    response = requests.request("GET", url, headers=YANDEX_WEATHER_HEADERS)

    if response.status_code != 200:
        raise ApiServiceError

    return response.text


def _parse_yandex_weather_response(yandex_weather_response: str) -> Weather:
    try:
        yandex_weather_dict = json.loads(yandex_weather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(yandex_weather_dict),
        weather_type=_parse_weather_type(yandex_weather_dict),
        sunrise=_parse_sun_time(yandex_weather_dict, "sunrise"),
        sunset=_parse_sun_time(yandex_weather_dict, "sunset"),
        city=_parse_city(yandex_weather_dict),
    )


def _parse_temperature(yandex_weather_dict: dict) -> Celsius:
    return round(yandex_weather_dict["fact"]["temp"])


def _parse_weather_type(yandex_weather_dict: dict) -> WeatherType:
    try:
        condition = yandex_weather_dict["fact"]["condition"].upper()
    except IndexError:
        raise ApiServiceError
    weather_type = WeatherType[condition]
    return weather_type.value


def _parse_sun_time(yandex_weather_dict: dict, time: Literal["sunrise", "sunset"]) -> datetime:
    return datetime.strptime(yandex_weather_dict["forecasts"][0][time], "%H:%M")


def _parse_city(yandex_weather_dict: dict) -> str:
    return yandex_weather_dict["geo_object"]["locality"]["name"]


if __name__ == '__main__':
    print(get_weather(Coordinates(longitude=37.812767, latitude=55.700877)))
