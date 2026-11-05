# =============================================================================
# utils/granite_client.py — IBM Granite / watsonx.ai client for SmartAgri
#
# Credentials are loaded exclusively from environment variables (never
# hardcoded).  A .env file in the project root is supported via python-dotenv.
#
# Public API
# ----------
# get_client()  -> ModelInference | None
#     Returns a ready-to-use ModelInference instance (cached in session_state),
#     or None if credentials are missing/invalid.
#
# chat(messages, max_tokens, temperature) -> tuple[str | None, str | None]
#     Sends a conversation to Granite and returns (reply_text, None) on
#     success, or (None, human_readable_error) on failure.
# =============================================================================

from __future__ import annotations

import os
import logging
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env from the project root (safe no-op if already loaded or absent)
load_dotenv()

# ---------------------------------------------------------------------------
# Required environment variables
# ---------------------------------------------------------------------------
_REQUIRED_VARS = ["WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_URL", "GRANITE_MODEL_ID"]

# ---------------------------------------------------------------------------
# Granite system prompt — agricultural domain context
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are SmartAgri, an expert AI agricultural assistant. "
    "You help farmers in India with crop management, soil health, disease diagnosis, "
    "irrigation advice, fertiliser recommendations, pest control, and market information. "
    "Be concise, practical, and use simple language. "
    "When specific data is unavailable, give general best-practice guidance. "
    "Always prioritise farmer safety and sustainable farming."
)

# ---------------------------------------------------------------------------
# Default generation parameters (can be overridden per call)
# ---------------------------------------------------------------------------
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.3


def _check_credentials() -> tuple[dict[str, str] | None, str | None]:
    """
    Read and validate all required env vars.

    Returns (creds_dict, None) on success, or (None, error_message) if any
    variable is missing.
    """
    creds: dict[str, str] = {}
    missing: list[str] = []
    for var in _REQUIRED_VARS:
        val = os.getenv(var, "").strip()
        if not val:
            missing.append(var)
        else:
            creds[var] = val

    if missing:
        return None, (
            f"Missing environment variable(s): {', '.join(missing)}. "
            "Add them to your .env file and restart the application."
        )
    return creds, None


def get_client() -> tuple[Any | None, str | None]:
    """
    Return a cached ModelInference instance, or (None, error_str) on failure.

    The instance is cached in st.session_state to avoid re-authenticating on
    every Streamlit rerun.
    """
    import streamlit as st  # local import — keeps module usable outside Streamlit

    cache_key = "_granite_client"
    if cache_key in st.session_state and st.session_state[cache_key] is not None:
        return st.session_state[cache_key], None

    creds, err = _check_credentials()
    if err:
        return None, err

    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference

        credentials = Credentials(
            url=creds["WATSONX_URL"],
            api_key=creds["WATSONX_APIKEY"],
        )
        client = ModelInference(
            model_id=creds["GRANITE_MODEL_ID"],
            credentials=credentials,
            project_id=creds["WATSONX_PROJECT_ID"],
        )
        st.session_state[cache_key] = client
        logger.info("Granite ModelInference client initialised successfully.")
        return client, None

    except Exception as exc:
        msg = _classify_error(exc)
        logger.error("Failed to initialise Granite client: %s", exc)
        return None, msg


def chat(
    messages: list[dict[str, str]],
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> tuple[str | None, str | None]:
    """
    Send a list of messages to Granite and return (reply_text, None) on
    success, or (None, error_message) on failure.

    Each message is a dict with keys "role" ("user" | "assistant" | "system")
    and "content" (str).  The system prompt is prepended automatically unless
    the caller already includes a system message.
    """
    client, err = get_client()
    if err:
        return None, err

    # Prepend system prompt if not already present
    has_system = any(m.get("role") == "system" for m in messages)
    full_messages = messages if has_system else [
        {"role": "system", "content": SYSTEM_PROMPT},
        *messages,
    ]

    try:
        response = client.chat(
            messages=full_messages,
            params={
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        reply = response["choices"][0]["message"]["content"]
        return reply, None

    except Exception as exc:
        msg = _classify_error(exc)
        logger.error("Granite chat() failed: %s", exc)
        return None, msg


def _classify_error(exc: Exception) -> str:
    """Map SDK / network exceptions to user-friendly messages."""
    name = type(exc).__name__
    text = str(exc).lower()

    if name in ("AuthenticationError", "InvalidCredentialsError"):
        return (
            "Authentication failed. Check that WATSONX_APIKEY is correct "
            "and the API key has not expired."
        )
    if name == "ExceededLimitOfAPICalls" or "rate limit" in text or "429" in text:
        return (
            "Rate limit reached. Please wait a moment and try again."
        )
    if name in ("ApiRequestFailure",) and ("404" in text or "not found" in text):
        return (
            "Model not found. Verify GRANITE_MODEL_ID in your .env file."
        )
    if "connection" in text or "timeout" in text or "network" in text:
        return (
            "Network error. Check your internet connection and WATSONX_URL, then try again."
        )
    if "project" in text and ("not found" in text or "invalid" in text):
        return (
            "Project not found. Verify WATSONX_PROJECT_ID in your .env file."
        )
    # Generic fallback — include the exception type for diagnosability
    return f"Unexpected error ({name}): {exc}"
