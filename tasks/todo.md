# Todo

## Current Work

- [x] Capture the next task with a clear scope and success criteria.
- [x] Add implementation steps before making code changes.
- [x] Reconcile the Category 3 runtime changes into canonical and sprint-level documentation.
- [x] Repair the repo-governance audit/reconcile scripts so they work with this repo layout.
- [x] Regenerate Category 3 governance artifacts to eliminate documentation drift.
- [x] Verify the runtime fixes, governance scripts, and generated reports before handoff.

## Review

- Status: Complete
- Notes: Matches now attempts a first-run embedding cache bootstrap when cache artifacts are missing and a Gemini key is configured. Embedding metadata now uses JSON instead of pickle, explanation caching only persists successful Gemini responses tagged with `source: gemini`, and Category 3 docs/governance artifacts now mirror that runtime contract.
- Verification:
  - `./.venv/bin/python -m pytest tests/test_app.py tests/test_embeddings.py tests/test_explanations.py` -> 39 passed
  - `./.venv/bin/python -m pytest` -> 199 passed
  - `python3 .agents/skills/repo-governance/scripts/audit.py --scope category:3 --report docs/governance/reports/2026-03-18-category-3-audit.md` -> 6 safe reconciliations, 0 human-decision items
  - `python3 .agents/skills/repo-governance/scripts/reconcile.py --scope category:3 --report docs/governance/reports/2026-03-18-category-3-governance.md` -> 0 remaining safe reconciliations, 0 human-decision items
- Follow-ups:
  - Existing local `.pkl` embedding metadata files are no longer read. The app will regenerate JSON metadata on next successful cache bootstrap.
