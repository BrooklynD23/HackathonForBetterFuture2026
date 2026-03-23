# Phase 4: Voice I/O Foundation - Research

**Researched:** 2026-03-23
**Domain:** Browser mic capture (streamlit-webrtc), speech-to-text (faster-whisper), text-to-speech (KittenTTS), Streamlit chat UI
**Confidence:** MEDIUM — KittenTTS is developer preview; streamlit-webrtc audio receiver pattern is MEDIUM; faster-whisper and Streamlit APIs are HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Voice Input Method**
- Use streamlit-webrtc with audio_frame_callback for browser mic capture — enables real-time frame streaming for live STT
- Use faster-whisper "base" model (~150MB) for STT — fast enough for CPU demo, good accuracy balance
- Transcribe per-utterance: push-to-talk captures a full clip, transcribes on release, shows in the input field
- Single shared input field for both text typing and STT transcript insertion — unified conversation flow

**TTS Voice and Playback**
- Use KittenTTS voice "af_heart" for Jarvis — warm, clear, professional tone
- Auto-play TTS output via `st.audio(autoplay=True)` — more natural demo UX, Jarvis "speaks" immediately after each response
- Sentence-chunked TTS generation — split response text on `.`/`?`, generate per sentence, play sequentially to reduce perceived latency
- Cache TTS model in `st.session_state["tts_model"]` — load once per session on first use, avoids 3-5s cold start on every call

**Command Center Tab Layout**
- Command Center is the first tab in the tab bar — primary interaction surface for v2.0 Jarvis, existing tabs shift right
- Voice panel (input field + mic button + TTS audio player) positioned at the top of the Command Center tab
- Chat-style conversation bubbles — coordinator messages aligned left, Jarvis responses aligned right, with timestamps
- Subtle intent badge on Jarvis responses (e.g., `[Intent: echo]`) — in Phase 4 this is a hardcoded echo; real parsing arrives Phase 5

### Claude's Discretion
- Exact CSS styling of chat bubbles and Command Center layout
- streamlit-webrtc configuration details (STUN server, codec selection)
- WAV buffer encoding details for TTS pipeline
- Error messaging and fallback UX when mic access is denied or TTS fails

### Deferred Ideas (OUT OF SCOPE)
- Real-time streaming transcription during speech (VOICE-05 — requires VAD + streaming Whisper)
- Wake word activation ("Hey Jarvis") for hands-free operation (VOICE-06)
- Intent parsing and action proposal (Phase 5 scope — HITL-01 through HITL-03)
- Agent dispatch and execution (Phase 6 scope — ORCH-01 through ORCH-03)
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VOICE-01 | Coordinator can type text commands in a Command Center tab and receive parsed intent responses | st.chat_message pattern + st.chat_input or st.text_input; hardcoded echo reply; new Command Center tab prepended to st.tabs() |
| VOICE-02 | Coordinator can hear Jarvis speak responses via KittenTTS voice synthesis | KittenTTS.generate() → numpy array → soundfile WAV bytes → st.audio(autoplay=True); model cached in session_state |
| VOICE-03 | Coordinator can use push-to-talk to speak commands, transcribed via faster-whisper STT | streamlit-webrtc SENDONLY + audio_receiver.get_frames() on stop; write WAV to tempfile; WhisperModel("base").transcribe() on release |
| VOICE-04 | Coordinator can see full conversation history (voice + text) in the Command Center | st.session_state["conversation_history"] list[dict]; rendered via st.chat_message loop; persists for session |
</phase_requirements>

---

## Summary

Phase 4 builds an isolated voice I/O layer — push-to-talk mic capture, STT transcription, TTS playback, and a chat-history display — before any real intent parsing or agent dispatch is added. The coordinator presses a mic button, speaks, and on release sees the transcript in the input field; submitting any command (text or transcribed) plays a hardcoded Jarvis echo reply via synthesized speech.

The key technical complexity is assembling three independent libraries into a coherent push-to-talk UX: **streamlit-webrtc** accumulates `av.AudioFrame` objects via `audio_receiver.get_frames()` while streaming, the frames are assembled into a WAV file when the user stops recording, **faster-whisper** transcribes that WAV file, and **KittenTTS** synthesizes the Jarvis reply. These three libraries have no shared interface — the bridge is raw bytes (WAV at 16 kHz for STT input, numpy float32 array at 24 kHz for TTS output).

