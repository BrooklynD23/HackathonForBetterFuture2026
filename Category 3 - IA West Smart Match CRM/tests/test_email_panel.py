"""Integration tests for demo-mode email preview behavior."""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock, patch


class TestEmailPreviewDemoMode:
    @patch("streamlit.session_state", new_callable=dict)
    def test_render_email_preview_uses_demo_fixture(
        self,
        mock_state: dict,
        monkeypatch,
    ) -> None:
        import src.ui.email_panel as mod

        @contextmanager
        def fake_context(*args, **kwargs):
            yield

        captured_markdown: list[str] = []
        monkeypatch.setattr(mod.st, "expander", fake_context)
        monkeypatch.setattr(mod.st, "spinner", fake_context)
        monkeypatch.setattr(mod.st, "markdown", lambda value, **kwargs: captured_markdown.append(str(value)))
        monkeypatch.setattr(mod.st, "divider", lambda *args, **kwargs: None)
        monkeypatch.setattr(mod.st, "caption", lambda *args, **kwargs: None)
        monkeypatch.setattr(mod.st, "code", lambda *args, **kwargs: None)
        monkeypatch.setattr(mod.st, "download_button", lambda *args, **kwargs: None)
        monkeypatch.setattr(mod.st, "button", lambda *args, **kwargs: False)
        monkeypatch.setattr(mod, "generate_outreach_email", MagicMock(return_value={"subject_line": "live", "full_email": "live"}))

        mock_state["demo_mode"] = True
        mod.render_email_preview(
            speaker={"Name": "Alice"},
            event={"Event / Program": "AI Hackathon"},
            match_scores={"total_score": 0.9},
        )

        mod.generate_outreach_email.assert_not_called()
        assert mock_state["emails_generated"] == 1
        assert any("Invitation: Judge the AI for a Better Future Hackathon" in line for line in captured_markdown)
