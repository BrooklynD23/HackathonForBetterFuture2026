from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import re

import yaml


DOC_KINDS = {
    "strategic_review",
    "master_sprint_plan",
    "sprint_plan",
    "prd_section",
    "status",
    "plan",
}
DOC_ROLES = {"canonical", "derived", "background", "superseded"}
PIPELINE_STAGE_NAMES = {"IDEA", "FEATURES", "DOC", "MEMORY", "VERIFY", "TEST", "DRIFT", "COMMIT"}
GOVERNANCE_MANAGER = "repo-governance"


class ManifestValidationError(ValueError):
    """Raised when the canonical map is malformed."""


@dataclass
class MarkdownDocument:
    path: Path
    text: str
    frontmatter: dict[str, Any]
    body: str
    had_frontmatter: bool


@dataclass
class DriftIssue:
    path: str
    field: str
    severity: str
    message: str
    current: Any = None
    expected: Any = None
    action: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_relpath(path: str | Path, repo_root: Path) -> str:
    if isinstance(path, Path):
        return path.relative_to(repo_root).as_posix()
    path_obj = Path(path)
    if path_obj.is_absolute():
        return path_obj.relative_to(repo_root).as_posix()
    return path_obj.as_posix()


def manifest_entries_by_path(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["path"]: entry for entry in manifest["documents"]}


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    errors = validate_manifest(manifest)
    if errors:
        message = "\n".join(f"- {error}" for error in errors)
        raise ManifestValidationError(f"Invalid manifest at {manifest_path}:\n{message}")
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if not isinstance(manifest, dict):
        return ["manifest must be a mapping"]

    if manifest.get("managed_by") != GOVERNANCE_MANAGER:
        errors.append("managed_by must be repo-governance")

    decision_domains = manifest.get("decision_domains")
    if not isinstance(decision_domains, dict) or not decision_domains:
        errors.append("decision_domains must be a non-empty mapping")

    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        errors.append("documents must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()

    for index, entry in enumerate(documents):
        label = f"documents[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue

        for key in ("id", "label", "path", "doc_kind", "doc_role", "authority_scope", "canonical_upstreams"):
            if key not in entry:
                errors.append(f"{label} missing {key}")

        entry_id = entry.get("id")
        entry_path = entry.get("path")
        doc_kind = entry.get("doc_kind")
        doc_role = entry.get("doc_role")
        authority_scope = entry.get("authority_scope")
        canonical_upstreams = entry.get("canonical_upstreams")
        category = entry.get("category")

        if entry_id in seen_ids:
            errors.append(f"duplicate document id: {entry_id}")
        elif isinstance(entry_id, str):
            seen_ids.add(entry_id)

        if entry_path in seen_paths:
            errors.append(f"duplicate document path: {entry_path}")
        elif isinstance(entry_path, str):
            seen_paths.add(entry_path)

        if doc_kind not in DOC_KINDS:
            errors.append(f"{label} has invalid doc_kind: {doc_kind}")

        if doc_role not in DOC_ROLES:
            errors.append(f"{label} has invalid doc_role: {doc_role}")

        if not isinstance(authority_scope, list) or not authority_scope:
            errors.append(f"{label} authority_scope must be a non-empty list")
        else:
            for scope in authority_scope:
                if not isinstance(scope, str) or scope not in decision_domains:
                    errors.append(f"{label} references unknown authority scope: {scope}")

        if not isinstance(canonical_upstreams, list):
            errors.append(f"{label} canonical_upstreams must be a list")

        if doc_kind in {"sprint_plan", "prd_section", "status", "plan"}:
            if not isinstance(category, int):
                errors.append(f"{label} category must be an int for {doc_kind}")
        elif category is not None:
            errors.append(f"{label} category must be null for {doc_kind}")

    if isinstance(decision_domains, dict):
        by_path = manifest_entries_by_path({"documents": documents})
        for domain_name, config in decision_domains.items():
            if not isinstance(config, dict):
                errors.append(f"decision domain {domain_name} must be a mapping")
                continue
            owner = config.get("owner")
            if owner not in by_path:
                errors.append(f"decision domain {domain_name} owner is not a managed document: {owner}")

    by_path = manifest_entries_by_path({"documents": documents})
    for index, entry in enumerate(documents):
        label = f"documents[{index}]"
        if isinstance(entry.get("canonical_upstreams"), list):
            for upstream in entry["canonical_upstreams"]:
                if upstream not in by_path:
                    errors.append(f"{label} references unknown canonical upstream: {upstream}")

    return errors


def discover_governed_docs(repo_root: Path) -> list[str]:
    discovered: set[str] = set()
    fixed = ["STRATEGIC_REVIEW.md", "MASTER_SPRINT_PLAN.md"]
    for path in fixed:
        absolute = repo_root / path
        if absolute.exists():
            discovered.add(path)

    for pattern in ("PRD_SECTION_CAT*.md", "Category */PLAN.md", "Category */SPRINT_PLAN.md", "Category */docs/SPRINT_PLAN.md", "Category */.status.md"):
        for path in repo_root.glob(pattern):
            discovered.add(path.relative_to(repo_root).as_posix())
    return sorted(discovered)


def _collect_upstreams(entries: list[dict[str, Any]], by_path: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    collected = {entry["path"]: entry for entry in entries}
    pending = list(entries)
    while pending:
        current = pending.pop()
        for upstream_path in current["canonical_upstreams"]:
            upstream = by_path[upstream_path]
            if upstream["path"] not in collected:
                collected[upstream["path"]] = upstream
                pending.append(upstream)
    return sorted(collected.values(), key=lambda item: item["path"])


def select_manifest_entries(manifest: dict[str, Any], scope: str) -> list[dict[str, Any]]:
    by_path = manifest_entries_by_path(manifest)
    documents = manifest["documents"]

    if scope == "portfolio":
        return sorted(documents, key=lambda item: item["path"])

    if scope.startswith("category:"):
        category = int(scope.split(":", 1)[1])
        selected = [entry for entry in documents if entry.get("category") == category]
        return _collect_upstreams(selected, by_path)

    if scope.startswith("doc:"):
        requested_path = scope.split(":", 1)[1]
        if requested_path not in by_path:
            raise KeyError(f"managed document not found: {requested_path}")
        return _collect_upstreams([by_path[requested_path]], by_path)

    raise ValueError(f"unsupported scope: {scope}")


def read_markdown(path: Path) -> MarkdownDocument:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return MarkdownDocument(path=path, text=text, frontmatter={}, body=text, had_frontmatter=False)

    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    return MarkdownDocument(path=path, text=text, frontmatter=frontmatter, body=body, had_frontmatter=True)


def render_frontmatter(frontmatter: dict[str, Any]) -> str:
    dumped = yaml.safe_dump(frontmatter, sort_keys=False, default_flow_style=False).strip()
    return f"---\n{dumped}\n---\n\n"


def build_frontmatter(entry: dict[str, Any], today: str) -> dict[str, Any]:
    return {
        "doc_role": entry["doc_role"],
        "authority_scope": entry["authority_scope"],
        "canonical_upstreams": entry["canonical_upstreams"],
        "last_reconciled": today,
        "managed_by": GOVERNANCE_MANAGER,
    }


def render_markdown(frontmatter: dict[str, Any], body: str) -> str:
    normalized_body = body.lstrip("\n").rstrip()
    return f"{render_frontmatter(frontmatter)}{normalized_body}\n"


def extract_inline_metadata(body: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    pattern = re.compile(r"\*\*(?P<key>[^*:\n]+?)(?::)?\*\*:?\s*(?P<value>[^|\n]+)")
    for line in body.splitlines():
        if "**" not in line:
            continue
        for match in pattern.finditer(line):
            metadata[match.group("key").strip()] = match.group("value").strip()
    return metadata


def replace_inline_metadata_value(body: str, key: str, new_value: str) -> str:
    pattern = re.compile(rf"(\*\*{re.escape(key)}(?::)?\*\*:?\s*)([^|\n]+)")
    return pattern.sub(lambda match: f"{match.group(1)}{new_value}", body, count=1)


def extract_percentage_range(text: str | None) -> str | None:
    if not text:
        return None
    match = re.search(r"(\d+\s*-\s*\d+%)", text)
    if not match:
        return None
    return match.group(1).replace(" ", "")


def extract_tier_token(text: str | None) -> str | None:
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    return match.group(1) if match else None


def extract_category_number(text: str | None) -> int | None:
    if not text:
        return None
    match = re.search(r"Cat(?:egory)?\s*(\d+)", text)
    return int(match.group(1)) if match else None


def _section_bounds(body: str, heading: str) -> tuple[int, int] | None:
    match = re.search(rf"(?m)^\s*##+\s+{re.escape(heading)}\s*$", body)
    if not match:
        return None
    next_match = re.search(r"(?m)^\s*##+\s+", body[match.end() :])
    end = len(body) if not next_match else match.end() + next_match.start()
    return match.start(), end


def extract_section(body: str, heading: str) -> str | None:
    bounds = _section_bounds(body, heading)
    if not bounds:
        return None
    start, end = bounds
    return body[start:end]


def parse_markdown_table(section_text: str | None) -> list[dict[str, str]]:
    if not section_text:
        return []

    lines = [line.strip() for line in section_text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return []

    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def extract_master_portfolio(body: str) -> dict[int, dict[str, str]]:
    rows = parse_markdown_table(extract_section(body, "Revised Tier Rankings"))
    portfolio: dict[int, dict[str, str]] = {}
    for row in rows:
        category = extract_category_number(row.get("Category"))
        if category is None:
            continue
        portfolio[category] = {
            "tier": row.get("Tier", "").strip(),
            "win_probability": row.get("Win Prob", "").strip(),
            "condition": row.get("Condition", "").strip(),
        }
    return portfolio


def extract_strategic_tiers(body: str) -> dict[int, str]:
    rows = parse_markdown_table(extract_section(body, "Revised Tier Rankings"))
    results: dict[int, str] = {}
    for row in rows:
        category = extract_category_number(row.get("Category"))
        if category is not None:
            results[category] = row.get("Tier", "").strip()
    return results


def extract_strategic_win_probabilities(body: str) -> dict[int, str]:
    rows = parse_markdown_table(extract_section(body, "Revised Win Probability Matrix"))
    results: dict[int, str] = {}
    for row in rows:
        category = extract_category_number(row.get("Category"))
        if category is not None:
            results[category] = row.get("Revised Range", "").strip()
    return results


def extract_pipeline_status(body: str) -> dict[str, dict[str, str]]:
    rows = parse_markdown_table(extract_section(body, "Pipeline Status"))
    results: dict[str, dict[str, str]] = {}
    for row in rows:
        stage = row.get("Stage", "").strip()
        if stage:
            results[stage] = row
    return results


def extract_last_drift_review(body: str) -> dict[str, str] | None:
    match = re.search(r"Last drift review:\s*(\d{4}-\d{2}-\d{2})(?:\s*\(`?([^`)]+)`?\))?", body)
    if not match:
        return None
    result = {"date": match.group(1)}
    if match.group(2):
        result["source"] = match.group(2)
    return result


def extract_canonical_docs(body: str) -> list[str]:
    governance_section = extract_section(body, "Governance")
    text = governance_section or body
    match = re.search(r"Canonical docs:\s*(.+)", text)
    if not match:
        return []
    raw = match.group(1)
    explicit = re.findall(r"`([^`]+)`", raw)
    if explicit:
        return explicit
    return [part.strip() for part in raw.split(",") if part.strip()]


def extract_overall_win_probability_range(body: str) -> str | None:
    match = re.search(r"Overall Win Probability:\*?\*?\s*([^\n]+)", body)
    if not match:
        return None
    return extract_percentage_range(match.group(1))


def expected_notice(entry: dict[str, Any]) -> str:
    path = entry["path"]
    upstreams = ", ".join(f"`{value}`" for value in entry["canonical_upstreams"]) or "none"
    category = entry.get("category")
    if entry["doc_kind"] == "plan":
        return (
            "> **Governance notice (repo-governance):** This file is background analysis only. "
            f"Use it for ideation and history, not as an authority for current planning decisions. Canonical upstreams: {upstreams}."
        )
    if entry["doc_kind"] == "prd_section":
        return (
            "> **Governance notice (repo-governance):** This document owns category feature-detail narrative. "
            f"It must not override execution, staffing, milestone, or gating decisions from its canonical upstreams: {upstreams}."
        )
    if entry["doc_kind"] == "sprint_plan":
        return (
            "> **Governance notice (repo-governance):** This document owns category execution decisions for this track. "
            f"Portfolio schedule, ranking, and conflict-resolution context must follow: {upstreams}."
        )
    if entry["doc_kind"] == "status":
        return (
            "> **Governance notice (repo-governance):** This file owns stage state only. "
            f"Planning values must mirror the canonical docs listed in the Governance section below for Category {category}."
        )
    if entry["doc_kind"] == "master_sprint_plan":
        return (
            "> **Governance notice (repo-governance):** This document owns portfolio rankings, win-probability ranges, "
            "the canonical day-number schedule, and the staffing model."
        )
    if entry["doc_kind"] == "strategic_review":
        return (
            f"> **Governance notice (repo-governance):** This document owns strategic rationale and conflict-resolution guidance. "
            f"Mirrored portfolio values must stay aligned with the canonical portfolio sources when referenced: {upstreams if upstreams != 'none' else '`MASTER_SPRINT_PLAN.md`'}."
        )
    return f"> **Governance notice (repo-governance):** Governed by {GOVERNANCE_MANAGER}. Canonical upstreams: {upstreams}."


def upsert_notice(body: str, notice: str) -> str:
    lines = body.splitlines()
    for index, line in enumerate(lines[:25]):
        if line.startswith("> **Governance notice (repo-governance):**"):
            lines[index] = notice
            return "\n".join(lines).rstrip() + "\n"

    insert_at = 0
    if lines and lines[0].startswith("#"):
        insert_at = 1
        while insert_at < len(lines) and lines[insert_at].strip():
            insert_at += 1
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1

    updated = lines[:insert_at] + [notice, ""] + lines[insert_at:]
    return "\n".join(updated).rstrip() + "\n"


def category_entries(manifest: dict[str, Any], category: int) -> list[dict[str, Any]]:
    return sorted(
        [entry for entry in manifest["documents"] if entry.get("category") == category],
        key=lambda item: item["path"],
    )


def canonical_doc_links_for_status(entry: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    ordered = []
    by_path = manifest_entries_by_path(manifest)

    def add(path: str) -> None:
        if path != entry["path"] and path not in ordered:
            ordered.append(path)

    for upstream in entry["canonical_upstreams"]:
        add(upstream)
    for candidate in category_entries(manifest, entry["category"]):
        if candidate["doc_kind"] in {"sprint_plan", "prd_section"}:
            add(candidate["path"])
    if "MASTER_SPRINT_PLAN.md" in by_path:
        add("MASTER_SPRINT_PLAN.md")
    if "STRATEGIC_REVIEW.md" in by_path:
        add("STRATEGIC_REVIEW.md")
    return ordered


def determine_last_drift_review(body: str) -> dict[str, str]:
    explicit = extract_last_drift_review(body)
    if explicit:
        return explicit
    pipeline = extract_pipeline_status(body)
    drift_row = pipeline.get("DRIFT", {})
    drift_date = drift_row.get("Date", "").strip()
    if drift_date and drift_date != "—":
        return {"date": drift_date}
    return {"date": "not recorded"}


def build_status_governance_section(entry: dict[str, Any], manifest: dict[str, Any], body: str) -> str:
    last_drift_review = determine_last_drift_review(body)
    drift_text = last_drift_review["date"]
    if last_drift_review.get("source"):
        drift_text = f"{drift_text} (`{last_drift_review['source']}`)"
    canonical_docs = ", ".join(f"`{path}`" for path in canonical_doc_links_for_status(entry, manifest))
    lines = [
        "## Governance",
        f"- Last drift review: {drift_text}",
        f"- Canonical docs: {canonical_docs}",
        "- Canonical links note: This file owns stage state only; planning values must mirror the canonical docs above.",
    ]
    return "\n".join(lines)


def upsert_status_governance_section(entry: dict[str, Any], manifest: dict[str, Any], body: str) -> str:
    section = build_status_governance_section(entry, manifest, body)
    bounds = _section_bounds(body, "Governance")
    if bounds:
        start, end = bounds
        updated = body[:start].rstrip() + "\n\n" + section + "\n"
        if body[end:].strip():
            updated += "\n" + body[end:].lstrip("\n")
        return updated.rstrip() + "\n"
    return body.rstrip() + "\n\n" + section + "\n"


def compare_frontmatter(current: dict[str, Any], expected: dict[str, Any]) -> list[tuple[str, Any, Any]]:
    mismatches: list[tuple[str, Any, Any]] = []
    for key, expected_value in expected.items():
        if current.get(key) != expected_value:
            mismatches.append((key, current.get(key), expected_value))
    extra_keys = [key for key in current if key not in expected]
    for key in extra_keys:
        mismatches.append((key, current.get(key), None))
    return mismatches


def update_tier_string(current_value: str, canonical_tier: str) -> str:
    match = re.match(r"(\d+(?:\.\d+)?(?:/Optional)?)(.*)", current_value.strip())
    if not match:
        return canonical_tier
    existing_prefix, suffix = match.groups()
    replacement = canonical_tier
    if existing_prefix.endswith("/Optional") and "/" not in canonical_tier:
        replacement = f"{canonical_tier}/Optional"
    return f"{replacement}{suffix}"


def update_percentage_range_in_text(text: str, canonical_range: str) -> str:
    return re.sub(r"\d+\s*-\s*\d+%", canonical_range, text, count=1)


def to_pretty_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, default_flow_style=False).strip() + "\n"
