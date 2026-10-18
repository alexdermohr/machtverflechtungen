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

    def test_responsive_website_features_are_present(self) -> None:
        config = load_mkdocs_config()
        self.assertIn("assets/stylesheets/extra.css", config["extra_css"])
        self.assertTrue((DOCS / "assets" / "stylesheets" / "extra.css").is_file())
        self.assertIn("navigation.sections", config["theme"]["features"])
        self.assertIn("search.suggest", config["theme"]["features"])
        home = (DOCS / "index.md").read_text(encoding="utf-8")
        self.assertIn("Themen entdecken", home)
        self.assertIn("Fallakten entdecken", home)
        self.assertIn("Quellenkatalog", home)


if __name__ == "__main__":
    unittest.main()