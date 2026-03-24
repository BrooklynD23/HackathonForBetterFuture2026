# Phase 7: NemoClaw Lead Agent and Live Dashboard - Research

**Researched:** 2026-03-24
**Domain:** OpenClaw SDK parallel dispatch, Streamlit real-time fragment polling, multi-step intent orchestration, proactive suggestion extension
**Confidence:** HIGH — openclaw-sdk 2.1.0 installed and inspected directly; Streamlit 1.42.2 fragment API verified in venv; existing codebase read in full

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**NemoClaw Integration Strategy**
- Adapter pattern behind TOOL_REGISTRY — NemoClaw becomes an optional orchestration layer wrapping the same tool callables, selectable via env var `USE_NEMOCLAW=1`. Direct dispatch remains default.
- Graceful skip with log warning — Try `import openclaw_sdk` at module load, set `NEMOCLAW_AVAILABLE = False` if ImportError. Direct dispatch activates silently. Follows Phase 4 TTS/STT graceful degradation pattern.
- Parallel dispatch via NemoClaw's native multi-tool dispatch when available. Falls through to serial direct-dispatch when NemoClaw is unavailable.
- Independent per-agent results on partial failure — each swimlane card shows independent status. Successful agents return results; failed agents show error with retry option.

**Swimlane Dashboard Design**
- Horizontal row of cards via `st.columns()` side-by-side — one card per dispatched agent, colored container with agent name + status badge
- Each card shows: agent name, status badge (idle/running/awaiting/complete/failed), elapsed time, and one-line result summary. Status badge uses colored pill (gray/blue-pulse/yellow/green/red).
- Fixed section between voice panel and conversation history — always visible when any agent has been dispatched, collapses when no active/recent agents
- Show all dispatched agents from current session (up to 8), with scroll if more. Older completed agents fade to compact single-line after 30s.

**POC Proactive Suggestions (POC-03)**
- Same proactive suggestion card as staleness check — on Command Center load, check `poc_contacts.json` for overdue `follow_up_due` dates, inject `check_contacts` action proposal with `source: "proactive"`
- Staggered with staleness: max 1 proactive suggestion at a time (existing guard). Staleness check first; if no staleness suggestion, then check contacts overdue.
- Approving runs `check_contacts` tool with same result rendering as existing `_render_contacts_result()`
- Suggestion message includes count and names — e.g., "3 contacts overdue for follow-up: Dr. Smith, Prof. Jones, Dr. Lee — review now?"

**TTS Result Summaries and Demo Polish**
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

### Deferred Ideas (OUT OF SCOPE)
- Real-time streaming transcription during speech (VOICE-05)
- Wake word activation "Hey Jarvis" (VOICE-06)
- Agent self-modification or dynamic tool creation (ORCH-05)
- Mobile-responsive command center layout (DASH-04)
- Full React migration using mockup design tokens from `docs/mockup/`
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DASH-01 | Visual command center shows per-agent swimlane cards with idle/running/awaiting/complete status | `st.columns()` for horizontal layout; `agent_swimlanes` session state dict keyed by proposal_id; swimlane_dashboard.py module |
| DASH-02 | Dashboard updates in real-time as agents dispatch, execute, and return results — no manual refresh | `@st.fragment(run_every=2)` verified working in Streamlit 1.42.2; existing `_poll_result_bus()` fragment extended to update swimlane state |
| DASH-03 | Command center integrates into existing Streamlit app as a new tab | Command Center tab already exists in `app.py` as `tab_command`; swimlane section inserted inside `render_command_center_tab()` |
| POC-03 | Jarvis surfaces POC follow-up status as part of proactive suggestions | `poc_contacts.json` has 3 contacts with `follow_up_due < 2026-03-24`; `check_overdue_contacts()` extends `suggestions.py`; existing HITL flow reused |
</phase_requirements>

---

## Summary

Phase 7 layers orchestration and visual monitoring on top of the Phase 6 direct-dispatch foundation. Three distinct delivery areas must be completed: (1) a NemoClaw adapter that wraps the existing TOOL_REGISTRY callables as an optional orchestration path, (2) a swimlane dashboard rendered inside the existing Command Center tab that shows real-time per-agent status using the already-verified `@st.fragment(run_every=2)` polling pattern, and (3) two extensions to the coordinator layer — a proactive overdue-contacts suggestion and a multi-step "prepare campaign" intent.

