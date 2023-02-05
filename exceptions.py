class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""
    pass


class ApiServiceError(Exception):
    """Program can't get weather"""
    pass


class CantRecordWeather(Exception):
    """Program can't record the weather in the history"""
    pass
