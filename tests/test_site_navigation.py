"""Public website navigation and overview invariants for the research catalogue."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml

import scripts.build_indexes as build_indexes


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def load_mkdocs_config() -> dict:
    """Read the local MkDocs configuration without executing its Python tag."""
    source = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    source = source.replace(
        "!!python/name:pymdownx.superfences.fence_code_format",
        "'pymdownx.superfences.fence_code_format'",
    )
    return yaml.safe_load(source)


def nav_paths(node: object) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, list):
        return [path for entry in node for path in nav_paths(entry)]
    if isinstance(node, dict):
        return [path for entry in node.values() for path in nav_paths(entry)]
    return []


class WebsiteNavigationTests(unittest.TestCase):
    def test_navigation_covers_every_markdown_page_exactly_once(self) -> None:
        config = load_mkdocs_config()
        paths = nav_paths(config["nav"])
        files = [path.relative_to(DOCS).as_posix() for path in DOCS.rglob("*.md")]
        self.assertEqual(len(paths), len(set(paths)), "navigation must not duplicate pages")
        # The research landing page is generated at build time from main, not copied to docs/.
        virtual = (
            {"research/index.md"}
            if "scripts/mkdocs_research_hook.py" in config.get("hooks", [])
            else set()
        )
        self.assertEqual(
            set(files) | virtual, set(paths),
            "every curated docs page and generated research landing page needs a navigation entry",
        )

    def test_all_cases_have_a_short_reader_intro_and_source_navigation(self) -> None:
        cases = build_indexes.records()
        self.assertEqual(
            {path for _meta, path in cases},
            set(build_indexes.CASE_TOPICS),
            "curated categories must cover every current case",
        )
        for meta, rel in cases:
            with self.subTest(case=meta["id"]):
                text = (DOCS / rel).read_text(encoding="utf-8")
                _frontmatter, separator, body = text[4:].partition("\n---\n")
                self.assertTrue(separator, "case must keep intact YAML frontmatter")
                self.assertEqual(body.count('class="mv-case-intro"'), 1)
                self.assertIn("**Auf einen Blick:**", body)
                self.assertIn("[Alle Fälle](../index.md)", body)
                self.assertIn("[Quellenkatalog](../../quellen/index.md)", body)
                self.assertIn("## Gesicherter Ereigniskern", body)

    def test_indexes_use_topic_grouping_and_clear_source_links(self) -> None:
        cases = build_indexes.records()
        catalog = build_indexes.render_cases(cases)
        self.assertIn("## Nachrichtendienste & Informanten", catalog)
        self.assertIn("## Rechtsterrorismus & Ermittlungen", catalog)
        self.assertIn("## Internationale Anschläge", catalog)
        self.assertIn("## Politik, Wirtschaft & Medien", catalog)
        network = (DOCS / "generated" / "network.md").read_text(encoding="utf-8")
        self.assertIn("[Netzwerkdiagramm öffnen](network-graph.md)", network)
        graph = (DOCS / "generated" / "network-graph.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", graph)
        self.assertIn("flowchart LR", graph)
        self.assertNotIn("??? info", graph)
        self.assertIn("../quellen/index.md#src-", network)

    def test_source_a_to_z_navigation_preserves_original_anchors(self) -> None:
        def source(source_id, institution, primary):
            return {
                "id": source_id,
                "institution": institution,
                "primary": primary,
                "date": "2020",
                "tier": "A",
                "title": "Originaldokument",
                "url": "https://example.org/original.pdf",
            }

        catalog = build_indexes.render_sources([
            source("SRC-TEST-Z", "Zentrum", True),
            source("SRC-TEST-A", "Archiv", True),
            source("SRC-TEST-B", "Bibliothek", False),
        ])
        self.assertIn("[A](#src-test-a)", catalog)
        self.assertIn("[Z](#src-test-z)", catalog)
        self.assertIn("[B](#src-test-b)", catalog)
        for identifier in ("src-test-a", "src-test-b", "src-test-z"):
            self.assertEqual(catalog.count(f'<a id="{identifier}"></a>'), 1)
        self.assertIn("## Originaldokumente & amtliche Quellen { #originalquellen }", catalog)
        self.assertIn("## Forschung & Dokumentation { #forschungsliteratur }", catalog)

    def test_actors_link_to_source_bound_relation_rows(self) -> None:
        entities = [
            {"id": "ORG-TEST-A", "name": "Archiv", "type": "organization", "countries": ["DE"]},
            {"id": "ORG-TEST-B", "name": "Bibliothek", "type": "organization", "countries": ["DE"]},
            {"id": "ORG-TEST-C", "name": "Keine Relation", "type": "organization", "countries": ["DE"]},
        ]
        relation = {
            "id": "REL-TEST-001",
            "from": "ORG-TEST-A",
            "to": "ORG-TEST-B",
            "label": "kooperiert",
            "type": "cooperation",
            "evidence_level": "established",
            "sources": ["SRC-TEST-A"],
        }
        actors = build_indexes.render_entities(entities, [relation])
        network = build_indexes.render_network([], entities, [relation])
        self.assertEqual(actors.count("[1](network.md#rel-test-001)"), 2)
        self.assertIn('<a id="rel-test-001"></a>', network)
        self.assertIn("[SRC-TEST-A](../quellen/index.md#src-test-a)", network)
        self.assertIn("Keine Relation", actors)

    def test_filterable_sources_keep_every_source_anchor_and_year(self) -> None:
        source = {
            "id": "SRC-TEST-1974", "institution": "Archiv",
            "primary": True, "date": "1974-05-12",
            "tier": "A", "title": "Aktenbestand",
            "url": "https://example.org/original.pdf",
        }
        other = {
            **source, "id": "SRC-TEST-UNDATED", "primary": False,
            "date": None, "tier": "C",
        }
        catalog = build_indexes.render_sources([source, other])
        self.assertIn('id="mv-source-browser"', catalog)
        self.assertEqual(catalog.count('class="mv-source-entry"'), 2)
        self.assertIn('data-source-kind="primary"', catalog)
        self.assertIn('data-source-kind="research"', catalog)
        self.assertIn('data-source-tier="A"', catalog)
        self.assertIn('data-source-year="1974"', catalog)
        self.assertIn('data-source-year=""', catalog)
        self.assertEqual(catalog.count('<a id="src-test-1974"></a>'), 1)
        self.assertEqual(catalog.count('<a id="src-test-undated"></a>'), 1)
        self.assertEqual(catalog.count("</article>"), 2)

    def test_hash_navigation_reveals_filtered_source(self) -> None:
        """Hash navigation without a click must not land on a hidden source."""
        import shutil
        import subprocess

        node = shutil.which("node")
        if not node:
            self.skipTest("Node is not installed")
        harness = r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const handlers = {};
const formHandlers = {};
const entry = {
  textContent: "Archive 1974",
  dataset: {sourceKind: "primary", sourceTier: "A", sourceYear: "1974"},
  hidden: false
};
const input = {value: "no-match"};
const kind = {value: ""}, tier = {value: ""}, period = {value: ""};
const count = {textContent: ""};
const form = {
  addEventListener(type, fn) {formHandlers[type] = fn;},
  dispatchEvent(event) {formHandlers[event.type](event);}
};
const fields = {
  form, "#mv-source-query": input, "#mv-source-type": kind,
  "#mv-source-tier": tier, "#mv-source-period": period,
  "#mv-source-count": count
};
const root = {
  dataset: {}, innerHTML: "",
  querySelector(selector) {return fields[selector];},
  closest() {return {addEventListener() {}};}
};
let scrollCalls = 0;
const target = {
  closest() {return entry;},
  scrollIntoView() {
    assert.equal(entry.hidden, false, "fragment scrolling must follow reveal");
    scrollCalls += 1;
  }
};
const document = {
  readyState: "complete",
  querySelectorAll() {return [entry];},
  getElementById(id) {
    if (id === "mv-source-browser") return root;
    if (id === "src-test-1974") return target;
    return null;
  }
};
const window = {
  location: {hash: ""},
  addEventListener(name, fn) {handlers[name] = fn;}
};
class Event {
  constructor(type) {this.type = type;}
  preventDefault() {}
}
vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"),
  {document, window, Event});
assert.equal(entry.hidden, true, "precondition: source filtered out");
window.location.hash = "#src-test-1974";
assert.equal(typeof handlers.hashchange, "function", "hashchange handler missing");
handlers.hashchange();
assert.equal(entry.hidden, false, "hash-linked source stays hidden");
assert.equal(input.value, "", "filter should clear for hidden permalink");
assert.equal(scrollCalls, 1, "hidden hash target was not scrolled into view");
handlers.hashchange();
assert.equal(scrollCalls, 1, "visible hash target should not trigger extra scrolling");
"""
        result = subprocess.run(
            [node, "-e", harness, str(DOCS / "assets/source-browser.js")],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_focus_graphs_only_include_immediate_relations(self) -> None:
        entities = [
            {"id": "ORG-A", "name": "A", "type": "organization", "countries": ["DE"]},
            {"id": "ORG-B", "name": "B", "type": "organization", "countries": ["DE"]},
            {"id": "ORG-C", "name": "C", "type": "organization", "countries": ["DE"]},
        ]
        relation = {
            "id": "REL-AB", "from": "ORG-A", "to": "ORG-B",
            "type": "cooperation", "label": "kooperiert",
            "evidence_level": "established", "sources": ["SRC-AB"],
        }
        other = {**relation, "id": "REL-BC", "from": "ORG-B", "to": "ORG-C"}
        focus = build_indexes.render_network_focus(
            [], entities, [relation, other], "ORG-A", "A"
        )
        self.assertIn("**1 quellengebundene Beziehungen**", focus)
        self.assertIn("flowchart LR", focus)
        self.assertIn("[REL-AB](network.md#rel-ab)", focus)
        self.assertIn("[SRC-AB](../quellen/index.md#src-ab)", focus)
        self.assertNotIn("REL-BC", focus)
        self.assertNotIn("N_ORG_C", focus)
        with self.assertRaises(ValueError):
            build_indexes.render_network_focus(
                [], entities, [relation], "ORG-C", "C"
            )
        self.assertEqual(len(build_indexes.FOCUS_NETWORKS), 10)
        finance = {slug: entity for _label, slug, entity in build_indexes.FOCUS_NETWORKS}
        self.assertEqual(finance["biz"], "ORG-INT-BIS")
        self.assertEqual(finance["ig-farben"], "ORG-DE-IG-FARBEN")
        self.assertEqual(finance["tradinvest"], "ORG-BS-TRADINVEST-ENI")
        self.assertEqual(finance["p2"], "ORG-IT-LOGGIA-P2-1970-1981")
        self.assertEqual(finance["rizzoli"], "ORG-IT-RIZZOLI-EDITORE-1975-1984")
        for slug in ("biz", "ig-farben", "tradinvest", "p2", "rizzoli"):
            self.assertTrue((DOCS / "generated" / f"network-focus-{slug}.md").is_file())

    def test_responsive_website_features_are_present(self) -> None:
        config = load_mkdocs_config()
        self.assertIn("assets/stylesheets/extra.css", config["extra_css"])
        self.assertIn("assets/source-browser.js", config["extra_javascript"])
        self.assertTrue((DOCS / "assets" / "source-browser.js").is_file())
        self.assertTrue((DOCS / "assets" / "stylesheets" / "extra.css").is_file())
        self.assertIn("navigation.sections", config["theme"]["features"])
        self.assertIn("search.suggest", config["theme"]["features"])
        home = (DOCS / "index.md").read_text(encoding="utf-8")
        self.assertIn("Themen entdecken", home)
        self.assertIn("Fallakten entdecken", home)
        self.assertIn("Quellenkatalog", home)


if __name__ == "__main__":
    unittest.main()