**Critical finding: "af_heart" is not a valid KittenTTS voice.** The eight valid voices for `KittenML/kitten-tts-mini-0.8` are: `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo`. CONTEXT.md specifies "af_heart" but this does not exist in the model. Use `"Bella"` as the default Jarvis voice (warm, female) or let the planner choose. This is a blocker for VOICE-02 if not resolved before coding.

**Primary recommendation:** Build `voice/stt.py` and `voice/tts.py` as pure Python services (no Streamlit imports) first. Wire to UI only in `src/ui/command_center.py`. Use streamlit-webrtc `audio_receiver` (polling pattern, not callback) for frame accumulation, and write frames to a temp WAV file before calling faster-whisper. Cache TTS model in `st.session_state["tts_model"]` to avoid 3-5s cold start.

---

## Standard Stack

### Core (Phase 4 additions only)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| kittentts | 0.8.1 (wheel) | TTS: text → numpy audio array at 24 kHz | Project constraint; CPU-only ONNX, 8 voices, ~80MB mini model |
| faster-whisper | latest pip | STT: audio file → transcript text | 4× faster than openai-whisper, CPU int8, bundles FFmpeg via PyAV |
| streamlit-webrtc | 0.6.0 | Browser mic capture → server-side audio frames | Only option for real-time audio streaming from Streamlit browser session |
| soundfile | latest pip | numpy float32 array → WAV BytesIO for st.audio playback | Required bridge between KittenTTS output and Streamlit audio widget |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| av (pyav) | pulled by streamlit-webrtc | Decode av.AudioFrame to numpy for WAV assembly | In audio_receiver frame loop |
| numpy | 1.26.4 (already present) | KittenTTS returns float32 ndarray; frame concatenation | Already in requirements.txt |
| tempfile (stdlib) | — | Write assembled WAV to disk for faster-whisper | faster-whisper needs a file path or numpy array at correct dtype |
| threading (stdlib) | — | Thread-safe audio frame buffer between webrtc thread and main | Required by streamlit-webrtc threading model |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| streamlit-webrtc audio_receiver | st.audio_input (native) | st.audio_input is simpler but captures only after stop-click; webrtc allows start/stop button control; both produce WAV — either works for push-to-talk |
| faster-whisper "base" model | "tiny" model (~75MB) | "tiny" is faster but lower accuracy; "base" is the locked decision |
| KittenTTS mini-0.8 | KittenTTS nano-0.8 (~25MB) | nano is smaller but fewer voices and lower quality |

**Installation:**
```bash
# KittenTTS — MUST use wheel, NOT pip install kittentts directly
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl

# STT
pip install faster-whisper

# Browser mic capture
pip install streamlit-webrtc

# WAV serialization
pip install soundfile
```

**requirements.txt lines to add:**
```
# ── Voice I/O (Phase 4) ───────────────────────────────────
# KittenTTS — install from GitHub wheel (see README for command)
faster-whisper
streamlit-webrtc==0.6.0
soundfile
```

> NOTE: KittenTTS cannot be pinned in requirements.txt as a standard PyPI package — it must be installed from the GitHub wheel URL. Document this in the project README and add a `# kittentts installed via wheel` comment.

---

## Architecture Patterns

### Recommended Project Structure (Phase 4 only)

```
Category 3 - IA West Smart Match CRM/src/
├── app.py                    # MODIFIED: prepend "Command Center" to st.tabs()
├── config.py                 # MODIFIED: add KITTENTTS_VOICE, WHISPER_MODEL_SIZE constants
├── runtime_state.py          # MODIFIED: add conversation_history, tts_model, stt_model keys
│
├── voice/                    # NEW — isolated, no Streamlit imports
│   ├── __init__.py
│   ├── stt.py                # faster-whisper wrapper: audio_bytes -> str
│   └── tts.py                # KittenTTS wrapper: str -> bytes (WAV)
│
└── ui/
    └── command_center.py     # NEW — renders Command Center tab with voice panel + chat history
```

Note: `voice/bridge.py` is deferred — Phase 4 wires stt.py and tts.py directly from command_center.py. Bridge abstraction belongs in Phase 5 when coordinator intent parsing is added.

### Pattern 1: KittenTTS — Text to WAV Bytes

**What:** Load model once into session_state; call `generate()` to get numpy array; serialize to WAV with soundfile.

