import requests

from config import OPEN_METEO, TZ


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
            "precipitation",
        ],
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "weather_code",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "sunrise",
            "sunset",
        ],
        "timezone": TZ,
    }

    for key in ("current", "hourly", "daily"):
        params[key] = ",".join(params[key])

    response = requests.get(OPEN_METEO, params=params, timeout=8)
    response.raise_for_status()
    return response.json()