The openclaw-sdk 2.1.0 is available on PyPI and was inspected directly. Its key parallel dispatch mechanism is `Agent.batch(queries, max_concurrency=N)` which calls `asyncio.gather` internally. The SDK does NOT expose a "register Python callable as a NemoClaw tool" API — it is an agent-execution client, not a function-registry. The correct integration pattern for Phase 7 is therefore: (a) construct an `OpenClawClient` that connects to a local/remote NemoClaw gateway, (b) create named agents corresponding to each TOOL_REGISTRY entry, (c) dispatch queries to those agents in parallel via `batch()`, and (d) map returned `ExecutionResult` objects back to the existing result bus format. The direct-dispatch fallback (current Phase 6 path) requires zero changes and activates silently when `USE_NEMOCLAW` is unset or the SDK import fails.

The Streamlit swimlane requirement is fully supported by the existing stack: `st.columns(N)` renders N side-by-side containers, each holding an agent status card; the existing `@st.fragment(run_every=2)` fragment in `_poll_result_bus()` already fires every 2 seconds and updates `st.session_state["action_proposals"]`. Adding a new `agent_swimlanes` dict to session state and rendering it inside the fragment is sufficient for DASH-01 and DASH-02 without any new dependencies.

**Primary recommendation:** Build the NemoClaw adapter as a thin async wrapper that calls `Agent.batch()` when `USE_NEMOCLAW=1` and falls back to the Phase 6 `dispatch()` calls otherwise. Build the swimlane dashboard as a new `src/ui/swimlane_dashboard.py` module rendered from within the existing `_poll_result_bus()` fragment. Extend `suggestions.py` with `check_overdue_contacts()`. Extend `intent_parser.py` with `prepare_campaign` intent. All 539 existing tests must remain green.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| streamlit | 1.42.2 (installed) | UI rendering and fragment polling | Already in use; fragment + columns API verified |
| openclaw-sdk | 2.1.0 (PyPI) | NemoClaw parallel agent dispatch | Only official NVIDIA/OpenClaw SDK; inspected API |
| asyncio | stdlib | Run `Agent.batch()` in executor thread | openclaw-sdk is async; must bridge to Streamlit's sync thread model |
| threading / queue | stdlib | Background dispatch (existing Phase 6 pattern) | Direct-dispatch fallback already uses this; no change needed |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| structlog | 25.5.0 | Structured logging (openclaw-sdk dependency) | Auto-installed with openclaw-sdk; use for adapter logging |
| pydantic | 2.x (installed) | openclaw-sdk model validation | Already in venv as openclaw-sdk dependency |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| openclaw-sdk Agent.batch() | asyncio.gather on raw HTTP calls | More fragile; loses SDK retry/error handling |
| st.fragment(run_every=2) | st.autorefresh (3rd party) | st.fragment is built-in and already working |
| New swimlane_dashboard.py module | Inline code in command_center.py | command_center.py is already 385 lines; module extraction keeps files focused |

**Installation (NemoClaw adapter path only):**
```bash
pip install openclaw-sdk==2.1.0
```
No other new dependencies. The swimlane dashboard and proactive suggestions extensions use only the existing stack.

**Version verification (confirmed 2026-03-24):**
```
openclaw-sdk 2.1.0   — released 2026-02-28, installed in project venv
streamlit    1.42.2  — installed in project venv
```

---

## Architecture Patterns

### Recommended Project Structure (additions only)
```
src/
├── coordinator/
│   ├── nemoclaw_adapter.py   # NEW: OpenClaw adapter wrapping TOOL_REGISTRY
│   └── suggestions.py        # EXTEND: add check_overdue_contacts()
│   └── intent_parser.py      # EXTEND: add prepare_campaign intent + multi-step parse
├── ui/
│   ├── swimlane_dashboard.py  # NEW: horizontal agent status cards
│   └── command_center.py     # EXTEND: wire swimlane + TTS on completion + demo hints
└── runtime_state.py          # EXTEND: add agent_swimlanes key
tests/
├── test_nemoclaw_adapter.py   # NEW
├── test_swimlane_dashboard.py # NEW
└── test_suggestions.py        # EXTEND with overdue contacts tests
```

