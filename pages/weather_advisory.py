# =============================================================================
# pages/weather_advisory.py — Weather Advisory page
# =============================================================================

import streamlit as st
from config import COLORS, t
from utils.demo_data import DEMO_WEATHER_CURRENT, DEMO_WEATHER_7DAY
from utils.charts import weather_range_chart, bar_chart
from utils.live_data import LiveDataError, get_live_weather


def _weather_icon(condition: str) -> str:
    mapping = {
        "sunny": "☀️", "clear": "☀️", "partly cloudy": "⛅",
        "cloudy": "☁️", "overcast": "☁️", "drizzle": "🌦️", "rain": "🌧️",
        "heavy rain": "⛈️", "thunderstorm": "⛈️", "fog": "🌫️", "windy": "💨",
    }
    return mapping.get(condition.lower(), "🌤️")


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>🌤️ {t('weather_advisory')}</h2>",
        unsafe_allow_html=True,
    )
    if st.button("Refresh live weather", key="refresh_live_weather"):
        get_live_weather.clear()
    st.markdown("<br/>", unsafe_allow_html=True)

    try:
        with st.spinner("Loading live weather..."):
            w, df = get_live_weather()
        weather_is_live = True
    except LiveDataError as exc:
        st.error(f"{exc} Showing clearly labeled demonstration weather instead.")
        w, df = DEMO_WEATHER_CURRENT, DEMO_WEATHER_7DAY
        weather_is_live = False

    # -----------------------------------------------------------------------
    # Current conditions
    # -----------------------------------------------------------------------
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>📍 Current Conditions — Nashik, Maharashtra</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )

    icon = _weather_icon(w["condition"])

    cur_col1, cur_col2 = st.columns([1, 3])
    with cur_col1:
        st.markdown(
            f"""<div style="text-align:center;background:{COLORS['primary_pale']};
                border:1px solid {COLORS['border']};border-radius:12px;padding:24px;">
                <div style="font-size:4rem;">{icon}</div>
                <p style="font-size:1.1rem;font-weight:700;color:{COLORS['primary']};margin:8px 0 0;">
                    {w['condition']}</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with cur_col2:
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("🌡️ Temperature", f"{w['temperature_c']}°C")
        mc2.metric("💧 Humidity",    f"{w['humidity_pct']}%")
        mc3.metric("💨 Wind",        f"{w['wind_kmh']} km/h")
        mc4.metric("🌧️ Rain (current)", f"{w['rainfall_mm_current']:.1f} mm" if weather_is_live else f"{w['rainfall_mm_today']} mm")
        if weather_is_live:
            st.caption(f"Live data from Open-Meteo · Updated {w['updated_at']}")
        else:
            st.caption("Demonstration values — live weather is unavailable.")

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # 7-day forecast table
    # -----------------------------------------------------------------------
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>📅 7-Day Forecast</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )

    tab_table, tab_temp, tab_rain = st.tabs(["📋 Table", "🌡️ Temperature Trend", "🌧️ Rainfall"])

    with tab_table:
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_temp:
        fig_temp = weather_range_chart(df, "Day", "Max Temp °C", "Min Temp °C")
        st.plotly_chart(fig_temp, use_container_width=True)

    with tab_rain:
        fig_rain = bar_chart(
            df, x="Day", y=["Rain mm"],
            title=f"Rainfall Forecast (mm) — {'Live' if weather_is_live else 'Demo'} Data",
        )
        st.plotly_chart(fig_rain, use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Farming advisories based on forecast
    # -----------------------------------------------------------------------
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>🌾 Farming Weather Advisories</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )

    advisories = []
    rainy_days = df[df["Rain mm"] >= 10]["Day"].tolist()
    hot_days = df[df["Max Temp °C"] >= 35]["Day"].tolist()
    if rainy_days:
        advisories.append((
            f"🌧️ Rain outlook — {', '.join(rainy_days)}",
            "Rain is forecast. Consider postponing spraying and check field drainage.",
            COLORS["info"],
        ))
    if hot_days:
        advisories.append((
            f"🌡️ High temperature outlook — {', '.join(hot_days)}",
            "High temperatures are forecast. Consider irrigating during cooler hours.",
            COLORS["warning"],
        ))
    if not advisories:
        advisories.append((
            "✅ No heavy-rain or high-temperature alert",
            "No days meeting these alert thresholds appear in the displayed forecast.",
            COLORS["primary"],
        ))
    if not weather_is_live:
        st.caption("Advisories below are based on demonstration forecast values.")

    for title, body, color in advisories:
        st.markdown(
            f"""<div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                border-left:4px solid {color};border-radius:8px;padding:16px 20px;margin-bottom:12px;">
                <p style="font-weight:700;color:{COLORS['text_dark']};margin:0 0 6px;">{title}</p>
                <p style="color:{COLORS['text_muted']};font-size:14px;margin:0;">{body}</p>
            </div>""",
            unsafe_allow_html=True,
        )
