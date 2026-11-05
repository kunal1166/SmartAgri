# =============================================================================
# utils/charts.py — Reusable Plotly chart helpers for SmartAgri
# =============================================================================

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS


# ---------------------------------------------------------------------------
# Shared layout defaults
# ---------------------------------------------------------------------------
_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=COLORS["surface"],
    font=dict(family="Segoe UI, Arial, sans-serif", color=COLORS["text_dark"], size=13),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)


def _apply_base(fig: go.Figure) -> go.Figure:
    fig.update_layout(**_BASE_LAYOUT)
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False)
    return fig


# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------
def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: list[str],
    title: str = "",
    barmode: str = "group",
) -> go.Figure:
    """Grouped or stacked bar chart."""
    fig = go.Figure()
    palette = COLORS["chart_green"]
    for i, col in enumerate(y):
        fig.add_trace(go.Bar(
            name=col,
            x=df[x],
            y=df[col],
            marker_color=palette[i % len(palette)],
        ))
    fig.update_layout(title=title, barmode=barmode)
    return _apply_base(fig)


# ---------------------------------------------------------------------------
# Line chart
# ---------------------------------------------------------------------------
def line_chart(
    df: pd.DataFrame,
    x: str,
    y: list[str],
    title: str = "",
) -> go.Figure:
    """Multi-line trend chart."""
    fig = go.Figure()
    palette = COLORS["chart_green"]
    for i, col in enumerate(y):
        fig.add_trace(go.Scatter(
            name=col,
            x=df[x],
            y=df[col],
            mode="lines+markers",
            line=dict(color=palette[i % len(palette)], width=2),
            marker=dict(size=6),
        ))
    fig.update_layout(title=title)
    return _apply_base(fig)


# ---------------------------------------------------------------------------
# Donut / Pie chart
# ---------------------------------------------------------------------------
def donut_chart(
    labels: list[str],
    values: list[float],
    title: str = "",
) -> go.Figure:
    """Donut chart."""
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=COLORS["chart_green"],
        textinfo="label+percent",
    ))
    fig.update_layout(title=title, showlegend=True)
    return _apply_base(fig)


# ---------------------------------------------------------------------------
# Gauge / indicator
# ---------------------------------------------------------------------------
def gauge_chart(
    value: float,
    title: str = "",
    suffix: str = "",
    min_val: float = 0,
    max_val: float = 100,
    thresholds: tuple[float, float] = (40, 70),
) -> go.Figure:
    """Gauge indicator for health scores / KPIs."""
    low, mid = thresholds
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 28}},
        title={"text": title, "font": {"size": 14}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickcolor": COLORS["text_muted"]},
            "bar": {"color": COLORS["primary"]},
            "steps": [
                {"range": [min_val, low], "color": "#FFCDD2"},
                {"range": [low, mid],     "color": "#FFF9C4"},
                {"range": [mid, max_val], "color": COLORS["primary_pale"]},
            ],
            "threshold": {
                "line": {"color": COLORS["primary"], "width": 3},
                "thickness": 0.75,
                "value": value,
            },
        },
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# Weather temperature range chart
# ---------------------------------------------------------------------------
def weather_range_chart(df: pd.DataFrame, day_col: str, max_col: str, min_col: str) -> go.Figure:
    """Min/Max temperature range chart for 7-day forecast."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="Max Temp",
        x=df[day_col], y=df[max_col],
        mode="lines+markers",
        line=dict(color=COLORS["warning"], width=2),
        marker=dict(size=7),
    ))
    fig.add_trace(go.Scatter(
        name="Min Temp",
        x=df[day_col], y=df[min_col],
        mode="lines+markers",
        fill="tonexty",
        fillcolor="rgba(200,230,200,0.35)",
        line=dict(color=COLORS["primary_light"], width=2),
        marker=dict(size=7),
    ))
    fig.update_layout(title="7-Day Temperature Range (°C)", yaxis_title="°C")
    return _apply_base(fig)
