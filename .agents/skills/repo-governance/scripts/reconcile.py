from __future__ import annotations

from argparse import ArgumentParser
from datetime import date
from pathlib import Path
from typing import Any
import json
import re
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit import audit_repo, render_markdown_report
from build_index import build_reference_markdown
from governance_common import (
    build_frontmatter,
    extract_inline_metadata,
    extract_master_portfolio,
    extract_percentage_range,
    extract_tier_token,
    expected_notice,
    load_manifest,
    read_markdown,
    render_markdown,
    replace_inline_metadata_value,
    select_manifest_entries,
    update_percentage_range_in_text,
    update_tier_string,
    upsert_notice,
    upsert_status_governance_section,
)


def _safe_scope_name(scope: str) -> str:
    return scope.replace(":", "-").replace("/", "-").replace(" ", "-")


def apply_reconciliations(repo_root: Path, manifest_path: Path, scope: str, today: str, dry_run: bool) -> list[str]:
    manifest = load_manifest(manifest_path)
    selected = select_manifest_entries(manifest, scope)
    master_portfolio = extract_master_portfolio(read_markdown(repo_root / "MASTER_SPRINT_PLAN.md").body)
    changed_paths: list[str] = []

    for entry in selected:
        absolute_path = repo_root / entry["path"]
        if not absolute_path.exists():
            continue

        document = read_markdown(absolute_path)
        body = document.body
        body = upsert_notice(body, expected_notice(entry))

        category = entry.get("category")
        canonical_portfolio = master_portfolio.get(category) if isinstance(category, int) else None
        if canonical_portfolio:
            metadata = extract_inline_metadata(body)
            if entry["doc_kind"] == "sprint_plan":
                tier_value = metadata.get("Tier")
                if tier_value and extract_tier_token(tier_value) != extract_tier_token(canonical_portfolio["tier"]):
                    body = replace_inline_metadata_value(
                        body,
                        "Tier",
                        update_tier_string(tier_value, canonical_portfolio["tier"]),
                    )
                win_probability = metadata.get("Win Probability")
                if win_probability and extract_percentage_range(win_probability) != extract_percentage_range(
                    canonical_portfolio["win_probability"]
                ):
                    body = replace_inline_metadata_value(body, "Win Probability", canonical_portfolio["win_probability"])

            if entry["doc_kind"] == "prd_section":
                cto_tier = metadata.get("CTO Tier")
                if cto_tier and extract_tier_token(cto_tier) != extract_tier_token(canonical_portfolio["tier"]):
                    body = replace_inline_metadata_value(
                        body,
                        "CTO Tier",
                        update_tier_string(cto_tier, canonical_portfolio["tier"]),
                    )
                canonical_range = extract_percentage_range(canonical_portfolio["win_probability"]) or canonical_portfolio["win_probability"]
                body = re.sub(
                    r"(?m)^(- \*\*Overall Win Probability:\*\*\s*[^\n]*?)(\d+\s*-\s*\d+%)",
                    lambda match: f"{match.group(1)}{canonical_range}",
                    body,
                    count=1,
                )

            if entry["doc_kind"] == "status":
                tier_value = metadata.get("Tier")
                if tier_value:
                    updated_tier = tier_value
                    if extract_tier_token(tier_value) != extract_tier_token(canonical_portfolio["tier"]):
                        updated_tier = update_tier_string(updated_tier, canonical_portfolio["tier"])
                    if extract_percentage_range(updated_tier) != extract_percentage_range(canonical_portfolio["win_probability"]):
                        updated_tier = update_percentage_range_in_text(
                            updated_tier, extract_percentage_range(canonical_portfolio["win_probability"]) or canonical_portfolio["win_probability"]
                        )
                    if updated_tier != tier_value:
                        body = replace_inline_metadata_value(body, "Tier", updated_tier)
                body = upsert_status_governance_section(entry, manifest, body)

        frontmatter = build_frontmatter(entry, today)
        rendered = render_markdown(frontmatter, body)
        if rendered != document.text:
            changed_paths.append(entry["path"])
            if not dry_run:
                absolute_path.write_text(rendered, encoding="utf-8")

    return changed_paths


def render_reconcile_report(
    pre_report: dict[str, Any],
    post_report: dict[str, Any],
    applied_changes: list[str],
    dry_run: bool,
    index_path: str,
) -> str:
    lines: list[str] = []
    lines.append("# Repo Governance Reconcile")
    lines.append("")
    lines.append(f"**Run date:** {post_report['run_date']}")
    lines.append(f"**Scope:** `{post_report['scope']}`")
    lines.append(f"**Mode:** {'dry-run' if dry_run else 'apply-safe-reconciliations'}")
    lines.append(f"**Reference index:** `{index_path}`")
    lines.append(f"**Safe issues before reconcile:** {len(pre_report['safe_reconcile'])}")
    lines.append(f"**Safe issues after reconcile:** {len(post_report['safe_reconcile'])}")
    lines.append(f"**Needs human decision after reconcile:** {len(post_report['needs_human_decision'])}")
    lines.append("")

    lines.append("## Applied Changes")
    lines.append("")
    if applied_changes:
        for path in applied_changes:
            lines.append(f"- `{path}`")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append(render_markdown_report(post_report, "Repo Governance State").strip())
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = ArgumentParser(description="Apply safe repo-governance reconciliations")
    parser.add_argument("--manifest", default="docs/governance/canonical-map.yaml")
    parser.add_argument("--scope", default="portfolio")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--report", default=None)
    parser.add_argument("--index-output", default="docs/governance/REPO_REFERENCE.md")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = (repo_root / args.manifest).resolve()
    safe_scope = _safe_scope_name(args.scope)
    report_path = (
        (repo_root / args.report).resolve()
        if args.report
        else (repo_root / f"docs/governance/reports/{args.date}-{safe_scope}-governance.md").resolve()
    )
    index_path = (repo_root / args.index_output).resolve()

    pre_report = audit_repo(repo_root, manifest_path, args.scope, args.date)
    applied_changes = apply_reconciliations(repo_root, manifest_path, args.scope, args.date, args.dry_run)

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(build_reference_markdown(repo_root, manifest_path), encoding="utf-8")
    post_report = audit_repo(repo_root, manifest_path, args.scope, args.date)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_report = render_reconcile_report(
        pre_report,
        post_report,
        applied_changes,
        args.dry_run,
        index_path.relative_to(repo_root).as_posix(),
    )
    report_path.write_text(rendered_report, encoding="utf-8")

    output = {
        "mode": "dry-run" if args.dry_run else "apply-safe-reconciliations",
        "scope": args.scope,
        "report": report_path.relative_to(repo_root).as_posix(),
        "index": index_path.relative_to(repo_root).as_posix(),
        "changed_paths": applied_changes,
        "post_safe_reconcile": len(post_report["safe_reconcile"]),
        "post_needs_human_decision": len(post_report["needs_human_decision"]),
    }

    if args.format == "json":
        print(json.dumps(output, indent=2))
        return 0

    print(rendered_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
