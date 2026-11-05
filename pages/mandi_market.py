# =============================================================================
# pages/mandi_market.py — Mandi Market Intelligence page
# =============================================================================

import streamlit as st
from config import COLORS, t
from utils.demo_data import DEMO_MANDI_PRICES, DEMO_PRICE_TREND
from utils.charts import bar_chart, line_chart
from utils.live_data import LiveDataError, get_live_mandi_prices


def render() -> None:
    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>📊 {t('mandi_market')}</h2>",
        unsafe_allow_html=True,
    )
    if st.button("Refresh mandi prices", key="refresh_live_mandi"):
        get_live_mandi_prices.clear()

    try:
        with st.spinner("Loading latest mandi prices..."):
            mandi_prices = get_live_mandi_prices()
        prices_are_live = True
        st.success("Live mandi data loaded from data.gov.in.")
    except LiveDataError as exc:
        mandi_prices = DEMO_MANDI_PRICES.copy()
        prices_are_live = False
        st.warning(f"{exc} Showing clearly labeled demonstration prices instead.")
    st.markdown("<br/>", unsafe_allow_html=True)

    tab_today, tab_trend, tab_insight = st.tabs(
        ["💰 Today's Prices", "📈 Price Trends", "💡 Market Insights"]
    )

    # -----------------------------------------------------------------------
    # Today's Prices
    # -----------------------------------------------------------------------
    with tab_today:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>APMC Mandi Prices — {'Live' if prices_are_live else 'Demo'} Data</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )

        # Filter by commodity
        commodities = ["All"] + sorted(mandi_prices["Commodity"].unique().tolist())
        selected = st.selectbox("Filter by Commodity", commodities)

        df = mandi_prices if selected == "All" else mandi_prices[mandi_prices["Commodity"] == selected]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # KPI row
        st.markdown("<br/>", unsafe_allow_html=True)
        kpi_cols = st.columns(3)
        for i, (_, row) in enumerate(mandi_prices.head(3).iterrows()):
            with kpi_cols[i]:
                st.markdown(
                    f"""<div style="background:{COLORS['primary_pale']};border:1px solid {COLORS['border']};
                        border-radius:8px;padding:16px;text-align:center;">
                        <p style="font-size:13px;color:{COLORS['text_muted']};margin:0;">{row.Commodity}</p>
                        <p style="font-size:24px;font-weight:700;color:{COLORS['primary']};margin:4px 0;">
                            ₹{row['Modal ₹/qtl']:,.0f}</p>
                        <p style="font-size:12px;color:{COLORS['text_muted']};margin:0;">
                            Modal price / qtl — {row['Market']}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )

        if prices_are_live:
            st.caption(
                f"Latest available daily arrival records · data.gov.in · "
                f"Arrival dates: {', '.join(mandi_prices['Arrival Date'].dropna().unique()[:3])}"
            )
        else:
            st.caption("Demonstration prices — not live market data.")

    # -----------------------------------------------------------------------
    # Price Trends
    # -----------------------------------------------------------------------
    with tab_trend:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>8-Week Price Trends — Demo Data</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )

        selected_crops = st.multiselect(
            "Select commodities to compare",
            options=["Tomato ₹/qtl", "Onion ₹/qtl", "Wheat ₹/qtl"],
            default=["Tomato ₹/qtl", "Onion ₹/qtl"],
        )

        if selected_crops:
            fig_trend = line_chart(
                df=DEMO_PRICE_TREND,
                x="Week",
                y=selected_crops,
                title="Weekly Modal Price Trend (₹/qtl) — Demo",
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Select at least one commodity above.")

        # Bar comparison
        st.markdown("<br/>", unsafe_allow_html=True)
        fig_bar = bar_chart(
            df=DEMO_MANDI_PRICES,
            x="Commodity",
            y=["Min ₹/qtl", "Modal ₹/qtl", "Max ₹/qtl"],
            title="Price Range by Commodity (₹/qtl) — Demo",
            barmode="group",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------------------------------------------------
    # Market Insights
    # -----------------------------------------------------------------------
    with tab_insight:
        st.markdown(
            f"<h3 style='color:{COLORS['primary']};'>Market Intelligence Insights — Demo Examples</h3>"
            f"<hr style='border:1px solid {COLORS['border']};margin:6px 0 16px;'/>",
            unsafe_allow_html=True,
        )

        insights = [
            ("📈 Tomato — Upward Trend",
             "Modal prices have risen ~17% over the past 8 weeks. Festival season demand and "
             "reduced supply from Pune belt are key drivers. Consider holding stock for 1–2 weeks.",
             COLORS["primary"]),
            ("➡️ Onion — Stable Range",
             "Prices have remained in the ₹750–790 range for the past 4 weeks at Lasalgaon APMC. "
             "National buffer stock management keeping prices stable.",
             COLORS["accent"]),
            ("⚠️ Wheat — Near MSP",
             "Current modal price (₹2,200/qtl) is near the MSP of ₹2,275/qtl. "
             "If prices fall below MSP, consider selling through government procurement channels.",
             COLORS["warning"]),
        ]

        for title, body, color in insights:
            st.markdown(
                f"""<div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                    border-left:4px solid {color};border-radius:8px;padding:16px 20px;margin-bottom:12px;">
                    <p style="font-weight:700;color:{COLORS['text_dark']};margin:0 0 6px;">{title}</p>
                    <p style="color:{COLORS['text_muted']};font-size:14px;margin:0;">{body}</p>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            f"""<div style="background:{COLORS['primary_pale']};border:1px solid {COLORS['border']};
                border-radius:8px;padding:16px 20px;">
                <h4 style="color:{COLORS['primary']};margin:0 0 8px;">ℹ️ About this data</h4>
                <p style="color:{COLORS['text_muted']};margin:0;">
                    Live prices above are sourced from <strong>Agmarknet (data.gov.in)</strong>.
                    These are the latest available daily market-arrival records, not tick-by-tick prices.
                    The trend chart and insight examples on this page remain demonstration data.
                </p>
            </div>""",
            unsafe_allow_html=True,
        )
