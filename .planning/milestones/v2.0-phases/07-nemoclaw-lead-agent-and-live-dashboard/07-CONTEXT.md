# Phase 7: NemoClaw Lead Agent and Live Dashboard - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver the full end-to-end demo experience: NemoClaw orchestrator integration (with automatic direct-dispatch fallback), per-agent swimlane dashboard with live status cycling, TTS result summaries, POC follow-up proactive suggestions, and a multi-step "prepare for event" command that showcases parallel sub-agent dispatch. Phase 7 completes the Jarvis Agent Coordinator by layering orchestration and visual monitoring on top of the working Phase 6 direct-dispatch foundation.

</domain>

<decisions>
## Implementation Decisions

### NemoClaw Integration Strategy
- Adapter pattern behind TOOL_REGISTRY — NemoClaw becomes an optional orchestration layer wrapping the same tool callables, selectable via env var `USE_NEMOCLAW=1`. Direct dispatch remains default.
- Graceful skip with log warning — Try `import openclaw` at module load, set `NEMOCLAW_AVAILABLE = False` if ImportError. Direct dispatch activates silently. Follows Phase 4 TTS/STT graceful degradation pattern.
- Parallel dispatch via NemoClaw's native multi-tool dispatch when available. Falls through to serial direct-dispatch when NemoClaw is unavailable.
- Independent per-agent results on partial failure — each swimlane card shows independent status. Successful agents return results; failed agents show error with retry option.

### Swimlane Dashboard Design
- Horizontal row of cards via `st.columns()` side-by-side — one card per dispatched agent, colored container with agent name + status badge
- Each card shows: agent name, status badge (idle/running/awaiting/complete/failed), elapsed time, and one-line result summary. Status badge uses colored pill (gray/blue-pulse/yellow/green/red).
- Fixed section between voice panel and conversation history — always visible when any agent has been dispatched, collapses when no active/recent agents
- Show all dispatched agents from current session (up to 8), with scroll if more. Older completed agents fade to compact single-line after 30s.

### POC Proactive Suggestions (POC-03)
- Same proactive suggestion card as staleness check — on Command Center load, check `poc_contacts.json` for overdue `follow_up_due` dates, inject `check_contacts` action proposal with `source: "proactive"`
- Staggered with staleness: max 1 proactive suggestion at a time (existing guard). Staleness check first; if no staleness suggestion, then check contacts overdue.
- Approving runs `check_contacts` tool with same result rendering as existing `_render_contacts_result()`
- Suggestion message includes count and names — e.g., "3 contacts overdue for follow-up: Dr. Smith, Prof. Jones, Dr. Lee — review now?"

### TTS Result Summaries & Demo Polish
- TTS on every completed action — when `_poll_result_bus()` transitions a proposal to "completed", call `_speak_text()` with the formatted result
- Multi-agent summaries: one sentence per agent, concatenated. e.g., "Discovery found 12 events. Speaker ranking complete for 8 speakers."
- Multi-step orchestration: "Prepare for the CPP career fair" triggers discover + match + outreach as parallel sub-agents (NemoClaw showcase intent, falls back to sequential direct-dispatch)
- Demo script hints: when conversation is empty, show 3 suggested commands as clickable chips: "Find new events", "Rank speakers for CPP Career Fair", "Prepare full outreach campaign"

### Claude's Discretion
- NemoClaw SDK configuration details and Nemotron model selection
- Exact CSS styling of swimlane status badges and animations
- Elapsed time display format and refresh cadence
- Multi-step intent parsing prompt template for Gemini
- Compact card fade timing and transition animation

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/coordinator/tools/__init__.py` — TOOL_REGISTRY mapping 4 intents to tool callables; extend with NemoClaw adapter
- `src/coordinator/result_bus.py` — `dispatch()` + `poll_results()` with per-proposal queues; extend for multi-agent tracking
- `src/coordinator/approval.py` — ActionProposal dataclass with full state machine (proposed→approved→executing→completed/failed)
- `src/coordinator/suggestions.py` — `check_staleness_conditions()` proactive engine; extend with overdue contact check
- `src/coordinator/intent_parser.py` — ParsedIntent + ACTION_REGISTRY; extend with multi-step "prepare" intent
- `src/ui/command_center.py` — Full Command Center tab with voice panel, action cards, conversation history, result bus polling
- `src/coordinator/tools/contacts_tool.py` — `run({})` returns contacts with overdue detection from `poc_contacts.json`
- `src/voice/tts.py` — `synthesize_to_wav_bytes()` and `split_into_sentences()` for Jarvis speech

### Established Patterns
- Pure Python service modules with no Streamlit imports (coordinator/, matching/, scraping/, voice/)
- `@st.fragment(run_every=2)` polling loop for non-blocking result delivery
- Session state initialization with `if key not in st.session_state` guards in `init_runtime_state()`
- Graceful degradation: try import, set `_AVAILABLE = False` on failure, log warning
- Tool wrappers as thin adapters calling existing functions unchanged
- Action proposals stored in `st.session_state["action_proposals"]` keyed by UUID

### Integration Points
- `_poll_result_bus()` in command_center.py — extend to update swimlane card state and trigger TTS on completion
- `_inject_proactive_suggestions()` — extend with overdue contact check after staleness check
- `TOOL_REGISTRY` — wrap with NemoClaw adapter when `USE_NEMOCLAW=1`
- `_render_conversation_history()` — swimlane dashboard section inserted before this
- `init_runtime_state()` — add `agent_swimlanes: {}` session state key for per-agent tracking
- `ACTION_REGISTRY` in intent_parser.py — add `prepare_campaign` multi-step intent
- `parse_intent()` — handle multi-step intents that spawn multiple sub-agent proposals

</code_context>

<specifics>
## Specific Ideas

- NemoClaw adapter at `src/coordinator/nemoclaw_adapter.py` — wraps TOOL_REGISTRY callables as OpenClaw tools, dispatches via NemoClaw client if available, falls back to result_bus.dispatch() otherwise
- Swimlane dashboard at `src/ui/swimlane_dashboard.py` — renders horizontal agent status cards, polls session state for status updates
- Overdue contact check function added to `src/coordinator/suggestions.py` — `check_overdue_contacts()` reads poc_contacts.json, returns proactive ActionProposal with count and names
- Multi-step intent: `prepare_campaign` in intent_parser ACTION_REGISTRY — Gemini parses "prepare for X" into sub-intents [discover_events, rank_speakers, generate_outreach], each gets its own ActionProposal
- Demo hint chips rendered as `st.button` row in empty conversation state
- All existing 528+ tests must continue to pass — zero changes to existing function signatures

</specifics>

<deferred>
## Deferred Ideas

- Real-time streaming transcription during speech (VOICE-05)
- Wake word activation "Hey Jarvis" (VOICE-06)
- Agent self-modification or dynamic tool creation (ORCH-05)
- Mobile-responsive command center layout (DASH-04)
- Full React migration using mockup design tokens from `docs/mockup/`

</deferred>
