# =============================================================================
# pages/crop_soil_advisory.py — Crop & Soil Advisory page
# =============================================================================

import streamlit as st
from config import COLORS, DEMO_NOTICE, t
from utils.demo_data import DEMO_SOIL, DEMO_CROP_ADVISORY, DEMO_CROPS
from utils.charts import gauge_chart, donut_chart


def _soil_progress(label: str, value: float, max_val: float, unit: str, optimal_range: str) -> None:
    pct = min(value / max_val * 100, 100)
    color = COLORS["primary_light"] if pct > 30 else COLORS["warning"]
    st.markdown(
        f"""<div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:13px;font-weight:600;color:{COLORS['text_dark']};">{label}</span>
                <span style="font-size:13px;color:{COLORS['text_muted']};">
                    {value} {unit} &nbsp;<em style="font-size:11px;">(Optimal: {optimal_range})</em>
                </span>
            </div>
            <div style="background:{COLORS['border']};border-radius:4px;height:8px;">
                <div style="width:{pct:.0f}%;background:{color};border-radius:4px;height:8px;"></div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>🌱 {t('crop_soil_advisory')}</h2>",
        unsafe_allow_html=True,
    )
    st.info(DEMO_NOTICE)
    st.markdown("<br/>", unsafe_allow_html=True)

    tab_soil, tab_crop, tab_calendar = st.tabs(
        ["🧪 Soil Analysis", "🌾 Crop Advisory", "📅 Crop Calendar"]
    )

    # -----------------------------------------------------------------------
    # Soil Analysis
    # -----------------------------------------------------------------------
    with tab_soil:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Soil Health Report</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        col_params, col_gauge = st.columns([3, 2])

        with col_params:
            st.markdown(
                f"<p style='color:{COLORS['text_muted']};font-size:13px;'>Soil Type: "
                f"<strong>Black Cotton Soil (Vertisol)</strong> — Last tested: Oct 2026 (Demo)</p>",
                unsafe_allow_html=True,
            )
            _soil_progress("pH",                 DEMO_SOIL["pH"],                        14,   "",     "6.0 – 7.5")
            _soil_progress("Nitrogen (N)",        DEMO_SOIL["Nitrogen (kg/ha)"],          400,  "kg/ha","200 – 280")
            _soil_progress("Phosphorus (P)",      DEMO_SOIL["Phosphorus (kg/ha)"],        100,  "kg/ha","30 – 60")
            _soil_progress("Potassium (K)",       DEMO_SOIL["Potassium (kg/ha)"],         300,  "kg/ha","150 – 200")
            _soil_progress("Organic Carbon",      DEMO_SOIL["Organic Carbon %"],          2.0,  "%",    "0.75 – 1.50")
            _soil_progress("EC",                  DEMO_SOIL["EC (dS/m)"],                 2.0,  "dS/m", "< 0.8")

        with col_gauge:
            fig_ph = gauge_chart(
                value=DEMO_SOIL["pH"],
                title="Soil pH",
                suffix="",
                min_val=4.0,
                max_val=9.0,
                thresholds=(5.5, 7.5),
            )
            st.plotly_chart(fig_ph, use_container_width=True)

            # Nutrient donut
            fig_nut = donut_chart(
                labels=["Nitrogen", "Phosphorus", "Potassium"],
                values=[
                    DEMO_SOIL["Nitrogen (kg/ha)"],
                    DEMO_SOIL["Phosphorus (kg/ha)"],
                    DEMO_SOIL["Potassium (kg/ha)"],
                ],
                title="NPK Ratio (Demo)",
            )
            st.plotly_chart(fig_nut, use_container_width=True)

        # Soil recommendations
        st.markdown(
            f"<h4 style='color:{COLORS['primary']};margin-top:16px;'>💡 Soil Improvement Recommendations</h4>",
            unsafe_allow_html=True,
        )
        soil_recs = [
            ("Organic Carbon",  "Low at 0.72%. Apply FYM (Farm Yard Manure) @ 5 tonnes/acre or vermicompost."),
            ("Phosphorus",      "Adequate. Maintain with DAP @ recommended dose at sowing."),
            ("Nitrogen",        "Slightly above optimal. Reduce urea application by 10–15%."),
        ]
        for nutrient, rec in soil_recs:
            st.markdown(
                f"""<div style="background:{COLORS['surface']};border-left:3px solid {COLORS['primary_light']};
                    border-radius:6px;padding:10px 14px;margin-bottom:8px;">
                    <strong style="color:{COLORS['primary']};">{nutrient}:</strong>
                    <span style="font-size:14px;color:{COLORS['text_muted']};"> {rec}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------------------------
    # Crop Advisory
    # -----------------------------------------------------------------------
    with tab_crop:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Current Crop Advisory</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        urgency_color = {"High": COLORS["error"], "Medium": COLORS["warning"], "Low": COLORS["primary_light"]}

        for adv in DEMO_CROP_ADVISORY:
            color = urgency_color.get(adv["urgency"], COLORS["primary"])
            st.markdown(
                f"""<div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                    border-left:5px solid {color};border-radius:8px;padding:16px 20px;margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="font-size:16px;color:{COLORS['text_dark']};">🌿 {adv['crop']}</strong>
                        <span style="background:{color};color:white;border-radius:12px;
                            padding:2px 12px;font-size:12px;font-weight:600;">{adv['urgency']}</span>
                    </div>
                    <p style="color:{COLORS['text_muted']};font-size:14px;margin:0;">{adv['advisory']}</p>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<br/>", unsafe_allow_html=True)
        st.dataframe(DEMO_CROPS, use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------------
    # Crop Calendar
    # -----------------------------------------------------------------------
    with tab_calendar:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Crop Sowing Calendar — Maharashtra (Demo)</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        import pandas as pd
        calendar_data = pd.DataFrame([
            {"Crop": "Tomato",  "Season": "Kharif / Rabi", "Sowing": "Jun–Jul / Oct–Nov",  "Harvest": "Oct–Nov / Feb–Mar", "Notes": "Requires staking; drip preferred"},
            {"Crop": "Onion",   "Season": "Rabi",          "Sowing": "Oct–Nov",             "Harvest": "Mar–Apr",           "Notes": "Avoid waterlogging"},
            {"Crop": "Wheat",   "Season": "Rabi",          "Sowing": "Nov–Dec",             "Harvest": "Mar–Apr",           "Notes": "GW-322 / HD-2781 varieties"},
            {"Crop": "Soybean", "Season": "Kharif",        "Sowing": "Jun–Jul",             "Harvest": "Oct",               "Notes": "Inoculate seed with Rhizobium"},
            {"Crop": "Cotton",  "Season": "Kharif",        "Sowing": "May–Jun",             "Harvest": "Nov–Dec",           "Notes": "BT varieties recommended"},
            {"Crop": "Maize",   "Season": "Kharif / Rabi", "Sowing": "Jun–Jul / Nov–Dec",  "Harvest": "Oct / Mar",         "Notes": "Hybrid varieties preferred"},
        ])
        st.dataframe(calendar_data, use_container_width=True, hide_index=True)
        st.caption("⚠️ Demonstration schedule — consult your local Krishi Vigyan Kendra for exact dates.")
