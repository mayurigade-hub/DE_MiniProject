# Weather & Air Quality ETL Dashboard

An end-to-end data engineering project that collects current weather and air-quality measurements for Mumbai, transforms them into a single record, stores them in MySQL, and presents recent readings in a Streamlit dashboard. An Apache Airflow DAG runs the ETL workflow every five minutes.

## Data pipeline

```text
Open-Meteo Weather API ─┐
                        ├─ Extract → Transform → Load → MySQL → Streamlit dashboard
Open-Meteo Air Quality ─┘                Apache Airflow
```

The APIs are queried for latitude `19.0760` and longitude `72.8777` (Mumbai). The Airflow DAG runs three tasks in order: extract both API responses, combine the selected values, then insert the resulting row into MySQL.

## Repository structure

```text
.
├── app.py                    # Streamlit dashboard
├── requirements.txt          # Pinned Python dependencies
├── dags/
│   └── weather_etl_dag.py    # Airflow ETL DAG
└── src/
    ├── extract.py            # Open-Meteo API calls
    ├── transform.py          # Maps API responses to database fields
    └── load.py               # Inserts transformed data into MySQL
```

## Prerequisites

- Python version supported by the pinned dependencies (use Python 3.12 for this environment)
- MySQL Server
- Network access to the Open-Meteo weather and air-quality APIs

`requirements.txt` pins Apache Airflow 3.3.2, the Airflow standard provider, Streamlit, pandas, MySQL Connector/Python, requests, and their resolved dependencies. Airflow installation can be platform- and Python-version-specific; use the official Airflow installation instructions and constraints for your environment if a direct install from the requirements file is incompatible.

## Installation

Create and activate a virtual environment from the repository root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the pinned dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configure MySQL

The application currently connects to a local MySQL server using these values, hard-coded in both `src/load.py` and `app.py`:

| Setting | Current value |
| --- | --- |
| Host | `localhost` |
| Database | `weather_etl` |
| User | `weather_user` |
| Password | `weather123` |

Create a database, a matching user, and the table before running the pipeline:

```sql
CREATE DATABASE weather_etl;
CREATE USER 'weather_user'@'localhost' IDENTIFIED BY 'weather123';
GRANT ALL PRIVILEGES ON weather_etl.* TO 'weather_user'@'localhost';

USE weather_etl;

CREATE TABLE weather_data (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    recorded_at DATETIME NOT NULL,
    temperature DOUBLE NULL,
    humidity DOUBLE NULL,
    apparent_temperature DOUBLE NULL,
    wind_speed DOUBLE NULL,
    weather_code INT NULL,
    pm10 DOUBLE NULL,
    pm2_5 DOUBLE NULL,
    carbon_monoxide DOUBLE NULL,
    nitrogen_dioxide DOUBLE NULL,
    ozone DOUBLE NULL,
    us_aqi DOUBLE NULL
);
```

If your MySQL credentials or host differ, update the connection settings in both `src/load.py` and `app.py` so the ETL process and dashboard use the same database. The current code does not read credentials from environment variables.

## Run the Airflow DAG

1. Initialize and configure Airflow for your local environment, following the Airflow 3.x installation guide.
2. Set Airflow's DAGs folder to this project's `dags/` directory, or copy `dags/weather_etl_dag.py` into the configured DAGs folder.
3. Ensure the Airflow Python environment has the project dependencies installed and can access the project root so it can import `src`.
4. Start Airflow using the command appropriate to your Airflow 3.x installation.
5. In the Airflow UI, enable `weather_air_quality_etl_pipeline` and trigger it, or wait for its scheduled run.

The DAG uses the cron schedule `*/5 * * * *` (every five minutes) and has catchup disabled. Its task order is `extract_data` → `transform_data` → `load_data`.

## Run the Streamlit dashboard

Start the dashboard from the project root after MySQL is running and the table contains data:

```bash
streamlit run app.py
```

Streamlit prints a local URL in the terminal. The dashboard displays the newest weather and air-quality metrics, history charts, and a raw-data table. It queries up to the 50 newest records from `weather_data`.

## Data stored

| Column | Meaning |
| --- | --- |
| `recorded_at` | Measurement timestamp from the weather API |
| `temperature` | Temperature at 2 m (°C) |
| `humidity` | Relative humidity (%) |
| `apparent_temperature` | Feels-like temperature (°C) |
| `wind_speed` | Wind speed at 10 m (km/h) |
| `weather_code` | Open-Meteo weather condition code |
| `pm10`, `pm2_5` | PM10 and PM2.5 concentrations (µg/m³) |
| `carbon_monoxide`, `nitrogen_dioxide`, `ozone` | Air-pollutant measurements returned by Open-Meteo |
| `us_aqi` | US Air Quality Index |

## Implementation notes

- The project requests current conditions from Open-Meteo; it does not provide historical backfill.
- Each successful DAG run inserts a row. The current implementation does not deduplicate by timestamp.
- Database connection values are hard-coded in the application source and should be changed for your local setup.
