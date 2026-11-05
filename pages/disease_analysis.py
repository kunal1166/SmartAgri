# =============================================================================
# pages/disease_analysis.py — Disease Analysis page
# =============================================================================

import streamlit as st
from config import COLORS, DEMO_NOTICE, t
from utils.demo_data import DEMO_DISEASES


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>🔬 {t('disease_analysis')}</h2>",
        unsafe_allow_html=True,
    )
    st.info(DEMO_NOTICE)
    st.markdown("<br/>", unsafe_allow_html=True)

    tab_library, tab_upload, tab_scouting = st.tabs(
        ["📚 Disease Library", "📷 Photo Diagnosis (Preview)", "📋 Scouting Log"]
    )

    # -----------------------------------------------------------------------
    # Disease Library
    # -----------------------------------------------------------------------
    with tab_library:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Common Diseases — Demo Entries</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )

        search = st.text_input("🔍 Search by disease name or crop", placeholder="e.g. blight, tomato")

        diseases = DEMO_DISEASES
        if search:
            search_lower = search.lower()
            diseases = [
                d for d in DEMO_DISEASES
                if search_lower in d["name"].lower() or search_lower in d["crops_affected"].lower()
            ]
            if not diseases:
                st.warning(f"No diseases found matching '{search}'.")

        for disease in diseases:
            with st.expander(f"🦠 {disease['name']}  |  Affects: {disease['crops_affected']}"):
                col_s, col_m = st.columns(2)
                with col_s:
                    st.markdown(
                        f"**🔎 Symptoms:**\n\n{disease['symptoms']}"
                    )
                with col_m:
                    st.markdown(
                        f"**💊 Management:**\n\n{disease['management']}"
                    )

        if not search:
            st.markdown("<br/>", unsafe_allow_html=True)
            st.info(
                "🌐 The full disease library will include 200+ entries for major Indian crops. "
                "Currently showing demo entries only."
            )

    # -----------------------------------------------------------------------
    # Photo Diagnosis (Preview / Coming Soon)
    # -----------------------------------------------------------------------
    with tab_upload:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>AI Photo Diagnosis</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div style="background:{COLORS['primary_pale']};border:1px solid {COLORS['border']};
                border-left:4px solid {COLORS['primary']};border-radius:8px;padding:20px 24px;
                margin-bottom:20px;">
                <h4 style="color:{COLORS['primary']};margin:0 0 8px;">IBM Granite Vision — Coming Soon</h4>
                <p style="color:{COLORS['text_muted']};margin:0;">
                    Upload a photo of your diseased plant and our AI will identify the disease,
                    severity, and suggest treatment — powered by IBM Granite multimodal models.
                </p>
            </div>""",
            unsafe_allow_html=True,
        )

        uploaded = st.file_uploader(
            "Upload a crop/leaf image (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            disabled=True,
            help="Photo diagnosis will be enabled once IBM Granite Vision integration is complete.",
        )

        # Mock result display
        st.markdown(
            f"<h4 style='color:{COLORS['primary']};margin-top:20px;'>Sample Diagnosis Result</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                border-radius:8px;padding:20px;">
                <p style="margin:0 0 6px;"><strong>Disease Detected:</strong> Early Blight (Alternaria solani)</p>
                <p style="margin:0 0 6px;"><strong>Confidence:</strong> 87%</p>
                <p style="margin:0 0 6px;"><strong>Crop:</strong> Tomato</p>
                <p style="margin:0 0 6px;"><strong>Severity:</strong> Moderate</p>
                <p style="margin:0;"><strong>Recommendation:</strong>
                    Apply Mancozeb 75 WP @ 2 g/L. Remove and destroy infected leaves.
                    Improve air circulation. Repeat spray after 7 days.
                </p>
                <p style="margin:8px 0 0;font-size:12px;color:{COLORS['text_muted']};">
                    ⚠️ Sample output — not from a live AI model.</p>
            </div>""",
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Scouting Log
    # -----------------------------------------------------------------------
    with tab_scouting:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Pest & Disease Scouting Log</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )
        import pandas as pd
        scouting_log = pd.DataFrame([
            {"Date": "2026-10-24", "Crop": "Tomato",  "Observation": "Minor early blight on lower leaves", "Action Taken": "Mancozeb spray",  "Follow-up": "2026-10-31"},
            {"Date": "2026-10-22", "Crop": "Onion",   "Observation": "Thrips sighting on 2 plots",         "Action Taken": "Spinosad spray",   "Follow-up": "2026-10-29"},
            {"Date": "2026-10-18", "Crop": "Wheat",   "Observation": "No pest activity observed",          "Action Taken": "None",             "Follow-up": "2026-11-01"},
        ])
        st.dataframe(scouting_log, use_container_width=True, hide_index=True)
        st.caption("⚠️ Demo scouting log — not real field records.")

        st.markdown("<br/>", unsafe_allow_html=True)
        with st.expander("➕ Add New Scouting Record (coming soon)", expanded=False):
            st.info("Scouting record entry will be enabled in a future release.")
