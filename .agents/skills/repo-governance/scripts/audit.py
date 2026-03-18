from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import Any
import json
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (
    DriftIssue,
    build_frontmatter,
    canonical_doc_links_for_status,
    compare_frontmatter,
    determine_last_drift_review,
    discover_governed_docs,
    expected_notice,
    extract_canonical_docs,
    extract_inline_metadata,
    extract_last_drift_review,
    extract_master_portfolio,
    extract_overall_win_probability_range,
    extract_percentage_range,
    extract_pipeline_status,
    extract_strategic_tiers,
    extract_strategic_win_probabilities,
    extract_tier_token,
    load_manifest,
    manifest_entries_by_path,
    read_markdown,
    select_manifest_entries,
)


def _issue(
    path: str,
    field: str,
    severity: str,
    message: str,
    current: Any = None,
    expected: Any = None,
    action: str | None = None,
) -> dict[str, Any]:
    return DriftIssue(
        path=path,
        field=field,
        severity=severity,
        message=message,
        current=current,
        expected=expected,
        action=action,
    ).to_dict()


def audit_repo(repo_root: Path, manifest_path: Path, scope: str, today: str) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    by_path = manifest_entries_by_path(manifest)
    selected = select_manifest_entries(manifest, scope)

    managed_paths = {entry["path"] for entry in manifest["documents"]}
    unmanaged_paths = []
    if scope == "portfolio":
        unmanaged_paths = [path for path in discover_governed_docs(repo_root) if path not in managed_paths]

    safe_reconcile: list[dict[str, Any]] = []
    needs_human_decision: list[dict[str, Any]] = []

    if unmanaged_paths:
        for path in unmanaged_paths:
            needs_human_decision.append(
                _issue(
                    path=path,
                    field="inventory.managed",
                    severity="needs-human-decision",
                    message="governed doc exists on disk but is missing from canonical-map.yaml",
                )
            )

    master_doc = read_markdown(repo_root / "MASTER_SPRINT_PLAN.md")
    master_portfolio = extract_master_portfolio(master_doc.body)

    strategic_doc = read_markdown(repo_root / "STRATEGIC_REVIEW.md")
    strategic_tiers = extract_strategic_tiers(strategic_doc.body)
    strategic_win_probabilities = extract_strategic_win_probabilities(strategic_doc.body)

    for entry in selected:
        doc_path = repo_root / entry["path"]
        if not doc_path.exists():
            needs_human_decision.append(
                _issue(
                    path=entry["path"],
                    field="inventory.exists",
                    severity="needs-human-decision",
                    message="managed doc is missing from the repo",
                )
            )
            continue

        document = read_markdown(doc_path)
        expected_frontmatter = build_frontmatter(entry, today)
        for key, current_value, expected_value in compare_frontmatter(document.frontmatter, expected_frontmatter):
            safe_reconcile.append(
                _issue(
                    path=entry["path"],
                    field=f"frontmatter.{key}",
                    severity="safe-reconcile",
                    message="governance frontmatter is missing or stale",
                    current=current_value,
                    expected=expected_value,
                    action="update_frontmatter",
                )
            )

        notice = expected_notice(entry)
        if notice not in document.body:
            safe_reconcile.append(
                _issue(
                    path=entry["path"],
                    field="governance.notice",
                    severity="safe-reconcile",
                    message="governance notice is missing or stale",
                    expected=notice,
                    action="upsert_notice",
                )
            )

        category = entry.get("category")
        canonical_portfolio = master_portfolio.get(category) if isinstance(category, int) else None

        if entry["doc_kind"] == "sprint_plan" and canonical_portfolio:
            metadata = extract_inline_metadata(document.body)
            tier_value = metadata.get("Tier")
            if tier_value and extract_tier_token(tier_value) != extract_tier_token(canonical_portfolio["tier"]):
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.rankings",
                        severity="safe-reconcile",
                        message="sprint-plan tier metadata does not match the master sprint plan",
                        current=tier_value,
                        expected=canonical_portfolio["tier"],
                        action="sync_sprint_tier",
                    )
                )
            win_probability = metadata.get("Win Probability")
            if win_probability and extract_percentage_range(win_probability) != extract_percentage_range(
                canonical_portfolio["win_probability"]
            ):
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.win_probabilities",
                        severity="safe-reconcile",
                        message="sprint-plan win probability metadata does not match the master sprint plan",
                        current=win_probability,
                        expected=canonical_portfolio["win_probability"],
                        action="sync_sprint_win_probability",
                    )
                )

        if entry["doc_kind"] == "prd_section" and canonical_portfolio:
            metadata = extract_inline_metadata(document.body)
            cto_tier = metadata.get("CTO Tier")
            if cto_tier and extract_tier_token(cto_tier) != extract_tier_token(canonical_portfolio["tier"]):
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.rankings",
                        severity="safe-reconcile",
                        message="PRD CTO tier metadata does not match the master sprint plan",
                        current=cto_tier,
                        expected=canonical_portfolio["tier"],
                        action="sync_prd_tier",
                    )
                )
            narrative_range = extract_overall_win_probability_range(document.body)
            canonical_range = extract_percentage_range(canonical_portfolio["win_probability"])
            if narrative_range and canonical_range and narrative_range != canonical_range:
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.win_probabilities",
                        severity="safe-reconcile",
                        message="PRD narrative win-probability range does not match the canonical master sprint plan",
                        current=narrative_range,
                        expected=canonical_range,
                        action="sync_prd_win_probability_range",
                    )
                )

        if entry["doc_kind"] == "status" and canonical_portfolio:
            metadata = extract_inline_metadata(document.body)
            tier_value = metadata.get("Tier")
            if extract_tier_token(tier_value) != extract_tier_token(canonical_portfolio["tier"]):
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.rankings",
                        severity="safe-reconcile",
                        message="status tier metadata does not match the master sprint plan",
                        current=tier_value,
                        expected=canonical_portfolio["tier"],
                        action="sync_status_tier",
                    )
                )
            current_range = extract_percentage_range(tier_value)
            canonical_range = extract_percentage_range(canonical_portfolio["win_probability"])
            if current_range and canonical_range and current_range != canonical_range:
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.portfolio.win_probabilities",
                        severity="safe-reconcile",
                        message="status win-probability range does not match the master sprint plan",
                        current=current_range,
                        expected=canonical_range,
                        action="sync_status_tier",
                    )
                )

            pipeline = extract_pipeline_status(document.body)
            missing_stages = sorted(stage for stage in ("DOC", "DRIFT") if stage not in pipeline)
            for stage in missing_stages:
                needs_human_decision.append(
                    _issue(
                        path=entry["path"],
                        field=f"status.pipeline.{stage}",
                        severity="needs-human-decision",
                        message=f".status.md is missing the {stage} row in Pipeline Status",
                    )
                )

            expected_canonical_docs = canonical_doc_links_for_status(entry, manifest)
            current_canonical_docs = extract_canonical_docs(document.body)
            if current_canonical_docs != expected_canonical_docs:
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.status.canonical_docs",
                        severity="safe-reconcile",
                        message="status governance canonical-doc links are missing or stale",
                        current=current_canonical_docs,
                        expected=expected_canonical_docs,
                        action="update_status_governance",
                    )
                )

            explicit_last_drift = extract_last_drift_review(document.body)
            derived_last_drift = determine_last_drift_review(document.body)
            if explicit_last_drift != derived_last_drift:
                safe_reconcile.append(
                    _issue(
                        path=entry["path"],
                        field=f"category.{category}.status.last_drift_review",
                        severity="safe-reconcile",
                        message="status governance drift metadata is missing or stale",
                        current=explicit_last_drift,
                        expected=derived_last_drift,
                        action="update_status_governance",
                    )
                )

    for category, master_values in master_portfolio.items():
        strategic_tier = strategic_tiers.get(category)
        if strategic_tier and extract_tier_token(strategic_tier) != extract_tier_token(master_values["tier"]):
            needs_human_decision.append(
                _issue(
                    path="STRATEGIC_REVIEW.md",
                    field=f"category.{category}.portfolio.rankings",
                    severity="needs-human-decision",
                    message="strategic-review ranking table disagrees with the canonical master sprint plan",
                    current=strategic_tier,
                    expected=master_values["tier"],
                )
            )
        strategic_range = extract_percentage_range(strategic_win_probabilities.get(category))
        master_range = extract_percentage_range(master_values["win_probability"])
        if strategic_range and master_range and strategic_range != master_range:
            needs_human_decision.append(
                _issue(
                    path="STRATEGIC_REVIEW.md",
                    field=f"category.{category}.portfolio.win_probabilities",
                    severity="needs-human-decision",
                    message="strategic-review revised range disagrees with the canonical master sprint plan",
                    current=strategic_range,
                    expected=master_range,
                )
            )

    return {
        "scope": scope,
        "run_date": today,
        "manifest": manifest_path.relative_to(repo_root).as_posix(),
        "managed_docs_in_scope": len(selected),
        "safe_reconcile": safe_reconcile,
        "needs_human_decision": needs_human_decision,
        "unmanaged_governed_docs": unmanaged_paths,
        "selected_documents": [entry["path"] for entry in selected],
    }