**When to use:** Every Jarvis response (hardcoded echo in Phase 4, real response in Phase 5+).

**CRITICAL — Voice Name:** The voice `"af_heart"` specified in CONTEXT.md does NOT exist in KittenTTS 0.8.1. Valid voices: `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo`. Use `"Bella"` as the default warm female voice that most closely matches the intent.

```python
# voice/tts.py
# Source: https://github.com/KittenML/KittenTTS + https://huggingface.co/KittenML/kitten-tts-mini-0.8
import io
import logging

import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)

KITTENTTS_MODEL_ID = "KittenML/kitten-tts-mini-0.8"
KITTENTTS_SAMPLE_RATE = 24000


def load_tts_model():
    """Load KittenTTS model. Call once; cache result in session_state."""
    from kittentts import KittenTTS  # import here to avoid import-time model load
    return KittenTTS(KITTENTTS_MODEL_ID)


def synthesize_to_wav_bytes(text: str, model, voice: str = "Bella") -> bytes:
    """Return WAV bytes for the given text using the provided KittenTTS model.

    Args:
        text: Input text to synthesize. Must be non-empty.
        model: A loaded KittenTTS instance (from load_tts_model()).
        voice: One of: Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo.

    Returns:
        WAV-encoded bytes at 24 kHz.

    Raises:
        ValueError: If text is empty after stripping.
    """
    if not text.strip():
        raise ValueError("Cannot synthesize empty text")
    audio: np.ndarray = model.generate(text, voice=voice)
    buffer = io.BytesIO()
    sf.write(buffer, audio, samplerate=KITTENTTS_SAMPLE_RATE, format="WAV")
    return buffer.getvalue()


def split_into_sentences(text: str) -> list[str]:
    """Split text on sentence boundaries for chunked TTS generation."""
    import re
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    return [s for s in sentences if s.strip()]
```

### Pattern 2: faster-whisper — Audio Bytes to Text

**What:** Write audio bytes to a temp file; call `WhisperModel.transcribe()`; join segment texts.

**When to use:** After push-to-talk recording stops and frames are assembled into WAV.

**Audio format required:** WAV at 16 kHz (matches `st.audio_input` default and is what streamlit-webrtc delivers via av.AudioFrame).

```python
# voice/stt.py
# Source: https://github.com/SYSTRAN/faster-whisper README
import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

WHISPER_MODEL_SIZE = "base"
WHISPER_COMPUTE_TYPE = "int8"  # CPU-optimized


def load_stt_model():
    """Load faster-whisper model. Call once; cache result in session_state."""
    from faster_whisper import WhisperModel
    return WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type=WHISPER_COMPUTE_TYPE)


def transcribe_audio_bytes(audio_bytes: bytes, model) -> str:
    """Transcribe WAV audio bytes to text.

    Args:
        audio_bytes: WAV file bytes at 16 kHz mono.
        model: A loaded WhisperModel instance (from load_stt_model()).

    Returns:
        Transcribed text, or empty string if no speech detected.
    """
    if not audio_bytes:
        return ""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        segments, _info = model.transcribe(
            tmp_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 300},
        )
        # segments is a generator — must iterate to trigger transcription
        texts = [seg.text for seg in segments]
        return " ".join(texts).strip()
    except Exception as exc:
        logger.error("STT transcription failed: %s", exc)
        return ""
    finally:
        Path(tmp_path).unlink(missing_ok=True)
```

### Pattern 3: streamlit-webrtc Push-to-Talk — SENDONLY Audio Receiver

**What:** Use `WebRtcMode.SENDONLY` with `audio_receiver_size=256` to stream browser mic to server. When streaming stops (user releases button by clicking Stop), drain `audio_receiver.get_frames()`, convert `av.AudioFrame` objects to numpy, concatenate, write to WAV, then transcribe.

**When to use:** Push-to-talk button triggers Start; coordinator speaks; Stop triggers transcription.

**Key API distinction:** Use `audio_receiver`, NOT `audio_frame_callback`. The receiver polling pattern (from the official example `10_sendonly_audio.py`) is the correct approach for accumulating a full utterance before STT.

