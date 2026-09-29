#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CASES = DOCS / "faelle"
DATA = ROOT / "data"

EVIDENCE_LABELS = {
    "established": "belegt",
    "strong": "stark gestützt",
    "plausible": "plausibel",
    "speculative": "spekulativ/offen",
    "contradicted": "widersprochen",
}


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing frontmatter")
    end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    return yaml.safe_load("\n".join(lines[1:end])) or {}


def start_sort_key(value: Any) -> tuple[int, int, int, str]:
    text = str(value).strip()
    match = re.match(r"^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?", text)
    if not match:
        return (9999, 99, 99, text)
    year = int(match.group(1))
    month = int(match.group(2)) if match.group(2) else 0
    day = int(match.group(3)) if match.group(3) else 0
    if month > 12 or day > 31:
        return (year, 99, 99, text)
    return (year, month, day, text)


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def records() -> list[tuple[dict[str, Any], str]]:
    out: list[tuple[dict[str, Any], str]] = []
    for path in sorted(CASES.rglob("*.md")):
        if path == CASES / "index.md":
            continue
        meta = frontmatter(path)
        if meta.get("type") == "case":
            out.append((meta, path.relative_to(DOCS).as_posix()))
    return sorted(
        out,
        key=lambda item: (
            *start_sort_key(item[0].get("period", {}).get("start", "")),
            item[0].get("title", ""),
        ),
    )


def claim_summary(meta: dict[str, Any]) -> str:
    counts = Counter(
        claim.get("evidence_level")
        for claim in meta.get("claims", [])
        if isinstance(claim, dict)
    )
    parts = [
        f"{counts[level]} {label}"
        for level, label in EVIDENCE_LABELS.items()
        if counts[level]
    ]
    return " · ".join(parts) if parts else "keine Claims"


def render_cases(cases: list[tuple[dict[str, Any], str]]) -> str:
    lines = [
        "# Fälle",
        "",
        "_Automatisch aus den Fall-Metadaten erzeugt._",
        "",
        "| Zeitraum | Fall | Länder | Claim-Evidenz | Mechanismen |",
        "|---|---|---|---|---|",
    ]
    for meta, rel in cases:
        period = str(meta["period"]["start"])
        if meta["period"].get("end"):
            period += f" – {meta['period']['end']}"
        case_rel = Path(rel).relative_to("faelle").as_posix()
        lines.append(
            f"| {esc(period)} | [{esc(meta['title'])}]({case_rel}) | "
            f"{', '.join(meta.get('countries', []))} | {esc(claim_summary(meta))} | "
            f"{', '.join(meta.get('mechanisms', []))} |"
        )
    return "\n".join(lines) + "\n"


def render_timeline(cases: list[tuple[dict[str, Any], str]]) -> str:
    lines = [
        "# Chronologie",
        "",
        "_Automatisch aus denselben Fall-Metadaten erzeugt._",
        "",
        "| Beginn | Ende | Fall | Länder | Claim-Evidenz |",
        "|---:|---:|---|---|---|",
    ]
    for meta, rel in cases:
        start = meta.get("period", {}).get("start", "?")
        end = meta.get("period", {}).get("end", "–") or "–"
        lines.append(
            f"| {start} | {end} | [{esc(meta['title'])}](../{rel}) | "
            f"{', '.join(meta.get('countries', []))} | {esc(claim_summary(meta))} |"
        )
    return "\n".join(lines) + "\n"


def render_entities(entities: list[dict[str, Any]]) -> str:
    lines = [
        "# Personen & Organisationen",
        "",
        "Die Aufnahme in diesen Katalog bedeutet weder Fehlverhalten noch politischen Einfluss. Er dokumentiert zunächst nur die im Datenmodell verwendeten Akteure.",
        "",
        "| ID | Typ | Name | Länder |",
        "|---|---|---|---|",
    ]
    for entity in sorted(entities, key=lambda x: x["name"]):
        lines.append(
            f"| `{entity['id']}` | {entity['type']} | {esc(entity['name'])} | "
            f"{', '.join(entity.get('countries', []))} |"
        )
    return "\n".join(lines) + "\n"


