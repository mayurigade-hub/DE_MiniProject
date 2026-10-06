import mysql.connector


def load_data(data):

    connection = mysql.connector.connect(
        host="localhost",
        user="weather_user",
        password="weather123",
        database="weather_etl"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO weather_data
        (
            recorded_at,
            temperature,
            humidity,
            apparent_temperature,
            wind_speed,
            weather_code,
            pm10,
            pm2_5,
            carbon_monoxide,
            nitrogen_dioxide,
            ozone,
            us_aqi
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["recorded_at"],
        data["temperature"],
        data["humidity"],
        data["apparent_temperature"],
        data["wind_speed"],
        data["weather_code"],
        data["pm10"],
        data["pm2_5"],
        data["carbon_monoxide"],
        data["nitrogen_dioxide"],
        data["ozone"],
        data["us_aqi"]
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()