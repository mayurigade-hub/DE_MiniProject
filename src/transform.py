def transform_data(weather_data, air_quality_data):

    weather = weather_data["current"]
    air_quality = air_quality_data["current"]

    transformed_data = {
        "recorded_at": weather["time"],

        # Weather
        "temperature": weather["temperature_2m"],
        "humidity": weather["relative_humidity_2m"],
        "apparent_temperature": weather["apparent_temperature"],
        "wind_speed": weather["wind_speed_10m"],
        "weather_code": weather["weather_code"],

        # Air Quality
        "pm10": air_quality["pm10"],
        "pm2_5": air_quality["pm2_5"],
        "carbon_monoxide": air_quality["carbon_monoxide"],
        "nitrogen_dioxide": air_quality["nitrogen_dioxide"],
        "ozone": air_quality["ozone"],
        "us_aqi": air_quality["us_aqi"]
    }

    return transformed_data