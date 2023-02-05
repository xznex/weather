from pathlib import Path

from exceptions import ApiServiceError, CantGetCoordinates, CantRecordWeather
from coordinates import get_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from history import save_weather, PlainFileWeatherStorage, JSONFileWeatherStorage


def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print("Не смог получить координаты")
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print("Не смог получить погоду в API-сервиса погоды")
        exit(1)
    try:
        save_weather(
            weather,
            PlainFileWeatherStorage(Path.cwd() / "history.txt")
        )
        save_weather(
            weather,
            JSONFileWeatherStorage(Path.cwd() / "history.json")
        )
    except CantRecordWeather:
        print("Не смог записать погоду в историю")
        exit(1)

    print(format_weather(weather))


if __name__ == '__main__':
    main()
