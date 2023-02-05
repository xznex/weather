from exceptions import ApiServiceError, CantGetCoordinates
from coordinates import get_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather


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
    print(format_weather(weather))


if __name__ == '__main__':
    main()
