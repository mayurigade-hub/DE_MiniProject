import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(
    page_title="Weather & Air Quality Dashboard",
    page_icon="🌤️",
    layout="wide"
)

def get_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="weather_user",
        password="weather123",
        database="weather_etl"
    )

    query = """
        SELECT
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
        FROM weather_data
        ORDER BY recorded_at DESC
        LIMIT 50
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df

st.title("🌤️ Weather & Air Quality Dashboard")

st.write(
    "Real-time weather and air quality data collected "
    "from Open-Meteo using Apache Airflow and stored in MySQL."
)

try:

    df = get_data()

except Exception as e:

    st.error(f"Database connection failed: {e}")
    st.stop()


if df.empty:

    st.warning("No weather data available.")

    st.stop()

latest = df.iloc[0]

st.subheader("🌡️ Current Weather")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Temperature",
        f"{latest['temperature']:.1f} °C"
    )

with col2:
    st.metric(
        "Feels Like",
        f"{latest['apparent_temperature']:.1f} °C"
    )

with col3:
    st.metric(
        "Humidity",
        f"{latest['humidity']:.0f} %"
    )

with col4:
    st.metric(
        "Wind Speed",
        f"{latest['wind_speed']:.1f} km/h"
    )


st.subheader("🌫️ Current Air Quality")

aq_col1, aq_col2, aq_col3, aq_col4 = st.columns(4)

with aq_col1:
    st.metric(
        "PM2.5",
        f"{latest['pm2_5']:.1f} µg/m³"
        if pd.notna(latest["pm2_5"])
        else "N/A"
    )

with aq_col2:
    st.metric(
        "PM10",
        f"{latest['pm10']:.1f} µg/m³"
        if pd.notna(latest["pm10"])
        else "N/A"
    )

with aq_col3:
    st.metric(
        "Ozone",
        f"{latest['ozone']:.1f} µg/m³"
        if pd.notna(latest["ozone"])
        else "N/A"
    )

with aq_col4:
    st.metric(
        "US AQI",
        f"{latest['us_aqi']:.0f}"
        if pd.notna(latest["us_aqi"])
        else "N/A"
    )

st.subheader("🌡️ Temperature History")

weather_chart = df.dropna(
    subset=["temperature", "apparent_temperature"]
).copy()

weather_chart["temperature"] = pd.to_numeric(
    weather_chart["temperature"]
)

weather_chart["apparent_temperature"] = pd.to_numeric(
    weather_chart["apparent_temperature"]
)

weather_chart = weather_chart.sort_values("recorded_at")

st.line_chart(
    weather_chart.set_index("recorded_at")[
        ["temperature", "apparent_temperature"]
    ]
)

st.subheader("📊 Air Quality History")

air_quality_chart = df.dropna(
    subset=["pm10", "pm2_5"]
).copy()

air_quality_chart["pm10"] = pd.to_numeric(
    air_quality_chart["pm10"]
)

air_quality_chart["pm2_5"] = pd.to_numeric(
    air_quality_chart["pm2_5"]
)

air_quality_chart = air_quality_chart.sort_values(
    "recorded_at"
)

if not air_quality_chart.empty:

    st.line_chart(
        air_quality_chart.set_index("recorded_at")[
            ["pm10", "pm2_5"]
        ]
    )

else:

    st.info("Air quality history will appear after data is collected.")

st.subheader("🫁 AQI History")

aqi_chart = df.dropna(
    subset=["us_aqi"]
).copy()

aqi_chart["us_aqi"] = pd.to_numeric(
    aqi_chart["us_aqi"]
)

aqi_chart = aqi_chart.sort_values("recorded_at")

if not aqi_chart.empty:

    st.line_chart(
        aqi_chart.set_index("recorded_at")[
            ["us_aqi"]
        ]
    )

else:

    st.info("AQI history will appear after data is collected.")

st.subheader("📋 Historical Data")

with st.expander("View Raw Data"):

    st.dataframe(
        df,
        use_container_width=True
    )