```python
# src/ui/command_center.py (voice panel section)
# Source: https://github.com/whitphx/streamlit-webrtc/blob/main/pages/10_sendonly_audio.py
import av
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer


def render_push_to_talk_panel(stt_model) -> str | None:
    """Render push-to-talk panel. Returns transcript on stop, None otherwise."""
    webrtc_ctx = webrtc_streamer(
        key="jarvis-ptt",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    # When streaming just stopped — drain the accumulated frames
    if not webrtc_ctx.state.playing and webrtc_ctx.audio_receiver:
        frames = []
        try:
            while True:
                frames.extend(webrtc_ctx.audio_receiver.get_frames(timeout=0))
        except Exception:
            pass  # Queue empty — normal exit condition

        if frames:
            return _frames_to_wav_bytes(frames)
    return None


def _frames_to_wav_bytes(frames: list) -> bytes:
    """Convert av.AudioFrame list to WAV bytes at 16 kHz."""
    import io
    import soundfile as sf

    arrays = [frame.to_ndarray().flatten().astype(np.float32) for frame in frames]
    audio = np.concatenate(arrays)
    # av frames are typically s16 format; normalize to float32 range [-1, 1]
    if audio.max() > 1.0:
        audio = audio / 32768.0
    sample_rate = frames[0].sample_rate if frames else 16000
    buffer = io.BytesIO()
    sf.write(buffer, audio, samplerate=sample_rate, format="WAV")
    return buffer.getvalue()
```

### Pattern 4: st.chat_message — Conversation History Display

**What:** Loop over `st.session_state["conversation_history"]` and render each message with `st.chat_message()`.

**When to use:** Bottom section of Command Center tab; renders after every interaction.

**Name values:** `"user"` for coordinator messages (person icon), `"assistant"` for Jarvis replies (bot icon).

```python
# Source: https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
def render_conversation_history(history: list[dict]) -> None:
    """Render chronological conversation history with chat bubbles."""
    for entry in history:
        role = entry.get("role", "user")  # "user" | "assistant"
        with st.chat_message(role):
            st.write(entry["text"])
            if entry.get("intent"):
                st.caption(f"[Intent: {entry['intent']}]")
            if entry.get("timestamp"):
                st.caption(entry["timestamp"])
```

### Pattern 5: Session State Keys for Phase 4

**Extension of `init_runtime_state()` in `src/runtime_state.py`:**

```python
# Add to init_runtime_state() — these are the Phase 4 new keys
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "tts_model" not in st.session_state:
    st.session_state["tts_model"] = None   # loaded lazily on first use
if "stt_model" not in st.session_state:
    st.session_state["stt_model"] = None   # loaded lazily on first use
```

`conversation_history` entry schema:
```python
{
    "role": "user" | "assistant",
    "text": str,
    "intent": str | None,    # None in Phase 4 (hardcoded echo); populated in Phase 5
    "timestamp": str,         # e.g., "14:32:05"
}
```

### Anti-Patterns to Avoid

- **No Streamlit imports in `voice/stt.py` or `voice/tts.py`:** These modules must be pure Python. UI error handling (st.error) belongs only in `command_center.py`.
- **Do not call `model.transcribe()` with a raw BytesIO object:** faster-whisper requires a file path string or numpy array. Always write to a temp file first.
- **Do not load KittenTTS or WhisperModel at import time:** Cold start is 3-5s. Use the lazy-load pattern via `st.session_state["tts_model"]` / `st.session_state["stt_model"]` with `if model is None: model = load_...()`.
- **Do not use `audio_frame_callback` for STT accumulation:** The callback pattern makes it impossible to know when the utterance is complete. Use `audio_receiver.get_frames()` polled after streaming stops.
- **Do not rely on st.audio(autoplay=True) without user interaction:** Browser autoplay policy blocks audio playback unless the user has clicked the page. Since the coordinator always submits a form/button to send a command, there IS a prior interaction — autoplay should succeed in the demo flow. However, the first TTS after page load (before any interaction) will be silently blocked. Design the UI so TTS is only triggered from button callbacks, not on page load.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Audio codec decode | Custom WAV parser | `av.AudioFrame.to_ndarray()` + soundfile | av/PyAV handles codec negotiation; soundfile handles WAV encoding |
| Speech recognition | Custom audio analysis | `faster_whisper.WhisperModel.transcribe()` | Whisper handles language detection, VAD, beam search |
| Text-to-speech | Custom neural TTS | `KittenTTS.generate()` | ONNX-accelerated; 8 voices; project constraint |
| Sentence splitting | Custom regex | `re.split(r'(?<=[.?!])\s+', text)` | One-liner; sufficient for short coordinator phrases |
| Browser mic access | PortAudio / PyAudio | streamlit-webrtc | Browser mic requires WebRTC; PortAudio is OS-level only |

