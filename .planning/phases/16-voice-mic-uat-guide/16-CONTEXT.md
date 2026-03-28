# Phase 16: Voice/Mic UAT Guide - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 16 delivers a standalone human UAT guide (`docs/UAT-VOICE-MIC.md`) for the Streamlit-based voice/mic coordinator path. The guide enables a human reviewer with no prior implementation knowledge to independently walk through the live voice/mic workflow, verify intent parsing and approval gating, and handle known edge cases — all without developer assistance.

</domain>

<decisions>
## Implementation Decisions

### Guide Document Format
- Location: `docs/UAT-VOICE-MIC.md` in the repo root docs/ folder — easily found by judges
- Structure: Prerequisites → Happy Path (numbered steps) → Edge Cases → Pass/Fail Checklist
- Step format: Each step has an **Action** line and an **Expected:** outcome line — enables clear pass/fail per step
- Text-only — no screenshots required; guide references component names (e.g., "Approve button", "approval card") for orientation

### Prerequisites & Startup Coverage
- Full startup sequence documented: `streamlit run src/app.py`, confirm `:8501` reachable, note FastAPI `:8000` is optional for voice path
- Gemini API key two-mode note: LLM intent parsing (key present) vs. keyword fallback (no key) — both produce testable approval cards
- `streamlit-webrtc` install note: critical dependency; missing install shows "streamlit-webrtc not installed. Use text commands." warning
- Browser requirement: Chrome/Chromium specified for WebRTC mic access; note Firefox may block WebRTC audio

### Voice Workflow Step Coverage
- Both paths documented as parallel sections: "Path A: Voice Input" and "Path B: Text Input (fallback)"
- Two representative intents demonstrated: `discover_events` ("find new events") and `prepare_campaign` ("prepare full outreach campaign") — one simple, one multi-step
- Intent parsing verification: reviewer looks for approval card in conversation history showing agent name + description + Approve/Reject buttons
- Approval gating verification: click Approve → observe status `proposed` → `executing` → `completed`; click Reject → observe "Action rejected by coordinator"

### Edge Case Documentation Depth
- Microphone permission prompt: full browser handling (click Allow in Chrome prompt; if Blocked, reset via chrome://settings/content/microphone)
- STT model load failure: document "Speech recognition unavailable. Please use text commands." warning and text fallback path
- No speech detected: retry guidance — re-press mic, speak closer to mic, check OS mic input level
- Gemini offline/keyword fallback: document expected behavior — same approval card appears, reasoning reads "Matched keyword in: '...'" instead of LLM explanation

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/ui/command_center.py` — authoritative source for all UI labels (button names, warning strings, spinner text)
- `src/coordinator/intent_parser.py` — defines all 5 supported intents and keyword patterns; `ACTION_REGISTRY` has agent names and descriptions shown in approval cards
- `src/voice/stt.py` — faster-whisper STT wrapper; `WHISPER_MODEL_SIZE = "base"`, `WHISPER_COMPUTE_TYPE = "int8"`
- `src/voice/tts.py` — TTS model; loaded lazily on first Command Center visit
- `src/coordinator/approval.py` — `ActionProposal` state machine: `proposed` → `approved` → `executing` → `completed`

### Established Patterns
- Voice input uses `streamlit-webrtc` push-to-talk widget (`WebRtcMode.SENDONLY`) — mic button appears to the right of the command text input
- STT and TTS models are lazy-loaded with spinner on first Command Center tab visit
- Approval cards render in conversation history (not as a separate panel)
- Multi-step `prepare_campaign` creates 3 sub-proposals: `discover_events`, `rank_speakers`, `generate_outreach`
- Proactive suggestions (staleness / overdue contacts) may appear as unprompted proposals

### Integration Points
- Streamlit app: `streamlit run src/app.py` → `:8501`
- Command Center tab: 2nd tab in the Coordinator Dashboard section (after landing / login)
- Voice panel: top of Command Center, two columns — text input (left, wide) + mic button (right, narrow)
- Conversation history: scrollable list below the voice panel divider

</code_context>

<specifics>
## Specific Ideas

- The guide should be usable by a judge who has just cloned the repo and followed the README startup instructions
- Approval card details (agent name, description, Approve/Reject buttons) should be described precisely so reviewers know exactly what to look for
- The two-mode Gemini behavior is worth documenting because demo environments may not have a valid API key

</specifics>

<deferred>
## Deferred Ideas

- Playwright automation of the voice path (WebRTC mic input is not automatable with Playwright headless) — captured as future requirement
- Video recording of a live walkthrough to supplement the text guide — beyond hackathon scope
- UAT guides for additional coordinator paths (QR flow, feedback flow) — QR/feedback already covered by Phase 15 Playwright evidence

</deferred>
