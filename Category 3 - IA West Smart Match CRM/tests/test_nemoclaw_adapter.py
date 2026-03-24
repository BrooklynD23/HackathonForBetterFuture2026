"""Tests for nemoclaw_adapter.py — NemoClaw dispatch with graceful degradation."""

from __future__ import annotations

import os
import sys
import types
from unittest.mock import MagicMock, call, patch

import pytest


class TestNemoClawAvailability:
    """Tests for NEMOCLAW_AVAILABLE flag based on import availability."""

    def test_nemoclaw_available_false_when_import_fails(self) -> None:
        """When openclaw_sdk is not installed, NEMOCLAW_AVAILABLE is False."""
        # Ensure openclaw_sdk is NOT in sys.modules
        mods_to_remove = [k for k in sys.modules if k.startswith("openclaw_sdk")]
        saved = {k: sys.modules.pop(k) for k in mods_to_remove}
        # Also remove the adapter module so it re-imports
        adapter_mod = sys.modules.pop("src.coordinator.nemoclaw_adapter", None)
        try:
            # Patch the import to fail
            with patch.dict(sys.modules, {"openclaw_sdk": None}):
                import src.coordinator.nemoclaw_adapter as adapter
                importlib_reload = False
                assert adapter.NEMOCLAW_AVAILABLE is False
        finally:
            # Restore
            sys.modules.update(saved)
            if adapter_mod is not None:
                sys.modules["src.coordinator.nemoclaw_adapter"] = adapter_mod


class TestDispatchParallelFallback:
    """Tests for the fallback path in dispatch_parallel()."""

    def _make_tasks(self, n: int = 2) -> list:
        """Create n dummy tasks as (proposal_id, tool_fn, params) tuples."""
        tasks = []
        for i in range(n):
            tool_fn = MagicMock(return_value={"status": "ok"})
            tasks.append((f"pid-{i}", tool_fn, {"key": f"val-{i}"}))
        return tasks

    def test_dispatch_parallel_fallback_when_no_env_var(self) -> None:
        """When USE_NEMOCLAW is unset, dispatch_parallel() calls fallback_dispatch for each task."""
        # Remove the adapter module so env changes take effect at import time
        sys.modules.pop("src.coordinator.nemoclaw_adapter", None)
        import src.coordinator.nemoclaw_adapter as adapter

        tasks = self._make_tasks(2)
        fallback = MagicMock()

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("USE_NEMOCLAW", None)
            adapter.dispatch_parallel(tasks, fallback)

        assert fallback.call_count == 2

    def test_dispatch_parallel_fallback_when_sdk_unavailable(self) -> None:
        """When NEMOCLAW_AVAILABLE is False even with USE_NEMOCLAW=1, uses fallback."""
        sys.modules.pop("src.coordinator.nemoclaw_adapter", None)
        import src.coordinator.nemoclaw_adapter as adapter

        original_available = adapter.NEMOCLAW_AVAILABLE
        adapter.NEMOCLAW_AVAILABLE = False

        tasks = self._make_tasks(2)
        fallback = MagicMock()

        try:
            with patch.dict(os.environ, {"USE_NEMOCLAW": "1"}):
                adapter.dispatch_parallel(tasks, fallback)
        finally:
            adapter.NEMOCLAW_AVAILABLE = original_available

        assert fallback.call_count == 2

    def test_dispatch_parallel_calls_fallback_sequentially(self) -> None:
        """Fallback path calls fallback_dispatch once per task, in order."""
        sys.modules.pop("src.coordinator.nemoclaw_adapter", None)
        import src.coordinator.nemoclaw_adapter as adapter

        original_available = adapter.NEMOCLAW_AVAILABLE
        adapter.NEMOCLAW_AVAILABLE = False

        fn0 = MagicMock(return_value={})
        fn1 = MagicMock(return_value={})
        fn2 = MagicMock(return_value={})
        tasks = [
            ("pid-0", fn0, {"a": 1}),
            ("pid-1", fn1, {"b": 2}),
            ("pid-2", fn2, {"c": 3}),
        ]
        fallback = MagicMock()

        try:
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("USE_NEMOCLAW", None)
                adapter.dispatch_parallel(tasks, fallback)
        finally:
            adapter.NEMOCLAW_AVAILABLE = original_available

        assert fallback.call_count == 3
        expected_calls = [
            call("pid-0", fn0, {"a": 1}),
            call("pid-1", fn1, {"b": 2}),
            call("pid-2", fn2, {"c": 3}),
        ]
        fallback.assert_has_calls(expected_calls, any_order=False)