### Pattern 1: NemoClaw Adapter with Graceful Degradation
**What:** Try `import openclaw_sdk` at module load; set `NEMOCLAW_AVAILABLE = False` on ImportError. When `USE_NEMOCLAW=1` AND `NEMOCLAW_AVAILABLE`, run parallel agent dispatch via `Agent.batch()`. Otherwise fall through to existing `result_bus.dispatch()` calls.
**When to use:** Every time an approved action needs dispatching.
**Example:**
```python
# src/coordinator/nemoclaw_adapter.py
from __future__ import annotations
import asyncio
import logging
import os
from typing import Any, Callable

logger = logging.getLogger(__name__)

try:
    from openclaw_sdk import OpenClawClient, AgentConfig
    NEMOCLAW_AVAILABLE = True
except ImportError:
    NEMOCLAW_AVAILABLE = False
    logger.warning("openclaw-sdk not installed — NemoClaw dispatch unavailable")


def dispatch_parallel(
    tasks: list[tuple[str, Callable[[dict], dict], dict]],
    fallback_dispatch: Callable,
) -> None:
    """Dispatch list of (proposal_id, tool_fn, params) in parallel.

    Uses NemoClaw Agent.batch() when USE_NEMOCLAW=1 and SDK is available.
    Falls back to sequential result_bus.dispatch() calls otherwise.

    Args:
        tasks: [(proposal_id, tool_fn, params), ...]
        fallback_dispatch: result_bus.dispatch callable
    """
    use_nemo = os.getenv("USE_NEMOCLAW", "0") == "1" and NEMOCLAW_AVAILABLE
    if not use_nemo:
        for proposal_id, tool_fn, params in tasks:
            fallback_dispatch(proposal_id, tool_fn, params)
        return
    # NemoClaw path — run in a daemon thread to avoid blocking Streamlit
    import threading
    thread = threading.Thread(
        target=_run_nemoclaw_parallel,
        args=(tasks, fallback_dispatch),
        daemon=True,
    )
    thread.start()


def _run_nemoclaw_parallel(
    tasks: list[tuple[str, Callable[[dict], dict], dict]],
    fallback_dispatch: Callable,
) -> None:
    """Sync wrapper: run asyncio event loop for NemoClaw batch dispatch."""
    try:
        asyncio.run(_nemo_batch(tasks))
    except Exception as exc:
        logger.error("NemoClaw parallel dispatch failed: %s — using fallback", exc)
        for proposal_id, tool_fn, params in tasks:
            fallback_dispatch(proposal_id, tool_fn, params)
```

**Key insight:** `openclaw_sdk.Agent.batch()` calls `asyncio.gather` internally. The `asyncio.run()` wrapper in a daemon thread avoids blocking the Streamlit event loop. Results must be written back to `st.session_state["result_queues"]` via `queue.Queue` — the same mechanism Phase 6 already uses.

### Pattern 2: Swimlane Dashboard via Fragment Polling
**What:** A `render_swimlane_dashboard()` function in `swimlane_dashboard.py` reads `agent_swimlanes` from session state and renders a horizontal row of status cards using `st.columns()`. It is called inside the existing `_poll_result_bus()` fragment so it refreshes every 2 seconds automatically.
**When to use:** After every result bus poll update.
**Example:**
```python
# src/ui/swimlane_dashboard.py
from __future__ import annotations
import streamlit as st


STATUS_COLORS = {
    "idle":      "gray",
    "running":   "blue",
    "awaiting":  "yellow",
    "completed": "green",
    "failed":    "red",
}


def render_swimlane_dashboard() -> None:
    """Render horizontal per-agent swimlane cards. No-op when no active agents."""
    swimlanes: dict = st.session_state.get("agent_swimlanes", {})
    if not swimlanes:
        return

    entries = list(swimlanes.values())[-8:]  # max 8 visible
    if not entries:
        return

    st.markdown("### Agent Status")
    cols = st.columns(len(entries))
    for col, entry in zip(cols, entries):
        with col:
            status = entry.get("status", "idle")
            color = STATUS_COLORS.get(status, "gray")
            elapsed = entry.get("elapsed_s", 0)
            summary = entry.get("summary", "")
            st.markdown(
                f'<div style="border:1px solid {color};border-radius:8px;padding:8px;">'
                f'<b>{entry["agent_name"]}</b><br>'
                f'<span style="color:{color}">{status.upper()}</span><br>'
                f'<small>{elapsed:.0f}s</small><br>'
                f'<small>{summary}</small>'
                f'</div>',
                unsafe_allow_html=True,
            )
```

