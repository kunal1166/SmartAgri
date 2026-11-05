# =============================================================================
# app.py — SmartAgri entry point
# Run with:  streamlit run app.py
# =============================================================================

import streamlit as st
import sys
import os

# Ensure the project root is on the path so local imports work regardless
# of how/where the app is launched.
sys.path.insert(0, os.path.dirname(__file__))

from config import PAGE_CONFIG, PAGES, APP_NAME, APP_TAGLINE, COLORS, LANGUAGES, DEFAULT_LANGUAGE

# ---------------------------------------------------------------------------
# Pre-import all page render functions
# (required before st.navigation so callables are ready)
# ---------------------------------------------------------------------------
from pages.dashboard import render as _render_dashboard
from pages.farmer_profile import render as _render_farmer_profile
from pages.ai_assistant import render as _render_ai_assistant
from pages.weather_advisory import render as _render_weather_advisory
from pages.crop_soil_advisory import render as _render_crop_soil
from pages.disease_analysis import render as _render_disease
from pages.mandi_market import render as _render_mandi
from pages.knowledge_base import render as _render_knowledge

# ---------------------------------------------------------------------------
# Page configuration — must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(**PAGE_CONFIG)

# ---------------------------------------------------------------------------
# st.navigation — MUST be called before any sidebar widgets.
#
# This is the ONLY supported way in Streamlit 1.x to suppress the automatic
# navigation menu that Streamlit generates from the pages/ directory.
#
# Key behaviour (from Streamlit source, navigation.py line 327):
#   PagesManager.uses_pages_directory = False
#   → the pages/ directory is completely ignored for navigation.
#
# position="hidden" means Streamlit renders NO built-in nav UI at all.
# Our custom st.radio sidebar nav takes full control.
# ---------------------------------------------------------------------------
# url_path must be unique per page.
# When st.Page receives a callable, it derives url_path from the function
# name — all render() functions share the name "render", causing a collision.
# Explicit url_path values eliminate the duplicate.
_NAV_PAGES = [
    st.Page(_render_dashboard,       title="Dashboard",                icon="🏠", url_path="dashboard",          default=True),
    st.Page(_render_farmer_profile,  title="Farmer Profile",           icon="👤", url_path="farmer-profile"),
    st.Page(_render_ai_assistant,    title="AI Farming Assistant",     icon="🤖", url_path="ai-assistant"),
    st.Page(_render_weather_advisory,title="Weather Advisory",         icon="🌤️", url_path="weather-advisory"),
    st.Page(_render_crop_soil,       title="Crop & Soil Advisory",     icon="🌱", url_path="crop-soil-advisory"),
    st.Page(_render_disease,         title="Disease Analysis",         icon="🔬", url_path="disease-analysis"),
    st.Page(_render_mandi,           title="Mandi Market Intelligence",icon="📊", url_path="mandi-market"),
    st.Page(_render_knowledge,       title="Knowledge Base",           icon="📚", url_path="knowledge-base"),
]

# Map PAGES labels (from config.py) to the corresponding st.Page object.
# This lets the radio selection drive st.switch_page().
_LABEL_TO_PAGE: dict[str, st.Page] = {
    label: page for label, page in zip(PAGES, _NAV_PAGES)
}

# Call st.navigation with position="hidden".
# Returns the currently active StreamlitPage (respects URL / session state).
_current_page = st.navigation(_NAV_PAGES, position="hidden")

# Determine which PAGES label corresponds to the active page so the radio
# can be pre-selected on the correct item after a switch or browser refresh.
_active_label = next(
    (label for label, page in _LABEL_TO_PAGE.items() if page == _current_page),
    PAGES[0],  # fall back to Dashboard
)
_active_index = PAGES.index(_active_label)

