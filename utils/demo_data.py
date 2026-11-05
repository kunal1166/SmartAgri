# =============================================================================
# utils/demo_data.py — Clearly labelled demonstration data
# All values are SAMPLE / ILLUSTRATIVE ONLY — not real live data.
# =============================================================================

import pandas as pd

# ---------------------------------------------------------------------------
# Farmer profile demo
# ---------------------------------------------------------------------------
DEMO_FARMER = {
    "name": "Ravi Kumar",
    "location": "Nashik, Maharashtra",
    "farm_size_acres": 12.5,
    "primary_crops": ["Tomato", "Onion", "Wheat"],
    "soil_type": "Black Cotton Soil (Vertisol)",
    "irrigation": "Drip Irrigation",
    "experience_years": 18,
    "phone": "+91-98XXX-XXXXX",
    "email": "ravi.kumar@example.com",
}

# ---------------------------------------------------------------------------
# Farm overview KPIs
# ---------------------------------------------------------------------------
DEMO_FARM_KPI = {
    "total_area_acres": 12.5,
    "cultivated_area_acres": 10.2,
    "fallow_area_acres": 2.3,
    "active_crops": 3,
    "estimated_yield_qtl": 142,
    "soil_health_score": 78,   # out of 100
}

# ---------------------------------------------------------------------------
# Crop information
# ---------------------------------------------------------------------------
DEMO_CROPS = pd.DataFrame([
    {"Crop": "Tomato",  "Area (acres)": 4.0, "Stage": "Flowering",    "Days to Harvest": 35, "Health": "Good"},
    {"Crop": "Onion",   "Area (acres)": 3.5, "Stage": "Bulbing",      "Days to Harvest": 50, "Health": "Fair"},
    {"Crop": "Wheat",   "Area (acres)": 2.7, "Stage": "Grain Filling","Days to Harvest": 22, "Health": "Good"},
])

# ---------------------------------------------------------------------------
# Weekly weather demo (⚠ NOT live data)
# ---------------------------------------------------------------------------
DEMO_WEATHER_CURRENT = {
    "temperature_c": 28,
    "humidity_pct": 62,
    "wind_kmh": 14,
    "condition": "Partly Cloudy",
    "rainfall_mm_today": 0,
}

DEMO_WEATHER_7DAY = pd.DataFrame({
    "Day":        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Max Temp °C":[30,    32,    29,    27,    28,    31,    33],
    "Min Temp °C":[21,    22,    20,    19,    20,    22,    23],
    "Rain mm":    [0,     0,     8,     12,    3,     0,     0],
    "Humidity %": [60,    58,    72,    78,    65,    55,    52],
})

# ---------------------------------------------------------------------------
# Yield history (past 6 seasons, demo)
# ---------------------------------------------------------------------------
DEMO_YIELD_HISTORY = pd.DataFrame({
    "Season":        ["Kharif 23", "Rabi 23-24", "Kharif 24", "Rabi 24-25", "Kharif 25", "Rabi 25-26"],
    "Tomato (qtl)":  [48, 0,  52, 0,  55, 0],
    "Onion (qtl)":   [0, 38,   0, 41,  0, 43],
    "Wheat (qtl)":   [0, 30,   0, 32,  0, 35],
})

# ---------------------------------------------------------------------------
# Recent farming activities
# ---------------------------------------------------------------------------
DEMO_ACTIVITIES = pd.DataFrame([
    {"Date": "2026-10-28", "Activity": "Drip irrigation – Tomato field",      "Status": "Completed"},
    {"Date": "2026-10-26", "Activity": "Fertiliser application – Onion field", "Status": "Completed"},
    {"Date": "2026-10-24", "Activity": "Pest scouting – all fields",           "Status": "Completed"},
    {"Date": "2026-10-22", "Activity": "Soil moisture check",                  "Status": "Completed"},
    {"Date": "2026-11-05", "Activity": "Wheat harvest (planned)",              "Status": "Upcoming"},
])

# ---------------------------------------------------------------------------
# Mandi (market) price demo
# ---------------------------------------------------------------------------
DEMO_MANDI_PRICES = pd.DataFrame([
    {"Commodity": "Tomato",  "Market": "Nashik APMC",   "Min ₹/qtl": 800,  "Max ₹/qtl": 1200, "Modal ₹/qtl": 1050},
    {"Commodity": "Onion",   "Market": "Lasalgaon APMC","Min ₹/qtl": 600,  "Max ₹/qtl": 950,  "Modal ₹/qtl": 780},
    {"Commodity": "Wheat",   "Market": "Pune APMC",     "Min ₹/qtl": 2100, "Max ₹/qtl": 2350, "Modal ₹/qtl": 2200},
    {"Commodity": "Soybean", "Market": "Latur APMC",    "Min ₹/qtl": 4200, "Max ₹/qtl": 4600, "Modal ₹/qtl": 4400},
    {"Commodity": "Cotton",  "Market": "Akola APMC",    "Min ₹/qtl": 6200, "Max ₹/qtl": 6700, "Modal ₹/qtl": 6500},
])

DEMO_PRICE_TREND = pd.DataFrame({
    "Week":          ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"],
    "Tomato ₹/qtl":  [900, 950, 1100, 1050, 980, 1020, 1080, 1050],
    "Onion ₹/qtl":   [700, 720, 750,  780,  760, 770,  790,  780],
    "Wheat ₹/qtl":   [2150,2170,2180, 2200, 2190,2210, 2220, 2200],
})

# ---------------------------------------------------------------------------
# Soil analysis demo
# ---------------------------------------------------------------------------
DEMO_SOIL = {
    "pH": 6.8,
    "Nitrogen (kg/ha)": 210,
    "Phosphorus (kg/ha)": 45,
    "Potassium (kg/ha)": 180,
    "Organic Carbon %": 0.72,
    "EC (dS/m)": 0.38,
}

# ---------------------------------------------------------------------------
# Crop advisory recommendations (demo)
# ---------------------------------------------------------------------------
DEMO_CROP_ADVISORY = [
    {
        "crop": "Tomato",
        "advisory": "Apply second dose of potassium fertiliser. Monitor for early blight.",
        "urgency": "Medium",
    },
    {
        "crop": "Onion",
        "advisory": "Bulbing stage — reduce irrigation frequency. Watch for thrips.",
        "urgency": "Low",
    },
    {
        "crop": "Wheat",
        "advisory": "Grain filling stage — ensure adequate moisture. Harvest approaching.",
        "urgency": "High",
    },
]

# ---------------------------------------------------------------------------
# Disease library (demo entries)
# ---------------------------------------------------------------------------
DEMO_DISEASES = [
    {
        "name": "Early Blight (Alternaria solani)",
        "crops_affected": "Tomato, Potato",
        "symptoms": "Dark brown circular spots with concentric rings on lower leaves.",
        "management": "Apply Mancozeb 75 WP @ 2 g/L. Remove infected leaves.",
    },
    {
        "name": "Powdery Mildew",
        "crops_affected": "Wheat, Onion, Pea",
        "symptoms": "White powdery coating on leaves and stems.",
        "management": "Spray Sulphur 80 WP @ 3 g/L or Hexaconazole @ 1 mL/L.",
    },
    {
        "name": "Stemphylium Blight",
        "crops_affected": "Onion",
        "symptoms": "Small, water-soaked lesions turning tan-coloured on leaves.",
        "management": "Apply Iprodione or Chlorothalonil fungicide.",
    },
]
