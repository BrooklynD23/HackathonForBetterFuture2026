from __future__ import annotations

from pathlib import Path
import sys
import textwrap

import yaml


TESTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
REPO_ROOT = SKILL_DIR.parents[2]

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from audit import audit_repo
from governance_common import (
    extract_inline_metadata,
    extract_percentage_range,
    extract_tier_token,
    load_manifest,
    read_markdown,
)
from reconcile import apply_reconciliations


def _sample_manifest() -> dict:
    return {
        "version": 1,
        "managed_by": "repo-governance",
        "generated_on": "2026-03-16",
        "decision_domains": {
            "portfolio.strategy_rationale": {"owner": "STRATEGIC_REVIEW.md", "description": "strategy"},
            "portfolio.conflict_resolution": {"owner": "STRATEGIC_REVIEW.md", "description": "conflicts"},
            "portfolio.rankings": {"owner": "MASTER_SPRINT_PLAN.md", "description": "rankings"},
            "portfolio.win_probabilities": {"owner": "MASTER_SPRINT_PLAN.md", "description": "win probabilities"},
            "portfolio.calendar": {"owner": "MASTER_SPRINT_PLAN.md", "description": "calendar"},
            "portfolio.staffing_model": {"owner": "MASTER_SPRINT_PLAN.md", "description": "staffing"},
            "category.1.execution_plan": {
                "owner": "Category 1 - Sample/SPRINT_PLAN.md",
                "description": "execution",
            },
            "category.1.feature_detail": {"owner": "PRD_SECTION_CAT1.md", "description": "feature detail"},
            "category.1.status": {"owner": "Category 1 - Sample/.status.md", "description": "status"},
            "category.1.background_analysis": {
                "owner": "Category 1 - Sample/PLAN.md",
                "description": "background",
            },
        },
        "documents": [
            {
                "id": "strategic",
                "label": "Strategic Review",
                "path": "STRATEGIC_REVIEW.md",
                "doc_kind": "strategic_review",
                "doc_role": "canonical",
                "category": None,
                "authority_scope": ["portfolio.strategy_rationale", "portfolio.conflict_resolution"],
                "canonical_upstreams": [],
            },
            {
                "id": "master",
                "label": "Master Sprint Plan",
                "path": "MASTER_SPRINT_PLAN.md",
                "doc_kind": "master_sprint_plan",
                "doc_role": "canonical",
                "category": None,
                "authority_scope": [
                    "portfolio.rankings",
                    "portfolio.win_probabilities",
                    "portfolio.calendar",
                    "portfolio.staffing_model",
                ],
                "canonical_upstreams": ["STRATEGIC_REVIEW.md"],
            },
            {
                "id": "cat1-prd",
                "label": "Category 1 PRD",
                "path": "PRD_SECTION_CAT1.md",
                "doc_kind": "prd_section",
                "doc_role": "canonical",
                "category": 1,
                "authority_scope": ["category.1.feature_detail"],
                "canonical_upstreams": [
                    "Category 1 - Sample/SPRINT_PLAN.md",
                    "MASTER_SPRINT_PLAN.md",
                    "STRATEGIC_REVIEW.md",
                ],
            },
            {
                "id": "cat1-plan",
                "label": "Category 1 PLAN",
                "path": "Category 1 - Sample/PLAN.md",
                "doc_kind": "plan",
                "doc_role": "background",
                "category": 1,
                "authority_scope": ["category.1.background_analysis"],
                "canonical_upstreams": [
                    "PRD_SECTION_CAT1.md",
                    "Category 1 - Sample/SPRINT_PLAN.md",
                    "MASTER_SPRINT_PLAN.md",
                    "STRATEGIC_REVIEW.md",
                ],
            },
            {
                "id": "cat1-sprint",
                "label": "Category 1 Sprint",
                "path": "Category 1 - Sample/SPRINT_PLAN.md",
                "doc_kind": "sprint_plan",
                "doc_role": "canonical",
                "category": 1,
                "authority_scope": ["category.1.execution_plan"],
                "canonical_upstreams": ["MASTER_SPRINT_PLAN.md", "STRATEGIC_REVIEW.md"],
            },
            {
                "id": "cat1-status",
                "label": "Category 1 Status",
                "path": "Category 1 - Sample/.status.md",
                "doc_kind": "status",
                "doc_role": "canonical",
                "category": 1,
                "authority_scope": ["category.1.status"],
                "canonical_upstreams": [
                    "PRD_SECTION_CAT1.md",
                    "Category 1 - Sample/SPRINT_PLAN.md",
                    "MASTER_SPRINT_PLAN.md",
                    "STRATEGIC_REVIEW.md",
                ],
            },
        ],
    }


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def _write_sample_repo(tmp_path: Path, *, strategic_range: str = "55-75%", sprint_range: str = "55-75%") -> Path:
    repo_root = tmp_path
    _write_text(
        repo_root / "MASTER_SPRINT_PLAN.md",
        f"""
        # Master Sprint Plan

        ## Revised Tier Rankings
        | Tier | Category | Win Prob | Condition |
        |------|----------|----------|-----------|
        | **1** | Cat 1 — Sample | 55-75% | Focus |
        """,
    )
    _write_text(
        repo_root / "STRATEGIC_REVIEW.md",
        f"""
        # Strategic Review

        ## Revised Win Probability Matrix
        | Category | Original | Revised Range | Realistic Midpoint | Key Risk |
        |----------|----------|---------------|--------------------|----------|
        | Cat 1 (Sample) | 40-60% | {strategic_range} | 65% | Demo |

        ## Revised Tier Rankings
        | Tier | Category | Condition |
        |------|----------|-----------|
        | **1** | Cat 1 (Sample) | Focus |
        """,
    )
    _write_text(
        repo_root / "PRD_SECTION_CAT1.md",
        """
        ## Category 1: Sample
        **Sponsor:** Sample | **CTO Tier:** 1 | **Verdict:** Approved

        ### Win Probability Assessment
        - **CTO Tier:** 1
        - **Overall Win Probability:** High (55-75%).
        """,
    )
    _write_text(
        repo_root / "Category 1 - Sample/PLAN.md",
        """
        # Category 1 — Sample PLAN

        Historical notes only.
        """,
    )
    _write_text(
        repo_root / "Category 1 - Sample/SPRINT_PLAN.md",
        f"""
        # Category 1 — Sample Sprint Plan
        **Category:** Sample | **Tier:** 1 | **Win Probability:** {sprint_range}
        """,
    )
    _write_text(
        repo_root / "Category 1 - Sample/.status.md",
        """
        # Category 1 — Sample

        **Tier:** 1 (55-75% range)

        ## Pipeline Status

        | Stage   | Status | Who / Agent | Date       | Notes |
        |---------|--------|-------------|------------|-------|
        | IDEA    | done   | pre-existing | 2026-03-14 | |
        | FEATURES| done   | pre-existing | 2026-03-14 | |
        | DOC     | done   | sprint-planner | 2026-03-15 | See SPRINT_PLAN.md |
        | MEMORY  | pending | — | — | |
        | VERIFY  | pending | — | — | |
        | TEST    | pending | — | — | |
        | DRIFT   | done   | audit | 2026-03-15 | Audit complete |
        | COMMIT  | pending | — | — | |
        """,
    )

    manifest_path = repo_root / "docs/governance/canonical-map.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(_sample_manifest(), sort_keys=False), encoding="utf-8")
    return manifest_path


