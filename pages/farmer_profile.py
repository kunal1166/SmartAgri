# =============================================================================
# pages/farmer_profile.py — Farmer Profile page
# =============================================================================

import streamlit as st
from config import DEMO_NOTICE, COLORS, t
from utils.demo_data import DEMO_FARMER, DEMO_FARM_KPI, DEMO_CROPS


def _field(label: str, value: str) -> None:
    st.markdown(
        f"""<div style="padding:10px 0;border-bottom:1px solid {COLORS['border']};">
            <span style="font-size:13px;color:{COLORS['text_muted']};font-weight:500;">{label}</span><br/>
            <span style="font-size:15px;color:{COLORS['text_dark']};font-weight:600;">{value}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>👤 {t('farmer_profile')}</h2>",
        unsafe_allow_html=True,
    )
    st.info(DEMO_NOTICE)
    st.markdown("<br/>", unsafe_allow_html=True)

    col_avatar, col_info = st.columns([1, 3])

    with col_avatar:
        st.markdown(
            f"""<div style="
                background:{COLORS['primary_pale']};
                border:2px solid {COLORS['border']};
                border-radius:50%;
                width:120px;height:120px;
                display:flex;align-items:center;justify-content:center;
                font-size:3rem;margin:0 auto;
            ">👨‍🌾</div>
            <p style="text-align:center;font-weight:700;color:{COLORS['primary']};
                margin-top:12px;font-size:1.1rem;">{DEMO_FARMER['name']}</p>
            <p style="text-align:center;color:{COLORS['text_muted']};font-size:13px;margin:0;">
                {DEMO_FARMER['location']}</p>""",
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};margin-bottom:0;'>Personal Details</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            _field("Full Name",            DEMO_FARMER["name"])
            _field("Location",             DEMO_FARMER["location"])
            _field("Phone",                DEMO_FARMER["phone"])
            _field("Email",                DEMO_FARMER["email"])
        with c2:
            _field("Farm Size",            f"{DEMO_FARMER['farm_size_acres']} acres")
            _field("Primary Crops",        ", ".join(DEMO_FARMER["primary_crops"]))
            _field("Soil Type",            DEMO_FARMER["soil_type"])
            _field("Irrigation System",    DEMO_FARMER["irrigation"])
            _field("Farming Experience",   f"{DEMO_FARMER['experience_years']} years")

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- Farm land breakdown ---
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>🏡 Farm Land Breakdown</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )
    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        st.metric("Total Area",      f"{DEMO_FARM_KPI['total_area_acres']} acres")
    with bc2:
        st.metric("Cultivated Area", f"{DEMO_FARM_KPI['cultivated_area_acres']} acres")
    with bc3:
        st.metric("Fallow Area",     f"{DEMO_FARM_KPI['fallow_area_acres']} acres")

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- Crop list ---
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>🌱 Current Crops</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )
    st.dataframe(DEMO_CROPS, use_container_width=True, hide_index=True)

    # --- Edit profile placeholder ---
    st.markdown("<br/>", unsafe_allow_html=True)
    with st.expander("✏️ Edit Profile (coming soon)", expanded=False):
        st.info("Profile editing will be enabled in a future release.")