**Key insight:** The voice pipeline is a data transformation chain. Each library handles one step: av decodes WebRTC frames → soundfile serializes WAV → faster-whisper transcribes → KittenTTS synthesizes → soundfile serializes again → st.audio plays. Never replicate what these libraries already do.

---

## Common Pitfalls

### Pitfall 1: "af_heart" Voice Name Does Not Exist

**What goes wrong:** KittenTTS raises a `ValueError` or `KeyError` at generation time because "af_heart" is not in the model's voice list.

**Why it happens:** CONTEXT.md specifies "af_heart" but the KittenTTS 0.8.1 voices are: `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo`. "af_heart" is a voice from Kokoro TTS (a different library), not KittenTTS.

**How to avoid:** Use `"Bella"` as the default Jarvis voice. Verify with `model.available_voices` at startup and log the list.

**Warning signs:** `KeyError: 'af_heart'` or similar on first TTS call.

### Pitfall 2: faster-whisper Segments Generator Not Iterated

**What goes wrong:** `transcribe()` returns immediately with an empty result; no transcription occurs.

**Why it happens:** faster-whisper returns a lazy generator. Transcription only starts when you iterate `for seg in segments`. If you check `len(segments)` or convert to list elsewhere, the generator may be empty.

**How to avoid:** Always consume the generator immediately: `texts = [seg.text for seg in segments]` in the same function scope as `transcribe()`.

**Warning signs:** Empty transcript even when speech was clearly recorded.

### Pitfall 3: st.audio autoplay Blocked on Page Load

**What goes wrong:** Jarvis TTS audio is silently not played on the first command after a fresh page load.

**Why it happens:** Modern browsers block `autoplay` unless the user has first interacted with the page (clicked something). Streamlit's `autoplay=True` parameter has no effect until there is a prior user gesture.

**How to avoid:** Ensure TTS playback is always triggered from a button callback (Submit, Send, or after push-to-talk Stop). The mic button press constitutes a user gesture. Do not call `st.audio` at page initialization.

**Warning signs:** "NotAllowedError: play() failed" in browser console; audio widget visible but silent.

### Pitfall 4: webrtc_streamer Requires HTTPS for Non-Localhost

**What goes wrong:** Microphone access is denied with a browser permissions error in the demo environment.

**Why it happens:** WebRTC MediaDevices API requires HTTPS for any host that is not `localhost` or `127.0.0.1`. If the demo is projected via a network URL (e.g., `http://192.168.1.10:8501`), browser blocks mic.

**How to avoid:** Run the demo on `localhost` only. Add an explicit preflight check that warns when `streamlit run` is accessed via a non-localhost URL. This was flagged as a pending todo in STATE.md.

**Warning signs:** "NotAllowedError: Permission denied" or browser mic icon blocked.

### Pitfall 5: KittenTTS Wheel Install Dependency Failure

**What goes wrong:** `pip install kittentts` (from PyPI) fails with `misaki>=0.9.4` not found, or installs a different/broken version.

**Why it happens:** KittenTTS is in developer preview and PyPI distribution may lag the GitHub releases. Reported in STATE.md as a known blocker.

**How to avoid:** Always install from the official GitHub wheel URL. Validate install on demo hardware before Phase 4 coding begins (existing todo in STATE.md).

**Warning signs:** `ModuleNotFoundError: No module named 'kittentts'` after PyPI install; import error for `misaki`.

### Pitfall 6: av.AudioFrame Format Mismatch

**What goes wrong:** After converting frames with `to_ndarray()`, the audio is clipped, distorted, or silently fails transcription.

**Why it happens:** WebRTC delivers audio in s16 (signed 16-bit integer) format. If you pass this directly to soundfile or faster-whisper expecting float32, values are in [-32768, 32767] instead of [-1.0, 1.0].

**How to avoid:** After `to_ndarray()`, check `frame.format.name`. If `s16`, normalize: `audio = audio.astype(np.float32) / 32768.0`.

**Warning signs:** Garbled or silent audio despite correctly assembled frames; faster-whisper returns nonsense text.

---

## Code Examples

### Command Center Tab — Complete Integration Sketch

