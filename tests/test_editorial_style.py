"""Protect concise presentation without weakening the structured evidence model."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REDUNDANT_BOUNDARY_BULLET = re.compile(
    r"(?m)^-\s+\*\*(?:Aussagegrenze|Grenze):\*\*"
)
REDUNDANT_NEGATIVE_SYNTHESIS = re.compile(r"(?m)^## Was folgt nicht\?\s*$")
REDUNDANT_BOUNDARY_HEADING = re.compile(r"(?m)^## Aussagegrenzen(?: und Gegenhypothesen)?\s*$")


def split_frontmatter(markdown: str) -> tuple[str, str]:
    if markdown.startswith("---\n"):
        _opening, sep, tail = markdown.partition("---\n")
        frontmatter, sep, body = tail.partition("\n---\n")
        if sep:
            return frontmatter, body
    return "", markdown


class EditorialStyleTest(unittest.TestCase):
    def test_case_prose_avoids_repeated_negative_templates(self) -> None:
        files = sorted((DOCS / "faelle").rglob("*.md"))
        self.assertTrue(files)
        for path in files:
            _, prose = split_frontmatter(path.read_text(encoding="utf-8"))
            with self.subTest(case=str(path.relative_to(ROOT))):
                self.assertIsNone(REDUNDANT_BOUNDARY_BULLET.search(prose))
                self.assertIsNone(REDUNDANT_NEGATIVE_SYNTHESIS.search(prose))
                self.assertIsNone(REDUNDANT_BOUNDARY_HEADING.search(prose))

    def test_structured_counterevidence_remains_required(self) -> None:
        files = sorted((DOCS / "faelle").rglob("*.md"))
        cases = 0
        for path in files:
            frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            if not frontmatter:
                continue
            meta = yaml.safe_load(frontmatter) or {}
            if meta.get("type") != "case":
                continue
            cases += 1
            for claim in meta.get("claims", []):
                with self.subTest(claim=claim.get("id")):
                    self.assertIn("counterevidence", claim)
                    self.assertIn("alternatives", claim)
                    self.assertIn("missing_evidence", claim)
                    self.assertIn("falsification", claim)
                    self.assertIn("does_not_support", claim.get("scope", {}))
            self.assertIn("what_does_not_follow", meta)
        self.assertGreater(cases, 0)

    def test_published_methodology_mirrors_canonical_version(self) -> None:
        self.assertEqual(
            (ROOT / "METHODOLOGY.md").read_text(encoding="utf-8"),
            (DOCS / "methodik.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
