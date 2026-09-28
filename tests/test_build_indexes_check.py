from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import scripts.build_indexes as build_indexes


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class GeneratedIndexCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="machtverflechtungen-index-check-")
        self.root = Path(self.tempdir.name)
        shutil.copytree(SOURCE_ROOT / "data", self.root / "data")
        shutil.copytree(SOURCE_ROOT / "docs", self.root / "docs")
        shutil.copy2(SOURCE_ROOT / "METHODOLOGY.md", self.root / "METHODOLOGY.md")

        self.original_paths = (
            build_indexes.ROOT,
            build_indexes.DOCS,
            build_indexes.CASES,
            build_indexes.DATA,
        )
        build_indexes.ROOT = self.root
        build_indexes.DOCS = self.root / "docs"
        build_indexes.CASES = build_indexes.DOCS / "faelle"
        build_indexes.DATA = self.root / "data"

    def tearDown(self) -> None:
        (
            build_indexes.ROOT,
            build_indexes.DOCS,
            build_indexes.CASES,
            build_indexes.DATA,
        ) = self.original_paths
        self.tempdir.cleanup()

    def _run_check(self) -> tuple[int, str]:
        output = io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["build_indexes.py", "--check"]),
            contextlib.redirect_stdout(output),
        ):
            code = build_indexes.main()
        return code, output.getvalue()

    def test_records_include_nested_directory_index_case(self) -> None:
        case_dir = self.root / "docs" / "faelle" / "directory-index-case"
        case_dir.mkdir(parents=True)
        (case_dir / "index.md").write_text(
            "---\n"
            "id: CASE-TEST-DIRECTORY-INDEX\n"
            "type: case\n"
            "title: Directory Index Case\n"
            "period:\n"
            "  start: '2098'\n"
            "evidence_level: speculative\n"
            "---\n",
            encoding="utf-8",
        )

        matched = [
            (meta["id"], path)
            for meta, path in build_indexes.records()
            if meta.get("id") == "CASE-TEST-DIRECTORY-INDEX"
        ]

        self.assertEqual(
            [("CASE-TEST-DIRECTORY-INDEX", "faelle/directory-index-case/index.md")],
            matched,
        )

    def test_records_sorts_same_year_by_complete_start_date(self) -> None:
        cases_dir = self.root / "docs" / "faelle" / "sort-test"
        cases_dir.mkdir(parents=True, exist_ok=True)
        (cases_dir / "december.md").write_text(
            "---\n"
            "id: CASE-TEST-DECEMBER\n"
            "type: case\n"
            "title: Alpha December\n"
            "period:\n"
            "  start: '2099-12-01'\n"
            "---\n",
            encoding="utf-8",
        )
        (cases_dir / "january.md").write_text(
            "---\n"
            "id: CASE-TEST-JANUARY\n"
            "type: case\n"
            "title: Zeta January\n"
            "period:\n"
            "  start: '2099-01-15'\n"
            "---\n",
            encoding="utf-8",
        )

        ordered = [
            meta["id"]
            for meta, _path in build_indexes.records()
            if meta.get("id") in {"CASE-TEST-DECEMBER", "CASE-TEST-JANUARY"}
        ]

        self.assertEqual(["CASE-TEST-JANUARY", "CASE-TEST-DECEMBER"], ordered)

    def test_render_sources_uses_unknown_for_null_date(self) -> None:
        rendered = build_indexes.render_sources(
            [
                {
                    "id": "SRC-TEST-NULL-DATE",
                    "title": "Quelle ohne bekanntes Datum",
                    "institution": "Testinstitut",
                    "date": None,
                    "primary": False,
                    "tier": "C",
                    "url": "https://example.invalid/null-date",
                }
            ]
        )

        self.assertIn("Testinstitut · unbekannt · Stufe **C**", rendered)
        self.assertNotIn(" · None · ", rendered)

    def test_check_accepts_current_generated_pages(self) -> None:
        code, output = self._run_check()
        self.assertEqual(0, code, output)
        self.assertIn("INDEX CHECK OK", output)

    def test_check_rejects_missing_generated_page_without_recreating_it(self) -> None:
        missing = self.root / "docs" / "generated" / "timeline.md"
        missing.unlink()

        code, output = self._run_check()

        self.assertEqual(1, code)
        self.assertIn("docs/generated/timeline.md", output)
        self.assertFalse(missing.exists())


    def test_check_rejects_stale_generated_page_without_overwriting_it(self) -> None:
        stale = self.root / "docs" / "generated" / "timeline.md"
        stale_content = stale.read_text(encoding="utf-8") + "STALE SENTINEL\n"
        stale.write_text(stale_content, encoding="utf-8")

        code, output = self._run_check()

        self.assertEqual(1, code)
        self.assertIn("docs/generated/timeline.md", output)
        self.assertEqual(stale_content, stale.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
