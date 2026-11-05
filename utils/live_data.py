"""Live weather and mandi data clients used by the Streamlit pages."""

import os

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AGMARKNET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
NASHIK_LATITUDE = 19.9975
NASHIK_LONGITUDE = 73.7898


class LiveDataError(RuntimeError):
    """Raised when a live data source cannot provide usable data."""


def _weather_description(code: int) -> str:
    if code == 0:
        return "Clear"
    if code in (1, 2):
        return "Partly cloudy"
    if code == 3:
        return "Overcast"
    if code in (45, 48):
        return "Fog"
    if code in (51, 53, 55, 56, 57):
        return "Drizzle"
    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "Rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "Snow"
    if code in (95, 96, 99):
        return "Thunderstorm"
    return "Unknown"


@st.cache_data(ttl=1800, show_spinner=False)
def get_live_weather(
    latitude: float = NASHIK_LATITUDE,
    longitude: float = NASHIK_LONGITUDE,
) -> tuple[dict[str, object], pd.DataFrame]:
    """Return current conditions and a seven-day forecast from Open-Meteo."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,wind_speed_10m,"
            "precipitation,weather_code"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_sum,relative_humidity_2m_mean"
        ),
        "forecast_days": 7,
        "timezone": "Asia/Kolkata",
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        raise LiveDataError(
            f"The live weather service returned HTTP {status}."
        ) from exc
    except requests.Timeout as exc:
        raise LiveDataError("The live weather service timed out.") from exc
    except requests.ConnectionError as exc:
        raise LiveDataError("Could not connect to the live weather service.") from exc
    except requests.RequestException as exc:
        raise LiveDataError("Could not reach the live weather service.") from exc
    except ValueError as exc:
        raise LiveDataError("The live weather service returned invalid data.") from exc

    try:
        current = payload["current"]
        daily = payload["daily"]
        current_weather = {
            "temperature_c": round(float(current["temperature_2m"])),
            "humidity_pct": int(current["relative_humidity_2m"]),
            "wind_kmh": round(float(current["wind_speed_10m"])),
            "condition": _weather_description(int(current["weather_code"])),
            "rainfall_mm_current": float(current["precipitation"]),
            "updated_at": current["time"],
        }
        forecast = pd.DataFrame({
            "Day": pd.to_datetime(daily["time"]).strftime("%a %d %b"),
            "Max Temp °C": daily["temperature_2m_max"],
            "Min Temp °C": daily["temperature_2m_min"],
            "Rain mm": daily["precipitation_sum"],
            "Humidity %": daily["relative_humidity_2m_mean"],
        })
    except (KeyError, TypeError, ValueError) as exc:
        raise LiveDataError("The live weather service returned incomplete data.") from exc

    if forecast.empty:
        raise LiveDataError("The live weather service returned an empty forecast.")
    return current_weather, forecast


@st.cache_data(ttl=1800, show_spinner=False)
def get_live_mandi_prices() -> pd.DataFrame:
    """Return the latest available Nashik district prices from data.gov.in."""
    api_key = os.getenv("AGMARKNET_API_KEY", "").strip()
    if not api_key:
        raise LiveDataError(
            "Add your data.gov.in key as AGMARKNET_API_KEY in the local .env file "
            "to enable live mandi prices."
        )

    params = {
        "api-key": api_key,
        "format": "json",
        "limit": 1000,
        "sort[arrival_date]": "desc",
        "filters[state]": "Maharashtra",
        "filters[district]": "Nashik",
    }
    try:
        response = requests.get(AGMARKNET_URL, params=params, timeout=12)
        response.raise_for_status()
        payload = response.json()
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        raise LiveDataError(
            f"data.gov.in returned HTTP {status}. Check the API key and its access."
        ) from exc
    except requests.Timeout as exc:
        raise LiveDataError("The data.gov.in mandi price service timed out.") from exc
    except requests.ConnectionError as exc:
        raise LiveDataError("Could not connect to the data.gov.in mandi price service.") from exc
    except requests.RequestException as exc:
        raise LiveDataError("Could not reach the data.gov.in mandi price service.") from exc
    except ValueError as exc:
        raise LiveDataError("The mandi price service returned invalid data.") from exc

    if not isinstance(payload, dict):
        raise LiveDataError("The mandi price service returned an unexpected response.")
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise LiveDataError(
            "The mandi price service returned no records for Nashik, Maharashtra."
        )

    frame = pd.DataFrame.from_records(records)
    required = {
        "commodity", "market", "arrival_date", "min_price", "max_price", "modal_price"
    }
    if not required.issubset(frame.columns):
        raise LiveDataError("The mandi price service returned an unexpected data format.")

    frame = frame.rename(columns={
        "commodity": "Commodity",
        "market": "Market",
        "arrival_date": "Arrival Date",
        "min_price": "Min ₹/qtl",
        "max_price": "Max ₹/qtl",
        "modal_price": "Modal ₹/qtl",
    })
    price_columns = ["Min ₹/qtl", "Max ₹/qtl", "Modal ₹/qtl"]
    for column in price_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["Arrival Date"] = pd.to_datetime(
        frame["Arrival Date"], dayfirst=True, errors="coerce"
    )
    frame = frame.dropna(subset=price_columns)
    if frame.empty:
        raise LiveDataError("The mandi price service returned no valid price records.")

    frame["Arrival Date"] = frame["Arrival Date"].dt.strftime("%d %b %Y")
    return frame[["Commodity", "Market", "Arrival Date", *price_columns]].reset_index(drop=True)
