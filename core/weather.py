import math
from datetime import date, timedelta

import pandas as pd
import requests


def geocode_list(query: str, count: int = 5):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": query, "count": count, "language": "en", "format": "json"}
    r = requests.get(url, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    return data.get("results", []) or []


def fetch_current_temp(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    r = requests.get(url, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    return (data.get("current_weather") or {}).get("temperature")


def fetch_design_tmin(lat: float, lon: float, years: int = 10):
    end_d = date.today()
    start_d = end_d - timedelta(days=365 * years)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_d.isoformat(),
        "end_date": end_d.isoformat(),
        "daily": "temperature_2m_min",
        "timezone": "auto",
    }

    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    daily = data.get("daily", {})
    vals = daily.get("temperature_2m_min", []) or []
    vals = [v for v in vals if v is not None]

    if not vals:
        return None, "Archive: no Tmin data"

    s = pd.Series(vals, dtype="float64")
    p01 = float(s.quantile(0.01))
    return math.floor(p01), f"Archive: {years}y Tmin (1st percentile, floored)"
