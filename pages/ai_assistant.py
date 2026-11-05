# =============================================================================
# pages/ai_assistant.py — AI Farming Assistant (IBM Granite powered)
# =============================================================================

import streamlit as st
from config import COLORS, t, APP_NAME
from utils.granite_client import chat as granite_chat, get_client, DEFAULT_MAX_TOKENS


# ---------------------------------------------------------------------------
# Session-state keys
# ---------------------------------------------------------------------------
_HISTORY_KEY = "ai_chat_history"   # list[dict]  role/content pairs
_INPUT_KEY   = "ai_user_input"     # str         current text-input value


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _bubble_user(message: str) -> None:
    st.markdown(
        f"""<div style="display:flex;justify-content:flex-end;margin-bottom:10px;">
            <div style="background:{COLORS['primary']};color:white;
                border-radius:12px 12px 2px 12px;
                padding:12px 16px;max-width:75%;font-size:14px;line-height:1.5;">
                <strong>You:</strong> {message}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def _bubble_assistant(message: str) -> None:
    st.markdown(
        f"""<div style="display:flex;justify-content:flex-start;margin-bottom:10px;">
            <div style="background:{COLORS['surface']};border:1px solid {COLORS['border']};
                border-radius:12px 12px 12px 2px;
                padding:12px 16px;max-width:75%;font-size:14px;line-height:1.5;">
                <strong style="color:{COLORS['primary']};">🤖 SmartAgri AI:</strong><br/>{message}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def _bubble_error(message: str) -> None:
    st.markdown(
        f"""<div style="display:flex;justify-content:flex-start;margin-bottom:10px;">
            <div style="background:#FFF3F3;border:1px solid #FFCDD2;
                border-radius:12px 12px 12px 2px;
                padding:12px 16px;max-width:75%;font-size:14px;line-height:1.5;">
                <strong style="color:{COLORS['error']};">⚠️ Error:</strong> {message}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def _section_header(title: str) -> None:
    st.markdown(
        f"<h3 style='color:{COLORS['primary']};margin-bottom:4px;'>{title}</h3>"
        f"<hr style='border:1px solid {COLORS['border']};margin:0 0 16px;'/>",
        unsafe_allow_html=True,
    )


def _init_history() -> None:
    """Initialise chat history in session state if not already present."""
    if _HISTORY_KEY not in st.session_state:
        st.session_state[_HISTORY_KEY] = []


def _send_message(user_text: str) -> None:
    """
    Append user message to history, call Granite, append assistant reply.
    Errors are stored as assistant messages with role='error'.
    """
    user_text = user_text.strip()
    if not user_text:
        return

    history: list[dict] = st.session_state[_HISTORY_KEY]

    # Append user turn
    history.append({"role": "user", "content": user_text})

    # Build message list for the API (user + assistant turns only)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in history
        if m["role"] in ("user", "assistant")
    ]

    # Call Granite
    reply, err = granite_chat(api_messages)

    if err:
        history.append({"role": "error", "content": err})
    else:
        history.append({"role": "assistant", "content": reply})


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render() -> None:
    _init_history()

    st.markdown(
        f"<h2 style='color:{COLORS['primary']};'>🤖 {t('ai_assistant')}</h2>",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Check connectivity once per session; show banner accordingly
    # ------------------------------------------------------------------
    client, client_err = get_client()

    if client_err:
        st.error(
            f"**IBM Granite connection unavailable.**  \n{client_err}  \n\n"
            "Check your `.env` file and restart the app.",
            icon="🔴",
        )
        _render_capabilities()
        return

    # Connected banner
    st.success(
        "**IBM Granite AI is active** — powered by IBM watsonx.ai.",
        icon="🟢",
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Chat history display
    # ------------------------------------------------------------------
    _section_header("💬 Chat")

    history: list[dict] = st.session_state[_HISTORY_KEY]

    if not history:
        st.markdown(
            f"""<div style="background:{COLORS['primary_pale']};
                border:1px solid {COLORS['border']};border-radius:8px;
                padding:16px 20px;color:{COLORS['text_muted']};font-size:14px;">
                👋 Hello! I'm your SmartAgri AI assistant powered by IBM Granite.
                Ask me anything about crops, soil, pests, irrigation, or market prices.
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        for msg in history:
            if msg["role"] == "user":
                _bubble_user(msg["content"])
            elif msg["role"] == "assistant":
                _bubble_assistant(msg["content"])
            elif msg["role"] == "error":
                _bubble_error(msg["content"])

    st.markdown("<br/>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Input form  (form prevents rerun on every keystroke)
    # ------------------------------------------------------------------
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Your question",
                placeholder=t("ai_placeholder"),
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("Send 📤", use_container_width=True)

    if submitted and user_input.strip():
        with st.spinner("SmartAgri AI is thinking…"):
            _send_message(user_input)
        st.rerun()

    # Clear chat button
    if history:
        if st.button("🗑️ Clear conversation", type="secondary"):
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Capability cards (always shown)
    # ------------------------------------------------------------------
    _render_capabilities()


def _render_capabilities() -> None:
    """Render the planned capabilities section (unchanged from original)."""
    st.markdown("<br/>", unsafe_allow_html=True)
    _section_header("🔮 Capabilities")

    caps = [
        ("🌾", "Crop Management",       "Planting schedules, irrigation advice, fertiliser plans"),
        ("🔬", "Disease Diagnosis",      "Describe symptoms and get treatment recommendations"),
        ("📈", "Market Guidance",        "Price trends and best time to sell your produce"),
        ("🌦️", "Weather-Based Advice",  "Farming actions based on current conditions"),
        ("🗣️", "Multilingual Support",  "Bengali (বাংলা) and Hindi (हिन्दी) — coming soon"),
        ("📄", "Document Q&A",          "Ask questions from uploaded farming guides (coming soon)"),
    ]
    cap_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(caps):
        with cap_cols[i % 3]:
            st.markdown(
                f"""<div style="background:{COLORS['primary_pale']};
                    border:1px solid {COLORS['border']};border-radius:8px;
                    padding:16px;margin-bottom:12px;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <p style="font-weight:700;color:{COLORS['primary']};margin:6px 0 4px;">{title}</p>
                    <p style="font-size:13px;color:{COLORS['text_muted']};margin:0;">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )
