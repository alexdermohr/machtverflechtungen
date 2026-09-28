#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CASE_DIR = DOCS / "faelle"
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    payload = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(payload, dict):
        raise ValueError("frontmatter must be a mapping")
    return payload


def schema_errors(instance: Any, schema_file: str, label: str) -> list[str]:
    validator = Draft202012Validator(load_json(SCHEMAS / schema_file))
    out: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        out.append(f"{label}: {location}: {error.message}")
    return out


def unique_ids(items: list[dict[str, Any]], label: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            errors.append(f"{label}: duplicate id {item_id}")
        seen.add(item_id)
    return seen


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def period_bounds(value: Any) -> tuple[date, date] | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if re.fullmatch(r"\d{4}", text):
        year = int(text)
        if not 1 <= year <= 9999:
            return None
        return (date(year, 1, 1), date(year, 12, 31))
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", text)
    if not match:
        return None
    try:
        exact = date(*(int(part) for part in match.groups()))
    except ValueError:
        return None
    return (exact, exact)


def established_supports(
    source_ids: list[str],
    source_by_id: dict[str, dict[str, Any]],
) -> bool:
    if not source_ids or any(source_id not in source_by_id for source_id in source_ids):
        return False
    resolved = [source_by_id[source_id] for source_id in source_ids]
    if any(
        source.get("tier") == "A" and source.get("primary") is True
        for source in resolved
    ):
        return True
    high_quality = [
        source for source in resolved if source.get("tier") in {"B", "C"}
    ]
    institutions = {
        source["institution"].strip().casefold()
        for source in high_quality
        if isinstance(source.get("institution"), str) and source["institution"].strip()
    }
    return len(high_quality) >= 2 and len(institutions) >= 2


def load_catalog(
    filename: str,
    key: str,
    schema_file: str,
    errors: list[str],
) -> list[dict[str, Any]]:
    path = DATA / filename
    payload = load_yaml(path)
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        errors.append(f"{path.relative_to(ROOT)}: expected top-level list '{key}'")
        return []
    rows = payload[key]
    valid_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{path.relative_to(ROOT)}[{index}]: expected mapping")
            continue
        row_errors = schema_errors(
            row, schema_file, f"{path.relative_to(ROOT)}[{index}]"
        )
        errors.extend(row_errors)
        if row_errors:
            continue
        valid_rows.append(row)
    return valid_rows


def main() -> int:
    errors: list[str] = []

    sources = load_catalog("sources.yml", "sources", "source.schema.json", errors)
    for source in sources:
        accessed = source.get("accessed")
        if isinstance(accessed, str) and period_bounds(accessed) is None:
            errors.append(
                f"sources:{source.get('id', '<unknown-source>')}: "
                "accessed must use a valid YYYY-MM-DD date"
            )

    entities = load_catalog("entities.yml", "entities", "entity.schema.json", errors)
    mechanisms = load_catalog(
        "mechanisms.yml", "mechanisms", "mechanism.schema.json", errors
    )
    relations = load_catalog(
        "relations.yml", "relations", "relation.schema.json", errors
    )

    source_ids = unique_ids(sources, "sources", errors)
    source_by_id = {
        item["id"]: item
        for item in sources
        if isinstance(item.get("id"), str)
    }
    source_tiers = {
        source_id: item.get("tier")
        for source_id, item in source_by_id.items()
    }
    entity_ids = unique_ids(entities, "entities", errors)
    mechanism_ids = unique_ids(mechanisms, "mechanisms", errors)
    unique_ids(relations, "relations", errors)

    case_ids: set[str] = set()
    claim_ids: set[str] = set()
    cases: list[tuple[Path, dict[str, Any]]] = []

    for path in sorted(CASE_DIR.rglob("*.md")):
        if path == CASE_DIR / "index.md":
            continue
        label = str(path.relative_to(ROOT))
        try:
            meta = frontmatter(path)
        except Exception as exc:
            errors.append(f"{label}: {exc}")
            continue

        errors.extend(schema_errors(meta, "case.schema.json", label))
        case_id = meta.get("id")
        if isinstance(case_id, str):
            if case_id in case_ids or case_id in entity_ids:
                errors.append(f"global IDs: duplicate id {case_id}")
            case_ids.add(case_id)

        raw_claims = meta.get("claims", [])
        if isinstance(raw_claims, list):
            for claim in raw_claims:
                if not isinstance(claim, dict):
                    errors.append(f"{label}: claim must be a mapping")
                    continue
                claim_label = f"{label}:{claim.get('id', '<unknown-claim>')}"
                errors.extend(schema_errors(claim, "claim.schema.json", claim_label))
                claim_id = claim.get("id")
                if isinstance(claim_id, str):
                    if claim_id in claim_ids:
                        errors.append(f"claims: duplicate id {claim_id}")
                    claim_ids.add(claim_id)
        cases.append((path, meta))

    for path, meta in cases:
        label = str(path.relative_to(ROOT))
        period = meta.get("period")
        if isinstance(period, dict):
            start_raw = period.get("start")
            end_raw = period.get("end")
            start_bounds = period_bounds(start_raw)
            end_bounds = period_bounds(end_raw) if end_raw is not None else None
            if isinstance(start_raw, str) and start_bounds is None:
                errors.append(
                    f"{label}: period.start must use a valid YYYY or YYYY-MM-DD value"
                )
            if isinstance(end_raw, str) and end_bounds is None:
                errors.append(
                    f"{label}: period.end must use a valid YYYY or YYYY-MM-DD value"
                )
            if (
                start_bounds is not None
                and end_bounds is not None
                and start_bounds[0] > end_bounds[1]
            ):
                errors.append(f"{label}: period.end precedes period.start")
        case_sources = string_list(meta.get("sources"))
        for source_id in case_sources:
            if source_id not in source_ids:
                errors.append(f"{label}: unknown source {source_id}")
        case_evidence = meta.get("evidence_level")
        if (
            case_evidence == "established"
            and case_sources
            and all(source_id in source_by_id for source_id in case_sources)
            and not established_supports(case_sources, source_by_id)
        ):
            errors.append(
                f"{label}: established case evidence requires a Tier-A primary source "
                "or at least two Tier-B/C sources from different institutions"
            )
        elif (
            isinstance(case_evidence, str)
            and case_evidence in {"strong", "plausible", "contradicted"}
            and case_sources
            and all(source_id in source_tiers for source_id in case_sources)
            and not any(source_tiers[source_id] in {"A", "B", "C", "D"} for source_id in case_sources)
        ):
            errors.append(
                f"{label}: non-speculative case evidence may not rely solely on Tier-E leads"
            )
        for actor_id in string_list(meta.get("actors")):
            if actor_id not in entity_ids:
                errors.append(f"{label}: unknown actor {actor_id}")
        for mechanism_id in string_list(meta.get("mechanisms")):
            if mechanism_id not in mechanism_ids:
                errors.append(f"{label}: unknown mechanism {mechanism_id}")

        for claim in mapping_list(meta.get("claims")):
            classification = claim.get("classification")
            evidence = claim.get("evidence_level")
            claim_sources = string_list(claim.get("sources"))
            source_optional = (
                (classification == "open_question" or classification == "hypothesis")
                and evidence == "speculative"
            )
            if not source_optional and not claim_sources:
                errors.append(
                    f"{label}: claim {claim.get('id')} requires at least one source"
                )
            for source_id in claim_sources:
                if source_id not in source_ids:
                    errors.append(
                        f"{label}: claim {claim.get('id')} references unknown source {source_id}"
                    )
            non_lead_required = (
                isinstance(classification, str)
                and (
                    classification in {"fact", "counterevidence", "interpretation"}
                    or (
                        classification in {"hypothesis", "open_question"}
                        and isinstance(evidence, str)
                        and evidence in {"established", "strong", "plausible", "contradicted"}
                    )
                )
            )
            if (
                evidence == "established"
                and claim_sources
                and all(source_id in source_by_id for source_id in claim_sources)
                and not established_supports(claim_sources, source_by_id)
            ):
                errors.append(
                    f"{label}: claim {claim.get('id')} with established evidence requires "
                    "a Tier-A primary source or at least two Tier-B/C sources from "
                    "different institutions"
                )
            elif (
                non_lead_required
                and claim_sources
                and all(source_id in source_tiers for source_id in claim_sources)
                and not any(
                    source_tiers[source_id] in {"A", "B", "C", "D"}
                    for source_id in claim_sources
                )
            ):
                errors.append(
                    f"{label}: claim {claim.get('id')} may not rely solely on Tier-E leads"
                )

    node_ids = entity_ids | case_ids
    for relation in relations:
        relation_id = relation.get("id", "<unknown-relation>")
        from_id = relation.get("from")
        to_id = relation.get("to")
        if isinstance(from_id, str) and from_id not in node_ids:
            errors.append(f"{relation_id}: unknown from-node {from_id}")
        if isinstance(to_id, str) and to_id not in node_ids:
            errors.append(f"{relation_id}: unknown to-node {to_id}")
        relation_sources = string_list(relation.get("sources"))
        for source_id in relation_sources:
            if source_id not in source_ids:
                errors.append(f"{relation_id}: unknown source {source_id}")
        relation_evidence = relation.get("evidence_level")
        if (
            relation_evidence == "established"
            and relation_sources
            and all(source_id in source_by_id for source_id in relation_sources)
            and not established_supports(relation_sources, source_by_id)
        ):
            errors.append(
                f"{relation_id}: established relation evidence requires a Tier-A "
                "primary source or at least two Tier-B/C sources from different institutions"
            )
        elif (
            relation_sources
            and all(source_id in source_tiers for source_id in relation_sources)
            and not any(
                source_tiers[source_id] in {"A", "B", "C", "D"}
                for source_id in relation_sources
            )
        ):
            errors.append(
                f"{relation_id}: relation may not rely solely on Tier-E leads"
            )

    organization_dir = DOCS / "organisationen"
    organization_profile_ids: set[str] = set()
    if organization_dir.exists():
        for path in sorted(organization_dir.rglob("*.md")):
            if path == organization_dir / "index.md":
                continue
            label = str(path.relative_to(ROOT))
            try:
                meta = frontmatter(path)
            except Exception as exc:
                errors.append(f"{label}: {exc}")
                continue
            errors.extend(schema_errors(meta, "organization.schema.json", label))
            entity_id = meta.get("id")
            if isinstance(entity_id, str):
                if entity_id in organization_profile_ids:
                    errors.append(f"organization profiles: duplicate id {entity_id}")
                organization_profile_ids.add(entity_id)
                if entity_id not in entity_ids:
                    errors.append(f"{label}: unknown organization entity {entity_id}")
            organization_sources = string_list(meta.get("sources"))
            for source_id in organization_sources:
                if source_id not in source_ids:
                    errors.append(f"{label}: unknown source {source_id}")
            organization_evidence = meta.get("evidence_level")
            if (
                organization_evidence == "established"
                and organization_sources
                and all(source_id in source_by_id for source_id in organization_sources)
                and not established_supports(organization_sources, source_by_id)
            ):
                errors.append(
                    f"{label}: established organization evidence requires a Tier-A "
                    "primary source or at least two Tier-B/C sources from different institutions"
                )
            elif (
                isinstance(organization_evidence, str)
                and organization_evidence in {"strong", "plausible", "contradicted"}
                and organization_sources
                and all(source_id in source_tiers for source_id in organization_sources)
                and not any(
                    source_tiers[source_id] in {"A", "B", "C", "D"}
                    for source_id in organization_sources
                )
            ):
                errors.append(
                    f"{label}: non-speculative organization evidence may not rely solely on Tier-E leads"
                )

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "VALIDATION OK: "
        f"{len(case_ids)} cases, {len(claim_ids)} claims, "
        f"{len(source_ids)} sources, {len(entity_ids)} entities, "
        f"{len(mechanism_ids)} mechanisms, {len(relations)} relations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