def render_markdown_report(report: dict[str, Any], title: str) -> str:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Run date:** {report['run_date']}")
    lines.append(f"**Scope:** `{report['scope']}`")
    lines.append(f"**Manifest:** `{report['manifest']}`")
    lines.append(f"**Managed docs in scope:** {report['managed_docs_in_scope']}")
    lines.append(f"**Safe reconciliations:** {len(report['safe_reconcile'])}")
    lines.append(f"**Needs human decision:** {len(report['needs_human_decision'])}")
    lines.append("")

    lines.append("## Inventory")
    lines.append("")
    if report["unmanaged_governed_docs"]:
        for path in report["unmanaged_governed_docs"]:
            lines.append(f"- Unmanaged governed doc: `{path}`")
    else:
        lines.append("- No unmanaged governed docs detected.")
    lines.append("")

    lines.append("## Safe Reconcile")
    lines.append("")
    if report["safe_reconcile"]:
        lines.append("| Doc | Field | Current | Expected | Action |")
        lines.append("|---|---|---|---|---|")
        for issue in report["safe_reconcile"]:
            current = json.dumps(issue["current"], ensure_ascii=True) if issue["current"] is not None else ""
            expected = json.dumps(issue["expected"], ensure_ascii=True) if issue["expected"] is not None else ""
            lines.append(
                f"| `{issue['path']}` | `{issue['field']}` | {current} | {expected} | `{issue.get('action') or ''}` |"
            )
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Needs Human Decision")
    lines.append("")
    if report["needs_human_decision"]:
        for issue in report["needs_human_decision"]:
            lines.append(f"- `{issue['path']}` `{issue['field']}`: {issue['message']}")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Managed Docs")
    lines.append("")
    for path in report["selected_documents"]:
        lines.append(f"- `{path}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = ArgumentParser(description="Audit repo governance drift")
    parser.add_argument("--manifest", default="docs/governance/canonical-map.yaml")
    parser.add_argument("--scope", default="portfolio")
    parser.add_argument("--date", default=None)
    parser.add_argument("--report", default=None)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = (repo_root / args.manifest).resolve()
    today = args.date
    if today is None:
        from datetime import date

        today = date.today().isoformat()

    report = audit_repo(repo_root, manifest_path, args.scope, today)

    if args.report:
        report_path = (repo_root / args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_markdown_report(report, "Repo Governance Audit"), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(report, indent=2))
        return 0

    print(render_markdown_report(report, "Repo Governance Audit"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