### Pattern 3: Overdue Contacts Proactive Suggestion
**What:** `check_overdue_contacts()` in `suggestions.py` loads `poc_contacts.json`, identifies contacts with `follow_up_due < today`, and returns an ActionProposal with `source="proactive"`.
**When to use:** Called from `_inject_proactive_suggestions()` in `command_center.py` after staleness check (stale check takes priority).
**Example:**
```python
# src/coordinator/suggestions.py — new function
def check_overdue_contacts(poc_contacts: list[dict]) -> list[ActionProposal]:
    """Return a proactive suggestion when overdue POC contacts exist.

    Called after check_staleness_conditions(). Returns empty list when
    no contacts are overdue. Returns at most one proposal.
    """
    today = datetime.date.today()
    overdue = [
        c for c in poc_contacts
        if c.get("follow_up_due")
        and datetime.date.fromisoformat(c["follow_up_due"]) < today
    ]
    if not overdue:
        return []
    names = ", ".join(c["name"] for c in overdue[:3])
    suffix = f" and {len(overdue) - 3} more" if len(overdue) > 3 else ""
    description = (
        f"{len(overdue)} contact(s) overdue for follow-up: "
        f"{names}{suffix} — review now?"
    )
    return [
        ActionProposal(
            intent="check_contacts",
            agent="Contacts Agent",
            description=description,
            reasoning="POC contacts have passed their follow_up_due date.",
            source="proactive",
        )
    ]
```

### Pattern 4: Multi-Step Intent (prepare_campaign)
**What:** `prepare_campaign` intent in `intent_parser.py` maps to a list of sub-intents. `parse_intent()` detects multi-step intents and returns a special `ParsedIntent` with `intent="prepare_campaign"`. `_handle_text_command()` detects this and creates one `ActionProposal` per sub-intent.
**When to use:** When user says "Prepare for X" or "Full outreach campaign".
**Example:**
```python
# intent_parser.py — extend SUPPORTED_INTENTS and ACTION_REGISTRY
SUPPORTED_INTENTS = frozenset({
    "discover_events", "rank_speakers", "generate_outreach",
    "check_contacts", "prepare_campaign", "unknown",
})

ACTION_REGISTRY.append({
    "intent": "prepare_campaign",
    "agent": "Campaign Orchestrator",
    "description": "Discover events + rank speakers + generate outreach (parallel)",
})

MULTI_STEP_INTENTS: dict[str, list[str]] = {
    "prepare_campaign": ["discover_events", "rank_speakers", "generate_outreach"],
}
```

### Pattern 5: Session State Extension for Swimlanes
**What:** Add `agent_swimlanes: dict[str, dict]` to `init_runtime_state()` in `runtime_state.py`. Each entry is keyed by `proposal_id` and stores `{"agent_name", "status", "elapsed_s", "summary", "started_at"}`.
**When to use:** When any proposal transitions from `proposed` → `executing`.
**Key:** Never store `ActionProposal` objects in swimlanes — only plain dicts. Avoids serialization issues and keeps swimlane rendering decoupled from the approval state machine.

### Anti-Patterns to Avoid
- **Calling `asyncio.run()` in the Streamlit main thread:** Streamlit's script thread has no event loop by default in 1.42.x; always run asyncio in a daemon thread via `threading.Thread`.
- **Putting NemoClaw client initialization in `import` scope:** OpenClawClient requires network connectivity; initialize lazily with `USE_NEMOCLAW=1` guard.
- **Mutating the `agent_swimlanes` dict from inside a fragment:** Fragments run in a sub-scope; write to `st.session_state["agent_swimlanes"]` directly (not to a local copy) so changes persist across reruns.
- **Growing swimlanes dict unboundedly:** Cap at 8 entries; pop oldest completed entries after 30s (check `entry["started_at"]`).
- **Modifying existing function signatures:** All 539 tests must stay green. No existing `run()`, `dispatch()`, or `poll_results()` signatures may change.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Parallel async execution | Custom asyncio task manager | `Agent.batch()` from openclaw-sdk | Already uses `asyncio.gather` with semaphore; handles errors per-task |
| Real-time UI polling | `st.empty()` loop with `time.sleep()` | `@st.fragment(run_every=2)` | Sleep loops block the thread; fragment is Streamlit-native |
| Sync-to-async bridge | `loop.run_until_complete()` in main thread | `asyncio.run()` in daemon thread + `queue.Queue` for results | Phase 6 threading pattern already proven; NemoClaw results post to same queues |
| Agent status persistence | Streamlit widget state | `st.session_state["agent_swimlanes"]` dict | Session state survives reruns; widget state does not |

