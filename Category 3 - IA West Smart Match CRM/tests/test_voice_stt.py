"""Unit tests for STT service module (src/voice/stt.py)."""

import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest


def _make_segments(texts: list[str]) -> list[SimpleNamespace]:
    """Build fake segment objects with .text attribute."""
    return [SimpleNamespace(text=t) for t in texts]


class TestTranscribeAudioBytes:
    """Tests for transcribe_audio_bytes function."""

    def test_transcribe_returns_string(self) -> None:
        """transcribe_audio_bytes with mocked model returns joined segment text."""
        from src.voice.stt import transcribe_audio_bytes

        mock_model = MagicMock()
        mock_model.transcribe.return_value = (
            _make_segments([" Hello", " world."]),
            SimpleNamespace(language="en"),
        )

        result = transcribe_audio_bytes(b"\x00" * 1000, mock_model)

        assert isinstance(result, str)
        assert "Hello" in result
        assert "world" in result

    def test_transcribe_empty_bytes_returns_empty(self) -> None:
        """transcribe_audio_bytes returns empty string for empty bytes input."""
        from src.voice.stt import transcribe_audio_bytes

        mock_model = MagicMock()
        result = transcribe_audio_bytes(b"", mock_model)

        assert result == ""
        mock_model.transcribe.assert_not_called()

    def test_transcribe_none_input_returns_empty(self) -> None:
        """transcribe_audio_bytes returns empty string for None input."""
        from src.voice.stt import transcribe_audio_bytes

        mock_model = MagicMock()
        result = transcribe_audio_bytes(None, mock_model)  # type: ignore[arg-type]

        assert result == ""
        mock_model.transcribe.assert_not_called()

    def test_transcribe_cleans_up_temp_file(self) -> None:
        """transcribe_audio_bytes removes temp file after transcription."""
        from src.voice.stt import transcribe_audio_bytes

        mock_model = MagicMock()
        mock_model.transcribe.return_value = (
            _make_segments(["Clean up test."]),
            SimpleNamespace(language="en"),
        )

        created_paths: list[str] = []

        original_named_temp = tempfile.NamedTemporaryFile

        def tracking_named_temp(**kwargs):
            tmp = original_named_temp(**kwargs)
            created_paths.append(tmp.name)
            return tmp

        with patch("src.voice.stt.tempfile.NamedTemporaryFile", side_effect=tracking_named_temp):
            transcribe_audio_bytes(b"\x00" * 100, mock_model)

        for path in created_paths:
            assert not Path(path).exists(), f"Temp file was not cleaned up: {path}"

    def test_transcribe_joins_multiple_segments(self) -> None:
        """transcribe_audio_bytes joins multiple segment texts with space."""
        from src.voice.stt import transcribe_audio_bytes

        mock_model = MagicMock()
        mock_model.transcribe.return_value = (
            _make_segments(["First segment.", "Second segment."]),
            SimpleNamespace(language="en"),
        )

        result = transcribe_audio_bytes(b"\x00" * 1000, mock_model)

        assert "First segment" in result
        assert "Second segment" in result


class TestLoadSttModel:
    """Tests for load_stt_model function."""

    def test_load_stt_model_constructs_whisper_model(self) -> None:
        """load_stt_model constructs WhisperModel with base, cpu, int8."""
        from src.voice import stt as stt_module

        mock_whisper_cls = MagicMock()
        mock_whisper_cls.return_value = MagicMock()

        with patch.dict(
            "sys.modules",
            {"faster_whisper": MagicMock(WhisperModel=mock_whisper_cls)},
        ):
            from importlib import reload
            reload(stt_module)
            result = stt_module.load_stt_model()

        mock_whisper_cls.assert_called_once_with(
            stt_module.WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type=stt_module.WHISPER_COMPUTE_TYPE,
        )
        assert result is not None