def render_regions(cases: list[tuple[dict[str, Any], str]]) -> str:
    by_country: dict[str, list[tuple[dict[str, Any], str]]] = {}
    for meta, rel in cases:
        for country in meta.get("countries", []):
            by_country.setdefault(country, []).append((meta, rel))
    lines = [
        "# Regionen",
        "",
        "_Gruppiert nach ISO-Ländercode. Die Kurzangabe zeigt die Claim-Verteilung, kein Fall-Gesamturteil._",
        "",
    ]
    for country in sorted(by_country):
        lines += [f"## {country}", ""]
        for meta, rel in by_country[country]:
            lines.append(
                f"- [{meta['title']}](../{rel}) — {meta['period']['start']} · {claim_summary(meta)}"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def render_hypotheses(cases: list[tuple[dict[str, Any], str]]) -> str:
    lines = [
        "# Offene Hypothesen",
        "",
        "Hier erscheinen nur Claims, die im Frontmatter ausdrücklich als Hypothese, offene Frage, plausibel oder spekulativ kodiert sind. Offene Forschungsfragen in den Falltexten werden bei weiterer Atomisierung hierher überführt.",
        "",
    ]
    count = 0
    for meta, rel in cases:
        for claim in meta.get("claims", []):
            if (
                claim.get("classification") in {"hypothesis", "open_question"}
                or claim.get("evidence_level") in {"plausible", "speculative"}
            ):
                count += 1
                lines += [
                    f"## [{meta['title']}](../{rel}) · {claim['id']}",
                    "",
                    f"**{claim.get('classification')} · {claim.get('evidence_level')}**",
                    "",
                    claim.get("text", ""),
                    "",
                ]
    if count == 0:
        lines.append(
            "Der strukturierte Claimbestand enthält derzeit keine als Hypothese oder offene Frage kodierten Claims. "
            "Das bedeutet nicht, dass die Fälle abgeschlossen sind; ihre offenen Prüfungen stehen in den Fallakten."
        )
        lines.append("")
    return "\n".join(lines) + "\n"


def render_mechanisms(mechanisms: list[dict[str, Any]]) -> str:
    lines = [
        "# Mechanismen",
        "",
        "Mechanismen sind Vergleichskategorien, keine automatische Erklärung eines Einzelfalls und keine Schuldzuweisung.",
        "",
    ]
    for item in sorted(mechanisms, key=lambda x: x["label"]):
        lines += [
            f"## {item['label']}",
            "",
            f"`{item['id']}` — {item['definition']}",
            "",
        ]
    return "\n".join(lines) + "\n"


def render_sources(sources: list[dict[str, Any]]) -> str:
    lines = [
        "# Quellen",
        "",
        "Quellen werden zentral registriert und über stabile IDs aus Claims, Fällen und Relationen referenziert. Die Stufe bewertet die Quellenart; eine Primärquelle kann trotzdem unvollständig, interessengeleitet oder fehlerhaft sein.",
        "",
    ]
    for source in sources:
        primary = "Primärquelle" if source.get("primary") else "Sekundär-/Forschungsquelle"
        source_date = source.get("date")
        date_label = source_date if source_date is not None else "unbekannt"
        lines += [
            f'<a id="{source["id"].lower()}"></a>',
            f"## {source['id']}",
            "",
            f"**[{source['title']}]({source['url']})**",
            "",
            f"{source['institution']} · {date_label} · Stufe **{source['tier']}** · {primary}",
            "",
            f"[{('PDF öffnen' if source['url'].lower().split('?', 1)[0].endswith('.pdf') else 'Seite öffnen')}]({source['url']})",
            "",
        ]
        if source.get("locator"):
            lines += [f"Fundstelle: {source['locator']}", ""]
    return "\n".join(lines) + "\n"


def render_network(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> str:
    entity_map = {x["id"]: x for x in entities}
    case_titles = {meta["id"]: meta["title"] for meta, _ in cases}

    def label(node: str) -> str:
        if node in entity_map:
            return entity_map[node]["name"]
        return case_titles.get(node, node)

    def mid(node: str) -> str:
        return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", node)

    lines = [
        "# Netzwerk",
        "",
        "_Automatisch aus data/relations.yml erzeugt. Jede Kante besitzt mindestens eine Quelle._",
        "",
        "```mermaid",
        "flowchart LR",
    ]
    seen: set[str] = set()
    for relation in relations:
        source, target = relation["from"], relation["to"]
        for node in (source, target):
            if node not in seen:
                lines.append(
                    f'    {mid(node)}["{label(node).replace(chr(34), chr(39))}"]'
                )
                seen.add(node)
        edge = relation.get("label", relation["type"]).replace('"', "'")
        lines.append(f'    {mid(source)} -->|"{edge}"| {mid(target)}')

    lines += [
        "```",
        "",
        "## Relationen",
        "",
        "| ID | Von | Beziehung | Zu | Evidenz | Quellen |",
        "|---|---|---|---|---|---|",
    ]
    for relation in relations:
        lines.append(
            f"| {relation['id']} | {esc(label(relation['from']))} | "
            f"{esc(relation.get('label', relation['type']))} | {esc(label(relation['to']))} | "
            f"{relation['evidence_level']} | {', '.join(relation['sources'])} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated website pages differ from the checked-in state",
    )
    args = parser.parse_args()

    cases = records()
    sources = load_yaml(DATA / "sources.yml").get("sources", [])
    entities = load_yaml(DATA / "entities.yml").get("entities", [])
    mechanisms = load_yaml(DATA / "mechanisms.yml").get("mechanisms", [])
    relations = load_yaml(DATA / "relations.yml").get("relations", [])

    outputs = {
        DOCS / "faelle" / "index.md": render_cases(cases),
        DOCS / "generated" / "timeline.md": render_timeline(cases),
        DOCS / "generated" / "network.md": render_network(cases, entities, relations),
        DOCS / "generated" / "entities.md": render_entities(entities),
        DOCS / "generated" / "regions.md": render_regions(cases),
        DOCS / "generated" / "hypotheses.md": render_hypotheses(cases),
        DOCS / "mechanismen" / "index.md": render_mechanisms(mechanisms),
        DOCS / "quellen" / "index.md": render_sources(sources),
        DOCS / "methodik.md": (ROOT / "METHODOLOGY.md").read_text(encoding="utf-8"),
    }

    stale: list[str] = []
    for path, content in outputs.items():
        content = content.rstrip() + "\n"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if stale:
        print("GENERATED CONTENT STALE")
        for path in stale:
            print(f"- {path}")
        return 1

    print(
        ("INDEX CHECK OK" if args.check else "INDEXES GENERATED")
        + f": {len(cases)} cases, {len(relations)} relations, {len(outputs)} pages"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())