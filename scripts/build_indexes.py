#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from html import escape as html_escape
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


# Curated presentation groups; stable source URLs and case IDs remain unchanged.
# Newly registered cases appear under "Weitere Fälle" until categorized.
CASE_TOPICS = {
    "faelle/de/organisation-gehlen.md": "Nachrichtendienste & Informanten",
    "faelle/de/langemann-informationsnetz-1976-1982.md": "Nachrichtendienste & Informanten",
    "faelle/de/peter-urbach-verfassungsschutz.md": "Nachrichtendienste & Informanten",
    "faelle/de/celler-loch.md": "Nachrichtendienste & Informanten",
    "faelle/de/technischer-dienst-bdj.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/deutsche-aktionsgruppen-roeder-1980-1998.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/oktoberfestattentat-1980.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/thueringer-heimatschutz-tino-brandt.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/nsu-v-leute-aktenvernichtung.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/britisch-deutsche-combat18-blood-honour-verflechtung-1993-2020.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/nsu-yozgat-temme.md": "Rechtsterrorismus & Ermittlungen",
    "faelle/de/la-belle-1986.md": "Internationale Anschläge",
    "faelle/it/piazza-fontana.md": "Internationale Anschläge",
    "faelle/de/cum-ex-warburg-steuerverfahren.md": "Politik, Wirtschaft & Medien",
    "faelle/de/medien-nachrichtendienst-crosslayer.md": "Politik, Wirtschaft & Medien",
    "faelle/de/transatlantik-mediennetzwerk-2017-2026.md": "Politik, Wirtschaft & Medien",
}
TOPIC_SECTIONS = (
    ("Nachrichtendienste & Informanten",
     "Geheime Informationswege, V-Personen, Behördenkontakte und staatliche Mittel."),
    ("Rechtsterrorismus & Ermittlungen",
     "Militante Netzwerke, Tatkomplexe, Quellenschutz und behördliche Aufklärung."),
    ("Internationale Anschläge",
     "Transnationale Zusammenhänge, Nachrichtendienstkontakte und Tatuntersuchungen."),
    ("Politik, Wirtschaft & Medien",
     "Finanzierungswege, politische Kontakte und dokumentierte Medienbeeinflussung."),
)


def render_cases(
    cases: list[tuple[dict[str, Any], str]],
    mechanism_names: dict[str, str] | None = None,
) -> str:
    mechanism_names = mechanism_names or {}
    by_topic: dict[str, list[tuple[dict[str, Any], str]]] = {}
    for meta, rel in cases:
        by_topic.setdefault(CASE_TOPICS.get(rel, "Weitere Fälle"), []).append((meta, rel))

    lines = [
        "# Fallakten",
        "",
        f"**{len(cases)} Fallakten** · Thematisch geordnet; innerhalb eines Bereichs chronologisch sortiert. "
        "Jeder Eintrag führt zum dokumentierten Ereigniskern und zu den Quellen.",
        "",
    ]
    sections = list(TOPIC_SECTIONS)
    if "Weitere Fälle" in by_topic:
        sections.append(("Weitere Fälle", "Neu hinzugefügte Fallakten."))
    for name, description in sections:
        items = by_topic.get(name, [])
        if not items:
            continue
        lines += [
            f"## {name}",
            "",
            description,
            "",
            "| Zeitraum | Fall | Länder | Claim-Evidenz | Mechanismen |",
            "|---|---|---|---|---|",
        ]
        for meta, rel in items:
            period = str(meta["period"]["start"])
            if meta["period"].get("end"):
                period += f" – {meta['period']['end']}"
            case_rel = Path(rel).relative_to("faelle").as_posix()
            mechanisms = ", ".join(
                mechanism_names.get(key, key) for key in meta.get("mechanisms", [])
            )
            lines.append(
                f"| {esc(period)} | [{esc(meta['title'])}]({case_rel}) | "
                f"{', '.join(meta.get('countries', []))} | {esc(claim_summary(meta))} | "
                f"{esc(mechanisms)} |"
            )
        lines.append("")
    lines += [
        "## Weitere Zugänge",
        "",
        "- [Chronologie](../generated/timeline.md) — alle Fälle nach Beginn.",
        "- [Personen und Organisationen](../generated/entities.md) — Akteursregister.",
        "- [Quellenkatalog](../quellen/index.md) — Originaldokumente und Fundstellen.",
        "",
    ]
    return "\n".join(lines) + "\n"


