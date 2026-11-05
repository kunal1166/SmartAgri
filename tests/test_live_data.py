import pytest

from utils import live_data


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_get_live_weather_normalizes_forecast(monkeypatch):
    payload = {
        "current": {
            "temperature_2m": 27.6,
            "relative_humidity_2m": 61,
            "wind_speed_10m": 12.4,
            "precipitation": 0.1,
            "weather_code": 2,
            "time": "2026-11-05T16:00",
        },
        "daily": {
            "time": ["2026-11-05", "2026-11-06"],
            "temperature_2m_max": [30, 31],
            "temperature_2m_min": [20, 21],
            "precipitation_sum": [0, 3.2],
            "relative_humidity_2m_mean": [55, 60],
        },
    }
    monkeypatch.setattr(live_data.requests, "get", lambda *args, **kwargs: FakeResponse(payload))
    live_data.get_live_weather.clear()

    current, forecast = live_data.get_live_weather()

    assert current["temperature_c"] == 28
    assert current["condition"] == "Partly cloudy"
    assert list(forecast.columns) == [
        "Day", "Max Temp °C", "Min Temp °C", "Rain mm", "Humidity %",
    ]
    assert len(forecast) == 2
    assert forecast.iloc[1]["Rain mm"] == 3.2


def test_get_live_mandi_prices_normalizes_records(monkeypatch):
    monkeypatch.setenv("AGMARKNET_API_KEY", "test-key")
    response = FakeResponse({
        "records": [{
            "commodity": "Onion",
            "market": "Lasalgaon",
            "arrival_date": "05/11/2026",
            "min_price": "600",
            "max_price": "950",
            "modal_price": "780",
        }],
    })
    request_args = {}

    def fake_get(url, *, params, timeout):
        request_args.update(url=url, params=params, timeout=timeout)
        return response

    monkeypatch.setattr(live_data.requests, "get", fake_get)
    live_data.get_live_mandi_prices.clear()

    prices = live_data.get_live_mandi_prices()

    assert prices.iloc[0]["Commodity"] == "Onion"
    assert prices.iloc[0]["Arrival Date"] == "05 Nov 2026"
    assert prices.iloc[0]["Modal ₹/qtl"] == 780
    assert request_args["params"]["filters[state]"] == "Maharashtra"
    assert request_args["params"]["filters[district]"] == "Nashik"


def test_get_live_mandi_prices_requires_api_key(monkeypatch):
    monkeypatch.delenv("AGMARKNET_API_KEY", raising=False)
    live_data.get_live_mandi_prices.clear()

    with pytest.raises(live_data.LiveDataError, match="AGMARKNET_API_KEY"):
        live_data.get_live_mandi_prices()
