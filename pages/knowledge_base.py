# =============================================================================
# pages/knowledge_base.py — Knowledge Base page
# =============================================================================

import streamlit as st
from config import COLORS, t


_ARTICLES = [
    {
        "category": "Soil Management",
        "title": "Understanding Soil pH and Its Impact on Crops",
        "summary": (
            "Soil pH affects nutrient availability, microbial activity, and root health. "
            "Most crops thrive between pH 6.0 and 7.5. Testing regularly helps you correct "
            "acidity with lime or alkalinity with sulphur applications."
        ),
        "tags": ["soil", "pH", "nutrients"],
    },
    {
        "category": "Irrigation",
        "title": "Drip Irrigation: Water Saving and Efficiency",
        "summary": (
            "Drip irrigation delivers water directly to the root zone, reducing evaporation by up to 60% "
            "compared to flood irrigation. Pair with fertigation for nutrient-efficient crop production."
        ),
        "tags": ["water", "drip", "efficiency"],
    },
    {
        "category": "Crop Protection",
        "title": "Integrated Pest Management (IPM) Principles",
        "summary": (
            "IPM combines biological controls, habitat manipulation, resistant crop varieties, and "
            "judicious use of pesticides. The goal is to minimise economic, health, and environmental risks."
        ),
        "tags": ["pest", "IPM", "protection"],
    },
    {
        "category": "Market",
        "title": "How to Read APMC Mandi Prices",
        "summary": (
            "APMC mandis report minimum, maximum, and modal prices. The modal price is the most "
            "frequently traded price and is the best indicator of current market value for a commodity."
        ),
        "tags": ["market", "mandi", "APMC"],
    },
    {
        "category": "Fertilisers",
        "title": "NPK Fertiliser Ratios: A Quick Guide",
        "summary": (
            "Nitrogen (N) drives vegetative growth, Phosphorus (P) supports root and flower development, "
            "and Potassium (K) builds disease resistance and fruit quality. Match the N:P:K ratio to the "
            "crop growth stage for best results."
        ),
        "tags": ["NPK", "fertiliser", "nutrition"],
    },
    {
        "category": "Government Schemes",
        "title": "PM-KISAN & Crop Insurance: Key Benefits for Farmers",
        "summary": (
            "PM-KISAN provides ₹6,000/year direct income support to small and marginal farmers. "
            "The Pradhan Mantri Fasal Bima Yojana (PMFBY) offers affordable crop insurance against "
            "natural calamities, pests, and diseases."
        ),
        "tags": ["government", "scheme", "insurance"],
    },
]

_CATEGORIES = sorted(set(a["category"] for a in _ARTICLES))


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>📚 {t('knowledge_base')}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color:{COLORS['text_muted']};'>Agricultural guides, best practices, and government scheme information.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    # --- Search and filter ---
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        query = st.text_input("🔍 Search articles", placeholder="e.g. soil pH, drip irrigation, IPM")
    with col_filter:
        cat_filter = st.selectbox("Category", ["All"] + _CATEGORIES)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Apply filters
    articles = _ARTICLES
    if cat_filter != "All":
        articles = [a for a in articles if a["category"] == cat_filter]
    if query:
        q = query.lower()
        articles = [
            a for a in articles
            if q in a["title"].lower() or q in a["summary"].lower()
            or any(q in tag for tag in a["tags"])
        ]

    if not articles:
        st.warning(f"No articles found for your search. Try a different term.")
        return

    st.markdown(
        f"<p style='color:{COLORS['text_muted']};font-size:13px;'>Showing {len(articles)} article(s)</p>",
        unsafe_allow_html=True,
    )

    # --- Article cards ---
    for article in articles:
        tag_html = " ".join(
            f"<span style='background:{COLORS['border']};color:{COLORS['primary']};border-radius:12px;"
            f"padding:2px 10px;font-size:11px;font-weight:600;margin-right:4px;'>#{tag}</span>"
            for tag in article["tags"]
        )
        st.markdown(
            f"""<div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                border-radius:10px;padding:20px 24px;margin-bottom:14px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                    <span style="background:{COLORS['primary']};color:white;border-radius:6px;
                        padding:2px 10px;font-size:11px;font-weight:600;">{article['category']}</span>
                    {tag_html}
                </div>
                <h4 style="color:{COLORS['text_dark']};margin:0 0 8px;">{article['title']}</h4>
                <p style="color:{COLORS['text_muted']};font-size:14px;margin:0;">{article['summary']}</p>
                <p style="font-size:12px;color:{COLORS['text_muted']};margin:8px 0 0;">
                    📖 Full article — coming soon.</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- Document upload placeholder ---
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};'>📄 Upload Your Own Documents</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div style="background:{COLORS['primary_pale']};border:1px solid {COLORS['border']};
            border-left:4px solid {COLORS['primary']};border-radius:8px;padding:20px 24px;">
            <h4 style="color:{COLORS['primary']};margin:0 0 8px;">RAG-Powered Document Q&A — Coming Soon</h4>
            <p style="color:{COLORS['text_muted']};margin:0;">
                Upload farming manuals, soil reports, or government circulars as PDFs.
                SmartAgri's RAG engine (powered by ChromaDB + IBM Granite) will let you
                ask questions directly from your documents in English, Bengali, or Hindi.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )
    st.file_uploader(
        "Upload PDF document",
        type=["pdf"],
        disabled=True,
        help="Document upload will be enabled once RAG integration is complete.",
    )
