"""Unit tests for Command Center tab: text command handling and conversation history."""
from __future__ import annotations

import re
import sys
from unittest.mock import MagicMock, call, patch

import pytest

# conftest.py ensures streamlit is mocked before import
import streamlit as st

from src.ui.command_center import _handle_text_command, _render_conversation_history


# ── Helpers ────────────────────────────────────────────────────────────────


def _reset_history() -> None:
    """Clear conversation_history in session_state before each test."""
    st.session_state["conversation_history"] = []


# ── Tests: _handle_text_command ─────────────────────────────────────────────


class TestHandleTextCommand:
    def setup_method(self) -> None:
        _reset_history()
        st.rerun.reset_mock()  # type: ignore[attr-defined]
        st.markdown.reset_mock()  # type: ignore[attr-defined]

    def test_text_command_appends_to_history(self) -> None:
        """handle_text_command appends 2 entries: user + assistant."""
        _handle_text_command("hello")
        history = st.session_state["conversation_history"]
        assert len(history) == 2

    def test_user_entry_fields(self) -> None:
        """User entry has role=user, correct text, intent=None."""
        _handle_text_command("hello")
        history = st.session_state["conversation_history"]
        user_entry = history[0]
        assert user_entry["role"] == "user"
        assert user_entry["text"] == "hello"
        assert user_entry["intent"] is None

    def test_assistant_entry_fields(self) -> None:
        """Assistant entry has role=assistant, echo text, intent=echo."""
        _handle_text_command("hello")
        history = st.session_state["conversation_history"]
        assistant_entry = history[1]
        assert assistant_entry["role"] == "assistant"
        assert assistant_entry["text"] == "Received: hello"
        assert assistant_entry["intent"] == "echo"

    def test_both_entries_have_timestamp(self) -> None:
        """Both entries have a timestamp matching HH:MM:SS format."""
        _handle_text_command("hello")
        history = st.session_state["conversation_history"]
        ts_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        assert ts_pattern.match(history[0]["timestamp"]), "user timestamp format invalid"
        assert ts_pattern.match(history[1]["timestamp"]), "assistant timestamp format invalid"

    def test_multiple_commands_grow_history(self) -> None:
        """Each command appends 2 entries; two commands → 4 entries."""
        _handle_text_command("first")
        _handle_text_command("second")
        history = st.session_state["conversation_history"]
        assert len(history) == 4

    def test_history_persists_across_calls(self) -> None:
        """History grows additively — entries from prior calls are retained."""
        _handle_text_command("one")
        _handle_text_command("two")
        history = st.session_state["conversation_history"]
        texts = [e["text"] for e in history]
        assert "one" in texts
        assert "Received: one" in texts
        assert "two" in texts
        assert "Received: two" in texts

    def test_rerun_called_after_command(self) -> None:
        """st.rerun() is called after appending to history."""
        _handle_text_command("hello")
        st.rerun.assert_called_once()  # type: ignore[attr-defined]


# ── Tests: _render_conversation_history ─────────────────────────────────────


class TestRenderConversationHistory:
    def setup_method(self) -> None:
        _reset_history()
        st.markdown.reset_mock()  # type: ignore[attr-defined]

    def test_render_empty_history_shows_guidance_text(self) -> None:
        """Empty history renders 'No conversation yet' guidance."""
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "No conversation yet" in rendered_html

    def test_render_empty_history_uses_chat_container(self) -> None:
        """Empty history renders a chat-container div."""
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "chat-container" in rendered_html

    def test_render_with_entries_shows_chat_bubbles(self) -> None:
        """Entries are rendered with chat-bubble class."""
        st.session_state["conversation_history"] = [
            {"role": "user", "text": "hi", "intent": None, "timestamp": "12:00:00"},
            {"role": "assistant", "text": "Received: hi", "intent": "echo", "timestamp": "12:00:00"},
        ]
        st.markdown.reset_mock()
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "chat-bubble" in rendered_html

    def test_render_coordinator_bubble_for_user(self) -> None:
        """User entry uses coordinator bubble class."""
        st.session_state["conversation_history"] = [
            {"role": "user", "text": "hi", "intent": None, "timestamp": "12:00:00"},
        ]
        st.markdown.reset_mock()
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "coordinator" in rendered_html

    def test_render_jarvis_bubble_for_assistant(self) -> None:
        """Assistant entry uses jarvis bubble class."""
        st.session_state["conversation_history"] = [
            {"role": "assistant", "text": "Received: hi", "intent": "echo", "timestamp": "12:00:00"},
        ]
        st.markdown.reset_mock()
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "jarvis" in rendered_html

    def test_render_intent_badge_for_assistant(self) -> None:
        """Assistant entry with intent renders an intent-badge span."""
        st.session_state["conversation_history"] = [
            {"role": "assistant", "text": "Received: hi", "intent": "echo", "timestamp": "12:00:00"},
        ]
        st.markdown.reset_mock()
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "intent-badge" in rendered_html
        assert "echo" in rendered_html

    def test_no_guidance_text_when_history_not_empty(self) -> None:
        """'No conversation yet' text is absent when history has entries."""
        st.session_state["conversation_history"] = [
            {"role": "user", "text": "hello", "intent": None, "timestamp": "12:00:00"},
        ]
        st.markdown.reset_mock()
        _render_conversation_history()
        all_calls = st.markdown.call_args_list
        rendered_html = " ".join(str(c) for c in all_calls)
        assert "No conversation yet" not in rendered_html
