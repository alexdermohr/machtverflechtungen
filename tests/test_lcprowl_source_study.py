"""Regressionen für die LCPROWL-OPC-Aktenstudie (August 1950)."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / "docs/quellen/lcprowl-1950-opc-planung.md"
NAVIGATION = ROOT / "mkdocs.yml"


class LCPROWLDocumentStudyTests(unittest.TestCase):
    def test_original_document_and_official_archival_fallback(self):
        document = DOCUMENT.read_text(encoding="utf-8")
        self.assertIn("LCPROWL VOL. 1_0042", document)
        self.assertIn("readingroom/docs/LCPROWL%20%20%20%20VOL.%201_0042.pdf", document)
        self.assertIn("www.archives.gov/iwg/declassified-records/rg-263-cia-records/", document)
        self.assertIn("Box 0042", document)
        self.assertIn("Bildseite 1", document)
        self.assertIn("Bildseite 2", document)
        self.assertIn("HHStAW, 502, 17886", document)

    def test_approval_request_and_operational_execution_stay_distinct(self):
        document = DOCUMENT.read_text(encoding="utf-8")
        self.assertIn("9. August 1950 grundsätzlich", document)
        self.assertIn("nur Phase 1", document)
        self.assertIn("Antrag an die OPC-Projektleitung", document)
        self.assertIn("29. August 1950", document)
        self.assertIn("EE-3", document)
        self.assertIn("Tarn- und Täuschungsmaßnahmen", document)
        self.assertNotIn("Phase 4 wurde am 9. August sofort umgesetzt", document)
        self.assertNotIn("7.000 ausgebildete Angehörige", document)

    def test_study_link_is_in_existing_sources_section(self):
        nav = NAVIGATION.read_text(encoding="utf-8")
        entry = "quellen/lcprowl-1950-opc-planung.md"
        self.assertEqual(nav.count(entry), 1)
        self.assertIn("  - Quellen & Akten:", nav)
        self.assertIn("LCPROWL / OPC-Akten August 1950", nav)


if __name__ == "__main__":
    unittest.main()
