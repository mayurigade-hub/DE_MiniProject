import requests


def extract_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=19.0760"
        "&longitude=72.8777"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "wind_speed_10m,"
        "weather_code"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def extract_air_quality_data():
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        "?latitude=19.0760"
        "&longitude=72.8777"
        "&current="
        "pm10,"
        "pm2_5,"
        "carbon_monoxide,"
        "nitrogen_dioxide,"
        "ozone,"
        "us_aqi"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()