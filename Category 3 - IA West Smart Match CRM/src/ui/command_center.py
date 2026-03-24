"""Command Center tab -- voice panel + text input + conversation history."""
from __future__ import annotations

import datetime
import logging

import streamlit as st

logger = logging.getLogger(__name__)


def render_command_center_tab() -> None:
    """Render Command Center tab: voice panel + text input + conversation history."""
    st.markdown(
        '<h2 style="font-family: var(--font-headline);">Jarvis -- Voice Command Center</h2>',
        unsafe_allow_html=True,
    )

    # Voice panel placeholder (wired in Plan 03)
    st.markdown('<div class="voice-panel">', unsafe_allow_html=True)
    col_input, col_mic = st.columns([6, 1])
    with col_input:
        user_text = st.text_input(
            "Command",
            placeholder="Type a command or use the mic...",
            key="jarvis_command_input",
            label_visibility="collapsed",
        )
        if st.button("Send Command", key="jarvis_send_btn", type="primary"):
            if user_text and user_text.strip():
                _handle_text_command(user_text.strip())
    with col_mic:
        st.markdown("*Mic: Plan 03*")
    st.markdown('</div>', unsafe_allow_html=True)

    # Conversation history
    st.divider()
    _render_conversation_history()


def _handle_text_command(text: str) -> None:
    """Add command to history with hardcoded echo reply (Phase 4)."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")

    history: list[dict] = st.session_state.get("conversation_history", [])

    history.append({
        "role": "user",
        "text": text,
        "intent": None,
        "timestamp": ts,
        "source": "text",
    })

    jarvis_reply = f"Received: {text}"
    history.append({
        "role": "assistant",
        "text": jarvis_reply,
        "intent": "echo",
        "timestamp": ts,
    })

    st.session_state["conversation_history"] = history
    st.rerun()


def _render_conversation_history() -> None:
    """Render chronological conversation history with chat bubbles."""
    history: list[dict] = st.session_state.get("conversation_history", [])
    if not history:
        st.markdown(
            '<div class="chat-container">'
            '<p style="text-align:center; color: var(--secondary);">'
            '<strong>No conversation yet</strong><br>'
            'Type a command above or press the mic button to speak. Jarvis will respond here.'
            '</p></div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for entry in history:
        role = entry.get("role", "user")
        text = entry.get("text", "")
        intent = entry.get("intent")
        timestamp = entry.get("timestamp", "")
        bubble_class = "coordinator" if role == "user" else "jarvis"

        intent_html = ""
        if intent:
            intent_html = f' <span class="intent-badge">[Intent: {intent}]</span>'

        meta_html = f'<div class="chat-meta">{timestamp}{intent_html}</div>'

        st.markdown(
            f'<div class="chat-bubble {bubble_class}">'
            f'{text}'
            f'{meta_html}'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
