"""Regression checks for two original Bundestag answers on the BKA Sicherungsgruppe."""

from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "data/sources.yml"
CATALOG = ROOT / "docs/quellen/index.md"
STUDY = ROOT / "docs/quellen/raf-westdeutsche-staatsakten-1975-1992.md"

ORIGINALS = {
    "SRC-DE-BT-KHK-S-19910627": {
        "date": "1991-06-27",
        "url": "https://dserver.bundestag.de/btd/12/008/1200868.pdf",
        "locator_fragments": ("12.02.", "18.05.1971", "08.04.1991"),
    },
    "SRC-DE-BT-MFS-KONTAKTE-19930721": {
        "date": "1993-07-21",
        "url": "https://dserver.bundestag.de/btd/12/054/1205479.pdf",
        "locator_fragments": ("Walter Sch.", "12/868", "S. 3"),
    },
}


class BkaSicherungsgruppeParliamentaryOriginals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = yaml.safe_load(SOURCE_FILE.read_text(encoding="utf-8"))["sources"]
        cls.catalog = CATALOG.read_text(encoding="utf-8")
        cls.study = STUDY.read_text(encoding="utf-8")

    def test_two_unique_primary_sources_with_stable_identifiers(self):
        ids = [source["id"] for source in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for source_id, expected in ORIGINALS.items():
            with self.subTest(source_id=source_id):
                self.assertEqual(ids.count(source_id), 1)
                source = next(s for s in self.sources if s["id"] == source_id)
                self.assertEqual(source["date"], expected["date"])
                self.assertEqual(source["url"], expected["url"])
                self.assertEqual(source["type"], "parliamentary_response")
                self.assertTrue(source["primary"])
                self.assertEqual(source["tier"], "A")
                self.assertEqual(source["accessed"], "2026-10-13")
                for fragment in expected["locator_fragments"]:
                    self.assertIn(fragment, source["locator"])

    def test_catalog_includes_both_originals_exactly_once(self):
        for source_id, expected in ORIGINALS.items():
            with self.subTest(source_id=source_id):
                self.assertEqual(self.catalog.count('<a id="' + source_id.lower() + '"></a>'), 1)
                self.assertEqual(self.catalog.count("[PDF öffnen](" + expected["url"] + ")"), 1)

    def test_study_distinguishes_questions_from_confirmed_government_answers(self):
        self.assertIn("## F. BKA-Sicherungsgruppe 1971", self.study)
        for source_id, marker in (
            ("SRC-DE-BT-KHK-S-19910627", "Q11"),
            ("SRC-DE-BT-MFS-KONTAKTE-19930721", "Q12"),
        ):
            self.assertIn(marker + " / " + source_id, self.study)
        self.assertIn("12. Februar bis 18. Mai 1971", self.study)
        self.assertIn("nicht ausdrücklich eine persönliche Beteiligung", self.study)
        self.assertIn("parlamentarischen Fragetext", self.study)
        self.assertIn("500–700 DM monatlich", self.study)
        self.assertIn("kein in der Drucksache bestätigter Zahlungsvorgang", self.study)
        self.assertIn("noch nicht im Original eingesehene BKA-Akten", self.study)
        self.assertIn("Werner Freund", self.study)
        self.assertIn("Die zwölf hier ausgewerteten Originalquellen", self.study)

    def test_archival_leads_stay_separate_from_verified_federal_records(self):
        for shelf in ("B 362/6202", "B 362/6234", "B 362/6224", "B 362/6222"):
            self.assertIn(shelf, self.study)
        self.assertIn("https://open.ifz-muenchen.de/bitstreams/", self.study)
        self.assertIn("eigenständige Sachverhalte", self.study)


if __name__ == "__main__":
    unittest.main()
