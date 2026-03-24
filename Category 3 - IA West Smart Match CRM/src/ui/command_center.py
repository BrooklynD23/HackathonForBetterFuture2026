"""Command Center tab -- voice panel + text input + conversation history."""
from __future__ import annotations

import datetime
import io
import logging

import numpy as np
import soundfile as sf
import streamlit as st

from src.coordinator.approval import ActionProposal
from src.coordinator.intent_parser import ACTION_REGISTRY, MULTI_STEP_INTENTS, ParsedIntent, parse_intent
from src.coordinator.result_bus import dispatch, poll_results
from src.coordinator.suggestions import check_overdue_contacts, check_staleness_conditions
from src.coordinator.tools import TOOL_REGISTRY
from src.ui.swimlane_dashboard import _update_swimlane, render_swimlane_dashboard

logger = logging.getLogger(__name__)


def render_command_center_tab() -> None:
    """Render Command Center tab: voice panel + text input + conversation history."""
    st.markdown(
        '<h2 style="font-family: var(--font-headline);">Jarvis -- Voice Command Center</h2>',
        unsafe_allow_html=True,
    )

    # Lazy-load TTS model
    if st.session_state.get("tts_model") is None:
        try:
            with st.spinner("Loading voice model (first use)..."):
                from src.voice.tts import load_tts_model
                st.session_state["tts_model"] = load_tts_model()
        except Exception as exc:
            logger.error("TTS model load failed: %s", exc)
            st.warning("Voice synthesis unavailable. Jarvis response shown as text above.")

    # Lazy-load STT model
    if st.session_state.get("stt_model") is None:
        try:
            with st.spinner("Loading speech recognition..."):
                from src.voice.stt import load_stt_model
                st.session_state["stt_model"] = load_stt_model()
        except Exception as exc:
            logger.error("STT model load failed: %s", exc)
            st.warning("Speech recognition unavailable. Please use text commands.")

    # Poll result bus for completed background tasks
    _poll_result_bus()

    # Proactive suggestions
    _inject_proactive_suggestions()

    # Voice panel
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
        _render_push_to_talk()
    st.markdown('</div>', unsafe_allow_html=True)

    # Conversation history
    st.divider()
    _render_conversation_history()