```python
# src/ui/command_center.py
# Source: combines patterns from official docs and examples above
import datetime
import logging

import streamlit as st

logger = logging.getLogger(__name__)


def render_command_center_tab() -> None:
    """Render Command Center tab: voice panel + text input + conversation history."""
    st.subheader("Jarvis Command Center")

    # ── Session state setup ───────────────────────────────────────────────
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = []

    # ── Model lazy-load ───────────────────────────────────────────────────
    if st.session_state.get("tts_model") is None:
        with st.spinner("Loading Jarvis voice..."):
            from src.voice.tts import load_tts_model
            st.session_state["tts_model"] = load_tts_model()

    if st.session_state.get("stt_model") is None:
        with st.spinner("Loading speech recognition..."):
            from src.voice.stt import load_stt_model
            st.session_state["stt_model"] = load_stt_model()

    # ── Push-to-talk section ──────────────────────────────────────────────
    st.markdown("**Voice Input (Push-to-Talk)**")
    _render_push_to_talk()

    # ── Text input ────────────────────────────────────────────────────────
    user_text = st.chat_input("Type a command or see transcription above...")
    if user_text:
        _handle_command(user_text, source="text")

    # ── Conversation history ──────────────────────────────────────────────
    st.divider()
    st.markdown("**Conversation History**")
    _render_history()


def _render_push_to_talk() -> None:
    """Render webrtc streamer; transcribe when streaming stops."""
    from streamlit_webrtc import WebRtcMode, webrtc_streamer
    from src.voice.stt import transcribe_audio_bytes

    webrtc_ctx = webrtc_streamer(
        key="jarvis-ptt",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    # Drain frames when streaming just stopped
    if not webrtc_ctx.state.playing and webrtc_ctx.audio_receiver:
        frames = []
        try:
            while True:
                frames.extend(webrtc_ctx.audio_receiver.get_frames(timeout=0))
        except Exception:
            pass
        if frames:
            import numpy as np
            import io
            import soundfile as sf
            arrays = []
            sample_rate = 16000
            for frame in frames:
                arr = frame.to_ndarray().flatten().astype(np.float32)
                if arr.max() > 1.0:
                    arr = arr / 32768.0
                arrays.append(arr)
                sample_rate = frame.sample_rate
            audio = np.concatenate(arrays)
            buf = io.BytesIO()
            sf.write(buf, audio, samplerate=sample_rate, format="WAV")
            wav_bytes = buf.getvalue()

            with st.spinner("Transcribing..."):
                transcript = transcribe_audio_bytes(
                    wav_bytes, st.session_state["stt_model"]
                )
            if transcript:
                _handle_command(transcript, source="voice")


def _handle_command(text: str, source: str) -> None:
    """Add command to history, generate echo reply, synthesize TTS."""
    from src.voice.tts import synthesize_to_wav_bytes, split_into_sentences
    import datetime

    ts = datetime.datetime.now().strftime("%H:%M:%S")

    # Add coordinator message
    st.session_state["conversation_history"].append({
        "role": "user",
        "text": text,
        "intent": None,
        "timestamp": ts,
        "source": source,
    })

    # Phase 4: hardcoded echo reply
    jarvis_reply = f"Received: {text}"
    st.session_state["conversation_history"].append({
        "role": "assistant",
        "text": jarvis_reply,
        "intent": "echo",
        "timestamp": ts,
    })

    # TTS playback — triggered from user interaction (safe for autoplay)
    tts_model = st.session_state.get("tts_model")
    if tts_model:
        sentences = split_into_sentences(jarvis_reply)
        for sentence in sentences:
            try:
                wav_bytes = synthesize_to_wav_bytes(
                    sentence, tts_model, voice="Bella"
                )
                st.audio(wav_bytes, format="audio/wav", autoplay=True)
            except Exception as exc:
                logger.error("TTS failed for sentence %r: %s", sentence, exc)
                st.error("Voice synthesis unavailable — reply shown as text only.")
    st.rerun()


def _render_history() -> None:
    """Render conversation history as chat bubbles."""
    history = st.session_state.get("conversation_history", [])
    if not history:
        st.caption("No conversation yet. Type a command or use the mic.")
        return
    for entry in history:
        role = entry.get("role", "user")
        with st.chat_message(role):
            st.write(entry["text"])
            parts = []
            if entry.get("intent"):
                parts.append(f"[Intent: {entry['intent']}]")
            if entry.get("timestamp"):
                parts.append(entry["timestamp"])
            if parts:
                st.caption("  |  ".join(parts))
```

