# 🌾 SmartAgri — Your Intelligent Agricultural Decision Assistant

A professional agricultural dashboard built with **Python** and **Streamlit**, powered by **IBM Granite** via **IBM watsonx.ai**. SmartAgri gives Indian farmers a unified interface for crop management, live weather, real-time mandi prices, AI-assisted advice, disease analysis, and more.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Pages Overview](#pages-overview)
- [Architecture Notes](#architecture-notes)
- [Data & Privacy](#data--privacy)
- [Roadmap](#roadmap)

---

## Features

| Feature | Status |
|---|---|
| Professional agricultural dashboard | ✅ Live |
| Farm overview KPI cards | ✅ Live |
| Crop & soil information | ✅ Live |
| Live weather (Open-Meteo API) | ✅ Live |
| Live mandi prices (data.gov.in) | ✅ Live |
| AI Farming Assistant — IBM Granite | ✅ Live |
| Disease library & scouting log | ✅ Live |
| Crop calendar & soil advisory | ✅ Live |
| Knowledge base with search | ✅ Live |
| Multi-turn chat with conversation history | ✅ Live |
| Bengali & Hindi language support | 🔄 Planned |
| Photo-based disease diagnosis | 🔄 Planned |
| RAG document Q&A | 🔄 Planned |

---

## Project Structure

```
SmartAgri/
├── app.py                        # Entry point — routing, sidebar, navigation
├── config.py                     # Colours, i18n strings, page config
├── requirements.txt
├── .env                          # Credentials — never committed to git
│
├── pages/
│   ├── dashboard.py              # Main dashboard with KPIs, weather, yield chart
│   ├── farmer_profile.py         # Farmer profile viewer
│   ├── ai_assistant.py           # IBM Granite-powered chat assistant
│   ├── weather_advisory.py       # Live 7-day weather + farming advisories
│   ├── crop_soil_advisory.py     # Soil NPK analysis, crop calendar
│   ├── disease_analysis.py       # Disease library, photo diagnosis (preview)
│   ├── mandi_market.py           # Live APMC mandi prices & trend charts
│   └── knowledge_base.py         # Searchable articles, RAG placeholder
│
└── utils/
    ├── granite_client.py         # IBM Granite / watsonx.ai client wrapper
    ├── live_data.py              # Live weather (Open-Meteo) & mandi (data.gov.in)
    ├── charts.py                 # Reusable Plotly chart helpers
    └── demo_data.py              # Clearly labelled demonstration data
```

---

## Requirements

- Python **3.10+**
- A valid **IBM watsonx.ai** account with an API key and project ID
- Internet access (for IBM watsonx.ai, Open-Meteo, and data.gov.in)

All Python dependencies are listed in [`requirements.txt`](requirements.txt):

```
streamlit
python-dotenv
pydantic
requests
pandas
plotly
ibm-watsonx-ai
chromadb
pymupdf
pytest
```

---

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd SmartAgri

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root. **Never commit this file to version control** — it is already listed in `.gitignore`.

```dotenv
# IBM watsonx.ai credentials
WATSONX_APIKEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Granite model identifier
GRANITE_MODEL_ID=ibm/granite-3-3-8b-instruct
```

### Finding your credentials

| Variable | Where to find it |
|---|---|
| `WATSONX_APIKEY` | IBM Cloud → Manage → Access (IAM) → API keys |
| `WATSONX_PROJECT_ID` | IBM watsonx.ai → Projects → your project → Manage → General |
| `WATSONX_URL` | IBM watsonx.ai service URL (region-specific) |
| `GRANITE_MODEL_ID` | IBM watsonx.ai → Model library → Granite models |

> **Note:** If credentials are missing or invalid, the AI Farming Assistant page will display a clear error banner. All other pages continue to work normally.

---

## Running the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** by default.

---

## Pages Overview

### 🏠 Dashboard
The main overview page. Shows:
- Welcome banner with demo farm profile
- Five KPI cards: total area, cultivated area, active crops, estimated yield, soil health score
- Crop information table with health status
- Soil health gauge chart
- Live weather summary (falls back to demo data if unavailable)
- Seasonal yield history bar chart
- Recent farming activities log
- Quick-access cards to key sections

### 👤 Farmer Profile
Displays the demo farmer's personal details, land breakdown, and current crop list. An edit profile placeholder is included for future development.

### 🤖 AI Farming Assistant
A live multi-turn chat interface powered by **IBM Granite** via IBM watsonx.ai.
- Conversation history persists within the browser session
- A system prompt provides agricultural domain context to the model
- Loading spinner shown during inference
- Errors (authentication, rate limits, network issues) displayed inline in the chat thread
- Falls back gracefully with a clear error banner if credentials are unavailable

### 🌤️ Weather Advisory
- Live current conditions fetched from **Open-Meteo** (free, no API key required)
- 7-day forecast table, temperature range chart, and rainfall bar chart
- Farming-specific advisories derived from the forecast (spray windows, heat stress, rain alerts)
- Falls back to clearly labelled demo data if the API is unreachable

### 🌱 Crop & Soil Advisory
Three tabs:
- **Soil Analysis** — NPK progress bars, pH gauge, nutrient donut chart, improvement recommendations
- **Crop Advisory** — Urgency-rated advisory cards per crop
- **Crop Calendar** — Maharashtra sowing and harvest schedule (demo)

### 🔬 Disease Analysis
Three tabs:
- **Disease Library** — Searchable entries for common Indian crop diseases, symptoms, and treatments
- **Photo Diagnosis** — IBM Granite Vision integration preview (coming soon)
- **Scouting Log** — Field observation records (demo)

### 📊 Mandi Market Intelligence
- Live APMC mandi prices fetched from **data.gov.in** (India Open Government Data)
- Falls back to clearly labelled demo prices if the API is unreachable
- 8-week price trend line charts, commodity comparison bar chart
- Narrative market insights

### 📚 Knowledge Base
- Searchable agricultural article library (category & tag filters)
- RAG-powered document Q&A placeholder (ChromaDB + IBM Granite — coming soon)

---

## Architecture Notes

### Navigation
The app uses Streamlit's `st.navigation(position="hidden")` to suppress the automatic multi-page navigation generated from the `pages/` directory. A custom `st.radio` sidebar widget provides navigation. Each page module exposes a single `render()` function; `st.switch_page()` handles transitions.

### IBM Granite Client (`utils/granite_client.py`)
- Credentials loaded from `.env` via `python-dotenv` — never hardcoded
- `ModelInference` instance cached in `st.session_state` for the browser session (one authentication round-trip per session)
- `chat(messages)` returns a `(reply, error)` tuple — callers always know whether the call succeeded
- Errors classified into: authentication failure, rate limit, model not found, network error, project ID error

### Live Data (`utils/live_data.py`)
- Weather: Open-Meteo free API (Nashik, Maharashtra coordinates)
- Mandi prices: data.gov.in APMC commodity API
- Both functions use `@st.cache_data` with a TTL; a `LiveDataError` is raised on failure so pages can fall back gracefully to demo data

### Demonstration Data (`utils/demo_data.py`)
All non-live figures are clearly labelled as demonstration/sample data throughout the UI. No fake live data is presented as real.

### i18n (`config.py`)
All UI strings pass through the `t(key)` helper. Adding Bengali or Hindi requires only a new language block in the `I18N` dictionary — no page code changes needed.

---

## Data & Privacy

- **No personal data is collected or stored.**
- The demo farmer profile (`Ravi Kumar`) is a sample persona — not a real person.
- Weather and mandi data are fetched from public APIs and cached temporarily.
- IBM watsonx.ai processes only the messages you type in the AI Assistant. Refer to [IBM's data privacy policy](https://www.ibm.com/privacy) for details.

---

## Roadmap

- [ ] Bengali and Hindi language support
- [ ] Editable farmer profile (persistent storage)
- [ ] IBM Granite Vision — photo-based disease diagnosis
- [ ] RAG document Q&A (ChromaDB + IBM Granite)
- [ ] Location-aware weather (user-configurable coordinates)
- [ ] Push alerts for mandi price thresholds
- [ ] Multi-agent orchestration (crop planner + market analyst)

---

*SmartAgri v0.1.0 — Built with Streamlit · IBM Granite · IBM watsonx.ai*