# ---------------------------------------------------------------------------
# Global CSS overrides
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        /* ════════════════════════════════════════════════
           GLOBAL LAYOUT
           ════════════════════════════════════════════════ */

        .stApp {{
            background-color: {COLORS['white']};
        }}

        /* Main content area */
        .block-container {{
            padding-top: 1.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }}

        /* ════════════════════════════════════════════════
           SIDEBAR STRUCTURE
           Streamlit 1.x sidebar DOM:
             section[data-testid="stSidebar"]
               └─ div[data-testid="stSidebarContent"]
                    └─ div.stSidebarUserContent
           ════════════════════════════════════════════════ */

        /* Outer sidebar panel – set fixed width */
        section[data-testid="stSidebar"] {{
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            background-color: {COLORS['primary_pale']} !important;
            border-right: 1px solid {COLORS['border']} !important;
        }}

        /* Inner scrollable content wrapper */
        [data-testid="stSidebarContent"] {{
            background-color: {COLORS['primary_pale']} !important;
            padding: 0 !important;
            overflow-x: hidden !important;
        }}

        /* User-content div inside sidebar */
        .stSidebarUserContent {{
            padding: 0 12px 16px !important;
        }}

        /* ════════════════════════════════════════════════
           SIDEBAR NAVIGATION — st.radio
           
           BaseWeb Radio DOM (Streamlit 1.58):
             div.stRadio[data-testid="stRadio"]
               └─ [label widget label]
               └─ div[data-testid="stRadioGroup"][role="radiogroup"]
                    └─ label   ← one per option
                         ├─ input[type="radio"] (visually hidden, 0×0)
                         ├─ div.RadioMarkOuter > div.RadioMarkInner
                         └─ div  ← the text label (BaseWeb Label styled-div)

           Goal: style the <label> and its text div.
           Do NOT hide any children — RadioMarkOuter IS a div child.
           ════════════════════════════════════════════════ */

        /* Each navigation item row */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label {{
            display: flex !important;
            align-items: center !important;
            padding: 7px 10px !important;
            margin-bottom: 2px !important;
            border-radius: 6px !important;
            cursor: pointer !important;
            width: 100% !important;
            box-sizing: border-box !important;
            overflow: visible !important;
            /* NO white-space constraint — let text wrap naturally */
        }}

        /* Radio mark (circle indicator) */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label > div:first-of-type {{
            flex-shrink: 0 !important;
            margin-right: 8px !important;
        }}

        /* The text content div (BaseWeb Label) — the last div inside label */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label > div:last-of-type,
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label > p {{
            font-size: 14px !important;
            font-weight: 600 !important;
            color: {COLORS['text_dark']} !important;
            line-height: 1.45 !important;
            white-space: normal !important;
            overflow-wrap: break-word !important;
            word-break: normal !important;
            overflow: visible !important;
            flex: 1 !important;
        }}

        /* Hover state */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label:hover {{
            background-color: {COLORS['border']} !important;
        }}

        /* Selected (checked) item — using :has() where supported;
           falls back gracefully on browsers without :has() */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label:has(input:checked) {{
            background-color: {COLORS['border']} !important;
            border-left: 3px solid {COLORS['primary']} !important;
            padding-left: 8px !important;
        }}

        /* Selected item text color */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label:has(input:checked) > div:last-of-type,
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label:has(input:checked) > p {{
            color: {COLORS['primary']} !important;
        }}

        /* Radio circle — color the outer mark for selected */
        [data-testid="stSidebar"] [data-testid="stRadioGroup"] label:has(input:checked) > div:first-of-type {{
            border-color: {COLORS['primary']} !important;
            background-color: {COLORS['primary']} !important;
        }}

        /* ════════════════════════════════════════════════
           METRIC CARDS
           ════════════════════════════════════════════════ */
        [data-testid="stMetric"] {{
            background: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px 14px;
        }}

        /* ════════════════════════════════════════════════
           TABS
           ════════════════════════════════════════════════ */
        .stTabs [data-baseweb="tab"] {{
            font-weight: 600;
            color: {COLORS['text_muted']};
        }}
        .stTabs [aria-selected="true"] {{
            color: {COLORS['primary']} !important;
            border-bottom-color: {COLORS['primary']} !important;
        }}

        /* ════════════════════════════════════════════════
           DATAFRAME
           ════════════════════════════════════════════════ */
        .stDataFrame thead tr th {{
            background-color: {COLORS['primary_pale']} !important;
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
        }}

        /* ════════════════════════════════════════════════
           BUTTONS
           ════════════════════════════════════════════════ */
        .stButton > button {{
            background-color: {COLORS['primary']};
            color: white;
            border-radius: 6px;
            border: none;
            font-weight: 600;
        }}
        .stButton > button:hover {{
            background-color: {COLORS['primary_light']};
        }}

        /* ════════════════════════════════════════════════
           ALERTS
           ════════════════════════════════════════════════ */
        .stAlert {{
            border-radius: 8px;
        }}

        /* ════════════════════════════════════════════════
           SIDEBAR — LANGUAGE SELECTBOX LABEL
           ════════════════════════════════════════════════ */
        [data-testid="stSidebar"] .stSelectbox label {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: {COLORS['text_dark']} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    # Logo / branding
    st.markdown(
        f"""<div style="text-align:center;padding:12px 8px 18px;">
            <div style="font-size:2.4rem;line-height:1;">🌾</div>
            <h2 style="color:{COLORS['primary']};margin:6px 0 2px;font-size:1.25rem;
                font-weight:700;letter-spacing:-0.3px;">{APP_NAME}</h2>
            <p style="color:{COLORS['text_muted']};font-size:10px;margin:0;
                line-height:1.4;word-break:break-word;">{APP_TAGLINE}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<hr style='border:0;border-top:1px solid {COLORS['border']};margin:0 0 10px;'/>",
        unsafe_allow_html=True,
    )

    # Navigation — index keeps radio in sync with the active page returned
    # by st.navigation (handles browser refresh / direct URL access correctly).
    selected_page = st.radio(
        "Navigation",
        PAGES,
        index=_active_index,
        label_visibility="collapsed",
    )

    # Language selector (i18n placeholder)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        f"<hr style='border:1px solid {COLORS['border']};margin:0 0 12px;'/>",
        unsafe_allow_html=True,
    )
    st.selectbox(
        "🌐 Language",
        options=list(LANGUAGES.values()),
        index=0,
        help="Bengali and Hindi support coming soon.",
    )

    # Sidebar footer
    st.markdown(
        f"""<div style="margin-top:32px;padding-top:16px;border-top:1px solid {COLORS['border']};
            text-align:center;">
            <p style="font-size:11px;color:{COLORS['text_muted']};margin:0;">
                SmartAgri v0.1.0<br/>
                © 2026 — Demonstration Build
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
# If the user clicked a different nav item, switch to that page.
# st.switch_page triggers a rerun; on the next run _current_page will match.
if selected_page != _active_label:
    st.switch_page(_LABEL_TO_PAGE[selected_page])

# Execute the current page.
# st.navigation already determined which page is active (handles URL routing).
_current_page.run()
