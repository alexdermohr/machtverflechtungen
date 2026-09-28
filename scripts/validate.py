#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import markdown
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


def lexical_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", normalized))


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


def valid_https_url(value: Any) -> bool:
    if not isinstance(value, str) or not value or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.netloc or not hostname:
        return False
    try:
        ascii_host = hostname.rstrip(".").encode("idna").decode("ascii")
    except UnicodeError:
        return False
    if not ascii_host or len(ascii_host) > 253:
        return False
    labels = ascii_host.split(".")
    host_label = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
    return all(host_label.fullmatch(label) for label in labels)


def markdown_body(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return ""
    return "\n".join(lines[end + 1 :])


def has_visible_text(value: str) -> bool:
    return any(
        unicodedata.category(char)[0] in {"L", "N", "P", "S"}
        for char in value
    )


class VisibleListLinkParser(HTMLParser):
    VOID_TAGS = frozenset(
        {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }
    )
    ALWAYS_HIDDEN_TAGS = frozenset({"head", "script", "style", "template"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._items: list[dict[str, Any]] = []
        self._anchors: list[dict[str, Any]] = []
        self._elements: list[tuple[str, bool]] = []
        self.visible_items: list[tuple[str, list[tuple[str, str]]]] = []

    @staticmethod
    def _declares_hidden(
        tag: str, attrs: list[tuple[str, str | None]]
    ) -> bool:
        lowered = {
            name.casefold(): value.casefold() if isinstance(value, str) else value
            for name, value in attrs
        }
        style = lowered.get("style")
        style_text = style.replace(" ", "") if isinstance(style, str) else ""
        return (
            tag in VisibleListLinkParser.ALWAYS_HIDDEN_TAGS
            or "hidden" in lowered
            or lowered.get("aria-hidden") == "true"
            or "display:none" in style_text
            or "visibility:hidden" in style_text
        )

    def _current_hidden(self) -> bool:
        return bool(self._elements and self._elements[-1][1])

    def _close_element(self, tag: str) -> None:
        for index in range(len(self._elements) - 1, -1, -1):
            if self._elements[index][0] == tag:
                del self._elements[index:]
                return

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        hidden = self._current_hidden() or self._declares_hidden(tag, attrs)
        if tag not in self.VOID_TAGS:
            self._elements.append((tag, hidden))
        if tag == "li":
            self._items.append({"text": [], "links": [], "hidden": hidden})
            return
        if tag == "a" and self._items:
            href = next(
                (value for name, value in attrs if name.casefold() == "href"),
                None,
            )
            self._anchors.append(
                {
                    "href": href if isinstance(href, str) else None,
                    "text": [],
                    "hidden": hidden,
                }
            )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        return

    def handle_data(self, data: str) -> None:
        if self._current_hidden():
            return
        if self._items:
            self._items[-1]["text"].append(data)
        if self._anchors:
            self._anchors[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag == "a" and self._anchors:
            anchor = self._anchors.pop()
            href = anchor.get("href")
            visible_anchor_text = " ".join("".join(anchor["text"]).split())
            if (
                self._items
                and anchor.get("hidden") is not True
                and isinstance(href, str)
            ):
                self._items[-1]["links"].append((href, visible_anchor_text))
        elif tag == "li" and self._items:
            item = self._items.pop()
            if item.get("hidden") is not True:
                visible_text = " ".join("".join(item["text"]).split())
                self.visible_items.append((visible_text, list(item["links"])))
        self._close_element(tag)


def rendered_list_links(path: Path) -> list[tuple[str, list[tuple[str, str]]]]:
    rendered = markdown.markdown(markdown_body(path), extensions=["extra"])
    parser = VisibleListLinkParser()
    parser.feed(rendered)
    parser.close()
    return parser.visible_items


class VisibleTextParser(HTMLParser):
    VOID_TAGS = VisibleListLinkParser.VOID_TAGS

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._elements: list[tuple[str, bool]] = []
        self._text: list[str] = []

    def _current_hidden(self) -> bool:
        return bool(self._elements and self._elements[-1][1])

    def _close_element(self, tag: str) -> None:
        for index in range(len(self._elements) - 1, -1, -1):
            if self._elements[index][0] == tag:
                del self._elements[index:]
                return

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        hidden = self._current_hidden() or VisibleListLinkParser._declares_hidden(
            tag, attrs
        )
        if tag not in self.VOID_TAGS:
            self._elements.append((tag, hidden))

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        return

    def handle_data(self, data: str) -> None:
        if not self._current_hidden():
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        self._close_element(tag.casefold())

    def text(self) -> str:
        return " ".join(" ".join(self._text).split())


def rendered_visible_text(path: Path) -> str:
    rendered = markdown.markdown(markdown_body(path), extensions=["extra"])
    parser = VisibleTextParser()
    parser.feed(rendered)
    parser.close()
    return parser.text()


def exact_visible_id(text: str, identifier: str) -> bool:
    pattern = rf"(?<![\w-]){re.escape(identifier)}(?![\w-])"
    return re.search(pattern, text) is not None


def direct_source_link_errors(
    path: Path,
    source_ids: list[str],
    source_by_id: dict[str, dict[str, Any]],
    label: str,
) -> list[str]:
    items = rendered_list_links(path)
    out: list[str] = []
    for source_id in source_ids:
        source = source_by_id.get(source_id)
        if not isinstance(source, dict):
            continue
        url = source.get("url")
        if not isinstance(url, str):
            continue
        if not any(
            exact_visible_id(visible_text, source_id)
            and any(
                href == url and has_visible_text(anchor_text)
                for href, anchor_text in links
            )
            for visible_text, links in items
        ):
            out.append(
                f"{label}: source {source_id} must be visibly listed with a "
                "clickable link to its registered URL"
            )
    return out


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


def evidence_sources(value: Any) -> list[str]:
    return [
        item["source"]
        for item in mapping_list(value)
        if isinstance(item.get("source"), str)
    ]


def main() -> int:
    errors: list[str] = []

    sources = load_catalog("sources.yml", "sources", "source.schema.json", errors)
    for source in sources:
        source_id = source.get("id", "<unknown-source>")
        publication_date = source.get("date")
        if (
            isinstance(publication_date, str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}", publication_date.strip())
            and period_bounds(publication_date) is None
        ):
            errors.append(
                f"sources:{source_id}: date must use a valid YYYY-MM-DD date"
            )

        accessed = source.get("accessed")
        if isinstance(accessed, str) and period_bounds(accessed) is None:
            errors.append(
                f"sources:{source_id}: accessed must use a valid YYYY-MM-DD date"
            )

        url = source.get("url")
        if isinstance(url, str) and not valid_https_url(url):
            errors.append(
                f"sources:{source_id}: url must be a valid HTTPS URL with a host"
            )
        archive_url = source.get("archive_url")
        if isinstance(archive_url, str) and not valid_https_url(archive_url):
            errors.append(
                f"sources:{source_id}: archive_url must be a valid HTTPS URL with a host"
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
    relation_by_id = {
        item["id"]: item
        for item in relations
        if isinstance(item.get("id"), str)
    }

    case_ids: set[str] = set()
    claim_ids: set[str] = set()
    claim_case_by_id: dict[str, str] = {}
    claim_by_id: dict[str, dict[str, Any]] = {}
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
                    claim_by_id.setdefault(claim_id, claim)
                    if isinstance(case_id, str):
                        claim_case_by_id[claim_id] = case_id
        cases.append((path, meta))

    for path, meta in cases:
        label = str(path.relative_to(ROOT))
        case_id = meta.get("id")
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
        errors.extend(
            direct_source_link_errors(path, case_sources, source_by_id, label)
        )

        for actor_id in string_list(meta.get("actors")):
            if actor_id not in entity_ids:
                errors.append(f"{label}: unknown actor {actor_id}")
        for mechanism_id in string_list(meta.get("mechanisms")):
            if mechanism_id not in mechanism_ids:
                errors.append(f"{label}: unknown mechanism {mechanism_id}")

        for event_claim_id in string_list(meta.get("event_claims")):
            event_claim = claim_by_id.get(event_claim_id)
            if event_claim is None:
                errors.append(f"{label}: event claim {event_claim_id} is unknown")
                continue
            owner_case = claim_case_by_id.get(event_claim_id)
            if isinstance(case_id, str) and owner_case != case_id:
                errors.append(
                    f"{label}: event claim {event_claim_id} belongs to case {owner_case}"
                )
                continue
            if event_claim.get("classification") != "fact":
                errors.append(
                    f"{label}: event claim {event_claim_id} must be classification fact"
                )
            event_level = event_claim.get("evidence_level")
            if not isinstance(event_level, str) or event_level not in {"established", "strong"}:
                errors.append(
                    f"{label}: event claim {event_claim_id} must be established or strong"
                )

        for synthesis_field in ("what_follows", "what_does_not_follow"):
            for synthesis in mapping_list(meta.get(synthesis_field)):
                for synthesis_claim_id in string_list(synthesis.get("claim_ids")):
                    synthesis_claim = claim_by_id.get(synthesis_claim_id)
                    if synthesis_claim is None:
                        errors.append(
                            f"{label}: {synthesis_field} references unknown claim {synthesis_claim_id}"
                        )
                        continue
                    owner_case = claim_case_by_id.get(synthesis_claim_id)
                    if isinstance(case_id, str) and owner_case != case_id:
                        errors.append(
                            f"{label}: {synthesis_field} claim {synthesis_claim_id} "
                            f"belongs to case {owner_case}"
                        )

        seen_links: set[tuple[str, str]] = set()
        for link in mapping_list(meta.get("case_links")):
            kind = link.get("kind")
            target = link.get("target")
            if isinstance(target, str):
                if target == case_id:
                    errors.append(f"{label}: case link may not target itself")
                if target not in case_ids:
                    errors.append(f"{label}: case link references unknown case {target}")
            if isinstance(kind, str) and isinstance(target, str):
                key = (kind, target)
                if key in seen_links:
                    errors.append(
                        f"{label}: duplicate {kind} case link to {target}"
                    )
                seen_links.add(key)
            if kind == "documented_connection":
                relation_id = link.get("relation_id")
                relation = relation_by_id.get(relation_id)
                if relation is None:
                    errors.append(
                        f"{label}: documented case link requires known relation {relation_id}"
                    )
                elif isinstance(case_id, str) and isinstance(target, str):
                    if {relation.get("from"), relation.get("to")} != {case_id, target}:
                        errors.append(
                            f"{label}: relation {relation_id} does not directly connect "
                            f"{case_id} and {target}"
                        )

        visible_body = rendered_visible_text(path)
        body_lexical = lexical_text(visible_body)

        for claim in mapping_list(meta.get("claims")):
            claim_id = claim.get("id")
            claim_text = claim.get("text")
            classification = claim.get("classification")
            evidence_level = claim.get("evidence_level")

            if isinstance(claim_id, str):
                claim_id_pattern = re.compile(
                    rf"(?<![\w-]){re.escape(claim_id)}(?![\w-])"
                )
                if claim_id_pattern.search(visible_body) is None:
                    errors.append(
                        f"{label}: claim {claim_id} must be visibly represented by ID in case body"
                    )
            if isinstance(claim_id, str) and isinstance(claim_text, str):
                claim_lexical = lexical_text(claim_text)
                if claim_lexical and claim_lexical not in body_lexical:
                    errors.append(
                        f"{label}: claim {claim_id} wording must be visibly represented in case body"
                    )
            claim_sources = string_list(claim.get("sources"))
            rich_support_sources = evidence_sources(claim.get("evidence"))
            counter_sources = evidence_sources(claim.get("counterevidence"))

            if set(claim_sources) != set(rich_support_sources):
                errors.append(
                    f"{label}: claim {claim_id} sources must exactly match evidence source IDs"
                )

            source_optional = (
                isinstance(classification, str)
                and classification in {"open_question", "hypothesis"}
                and evidence_level == "speculative"
            )
            if not source_optional and not claim_sources:
                errors.append(f"{label}: claim {claim_id} requires at least one source")

            all_claim_source_ids = list(
                dict.fromkeys([*claim_sources, *rich_support_sources, *counter_sources])
            )
            for source_id in all_claim_source_ids:
                if source_id not in source_ids:
                    errors.append(
                        f"{label}: claim {claim_id} references unknown source {source_id}"
                    )
                if source_id not in case_sources:
                    errors.append(
                        f"{label}: claim source {source_id} must also appear in case.sources "
                        f"(claim {claim_id})"
                    )

            non_lead_required = (
                isinstance(classification, str)
                and (
                    classification in {"fact", "counterevidence", "interpretation"}
                    or (
                        classification in {"hypothesis", "open_question"}
                        and isinstance(evidence_level, str)
                        and evidence_level
                        in {"established", "strong", "plausible", "contradicted"}
                    )
                )
            )
            if (
                evidence_level == "established"
                and claim_sources
                and all(source_id in source_by_id for source_id in claim_sources)
                and not established_supports(claim_sources, source_by_id)
            ):
                errors.append(
                    f"{label}: claim {claim_id} with established evidence requires "
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
                    f"{label}: claim {claim_id} may not rely solely on Tier-E leads"
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
        relation_claim_ids = string_list(relation.get("claim_ids"))
        for claim_id in relation_claim_ids:
            if claim_id not in claim_ids:
                errors.append(f"{relation_id}: unknown claim {claim_id}")
        if from_id in case_ids and to_id in case_ids:
            if not relation_claim_ids:
                errors.append(
                    f"{relation_id}: case-to-case relation requires at least one claim_id"
                )
            for claim_id in relation_claim_ids:
                claim_case = claim_case_by_id.get(claim_id)
                if claim_case is not None and claim_case not in {from_id, to_id}:
                    errors.append(
                        f"{relation_id}: claim {claim_id} belongs to unrelated case {claim_case}"
                    )
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
            errors.append(f"{relation_id}: relation may not rely solely on Tier-E leads")

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
            errors.extend(
                direct_source_link_errors(
                    path, organization_sources, source_by_id, label
                )
            )
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