### app.py Tab Modification (minimal diff)

```python
# BEFORE (existing in src/app.py ~line 319):
tab_matches, tab_discovery, tab_pipeline, tab_expansion, tab_volunteers = st.tabs([
    "🎯 Matches",
    "🔍 Discovery",
    "📊 Pipeline",
    "🗺️ Expansion",
    "👥 Volunteers",
])

# AFTER (Command Center prepended):
from src.ui.command_center import render_command_center_tab  # noqa: E402
tab_command, tab_matches, tab_discovery, tab_pipeline, tab_expansion, tab_volunteers = st.tabs([
    "🤖 Command Center",
    "🎯 Matches",
    "🔍 Discovery",
    "📊 Pipeline",
    "🗺️ Expansion",
    "👥 Volunteers",
])

with tab_command:
    render_command_center_tab()
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `st.audio_input` (clip-only) | streamlit-webrtc SENDONLY + audio_receiver | 2024-2025 | Enables push-to-talk start/stop control rather than single-clip record |
| openai-whisper | faster-whisper | 2023+ | 4× faster, CPU int8 quantization, no system FFmpeg needed |
| `audio_frame_callback` for accumulation | `audio_receiver.get_frames()` polling | webrtc 0.5+ | Callback can't signal utterance end; receiver polling drains after stop |
| `@st.fragment(run_every=N)` for STT poll | Direct drain on `webrtc_ctx.state.playing == False` | Phase 4 scope | Simpler for push-to-talk; fragment polling needed only for Phase 5+ background agents |

**Note:** `st.chat_message` + `st.chat_input` are the current Streamlit-native patterns for conversational UI (added in Streamlit 1.31). Use these instead of custom markdown bubbles.

---

## Open Questions

1. **Voice name resolution ("af_heart" vs KittenTTS voices)**
   - What we know: "af_heart" does not exist in KittenTTS 0.8.1. Valid voices: Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo.
   - What's unclear: The CONTEXT.md decision specifies "af_heart" by name. This may be a mistake (copied from Kokoro TTS docs) or the user has a specific preference among the real voices.
   - Recommendation: Treat "Bella" as the default Jarvis voice. Add a `KITTENTTS_VOICE = "Bella"` constant in `src/config.py`. Raise this with the user during plan review.

2. **av.AudioFrame format from streamlit-webrtc**
   - What we know: The official sendonly example uses pydub to process frames; documentation confirms s16 is common.
   - What's unclear: Whether all browsers deliver s16 or if some deliver float32 / s16p (planar). Need to handle both in `_frames_to_wav_bytes`.
   - Recommendation: Check `frame.format.name` at runtime; normalize conditionally.

3. **KittenTTS wheel install on demo hardware**
   - What we know: Reported `misaki>=0.9.4` failures on PyPI install. Wheel install from GitHub releases is the workaround.
   - What's unclear: Not validated on the actual demo machine (Windows/WSL2 based on env context).
   - Recommendation: This is a blocking pending todo from STATE.md. Validate before any Phase 4 code is written. If wheel fails, the entire TTS pipeline is blocked.

4. **st.audio autoplay after TTS for sequential sentences**
   - What we know: autoplay works after user interaction but browsers may block rapid successive autoplay calls.
   - What's unclear: Whether calling `st.audio(autoplay=True)` multiple times in the same rerun (one per sentence chunk) plays all chunks or only the last one.
   - Recommendation: Start with single TTS call for the full reply text. Only implement sentence chunking if latency is observed as a problem during demo rehearsal.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.3.4 |
| Config file | none — no pytest.ini detected; tests discovered from `Category 3 - IA West Smart Match CRM/tests/` |
| Quick run command | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/test_voice_stt.py tests/test_voice_tts.py tests/test_command_center.py -x -q` |
| Full suite command | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| VOICE-01 | Text command submitted → echo reply appended to conversation_history | unit | `pytest tests/test_command_center.py::test_text_command_appends_to_history -x` | Wave 0 |
| VOICE-01 | Command Center tab renders without error (no models needed) | unit | `pytest tests/test_command_center.py::test_render_command_center_tab_smoke -x` | Wave 0 |
| VOICE-02 | synthesize_to_wav_bytes() returns WAV bytes for valid text | unit | `pytest tests/test_voice_tts.py::test_synthesize_returns_wav_bytes -x` | Wave 0 |
| VOICE-02 | synthesize_to_wav_bytes() raises ValueError on empty text | unit | `pytest tests/test_voice_tts.py::test_synthesize_raises_on_empty_text -x` | Wave 0 |
| VOICE-02 | split_into_sentences() splits on sentence boundaries | unit | `pytest tests/test_voice_tts.py::test_split_into_sentences -x` | Wave 0 |
| VOICE-03 | transcribe_audio_bytes() returns string for valid WAV bytes | unit | `pytest tests/test_voice_stt.py::test_transcribe_returns_string -x` | Wave 0 |
| VOICE-03 | transcribe_audio_bytes() returns empty string for empty bytes | unit | `pytest tests/test_voice_stt.py::test_transcribe_empty_bytes_returns_empty -x` | Wave 0 |
| VOICE-04 | conversation_history grows with each command | unit | `pytest tests/test_command_center.py::test_history_grows_with_commands -x` | Wave 0 |
| VOICE-04 | render_conversation_history() renders all history entries | unit | `pytest tests/test_command_center.py::test_render_conversation_history -x` | Wave 0 |
| ALL | 392 existing tests still pass after Phase 4 additions | regression | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/ -q` | Existing |

**Manual-only verification:**
- Browser mic access granted and push-to-talk audio plays (requires live browser interaction)
- `st.audio(autoplay=True)` audible after command submission (browser audio policy)

### Sampling Rate

- **Per task commit:** `python -m pytest tests/test_voice_stt.py tests/test_voice_tts.py tests/test_command_center.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -q` (full 392+ suite must stay green)
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_voice_stt.py` — covers VOICE-03 STT unit tests (mock WhisperModel)
- [ ] `tests/test_voice_tts.py` — covers VOICE-02 TTS unit tests (mock KittenTTS model)
- [ ] `tests/test_command_center.py` — covers VOICE-01, VOICE-04 command center UI logic
- [ ] `tests/conftest.py` extension — add mock for `kittentts`, `faster_whisper`, `streamlit_webrtc` modules (same pattern as existing streamlit mock)