**Key insight:** openclaw-sdk 2.1.0 does NOT provide a "register Python callable as a NemoClaw tool" API. The `Orchestrator` routes goals to named agents (remote processes), not to local Python functions. For this project, the correct NemoClaw pattern is: local tool callables remain in TOOL_REGISTRY; NemoClaw's value is parallel execution via `Agent.batch()` which fires multiple agent queries simultaneously. In practice, since the project's "agents" are local Python functions, the NemoClaw adapter wraps them as queries to a local OpenShell gateway — but this requires a running NemoClaw instance (NVIDIA NGC API key). The direct-dispatch fallback using `threading.Thread` + `queue.Queue` is the production-safe path.

---

## Runtime State Inventory

> Not a rename/refactor phase — this section is included only to document the new session state key that Phase 7 introduces.

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | `poc_contacts.json` — 5 contacts, 3 with `follow_up_due < 2026-03-24` (Maria Santos: 2026-02-28, James Okafor: 2026-03-15, Karen Liu: 2026-03-10) | No migration needed; file is seed data, already on disk |
| Live service config | `USE_NEMOCLAW` env var — new, not yet in `.env` | Add to `.env.example` and document in preflight checklist |
| OS-registered state | None — verified; no task scheduler, pm2, or systemd involvement | None |
| Secrets/env vars | `NVIDIA_NGC_API_KEY` — required for NemoClaw gateway; not yet in repo | Add to `.env.example`; graceful degradation if absent means this is non-blocking |
| Build artifacts | None — openclaw-sdk 2.1.0 installed, no compiled extensions | None |

New `st.session_state` keys introduced in Phase 7:

| Key | Type | Purpose |
|-----|------|---------|
| `agent_swimlanes` | `dict[str, dict]` | Per-agent status tracking for swimlane dashboard |

Initialized in `init_runtime_state()` with `{}` guard pattern (same as existing keys).

---

## Common Pitfalls

### Pitfall 1: asyncio.run() in Streamlit Main Thread
**What goes wrong:** `asyncio.run()` raises `RuntimeError: This event loop is already running` if called in the Streamlit script thread in certain configurations, or blocks the UI if called synchronously.
**Why it happens:** Streamlit 1.x does not expose a running event loop in the script thread; however, some environments (e.g. Jupyter-derived kernels) do, causing conflicts.
**How to avoid:** Always wrap `asyncio.run()` in a `threading.Thread(daemon=True)` and post results to `queue.Queue` — exactly the Phase 6 pattern. NemoClaw adapter must follow this same pattern.
**Warning signs:** `RuntimeError: This event loop is already running` or UI freezing after approve click.

### Pitfall 2: NemoClaw Gateway Not Running
**What goes wrong:** `OpenClawClient.connect()` raises `GatewayError` or `APIConnectionError` when no NemoClaw gateway is available.
**Why it happens:** The openclaw-sdk requires a running OpenClaw/NemoClaw gateway process. On demo day, this may not be started.
**How to avoid:** Wrap the NemoClaw dispatch path in try/except `(GatewayError, APIConnectionError, APITimeoutError)` — catch all openclaw exceptions and fall back to direct dispatch. Log at WARNING level. Do not raise.
**Warning signs:** Demo shows "failed" status cards for all agents simultaneously right after approve click.

### Pitfall 3: Fragment Rendering swimlane_dashboard Inside Poll Fragment
**What goes wrong:** Calling `render_swimlane_dashboard()` inside `_poll_result_bus()` may cause the swimlane section to render in an unexpected location if the fragment's output position is not fixed.
**Why it happens:** `@st.fragment` renders in the position where the fragment function is CALLED, not where it is defined. The fragment call position in `render_command_center_tab()` must be between the voice panel and conversation history.
**How to avoid:** Keep `_poll_result_bus()` call immediately after the voice panel `</div>` close tag, before `st.divider()` and `_render_conversation_history()`. The swimlane render happens inside the fragment so it auto-updates.
**Warning signs:** Swimlane cards appear below conversation history or disappear on rerun.

### Pitfall 4: Swimlane Dict Growing Unboundedly
**What goes wrong:** Every dispatched agent adds an entry to `agent_swimlanes`; after many commands the session accumulates dozens of stale entries, slowing rendering.
**Why it happens:** Entries are never evicted without explicit cleanup logic.
**How to avoid:** In `_poll_result_bus()`, after updating a swimlane entry to "completed" or "failed", check `started_at` and remove entries older than 30 seconds in "completed" state. Keep failed entries visible until manually dismissed (or cap at 8 total).
**Warning signs:** More than 8 columns rendered, causing narrow cards that overflow the viewport.

### Pitfall 5: Proactive Suggestion Guard Not Extended
**What goes wrong:** Both the staleness suggestion AND the overdue contacts suggestion inject simultaneously, violating the "at most 1 proactive suggestion" guard.
**Why it happens:** `_inject_proactive_suggestions()` must be extended to call `check_overdue_contacts()` ONLY when `check_staleness_conditions()` returns an empty list.
**How to avoid:** Implement as a two-phase check: `suggestions = check_staleness_conditions(...); if not suggestions: suggestions = check_overdue_contacts(...)`. The existing single-item guard in `_inject_proactive_suggestions()` then enforces the cap.
**Warning signs:** Two proactive proposal cards appear simultaneously in conversation history on a fresh session.

### Pitfall 6: prepare_campaign Creates Duplicate Proposals
**What goes wrong:** "Prepare for X" creates 3 simultaneous proposals (discover + rank + outreach). Each goes through the normal HITL approve/reject flow. If the user approves them sequentially, the results return at different times and the swimlane correctly shows them independently. But if `_handle_text_command()` creates all 3 at once and calls `st.rerun()` once, only the last proposal appears in the conversation history.
**Why it happens:** `st.rerun()` is called once per `_handle_text_command()` invocation; appending 3 history entries before the single rerun is correct.
**How to avoid:** Append all 3 `role: "proposal"` entries to `conversation_history` in a single `_handle_text_command()` call, THEN call `st.rerun()` once. Do not call `_handle_text_command()` recursively.
**Warning signs:** Only one of three prepare_campaign sub-proposals appears in conversation history.

---

## Code Examples

Verified patterns from direct code inspection:

### st.fragment run_every (verified: Streamlit 1.42.2)
```python
# Source: venv inspect of streamlit.fragment
@st.fragment(run_every=2)
def _poll_result_bus() -> None:
    """Polls every 2 seconds; updates session state; renders swimlane."""
    proposals = st.session_state.get("action_proposals", {})
    for proposal_id, payload in poll_results():
        proposal = proposals.get(proposal_id)
        if proposal is None:
            continue
        if payload["status"] == "completed":
            proposal.status = "completed"
            proposal.result = _format_result(payload["result"])
            _update_swimlane(proposal_id, "completed", proposal.result)
            _speak_text(proposal.result)   # TTS on completion
        else:
            proposal.status = "failed"
            proposal.result = f"Error: {payload.get('error', 'unknown')}"
            _update_swimlane(proposal_id, "failed", proposal.result)
    # Render swimlane inside the fragment so it auto-refreshes
    render_swimlane_dashboard()
```

### openclaw_sdk Agent.batch() parallel dispatch (verified: SDK 2.1.0 source)
```python
# Source: openclaw_sdk Agent class (inspected from installed wheel)
# Agent.batch() signature:
async def batch(
    self,
    queries: list[str],
    options: ExecutionOptions | None = None,
    callbacks: list[CallbackHandler] | None = None,
    max_concurrency: int | None = None,
) -> list[ExecutionResult]:
    sem = asyncio.Semaphore(max_concurrency if max_concurrency is not None else len(queries))
    async def _run(query: str) -> ExecutionResult:
        async with sem:
            return await self.execute(query, options=options, callbacks=callbacks)
    return list(await asyncio.gather(*[_run(q) for q in queries]))
```

### openclaw_sdk KNOWN_PROVIDERS (verified: SDK 2.1.0)
```python
# Note: Nemotron is NOT in KNOWN_PROVIDERS. Available providers:
KNOWN_PROVIDERS = {
    'anthropic': ['claude-opus-4-6', 'claude-sonnet-4-6', ...],
    'openai': ['gpt-4o', 'gpt-4o-mini', 'gpt-4.1', ...],
    'google': ['gemini-3-flash', 'gemini-2.5-pro', ...],
    'ollama': ['llama3.3', 'mistral', 'codellama', 'deepseek-r1'],
    # No 'nvidia' or 'nemotron' provider listed
}
```

### swimlane session state update helper
```python
def _update_swimlane(proposal_id: str, status: str, summary: str) -> None:
    """Update or create a swimlane entry in session state."""
    import time
    swimlanes: dict = st.session_state.setdefault("agent_swimlanes", {})
    entry = swimlanes.get(proposal_id, {})
    entry["status"] = status
    entry["summary"] = summary[:80]
    if "started_at" not in entry:
        entry["started_at"] = time.monotonic()
    entry["elapsed_s"] = time.monotonic() - entry["started_at"]
    swimlanes[proposal_id] = entry
```

### demo hint chips (st.button row on empty conversation)
```python
# Inside _render_conversation_history() when history is empty:
DEMO_HINTS = [
    "Find new events",
    "Rank speakers for CPP Career Fair",
    "Prepare full outreach campaign",
]
cols = st.columns(len(DEMO_HINTS))
for col, hint in zip(cols, DEMO_HINTS):
    with col:
        if st.button(hint, key=f"hint_{hint}"):
            _handle_text_command(hint)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `st.experimental_fragment` | `st.fragment` (stable) | Streamlit 1.33+ | `run_every` parameter stable; no experimental import needed |
| Serial tool dispatch (Phase 5 stub) | Threaded dispatch via result_bus (Phase 6) | Phase 6 complete | Phase 7 can use the same threading model for NemoClaw fallback |
| NemoClaw alpha (March 2026) | openclaw-sdk 2.1.0 (released 2026-02-28) | 2026-02-28 | API has stabilized from the alpha noted in STATE.md; `Agent.batch()` is confirmed present |

**Deprecated/outdated:**
- `st.experimental_fragment`: replaced by `st.fragment` (already using stable form in codebase)
- Nemotron model in `KNOWN_PROVIDERS`: **NOT listed** — openclaw-sdk 2.1.0 does not include a `nvidia` or `nemotron` provider key. Nemotron dispatch would require a custom gateway or `ollama` with a locally pulled Nemotron model. This is a MEDIUM-confidence finding (see Open Questions).

---

## Open Questions

1. **Nemotron model availability via openclaw-sdk**
   - What we know: `KNOWN_PROVIDERS` in openclaw-sdk 2.1.0 does not include `nvidia` or `nemotron`. The SDK supports `ollama` with local models.
   - What's unclear: Whether NVIDIA NGC API keys can be used via a custom gateway pointing openclaw-sdk's `openai`-compatible provider at `build.nvidia.com`.
   - Recommendation: For the demo, use `ollama` with a local Nemotron-compatible model OR use the `openai`-compatible provider pointed at NGC. The adapter should accept an env var `NEMOCLAW_MODEL` defaulting to a safe value. If NGC key is unavailable, the graceful degradation to direct-dispatch covers the demo.

2. **NemoClaw gateway requirement**
   - What we know: `OpenClawClient.connect()` probes for a running OpenClaw/NemoClaw gateway process. Without it, the NemoClaw path fails immediately.
   - What's unclear: Whether the demo environment will have NemoClaw installed and running on the day.
   - Recommendation: The direct-dispatch fallback is the primary demo path. NemoClaw path is a "bonus" that activates with `USE_NEMOCLAW=1`. Plan swimlane dashboard to work fully with direct-dispatch.

3. **prepare_campaign Gemini prompt template**
   - What we know: Gemini is used for intent parsing via `parse_intent()`; current prompt lists single-intent actions only.
   - What's unclear: Whether Gemini reliably maps "Prepare for X" to `prepare_campaign` vs. one of the three sub-intents.
   - Recommendation: Add `prepare_campaign` to the system prompt's action list with a clear description: "Orchestrate full campaign: discover events, rank speakers, AND generate outreach in parallel." Test with 3-4 phrasings and add keyword fallback in `parse_intent()` if Gemini returns a single sub-intent for "prepare" commands.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.3.4 |
| Config file | `pytest.ini` or auto-discovery (no explicit config file found; uses `tests/` directory) |
| Quick run command | `cd "Category 3 - IA West Smart Match CRM" && .venv/bin/python -m pytest tests/ -x -q` |
| Full suite command | `cd "Category 3 - IA West Smart Match CRM" && .venv/bin/python -m pytest tests/ -q` |

**Baseline:** 539 tests collected, all passing (verified 2026-03-24).

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| DASH-01 | Swimlane cards render for dispatched agents | unit | `pytest tests/test_swimlane_dashboard.py -x` | ❌ Wave 0 |
| DASH-01 | Swimlane shows idle/running/complete/failed statuses | unit | `pytest tests/test_swimlane_dashboard.py::TestSwimlaneDashboard -x` | ❌ Wave 0 |
| DASH-02 | `_poll_result_bus()` updates swimlane state on completion | unit | `pytest tests/test_command_center.py::TestPollResultBus -x` | ✅ extend existing |
| DASH-02 | Dashboard renders within fragment (2s cadence relies on Streamlit runtime — manual only) | manual-only | N/A — requires running Streamlit | N/A |
| DASH-03 | Command Center tab exists and renders without error | unit | `pytest tests/test_app.py -x` | ✅ extend existing |
| POC-03 | `check_overdue_contacts()` returns proposal when contacts overdue | unit | `pytest tests/test_suggestions.py::TestOverdueContacts -x` | ❌ Wave 0 |
| POC-03 | `_inject_proactive_suggestions()` injects contact suggestion after staleness check | unit | `pytest tests/test_command_center.py::TestProactiveSuggestion -x` | ✅ extend existing |
| N/A | All 539 existing tests still pass | regression | `pytest tests/ -q` | ✅ |
| N/A | NemoClaw adapter graceful degradation on ImportError | unit | `pytest tests/test_nemoclaw_adapter.py::TestGracefulDegradation -x` | ❌ Wave 0 |
| N/A | multi-step prepare_campaign creates 3 sub-proposals | unit | `pytest tests/test_intent_parser.py::TestPrepareIntent -x` | ❌ Wave 0 |
| N/A | TTS called on every completed proposal | unit | `pytest tests/test_command_center.py::TestTTSOnCompletion -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `cd "Category 3 - IA West Smart Match CRM" && .venv/bin/python -m pytest tests/ -x -q`
- **Per wave merge:** `cd "Category 3 - IA West Smart Match CRM" && .venv/bin/python -m pytest tests/ -q`
- **Phase gate:** Full suite green (539+ tests) before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_swimlane_dashboard.py` — covers DASH-01 rendering, status badge colors, compact fade logic
- [ ] `tests/test_nemoclaw_adapter.py` — covers graceful degradation (ImportError), direct-fallback path, parallel dispatch smoke test
- [ ] `tests/test_suggestions.py` — extend with `TestOverdueContacts`: overdue detection, empty list when no overdue, message formatting with names

*(Existing test infrastructure covers all other phase requirements with extensions to `test_command_center.py`, `test_intent_parser.py`, and `test_app.py`.)*

---

## Sources

### Primary (HIGH confidence)
- openclaw-sdk 2.1.0 wheel — inspected `Agent.batch()`, `Orchestrator`, `Pipeline`, `ConsensusGroup`, `KNOWN_PROVIDERS`, `AgentConfig` directly from installed package source
- Streamlit 1.42.2 installed in project venv — verified `st.fragment(run_every=N)` signature via `inspect.getsource`
- Project codebase (phases 4-6) — read `command_center.py`, `result_bus.py`, `suggestions.py`, `intent_parser.py`, `approval.py`, `runtime_state.py`, `tools/__init__.py`, `tests/conftest.py` directly
- `data/poc_contacts.json` — read directly; 3 of 5 contacts have `follow_up_due` dates in the past as of 2026-03-24

### Secondary (MEDIUM confidence)
- PyPI openclaw-sdk page (fetched 2026-03-24) — confirmed version 2.1.0, Python 3.11-3.14, dependencies
- WebSearch: openclaw-sdk NemoClaw tool registration — confirmed NemoClaw is an agent-execution orchestration layer, not a function-registry

### Tertiary (LOW confidence)
- Nemotron model availability via NGC API compatible with openclaw-sdk — unverified; `KNOWN_PROVIDERS` does not list nvidia/nemotron; requires hands-on validation with NGC key

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — openclaw-sdk 2.1.0 installed and directly inspected; Streamlit version verified
- Architecture: HIGH — adapter/fallback pattern matches existing Phase 4/6 graceful degradation patterns; all integration points verified from source
- NemoClaw parallel dispatch: HIGH — `Agent.batch()` confirmed in SDK source; asyncio.gather usage confirmed
- Nemotron model config: LOW — not in KNOWN_PROVIDERS; NGC compatibility unverified
- Pitfalls: HIGH — asyncio/Streamlit threading pitfall verified from known Streamlit constraints; others derived from direct code inspection

**Research date:** 2026-03-24
**Valid until:** 2026-04-24 (openclaw-sdk is stabilizing; check for patch releases before Phase 7 execution)
