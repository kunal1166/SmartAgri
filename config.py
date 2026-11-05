# =============================================================================
# config.py — SmartAgri application configuration
# =============================================================================

APP_NAME = "SmartAgri"
APP_TAGLINE = "Your Intelligent Agricultural Decision Assistant"
APP_VERSION = "0.1.0"

# ---------------------------------------------------------------------------
# Color palette (green / white / light-neutral)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#2E7D32",        # deep green
    "primary_light": "#4CAF50",  # medium green
    "primary_pale": "#E8F5E9",   # very light green background
    "accent": "#81C784",         # soft green accent
    "white": "#FFFFFF",
    "surface": "#F9FBF9",        # off-white surface
    "border": "#C8E6C9",         # light green border
    "text_dark": "#1B2B1C",      # near-black text
    "text_muted": "#546E50",     # muted green-grey
    "warning": "#F9A825",        # amber warning
    "error": "#C62828",          # red error
    "info": "#0288D1",           # blue info
    "chart_green": ["#1B5E20", "#2E7D32", "#388E3C", "#43A047",
                    "#66BB6A", "#A5D6A7", "#C8E6C9"],
}

# ---------------------------------------------------------------------------
# Sidebar navigation pages
# ---------------------------------------------------------------------------
PAGES = [
    "🏠  Dashboard",
    "👤  Farmer Profile",
    "🤖  AI Farming Assistant",
    "🌤️  Weather Advisory",
    "🌱  Crop & Soil Advisory",
    "🔬  Disease Analysis",
    "📊  Mandi Market Intelligence",
    "📚  Knowledge Base",
]

# ---------------------------------------------------------------------------
# Internationalisation (i18n) — English default
# Future: add 'bn' (Bengali) and 'hi' (Hindi) blocks
# ---------------------------------------------------------------------------
LANGUAGES = {
    "en": "English",
    # "bn": "বাংলা",   # Bengali  — reserved for future release
    # "hi": "हिन्दी", # Hindi    — reserved for future release
}

DEFAULT_LANGUAGE = "en"

I18N: dict[str, dict[str, str]] = {
    "en": {
        # General
        "welcome": "Welcome back",
        "demo_banner": "⚠️ Demonstration data only — not real live data",
        "last_updated": "Last updated",
        # Dashboard
        "farm_overview": "Farm Overview",
        "crop_info": "Crop Information",
        "weather_overview": "Weather Overview",
        "recent_activities": "Recent Farming Activities",
        "quick_access": "Quick Access",
        # Farmer profile
        "farmer_profile": "Farmer Profile",
        # AI assistant
        "ai_assistant": "AI Farming Assistant",
        "ai_placeholder": "Ask me anything about your farm…",
        "ai_coming_soon": "Powered by IBM Granite via IBM watsonx.ai.",
        # Weather
        "weather_advisory": "Weather Advisory",
        # Crop & Soil
        "crop_soil_advisory": "Crop & Soil Advisory",
        # Disease
        "disease_analysis": "Disease Analysis",
        # Market
        "mandi_market": "Mandi Market Intelligence",
        # Knowledge base
        "knowledge_base": "Knowledge Base",
    }
}


def t(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """Translate a key to the given language, falling back to English."""
    return I18N.get(lang, I18N["en"]).get(key, key)


# ---------------------------------------------------------------------------
# Demo data metadata
# ---------------------------------------------------------------------------
DEMO_NOTICE = (
    "**⚠️ Demonstration Data** — All figures shown are sample values "
    "for illustrative purposes only and do not represent real live data."
)

# ---------------------------------------------------------------------------
# Streamlit page config defaults
# ---------------------------------------------------------------------------
PAGE_CONFIG = {
    "page_title": f"{APP_NAME} – {APP_TAGLINE}",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