---

## Sources

### Primary (HIGH confidence)

- https://github.com/KittenML/KittenTTS — constructor signature, generate() signature, available_voices list, sample rate (24 kHz), wheel install URL
- https://huggingface.co/KittenML/kitten-tts-mini-0.8 — confirmed voice names: Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo; NO "af_heart"
- https://github.com/SYSTRAN/faster-whisper README — WhisperModel constructor, transcribe() signature, segments generator, CPU compute_type="int8"
- https://docs.streamlit.io/develop/api-reference/chat/st.chat_message — name parameter, avatar, with-notation pattern
- https://docs.streamlit.io/develop/api-reference/media/st.audio — autoplay parameter, browser restriction documented
- https://docs.streamlit.io/develop/api-reference/widgets/st.audio_input — sample_rate=16000 default, WAV format, UploadedFile return type
- https://github.com/whitphx/streamlit-webrtc/blob/main/pages/10_sendonly_audio.py — audio_receiver.get_frames() polling pattern, WebRtcMode.SENDONLY, audio_receiver_size

### Secondary (MEDIUM confidence)

- https://pypi.org/project/streamlit-webrtc/ — version 0.6.0, Python >=3.10 requirement, HTTPS constraint for non-localhost

### Tertiary (LOW confidence)

- Existing STACK.md and ARCHITECTURE.md — milestone-level research, cross-referenced and consistent with primary sources

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — KittenTTS, faster-whisper, soundfile APIs verified from official GitHub docs; streamlit-webrtc from official example
- Architecture: HIGH — patterns derived from official examples and API docs, not community posts
- Pitfalls: HIGH for "af_heart" (hard fact, verified), MEDIUM for autoplay behavior (documented but browser-dependent), MEDIUM for frame format (av behavior confirmed conceptually)
- Voice name mismatch: HIGH confidence this is a bug in CONTEXT.md — "af_heart" is a Kokoro TTS voice, not KittenTTS

**Research date:** 2026-03-23
**Valid until:** 2026-04-23 (KittenTTS developer preview — check for API changes if more than 2 weeks pass before implementation)
