# =============================================================================
# pages/dashboard.py — Main Dashboard page
# =============================================================================

import streamlit as st
from config import COLORS, t
from utils.demo_data import (
    DEMO_FARMER, DEMO_FARM_KPI, DEMO_CROPS,
    DEMO_WEATHER_CURRENT, DEMO_ACTIVITIES, DEMO_YIELD_HISTORY,
)
from utils.charts import bar_chart, gauge_chart
from utils.live_data import LiveDataError, get_live_weather


# ---------------------------------------------------------------------------
# Helper widgets
# ---------------------------------------------------------------------------
def _kpi_card(label: str, value: str, unit: str = "", color: str = COLORS["primary"]) -> None:
    """Render a KPI metric card that never wraps its value+unit onto separate lines."""
    st.markdown(
        f"""<div style="
            background:{COLORS['surface']};
            border:1px solid {COLORS['border']};
            border-left:4px solid {color};
            border-radius:8px;
            padding:14px 12px;
            text-align:center;
            min-height:80px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        ">
            <p style="margin:0 0 4px;font-size:12px;color:{COLORS['text_muted']};
                font-weight:500;line-height:1.3;">{label}</p>
            <p style="margin:0;line-height:1.2;white-space:nowrap;overflow:hidden;
                text-overflow:ellipsis;">
                <span style="font-size:22px;font-weight:700;
                    color:{COLORS['text_dark']};">{value}</span>&#8202;<span
                    style="font-size:13px;color:{COLORS['text_muted']};
                    font-weight:500;">{unit}</span>
            </p>
        </div>""",
        unsafe_allow_html=True,
    )


