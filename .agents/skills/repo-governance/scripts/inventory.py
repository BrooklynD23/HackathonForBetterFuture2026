from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import json
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import discover_governed_docs, load_manifest, select_manifest_entries


def build_inventory(repo_root: Path, manifest_path: Path, scope: str) -> dict[str, object]:
    manifest = load_manifest(manifest_path)
    selected = select_manifest_entries(manifest, scope)
    managed_paths = {entry["path"] for entry in manifest["documents"]}
    discovered = discover_governed_docs(repo_root)
    unmanaged = [path for path in discovered if path not in managed_paths]
    return {
        "scope": scope,
        "manifest": manifest_path.relative_to(repo_root).as_posix(),
        "managed_count": len(manifest["documents"]),
        "selected_count": len(selected),
        "selected_documents": selected,
        "unmanaged_governed_docs": unmanaged,
    }


def main() -> int:
    parser = ArgumentParser(description="Enumerate governed docs from canonical-map.yaml")
    parser.add_argument("--manifest", default="docs/governance/canonical-map.yaml")
    parser.add_argument("--scope", default="portfolio")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = (repo_root / args.manifest).resolve()
    inventory = build_inventory(repo_root, manifest_path, args.scope)

    if args.format == "json":
        print(json.dumps(inventory, indent=2))
        return 0

    print(f"Scope: {inventory['scope']}")
    print(f"Manifest: {inventory['manifest']}")
    print(f"Managed docs: {inventory['managed_count']}")
    print(f"Selected docs: {inventory['selected_count']}")
    print()
    for entry in inventory["selected_documents"]:
        role = entry["doc_role"]
        kind = entry["doc_kind"]
        category = entry["category"]
        category_label = f"cat{category}" if category is not None else "portfolio"
        scopes = ", ".join(entry["authority_scope"])
        print(f"- {entry['path']} [{kind} | {role} | {category_label}]")
        print(f"  authority: {scopes}")

    unmanaged = inventory["unmanaged_governed_docs"]
    print()
    if unmanaged:
        print("Unmanaged governed docs:")
        for path in unmanaged:
            print(f"- {path}")
    else:
        print("Unmanaged governed docs: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
