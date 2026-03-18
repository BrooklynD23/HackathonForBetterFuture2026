from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (
    category_entries,
    canonical_doc_links_for_status,
    extract_last_drift_review,
    load_manifest,
    manifest_entries_by_path,
    read_markdown,
)


def build_reference_markdown(repo_root: Path, manifest_path: Path) -> str:
    manifest = load_manifest(manifest_path)
    by_path = manifest_entries_by_path(manifest)
    lines: list[str] = []
    lines.append("# Repo Reference Map")
    lines.append("")
    lines.append(f"**Managed by:** `repo-governance` | **Manifest:** `{manifest_path.relative_to(repo_root).as_posix()}`")
    lines.append("")
    lines.append("## Canonical Docs By Decision Type")
    lines.append("")
    lines.append("| Decision Domain | Owner | Description |")
    lines.append("|---|---|---|")
    for domain_name in sorted(manifest["decision_domains"]):
        config = manifest["decision_domains"][domain_name]
        owner = config["owner"]
        lines.append(f"| `{domain_name}` | `{owner}` | {config.get('description', '')} |")

    lines.append("")
    lines.append("## Derived Docs By Category")
    lines.append("")
    for category in range(1, 6):
        entries = [
            entry
            for entry in category_entries(manifest, category)
            if entry["canonical_upstreams"] and entry["doc_kind"] != "plan"
        ]
        lines.append(f"### Category {category}")
        if not entries:
            lines.append("")
            lines.append("_None_")
            lines.append("")
            continue
        lines.append("")
        for entry in entries:
            upstreams = ", ".join(f"`{path}`" for path in entry["canonical_upstreams"])
            lines.append(
                f"- `{entry['path']}` ({entry['doc_role']}, `{entry['doc_kind']}`) mirrors `{', '.join(entry['authority_scope'])}` via {upstreams}"
            )
        lines.append("")

    background_entries = [entry for entry in manifest["documents"] if entry["doc_role"] in {"background", "superseded"}]
    lines.append("## Background And Superseded Docs")
    lines.append("")
    for entry in background_entries:
        lines.append(f"- `{entry['path']}` ({entry['doc_role']})")
    if not background_entries:
        lines.append("_None_")
    lines.append("")

    lines.append("## Last Drift Review By Category")
    lines.append("")
    lines.append("| Category | Status File | Last Drift Review | Canonical Docs |")
    lines.append("|---|---|---|---|")
    for category in range(1, 6):
        status_entry = next(entry for entry in category_entries(manifest, category) if entry["doc_kind"] == "status")
        status_doc = read_markdown(repo_root / status_entry["path"])
        last_drift_review = extract_last_drift_review(status_doc.body)
        if last_drift_review:
            drift_text = last_drift_review["date"]
            if last_drift_review.get("source"):
                drift_text = f"{drift_text} (`{last_drift_review['source']}`)"
        else:
            drift_text = "not recorded"
        canonical_docs = ", ".join(f"`{path}`" for path in canonical_doc_links_for_status(status_entry, manifest))
        lines.append(f"| {category} | `{status_entry['path']}` | {drift_text} | {canonical_docs} |")

    lines.append("")
    lines.append("## Canonical Ownership Summary")
    lines.append("")
    lines.append("| Document | Role | Owned Domains |")
    lines.append("|---|---|---|")
    for entry in manifest["documents"]:
        role = entry["doc_role"]
        owned_domains = ", ".join(f"`{scope}`" for scope in entry["authority_scope"])
        lines.append(f"| `{entry['path']}` | `{role}` | {owned_domains} |")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = ArgumentParser(description="Regenerate docs/governance/REPO_REFERENCE.md")
    parser.add_argument("--manifest", default="docs/governance/canonical-map.yaml")
    parser.add_argument("--output", default="docs/governance/REPO_REFERENCE.md")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = (repo_root / args.manifest).resolve()
    output_path = (repo_root / args.output).resolve()
    output_path.write_text(build_reference_markdown(repo_root, manifest_path), encoding="utf-8")
    print(output_path.relative_to(repo_root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
