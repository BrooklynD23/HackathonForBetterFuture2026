---
name: repo-governance
description: "Audit and reconcile repo-checked-in planning governance for canonical sources, derived mirrors, background docs, governance frontmatter, reference indexes, and dated drift reports. Use when planning docs change, category-level decisions change, or before handoff. Supported scopes: portfolio, category:<n>, doc:<path>."
---

# Repo Governance

Use the repo copy of this skill as the authority for planning-doc governance. Keep path layouts intact in v1. Add and maintain a canonical source contract on top of the current markdown corpus.

## Workflow

Run this sequence in order:

1. Inventory governed docs from `docs/governance/canonical-map.yaml`.
2. Extract governed fields from frontmatter and known markdown patterns.
3. Detect drift by field, not only by file presence.
4. Classify drift as `safe-reconcile` or `needs-human-decision`.
5. Apply only safe reconciliations.
6. Regenerate `docs/governance/REPO_REFERENCE.md`.
7. Emit a dated report in `docs/governance/reports/`.

## Scope Contract

Use one of these scopes:

- `portfolio`
- `category:<n>`
- `doc:<path>`

## Canonical Policy

- Treat `STRATEGIC_REVIEW.md` as the owner of strategic rationale and conflict-resolution guidance.
- Treat `MASTER_SPRINT_PLAN.md` as the owner of portfolio rankings, portfolio staffing model, and the canonical day-number schedule.
- Treat each category `SPRINT_PLAN.md` as the owner of stack, scope, staffing, milestones, and gating rules for that category.
- Treat each `PRD_SECTION_CAT<n>.md` as the owner of category feature-detail narrative. Do not let it override sprint-plan execution decisions.
- Treat each `Category <n>/.status.md` as the owner of stage state only.
- Treat each `Category <n>/PLAN.md` as background analysis unless the manifest explicitly promotes it.
- Any doc that is not canonical for a field must mirror the canonical value or declare itself background or superseded.
- Do not invent new canonical values when sources disagree.

## Safe Auto-Edits

- Add or refresh governance frontmatter.
- Add or refresh governance notices for canonical, derived, background, or superseded docs.
- Sync supported derived metadata values from canonical docs when the pattern is deterministic.
- Refresh `last_reconciled`.
- Normalize `.status.md` governance metadata and canonical-doc links.
- Regenerate the governance report and repo reference index.

## Forbidden Auto-Edits

- Change substantive product decisions inside canonical docs.
- Move files.
- Change application code.
- Resolve conflicting canonical values without an explicit human decision.

## Commands

Use the bundled scripts from the repo root:

```bash
python .agents/skills/repo-governance/scripts/inventory.py --scope portfolio
python .agents/skills/repo-governance/scripts/audit.py --scope category:3 --report docs/governance/reports/2026-03-16-category-3-audit.md
python .agents/skills/repo-governance/scripts/reconcile.py --scope portfolio
python .agents/skills/repo-governance/scripts/reconcile.py --scope doc:PRD_SECTION_CAT2.md --dry-run
python .agents/skills/repo-governance/scripts/build_index.py
```

## Output Expectations

- Reports must say what was scanned, what was safely reconciled, and what still needs a human decision.
- `needs-human-decision` items must stay explicit. Do not silently “fix” them.
- `REPO_REFERENCE.md` must show canonical docs by decision type, derived docs by category, background or superseded docs, and the last drift review per category.