def _section_header(title: str) -> None:
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};margin-bottom:4px;'>{title}</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:0 0 16px 0;'/>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render() -> None:
    # --- Welcome banner ---
    st.markdown(
        f"""<div style="
            background:{COLORS['primary']};
            border-radius:10px;
            padding:22px 28px;
            margin-bottom:20px;
            color:white;
        ">
            <h1 style="margin:0;font-size:1.7rem;font-weight:700;line-height:1.3;">
                🌾 {t('welcome')}, {DEMO_FARMER['name']}!
                <span style="font-size:13px;font-weight:400;opacity:0.75;
                    margin-left:8px;">(Demo Profile)</span>
            </h1>
            <p style="margin:8px 0 0;opacity:0.85;font-size:0.9rem;">
                {DEMO_FARMER['location']} &nbsp;|&nbsp; {DEMO_FARMER['farm_size_acres']} acres &nbsp;|&nbsp;
                {DEMO_FARMER['irrigation']}
            </p>
        </div>""",
        unsafe_allow_html=True,
    )
    st.info("Farm profile, crop, soil, yield and activity figures are demonstration values.")

    # -----------------------------------------------------------------------
    # Farm Overview KPIs
    # -----------------------------------------------------------------------
    _section_header(f"🏡 {t('farm_overview')}")
    # Use gap= to give each card a little breathing room; spec via column_config avoids overflow
    k1, k2, k3, k4, k5 = st.columns([1, 1, 1, 1, 1], gap="small")
    with k1:
        _kpi_card("Total Area", "12.5", "acres")
    with k2:
        _kpi_card("Cultivated", "10.2", "acres", COLORS["primary_light"])
    with k3:
        _kpi_card("Active Crops", str(DEMO_FARM_KPI["active_crops"]), "crops", COLORS["accent"])
    with k4:
        _kpi_card("Est. Yield", str(DEMO_FARM_KPI["estimated_yield_qtl"]), "qtl", COLORS["warning"])
    with k5:
        _kpi_card("Soil Health", str(DEMO_FARM_KPI["soil_health_score"]), "/100", COLORS["primary"])

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Crop info + Soil Health gauge (side by side)
    # -----------------------------------------------------------------------
    # Widen crop column; give gauge column enough room for the chart
    col_crop, col_gauge = st.columns([3, 2], gap="medium")

    with col_crop:
        _section_header(f"🌱 {t('crop_info')}")
        styled = DEMO_CROPS.style.applymap(
            lambda v: f"color:{COLORS['primary']};font-weight:600;" if v == "Good"
            else (f"color:{COLORS['warning']};font-weight:600;" if v == "Fair" else ""),
            subset=["Health"],
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with col_gauge:
        _section_header("🧪 Soil Health")
        fig_gauge = gauge_chart(
            value=DEMO_FARM_KPI["soil_health_score"],
            title="Soil Health Score",
            suffix="/100",
            thresholds=(40, 65),
        )
        # height=220 prevents the gauge from being squeezed into a tiny square
        st.plotly_chart(fig_gauge, use_container_width=True, height=220)

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Weather overview
    # -----------------------------------------------------------------------
    _section_header(f"☁️ {t('weather_overview')}")
    try:
        w, _ = get_live_weather()
        weather_is_live = True
    except LiveDataError as exc:
        st.warning(f"{exc} Showing clearly labeled demonstration weather instead.")
        w = DEMO_WEATHER_CURRENT
        weather_is_live = False
    wc1, wc2, wc3, wc4 = st.columns([1, 1, 1, 1], gap="small")
    with wc1:
        _kpi_card("Temperature", str(w["temperature_c"]), "°C", COLORS["warning"])
    with wc2:
        _kpi_card("Humidity", str(w["humidity_pct"]), "%", COLORS["info"])
    with wc3:
        _kpi_card("Wind Speed", str(w["wind_kmh"]), "km/h", COLORS["text_muted"])
    with wc4:
        _kpi_card("Condition", w["condition"], "", COLORS["primary"])
    if weather_is_live:
        st.caption(f"Live weather for Nashik, Maharashtra · Updated {w['updated_at']} · Open-Meteo")
    else:
        st.caption("Demonstration weather — live data is unavailable.")

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Yield history chart + Recent activities
    # -----------------------------------------------------------------------
    col_chart, col_act = st.columns([3, 2], gap="medium")

    with col_chart:
        _section_header("📈 Seasonal Yield History")
        fig_yield = bar_chart(
            df=DEMO_YIELD_HISTORY,
            x="Season",
            y=["Tomato (qtl)", "Onion (qtl)", "Wheat (qtl)"],
            title="Yield by Season (qtl) — Demo Data",
            barmode="stack",
        )
        st.plotly_chart(fig_yield, use_container_width=True)

    with col_act:
        _section_header(f"📋 {t('recent_activities')}")
        for _, row in DEMO_ACTIVITIES.iterrows():
            icon = "✅" if row["Status"] == "Completed" else "🔔"
            color = COLORS["primary"] if row["Status"] == "Completed" else COLORS["warning"]
            st.markdown(
                f"""<div style="padding:8px 12px;margin-bottom:6px;
                    border-radius:6px;border-left:3px solid {color};
                    background:{COLORS['surface']};">
                    <span style="font-size:12px;color:{COLORS['text_muted']};">{row['Date']}</span><br/>
                    {icon} <span style="font-size:14px;">{row['Activity']}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Quick access cards
    # -----------------------------------------------------------------------
    _section_header(f"⚡ {t('quick_access')}")
    qa_cols = st.columns(4)
    quick_items = [
        ("🤖", "AI Assistant",      "Ask your farming questions"),
        ("🌤️", "Weather Advisory",  "7-day forecast & alerts"),
        ("🌱", "Crop & Soil",       "Soil health & recommendations"),
        ("📊", "Mandi Prices",      "Today's market prices"),
    ]
    for col, (icon, label, desc) in zip(qa_cols, quick_items):
        with col:
            st.markdown(
                f"""<div style="
                    background:{COLORS['primary_pale']};
                    border:1px solid {COLORS['border']};
                    border-radius:10px;padding:20px;text-align:center;
                    cursor:pointer;transition:box-shadow .2s;
                ">
                    <div style="font-size:2rem;">{icon}</div>
                    <p style="font-weight:700;color:{COLORS['primary']};margin:8px 0 4px;">{label}</p>
                    <p style="font-size:12px;color:{COLORS['text_muted']};margin:0;">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )
