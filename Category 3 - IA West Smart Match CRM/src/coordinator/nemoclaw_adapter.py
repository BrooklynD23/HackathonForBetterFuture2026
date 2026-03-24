"""NemoClaw parallel dispatch adapter with graceful degradation.

Pure Python — no top-level Streamlit imports. Fully testable in isolation.

When USE_NEMOCLAW=1 and openclaw-sdk is installed, dispatches tasks in
parallel using the NemoClaw Agent.batch() API. Otherwise falls back silently
to the result_bus.dispatch() serial direct-dispatch path.
"""

from __future__ import annotations

import asyncio
import logging
import os
import threading
from typing import Any, Callable

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# SDK availability probe — try/except at module load time
# ---------------------------------------------------------------------------
try:
    from openclaw_sdk import AgentConfig, OpenClawClient  # type: ignore[import]

    NEMOCLAW_AVAILABLE: bool = True
except ImportError:
    NEMOCLAW_AVAILABLE = False
    logger.warning("openclaw-sdk not installed -- NemoClaw dispatch unavailable")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

TaskList = list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]], dict[str, Any]]]


def dispatch_parallel(
    tasks: TaskList,
    fallback_dispatch: Callable,
) -> None:
    """Dispatch a batch of tasks in parallel via NemoClaw, or fall back to serial dispatch.

    Args:
        tasks: List of (proposal_id, tool_fn, params) triples.
        fallback_dispatch: Callable matching result_bus.dispatch(proposal_id, tool_fn, params).
    """
    use_nemo = os.getenv("USE_NEMOCLAW", "0") == "1" and NEMOCLAW_AVAILABLE
    if not use_nemo:
        # Serial direct-dispatch fallback — guaranteed to work on all environments
        for proposal_id, tool_fn, params in tasks:
            fallback_dispatch(proposal_id, tool_fn, params)
        return

    # Spawn a daemon thread so the Streamlit main thread is never blocked
    thread = threading.Thread(
        target=_run_nemoclaw_parallel,
        args=(tasks, fallback_dispatch),
        daemon=True,
    )
    thread.start()


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _run_nemoclaw_parallel(
    tasks: TaskList,
    fallback_dispatch: Callable,
) -> None:
    """Thread target: run NemoClaw batch, fall back to serial on any error."""
    try:
        asyncio.run(_nemo_batch(tasks))
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "NemoClaw parallel dispatch failed (%s) — falling back to serial dispatch",
            exc,
        )
        for proposal_id, tool_fn, params in tasks:
            fallback_dispatch(proposal_id, tool_fn, params)


async def _nemo_batch(tasks: TaskList) -> None:
    """Async coroutine: run all tasks in parallel via OpenClawClient.

    Lazy-imports streamlit to avoid top-level dependency (tests mock st).
    Results are posted to the same queue.Queue mechanism as result_bus.
    """
    import queue as queue_module  # noqa: PLC0415 — intentional lazy import

    import streamlit as st  # noqa: PLC0415 — intentional lazy import

    client = OpenClawClient()
    await client.connect()

    async def _run_one(proposal_id: str, tool_fn: Callable, params: dict) -> None:
        result_queues: dict[str, queue_module.Queue] = st.session_state.setdefault(
            "result_queues", {}
        )
        q: queue_module.Queue = queue_module.Queue(maxsize=1)
        result_queues[proposal_id] = q
        try:
            cfg = AgentConfig(fn=lambda: tool_fn(params))
            result = await client.run_agent(cfg)
            q.put({"status": "completed", "result": result})
        except Exception as exc:  # noqa: BLE001
            q.put({"status": "failed", "error": str(exc)})

    await asyncio.gather(*[
        _run_one(pid, fn, params) for pid, fn, params in tasks
    ])