def render_timeline(cases: list[tuple[dict[str, Any], str]]) -> str:
    lines = [
        "# Chronologie",
        "",
        "_Automatisch aus denselben Fall-Metadaten erzeugt._",
        "",
        "Die [Beziehungs-Chronologie](relation-timeline.md) zeigt zusätzlich "
        "sämtliche belegten Zeiträume aus dem Netzwerkregister.",
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



def render_relation_timeline(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> str:
    """Render every source-bound relation by its documented time span, not inference."""
    entity_names = {item["id"]: item["name"] for item in entities}
    case_names = {item["id"]: item["title"] for item, _path in cases}

    def name(node_id: str) -> str:
        return esc(entity_names.get(node_id, case_names.get(node_id, node_id)))

    def render_row(item: dict[str, Any]) -> str:
        period = item.get("period") or {}
        start = period.get("start") or "–"
        end = period.get("end") or "–"
        relation_id = item["id"]
        reference = f"[{relation_id}](network.md#{relation_id.lower()})"
        source_links = ", ".join(
            f"[{source}](../quellen/index.md#{source.lower()})"
            for source in item["sources"]
        )
        return (
            f"| {start} | {end} | {reference} | "
            f"{name(item['from'])} → {name(item['to'])} | "
            f"{esc(item.get('label', item['type']))} | "
            f"{EVIDENCE_LABELS.get(item['evidence_level'], item['evidence_level'])} | "
            f"{source_links} |"
        )

    dated = sorted(
        (r for r in relations if (r.get("period") or {}).get("start")),
        key=lambda r: (start_sort_key(r["period"]["start"]), r["id"]),
    )
    undated = sorted(
        (r for r in relations if not (r.get("period") or {}).get("start")),
        key=lambda r: r["id"],
    )
    lines = [
        "# Beziehungs-Chronologie",
        "",
        f"**{len(relations)} quellengebundene Beziehungen**: "
        f"**{len(dated)} datiert**, **{len(undated)} ohne belegten Beginn**. "
        "Alle Einträge werden automatisch aus dem kanonischen Relationskatalog erzeugt.",
        "",
        "Die Anfangs- und Endangaben sind die in der jeweiligen Quelle belegte "
        "**zeitliche Einordnung der Beziehung**, nicht notwendigerweise die "
        "Valuta einer Zahlung, die persönliche Teilnahme an einer Sitzung "
        "oder die Dauer fortgesetzter Kontrolle. Kreditrahmen, "
        "Zeugenaussagen und Buchungsbelege bleiben unterscheidbar.",
        "",
        "[Fallchronologie](timeline.md) · "
        "[Quellengebundene Relationstabelle](network.md) · "
        "[Netzwerkdiagramm](network-graph.md)",
        "",
        "## Datierte Beziehungen",
        "",
    ]
    header = [
        "| Beginn | Ende | Relation | Akteure | Dokumentierter Zusammenhang | Evidenz | Quellen |",
        "|---|---|---|---|---|---|---|",
    ]
    if dated:
        lines += header + [render_row(item) for item in dated]
    else:
        lines += ["Keine datierten Beziehungen vorhanden."]
    lines += ["", "## Ohne gesicherte Anfangsdatierung", ""]
    if undated:
        lines += header + [render_row(item) for item in undated]
    else:
        lines += ["Alle erfassten Beziehungen haben eine Datierung."]
    return "\n".join(lines) + "\n"


def render_entities(
    entities: list[dict[str, Any]], relations: list[dict[str, Any]]
) -> str:
    """Link each entity to a stable, source-bound relation entry point."""
    relation_ids: dict[str, list[str]] = {}
    for relation in relations:
        for node in {relation["from"], relation["to"]}:
            relation_ids.setdefault(node, []).append(relation["id"].lower())
    groups = [
        ("Personen", [item for item in entities if item["type"] == "person"]),
        ("Organisationen & Institutionen", [
            item for item in entities if item["type"] not in {
                "person", "program", "historical_contract_document",
                "historical_press_contract_document",
            }
        ]),
        ("Programme", [item for item in entities if item["type"] == "program"]),
        ("Historische Vertragsurkunden", [
            item for item in entities if item["type"] in {
                "historical_contract_document", "historical_press_contract_document"
            }
        ]),
    ]
    lines = [
        "# Personen & Organisationen",
        "",
        f"**{len(entities)} Einträge** · Alphabetisch innerhalb der Kategorien geordnet. "
        "Die Zahl in der Spalte Beziehungen führt zur ersten dokumentierten "
        "Relation in der [quellengebundenen Netzwerkübersicht](network.md).",
        "",
    ]
    for heading, items in groups:
        if not items:
            continue
        lines += [
            f"## {heading}",
            "",
            "| Name | Typ | ID | Länder | Beziehungen |",
            "|---|---|---|---|---|",
        ]
        for entity in sorted(items, key=lambda item: item["name"].casefold()):
            matches = relation_ids.get(entity["id"], [])
            relation_link = (
                f"[{len(matches)}](network.md#{matches[0]})" if matches else "–"
            )
            lines.append(
                f"| {esc(entity['name'])} | {esc(entity['type'])} | "
                f"`{entity['id']}` | {', '.join(entity.get('countries', []))} | "
                f"{relation_link} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def render_regions(cases: list[tuple[dict[str, Any], str]]) -> str:
    by_country: dict[str, list[tuple[dict[str, Any], str]]] = {}
    for meta, rel in cases:
        for country in meta.get("countries", []):
            by_country.setdefault(country, []).append((meta, rel))
    lines = [
        "# Regionen",
        "",
        "Fallakten nach Ländern, jeweils mit Zeitraum und Verteilung der dokumentierten Claims.",
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
            "Weitere Archivfragen finden sich in den Fallakten."
        )
        lines.append("")
    return "\n".join(lines) + "\n"


def render_mechanisms(mechanisms: list[dict[str, Any]]) -> str:
    lines = [
        "# Mechanismen",
        "",
        "Wiederkehrende Abläufe und institutionelle Mechanismen als Vergleichsrahmen für die Fallakten.",
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
        "# Quellenkatalog",
        "",
        f"**{len(sources)} registrierte Quellen** · Originaldokumente und Forschung "
        "mit stabiler Kennung, direktem Link und genauer Fundstelle.",
        "",
        '<div id="mv-source-browser"></div>',
        "",
        "Schnelleinstieg: [Originaldokumente & amtliche Quellen](#originalquellen)"
        " · [Forschung & Dokumentation](#forschungsliteratur). "
        "Die Buchstabenlinks in den Abschnitten springen zur ersten Quelle "
        "der jeweiligen Institution. Mit der Seitensuche können weitere "
        "Begriffe gefunden werden; Links mit Quellen-IDs bleiben dauerhaft gültig.",
        "",
    ]
    for heading, selected in [
        ("Originaldokumente & amtliche Quellen", [
            item for item in sources if item.get("primary")
        ]),
        ("Forschung & Dokumentation", [
            item for item in sources if not item.get("primary")
        ]),
    ]:
        if not selected:
            continue
        section_anchor = "originalquellen" if selected[0].get("primary") else "forschungsliteratur"
        sorted_sources = sorted(
            selected, key=lambda item: (
                str(item.get("institution") or "").casefold(),
                str(item.get("date") or ""),
                str(item.get("title") or "").casefold(),
            )
        )
        # Existing src-* fragment identifiers remain the canonical destinations.
        first_by_letter: dict[str, str] = {}
        for source in sorted_sources:
            initial = (str(source.get("institution") or "").strip()[:1] or "#").upper()
            first_by_letter.setdefault(initial, source["id"].lower())
        letters = " · ".join(
            f"[{letter}](#{first_by_letter[letter]})"
            for letter in sorted(first_by_letter)
        )
        lines += [f"## {heading} {{ #{section_anchor} }}", "",
                  f"**Institutionen A–Z:** {letters}", ""]
        for source in sorted_sources:
            primary = "Primärquelle" if source.get("primary") else "Sekundär-/Forschungsquelle"
            source_date = source.get("date")
            date_label = source_date if source_date is not None else "unbekannt"
            year_match = re.search(r"(?<!\d)[12]\d{3}(?!\d)", str(date_label))
            year = year_match.group() if year_match else ""
            kind = "primary" if source.get("primary") else "research"
            tier = html_escape(str(source["tier"]), quote=True)
            lines += [
                f'<article class="mv-source-entry" markdown="1" '
                f'data-source-kind="{kind}" data-source-tier="{tier}" data-source-year="{year}">',
                "",
                f'<a id="{source["id"].lower()}"></a>',
                f"### {source['institution']}",
                "",
                f"**[{source['title']}]({source['url']})**",
                "",
                f"{source['institution']} · {date_label} · Stufe **{source['tier']}** · {primary} · `{source['id']}`",
                "",
                f"[{('PDF öffnen' if source['url'].lower().split('?', 1)[0].endswith('.pdf') else 'Seite öffnen')}]({source['url']})",
                "",
            ]
            if source.get("archive_url"):
                lines += [f"[Archiv/Recovery öffnen]({source['archive_url']})", ""]
            if source.get("locator"):
                lines += [f"Fundstelle: {source['locator']}", ""]
            lines += ["</article>", ""]
    return "\n".join(lines) + "\n"


def render_network(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> str:
    entity_map = {item["id"]: item for item in entities}
    case_titles = {meta["id"]: meta["title"] for meta, _ in cases}

    def label(node: str) -> str:
        if node in entity_map:
            return entity_map[node]["name"]
        return case_titles.get(node, node)

    lines = [
        "# Beziehungsnetzwerk",
        "",
        f"**{len(relations)} quellengebundene Beziehungen** zwischen den erfassten Akteuren und Fällen. "
        "Die Tabelle ist alphabetisch nach Ausgangsakteur sortiert.",
        "",
        "[Netzwerkdiagramm öffnen](network-graph.md) — grafische Übersicht aller Relationen. "
        "Jede Zeile ist über ihre Kennung direkt verlinkbar.",
        "",
        "## Dokumentierte Relationen",
        "",
        "| ID | Von | Beziehung | Zu | Evidenz | Quellen |",
        "|---|---|---|---|---|---|",
    ]
    for relation in sorted(
        relations, key=lambda item: (
            label(item["from"]).casefold(), label(item["to"]).casefold(), item["id"]
        )
    ):
        source_links = ", ".join(
            f"[{key}](../quellen/index.md#{key.lower()})"
            for key in relation["sources"]
        )
        lines.append(
            f'| <a id="{relation["id"].lower()}"></a>`{relation["id"]}` | {esc(label(relation["from"]))} | '
            f"{esc(relation.get('label', relation['type']))} | {esc(label(relation['to']))} | "
            f"{EVIDENCE_LABELS.get(relation['evidence_level'], relation['evidence_level'])} | "
            f"{source_links} |"
        )
    return "\n".join(lines) + "\n"


# Focus pages show only direct relations from the canonical dataset.
# They make no new claims about causation or community membership.
FOCUS_NETWORKS = (
    ("Atlantik-Brücke", "atlantik-bruecke", "ORG-DE-ATLANTIK-BRUECKE"),
    ("Bilderberg Meetings", "bilderberg", "ORG-INT-BILDERBERG-MEETINGS"),
    ("Organisation Gehlen", "organisation-gehlen", "ORG-DE-ORGANISATION-GEHLEN"),
    ("Bund Deutscher Jugend", "bdj", "ORG-DE-BDJ"),
    ("BAFISUD", "bafisud", "ORG-UY-BANCO-FINANCIERO-SUDAMERICANO"),
    ("BIZ / BIS", "biz", "ORG-INT-BIS"),
    ("I.G. Farben", "ig-farben", "ORG-DE-IG-FARBEN"),
    ("ENI / Tradinvest", "tradinvest", "ORG-BS-TRADINVEST-ENI"),
    ("M.M.Warburg / Eigentum & Aufsicht", "warburg-kontrolle", "ORG-DE-MM-WARBURG"),
    ("Döpfner / Springer", "springer-doepfner", "PER-DE-MATHIAS-DOEPFNER"),
    ("P2 / Loge", "p2", "ORG-IT-LOGGIA-P2-1970-1981"),
    ("Rizzoli / Corriere", "rizzoli", "ORG-IT-RIZZOLI-EDITORE-1975-1984"),
    ("UBS Genf / Bologna 1980", "ubs-genf-1980", "ORG-CH-UBS-GENEVA-1980"),
)


def mermaid_network_lines(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> list[str]:
    entity_map = {item["id"]: item for item in entities}
    case_titles = {meta["id"]: meta["title"] for meta, _ in cases}

    def label(node: str) -> str:
        return entity_map[node]["name"] if node in entity_map else case_titles.get(node, node)

    def mid(node: str) -> str:
        return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", node)

    lines = ["flowchart LR"]
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
    return lines


def render_network_graph(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> str:
    """Keep the full network available, with smaller views above it."""
    lines = [
        "# Netzwerkdiagramm",
        "",
        f"**{len(relations)} Beziehungen** als grafische Gesamtübersicht. "
        "Die [alphabetische Relationstabelle](network.md) zeigt zusätzlich Evidenzstufen und Quellen.",
        "",
        "## Direkte Verbindungen im Fokus",
        "",
        "Diese Ausschnitte zeigen nur die unmittelbar dokumentierten Beziehungen "
        "des gewählten Akteurs. Weitere Beziehungen oder eine gemeinsame "
        "Steuerung sind daraus nicht automatisch ableitbar.",
        "",
    ]
    for label, slug, node_id in FOCUS_NETWORKS:
        count = sum(node_id in (relation["from"], relation["to"]) for relation in relations)
        lines.append(
            f"- [{label}](network-focus-{slug}.md) — {count} direkte Beziehungen"
        )
    lines += ["", "## Gesamtnetzwerk", "", "```mermaid",
              *mermaid_network_lines(cases, entities, relations),
              "```", "", "[Zur Relationstabelle](network.md)", ""]
    return "\n".join(lines) + "\n"


def render_network_focus(
    cases: list[tuple[dict[str, Any], str]],
    entities: list[dict[str, Any]],
    relations: list[dict[str, Any]],
    focal_node: str,
    title: str,
) -> str:
    """One-hop graph and a full source-linked relation list."""
    entity_names = {item["id"]: item["name"] for item in entities}
    case_names = {meta["id"]: meta["title"] for meta, _ in cases}
    if focal_node not in entity_names:
        raise ValueError(f"Unknown focus entity: {focal_node}")
    selected = [
        item for item in relations
        if focal_node in (item["from"], item["to"])
    ]
    if not selected:
        raise ValueError(f"No relations for focus entity: {focal_node}")

    def label(node: str) -> str:
        return entity_names.get(node, case_names.get(node, node))

    lines = [
        f"# {title} – direkte Beziehungen",
        "",
        f"**{len(selected)} quellengebundene Beziehungen** mit {title} als Ausgangs- "
        "oder Zielakteur. Die Ansicht zeigt **nur unmittelbare Relationen**; "
        "sie beweist weder gemeinsame Steuerung noch Beziehungen zwischen "
        "den übrigen dargestellten Akteuren.",
        "",
        "[Alle Fokusansichten](network-graph.md) · [Vollständige Relationstabelle](network.md)",
        "",
        "```mermaid",
        *mermaid_network_lines(cases, entities, selected),
        "```",
        "",
        "## Quellen und Evidenz",
        "",
        "| Relation | Richtung und anderer Akteur | Befund | Evidenz | Quellen |",
        "|---|---|---|---|---|",
    ]
    for relation in sorted(selected, key=lambda item: (
        label(item["to"] if item["from"] == focal_node else item["from"]).casefold(),
        item["id"],
    )):
        outgoing = relation["from"] == focal_node
        other = relation["to"] if outgoing else relation["from"]
        direction = "→" if outgoing else "←"
        refs = ", ".join(
            f"[{key}](../quellen/index.md#{key.lower()})"
            for key in relation["sources"]
        )
        lines.append(
            f"| [{relation['id']}](network.md#{relation['id'].lower()}) | "
            f"{direction} {esc(label(other))} | "
            f"{esc(relation.get('label', relation['type']))} | "
            f"{EVIDENCE_LABELS.get(relation['evidence_level'], relation['evidence_level'])} | "
            f"{refs} |"
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
        DOCS / "faelle" / "index.md": render_cases(
            cases, {item["id"]: item["label"] for item in mechanisms}
        ),
        DOCS / "generated" / "timeline.md": render_timeline(cases),
        DOCS / "generated" / "relation-timeline.md": render_relation_timeline(cases, entities, relations),
        DOCS / "generated" / "network.md": render_network(cases, entities, relations),
        DOCS / "generated" / "network-graph.md": render_network_graph(cases, entities, relations),
        DOCS / "generated" / "entities.md": render_entities(entities, relations),
        DOCS / "generated" / "regions.md": render_regions(cases),
        DOCS / "generated" / "hypotheses.md": render_hypotheses(cases),
        DOCS / "mechanismen" / "index.md": render_mechanisms(mechanisms),
        DOCS / "quellen" / "index.md": render_sources(sources),
        DOCS / "methodik.md": (ROOT / "METHODOLOGY.md").read_text(encoding="utf-8"),
    }
    for label, slug, focal_node in FOCUS_NETWORKS:
        outputs[DOCS / "generated" / f"network-focus-{slug}.md"] = (
            render_network_focus(cases, entities, relations, focal_node, label)
        )

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