def _handle_text_command(text: str, source: str = "text") -> None:
    """Parse intent from command text and create an ActionProposal or unknown reply."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")

    history: list[dict] = st.session_state.get("conversation_history", [])

    history.append({
        "role": "user",
        "text": text,
        "intent": None,
        "timestamp": ts,
        "source": source,
    })

    parsed: ParsedIntent = parse_intent(text)

    if parsed.intent == "unknown":
        unknown_reply = (
            f"I couldn't understand that command. You said: '{text}'. "
            "Try rephrasing — for example, 'find new events' or 'rank speakers for event X'."
        )
        history.append({
            "role": "assistant",
            "text": unknown_reply,
            "intent": "unknown",
            "timestamp": ts,
        })
        st.session_state["conversation_history"] = history

        # TTS playback for unknown reply
        _speak_text(unknown_reply)

        st.rerun()
        return

    # Multi-step intent: create sub-proposals for each step
    if parsed.intent in MULTI_STEP_INTENTS:
        sub_intents = MULTI_STEP_INTENTS[parsed.intent]
        for sub_intent in sub_intents:
            sub_description = next(
                (a["description"] for a in ACTION_REGISTRY if a["intent"] == sub_intent),
                sub_intent,
            )
            sub_agent = next(
                (a["agent"] for a in ACTION_REGISTRY if a["intent"] == sub_intent),
                "Agent",
            )
            sub_proposal = ActionProposal(
                intent=sub_intent,
                agent=sub_agent,
                description=sub_description,
                reasoning=f"Part of '{text}' campaign orchestration.",
                params=parsed.params,
            )
            st.session_state["action_proposals"][sub_proposal.id] = sub_proposal
            history.append({
                "role": "proposal",
                "action_id": sub_proposal.id,
                "timestamp": ts,
            })
        st.session_state["conversation_history"] = history
        st.rerun()
        return

    # Known intent: create and store action proposal
    description = next(
        (a["description"] for a in ACTION_REGISTRY if a["intent"] == parsed.intent),
        parsed.agent,
    )
    proposal = ActionProposal(
        intent=parsed.intent,
        agent=parsed.agent,
        description=description,
        reasoning=parsed.reasoning,
        params=parsed.params,
    )
    st.session_state["action_proposals"][proposal.id] = proposal
    history.append({
        "role": "proposal",
        "action_id": proposal.id,
        "timestamp": ts,
    })
    st.session_state["conversation_history"] = history

    st.rerun()


def _speak_text(text: str) -> None:
    """Speak text via TTS if model is available. Silently skips if unavailable."""
    tts_model = st.session_state.get("tts_model")
    if tts_model:
        try:
            from src.voice.tts import split_into_sentences, synthesize_to_wav_bytes
            for sentence in split_into_sentences(text):
                wav_bytes = synthesize_to_wav_bytes(sentence, tts_model, voice="Bella")
                st.audio(wav_bytes, format="audio/wav", autoplay=True)
        except Exception as exc:
            logger.error("TTS failed: %s", exc)
            st.info("Voice synthesis unavailable. Jarvis response shown as text above.")


def _format_result(result: dict) -> str:
    """Format a tool result dict into a human-readable string for the action card."""
    if "events" in result:
        count = len(result["events"])
        source = result.get("source", "unknown")
        return f"Found {count} event(s) (source: {source})"
    if "rankings" in result:
        count = len(result["rankings"])
        return f"Ranked {count} speaker(s)"
    if "email" in result:
        subject = result["email"].get("subject", "Outreach email")
        return f"Generated email: {subject}"
    if "contacts" in result:
        total = result.get("total", 0)
        overdue = result.get("overdue_count", 0)
        return f"{total} contacts, {overdue} overdue for follow-up"
    if "error" in result:
        return f"Error: {result['error']}"
    return str(result)


@st.fragment(run_every=2)
def _poll_result_bus() -> None:
    """Poll result queues every 2s; update proposal and swimlane state."""
    proposals = st.session_state.get("action_proposals", {})
    for proposal_id, payload in poll_results():
        proposal = proposals.get(proposal_id)
        if proposal is None:
            continue
        if payload["status"] == "completed":
            proposal.status = "completed"
            proposal.result = _format_result(payload["result"])
            _update_swimlane(proposal_id, "completed", proposal.result, agent_name=proposal.agent)
            _speak_text(proposal.result)
        else:
            proposal.status = "failed"
            proposal.result = f"Error: {payload.get('error', 'unknown')}"
            _update_swimlane(proposal_id, "failed", proposal.result, agent_name=proposal.agent)
    render_swimlane_dashboard()


def _render_contacts_result(proposal: ActionProposal) -> None:
    """Render POC contact cards when a check_contacts action completes."""
    from src.coordinator.tools.contacts_tool import run as contacts_run
    data = contacts_run({})
    if data["status"] != "ok":
        return
    for contact in data.get("contacts", []):
        is_overdue = contact["name"] in [c["name"] for c in data.get("overdue", [])]
        badge = " -- OVERDUE" if is_overdue else ""
        with st.expander(f"{contact['name']} ({contact['org']}){badge}", expanded=is_overdue):
            st.markdown(f"**Role:** {contact.get('role', 'N/A')}")
            st.markdown(f"**Email:** {contact.get('email', 'N/A')}")
            st.markdown(f"**Last Contact:** {contact.get('last_contact', 'N/A')}")
            st.markdown(f"**Follow-up Due:** {contact.get('follow_up_due', 'N/A')}")
            history = contact.get("comm_history", [])
            if history:
                st.markdown("**Communication History:**")
                for entry in history:
                    st.markdown(f"- {entry.get('date', '?')}: [{entry.get('type', '?')}] {entry.get('summary', '')}")


def _render_action_card(proposal: ActionProposal) -> None:
    """Render an action card with agent info, status, and approve/reject/edit controls."""
    with st.container():
        st.markdown(
            f"**{proposal.agent}** | Status: `{proposal.status}`",
            unsafe_allow_html=True,
        )
        st.markdown(proposal.description)
        st.caption(f"Reasoning: {proposal.reasoning}")

        if proposal.status == "proposed":
            with st.expander("Edit Parameters", expanded=False):
                for k in list(proposal.params.keys()):
                    new_val = st.text_input(
                        k,
                        value=str(proposal.params[k]),
                        key=f"param_{proposal.id}_{k}",
                    )
                    proposal.params[k] = new_val

            col_approve, col_reject = st.columns(2)
            with col_approve:
                if st.button("Approve", key=f"approve_{proposal.id}", type="primary"):
                    proposal.approve()
                    tool_fn = TOOL_REGISTRY.get(proposal.intent)
                    if tool_fn:
                        proposal.status = "executing"
                        dispatch(proposal.id, tool_fn, proposal.params)
                        _update_swimlane(proposal.id, "executing", "Running...", agent_name=proposal.agent)
                    else:
                        proposal.stub_execute()
                        if proposal.result:
                            _speak_text(proposal.result)
                    st.rerun()
            with col_reject:
                if st.button("Reject", key=f"reject_{proposal.id}"):
                    proposal.reject()
                    st.rerun()

        elif proposal.status == "completed":
            st.success(f"Result: {proposal.result}")
            # Render POC contact details if this was a contacts check
            if proposal.intent == "check_contacts":
                _render_contacts_result(proposal)

        elif proposal.status == "rejected":
            st.warning("Action rejected by coordinator.")

        elif proposal.status in ("approved", "executing"):
            st.info(f"Status: {proposal.status}...")

        elif proposal.status == "failed":
            st.error(f"Failed: {proposal.result}")


def _inject_proactive_suggestions() -> None:
    """Inject proactive suggestions: staleness first, then overdue contacts."""
    proposals: dict = st.session_state.get("action_proposals", {})

    # Guard: at most one active proactive suggestion
    for p in proposals.values():
        if p.source == "proactive" and p.status in ("proposed", "approved"):
            return

    suggestions = check_staleness_conditions(
        st.session_state.get("scraped_events", []),
        st.session_state.get("scraped_events_timestamp"),
    )

    # Fallback to overdue contacts if no staleness suggestion
    if not suggestions:
        suggestions = check_overdue_contacts(
            st.session_state.get("poc_contacts", [])
        )

    for suggestion in suggestions:
        st.session_state["action_proposals"][suggestion.id] = suggestion
        st.session_state.setdefault("conversation_history", []).append({
            "role": "proposal",
            "action_id": suggestion.id,
            "timestamp": suggestion.created_at,
        })


def _render_push_to_talk() -> None:
    """Render push-to-talk mic button; transcribe on stop."""
    try:
        from streamlit_webrtc import WebRtcMode, webrtc_streamer
    except ImportError:
        st.warning("streamlit-webrtc not installed. Use text commands.")
        return

    webrtc_ctx = webrtc_streamer(
        key="jarvis-ptt",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    if not webrtc_ctx.state.playing and webrtc_ctx.audio_receiver:
        frames = []
        try:
            while True:
                frames.extend(webrtc_ctx.audio_receiver.get_frames(timeout=0))
        except Exception:
            pass

        if frames:
            wav_bytes = _frames_to_wav_bytes(frames)
            stt_model = st.session_state.get("stt_model")
            if stt_model and wav_bytes:
                with st.spinner("Transcribing..."):
                    from src.voice.stt import transcribe_audio_bytes
                    transcript = transcribe_audio_bytes(wav_bytes, stt_model)
                if transcript:
                    st.session_state["jarvis_command_input"] = transcript
                    _handle_text_command(transcript, source="voice")
                else:
                    st.warning("No speech detected. Please try again.")
            elif not stt_model:
                st.error("Speech recognition not loaded. Please use text commands.")


def _frames_to_wav_bytes(frames: list) -> bytes:
    """Convert av.AudioFrame list to WAV bytes at 16 kHz."""
    arrays = []
    sample_rate = 16000
    for frame in frames:
        arr = frame.to_ndarray().flatten().astype(np.float32)
        if arr.max() > 1.0:
            arr = arr / 32768.0
        arrays.append(arr)
        sample_rate = getattr(frame, "sample_rate", 16000)
    audio = np.concatenate(arrays)
    buffer = io.BytesIO()
    sf.write(buffer, audio, samplerate=sample_rate, format="WAV")
    return buffer.getvalue()


def _render_conversation_history() -> None:
    """Render chronological conversation history with chat bubbles."""
    history: list[dict] = st.session_state.get("conversation_history", [])
    if not history:
        # Demo hint chips
        DEMO_HINTS = [
            "Find new events",
            "Rank speakers for CPP Career Fair",
            "Prepare full outreach campaign",
        ]
        hint_cols = st.columns(len(DEMO_HINTS))
        for col, hint in zip(hint_cols, DEMO_HINTS):
            with col:
                if st.button(hint, key=f"hint_{hint}"):
                    _handle_text_command(hint)
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

        if role == "proposal":
            proposal_id = entry.get("action_id")
            proposal = st.session_state.get("action_proposals", {}).get(proposal_id)
            if proposal:
                _render_action_card(proposal)
            continue

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