def _managed_text_snapshot(repo_root: Path) -> dict[str, str]:
    manifest = _sample_manifest()
    return {
        entry["path"]: (repo_root / entry["path"]).read_text(encoding="utf-8")
        for entry in manifest["documents"]
        if (repo_root / entry["path"]).exists()
    }


def test_repo_manifest_loads() -> None:
    manifest = load_manifest(REPO_ROOT / "docs/governance/canonical-map.yaml")
    assert manifest["managed_by"] == "repo-governance"
    assert len(manifest["documents"]) == 22


def test_extracts_frontmatter_and_known_markdown_patterns(tmp_path: Path) -> None:
    path = tmp_path / "sample.md"
    path.write_text(
        """---
doc_role: canonical
authority_scope:
  - portfolio.rankings
canonical_upstreams: []
last_reconciled: 2026-03-16
managed_by: repo-governance
---

# Sample
**Tier:** 1 (55-75% range)
**Win Probability:** 55-75%
""",
        encoding="utf-8",
    )
    document = read_markdown(path)
    metadata = extract_inline_metadata(document.body)
    assert document.frontmatter["doc_role"] == "canonical"
    assert metadata["Tier"] == "1 (55-75% range)"
    assert extract_tier_token(metadata["Tier"]) == "1"
    assert extract_percentage_range(metadata["Tier"]) == "55-75%"
    assert extract_percentage_range(metadata["Win Probability"]) == "55-75%"


def test_audit_golden_clean_repo(tmp_path: Path) -> None:
    manifest_path = _write_sample_repo(tmp_path)
    apply_reconciliations(tmp_path, manifest_path, "portfolio", "2026-03-16", dry_run=False)
    report = audit_repo(tmp_path, manifest_path, "portfolio", "2026-03-16")
    assert report["safe_reconcile"] == []
    assert report["needs_human_decision"] == []
    assert report["unmanaged_governed_docs"] == []


def test_audit_golden_safe_drift(tmp_path: Path) -> None:
    manifest_path = _write_sample_repo(tmp_path, sprint_range="10-20%")
    report = audit_repo(tmp_path, manifest_path, "portfolio", "2026-03-16")
    fields = {issue["field"] for issue in report["safe_reconcile"]}
    assert "frontmatter.doc_role" in fields
    assert "governance.notice" in fields
    assert "category.1.portfolio.win_probabilities" in fields
    assert report["needs_human_decision"] == []


def test_audit_golden_needs_human_decision(tmp_path: Path) -> None:
    manifest_path = _write_sample_repo(tmp_path, strategic_range="40-50%")
    report = audit_repo(tmp_path, manifest_path, "portfolio", "2026-03-16")
    human_fields = {(issue["path"], issue["field"]) for issue in report["needs_human_decision"]}
    assert ("STRATEGIC_REVIEW.md", "category.1.portfolio.win_probabilities") in human_fields


def test_reconcile_is_idempotent(tmp_path: Path) -> None:
    manifest_path = _write_sample_repo(tmp_path, sprint_range="10-20%")
    first_changes = apply_reconciliations(tmp_path, manifest_path, "portfolio", "2026-03-16", dry_run=False)
    snapshot_after_first = _managed_text_snapshot(tmp_path)
    second_changes = apply_reconciliations(tmp_path, manifest_path, "portfolio", "2026-03-16", dry_run=False)
    snapshot_after_second = _managed_text_snapshot(tmp_path)

    assert first_changes
    assert second_changes == []
    assert snapshot_after_first == snapshot_after_second
