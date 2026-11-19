#!/usr/bin/env python3
"""Check that new or changed research is reviewed for network integration.

Existing research at BASELINE_REVISION remains visible as an explicit legacy
backlog.  Once a study changes, its exact content hash and either source-bound
relation IDs or a substantive explanation are required.  A diagram cannot
safely infer relationships from mentions in prose.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINE_REVISION = "5190a010f145ca060ec55a4aace16861f1d776e0"
REGISTRY = Path("data/research-integrations.yml")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass
class Coverage:
    legacy: list[str] = field(default_factory=list)
    network: list[str] = field(default_factory=list)
    no_network_relation: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def read_registry(root: Path = ROOT) -> dict[str, Any]:
    path = root / REGISTRY
    if not path.exists():
        raise ValueError(f"missing {REGISTRY}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("studies"), dict):
        raise ValueError(f"{REGISTRY} must contain a studies mapping")
    return data["studies"]


def baseline_blobs(root: Path = ROOT) -> dict[str, str]:
    """Names and Git object IDs of unchanged research files at the pinned baseline."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-rz", f"{BASELINE_REVISION}:research"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(
            f"Cannot read pinned research baseline {BASELINE_REVISION}: {message}. "
            "Checkout must include history (fetch-depth: 0)."
        )
    entries = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        attrs, sep, name = entry.partition(b"\t")
        if not sep:
            raise ValueError("malformed Git baseline")
        mode, object_type, blob = attrs.split()
        filename = name.decode("utf-8")
        if mode in (b"100644", b"100755") and object_type == b"blob" and filename.endswith(".md"):
            entries[filename] = blob.decode("ascii")
    return entries


def git_blob_id(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()


def audit(root: Path = ROOT, baseline: dict[str, str] | None = None) -> Coverage:
    report = Coverage()
    try:
        registry = read_registry(root)
        old = baseline if baseline is not None else baseline_blobs(root)
        relation_doc = yaml.safe_load((root / "data/relations.yml").read_text(encoding="utf-8")) or {}
        relation_rows = relation_doc.get("relations", [])
        relation_ids = {item["id"] for item in relation_rows}
    except (OSError, ValueError, yaml.YAMLError, KeyError, TypeError) as exc:
        report.errors.append(str(exc))
        return report

    studies = {
        path.name: path
        for path in (root / "research").glob("*.md")
        if path.is_file() and not path.name.startswith(".")
    }
    for name in sorted(set(registry) - set(studies)):
        report.errors.append(f"{REGISTRY}: entry for missing study {name}")
    for name, path in sorted(studies.items()):
        content = path.read_bytes()
        is_legacy = old.get(name) == git_blob_id(content)
        entry = registry.get(name)
        if entry is None:
            if is_legacy:
                report.legacy.append(name)
            else:
                report.errors.append(f"research/{name}: changed/new study lacks a network-integration decision in {REGISTRY}")
            continue
        if not isinstance(entry, dict):
            report.errors.append(f"{REGISTRY}: {name} must be a mapping")
            continue
        digest = entry.get("sha256")
        actual = hashlib.sha256(content).hexdigest()
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest) or digest != actual:
            report.errors.append(f"research/{name}: integration review hash is missing or stale (expected {actual})")
        mode = entry.get("status")
        if mode == "network":
            ids = entry.get("relation_ids")
            if not isinstance(ids, list) or not ids or not all(isinstance(x, str) for x in ids):
                report.errors.append(f"research/{name}: network status requires relation_ids")
            else:
                if len(set(ids)) != len(ids):
                    report.errors.append(f"research/{name}: duplicate relation_ids")
                for relation_id in ids:
                    if relation_id not in relation_ids:
                        report.errors.append(f"research/{name}: unknown relation {relation_id}")
            if entry.get("reason") is not None:
                report.errors.append(f"research/{name}: network entry must not contain a no-relation reason")
            report.network.append(name)
        elif mode == "no_network_relation":
            reason = entry.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 30:
                report.errors.append(f"research/{name}: no_network_relation requires a substantive reason (30+ characters)")
            if entry.get("relation_ids"):
                report.errors.append(f"research/{name}: no_network_relation must not specify relation_ids")
            report.no_network_relation.append(name)
        else:
            report.errors.append(f"research/{name}: status must be network or no_network_relation")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate committed research coverage")
    args = parser.parse_args()
    if not args.check:
        parser.error("only --check is supported")
    result = audit()
    print(
        f"RESEARCH INTEGRATION: {len(result.network)} network-linked, "
        f"{len(result.no_network_relation)} reviewed without relation, "
        f"{len(result.legacy)} unchanged legacy studies"
    )
    for problem in result.errors:
        print("ERROR: " + problem, file=sys.stderr)
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
