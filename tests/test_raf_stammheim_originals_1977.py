"""Prüfungen der Originalanlagen 1977: Fundstellen, Provenienz, Behauptung vs. Befund."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/raf-aktenanlage-aussagegenehmigung-1977.md"
SOURCES = ROOT / "data/sources.yml"
INDEX = ROOT / "docs/quellen/index.md"
NAV = ROOT / "mkdocs.yml"

ORIGINALS = {
    "SRC-DE-STAMMHEIM-SCHILY-HEROLD-19770114": (
        "1977-01-14", "13272–13273", "Anl.-5-20.1.1977-S.-13272-13273"),
    "SRC-DE-STAMMHEIM-HEROLD-SCHREIBEN-19770211": (
        "1977-02-11", "13425", "Anl.-1-17.2.1977-S.-13425"),
    "SRC-DE-STAMMHEIM-BUBACK-VERFUEGUNG-19770215": (
        "1977-02-15", "13428", "Anl.-2-17.2.1977-S.-13428-13429"),
    "SRC-DE-BMI-HEROLD-AUSSAGEGENEHMIGUNG-19770303": (
        "1977-03-03", "13619–13620", "Anl.-3-15.3.1977-S.-13619-13620"),
    "SRC-DE-STAMMHEIM-HEROLD-184-19770315": (
        "1977-03-15", "13664–13667", "/184-verhandlungstag/"),
}


class RafStammheim1977Originals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))["sources"]
        cls.study = STUDY.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")
        cls.navigation = NAV.read_text(encoding="utf-8")

    def test_originals_have_unique_tier_a_ids_dates_and_exact_anchors(self):
        ids = [s["id"] for s in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for source_id, (date, locator, url_fragment) in ORIGINALS.items():
            with self.subTest(source_id=source_id):
                self.assertEqual(ids.count(source_id), 1)
                source = next(s for s in self.sources if s["id"] == source_id)
                self.assertEqual(source["date"], date)
                self.assertEqual(source["tier"], "A")
                self.assertTrue(source["primary"])
                self.assertEqual(source["accessed"], "2026-10-14")
                self.assertIn(locator, source["locator"])
                self.assertIn(url_fragment, source["url"])
                self.assertIn(source_id, self.study)

    def test_facsimiles_stay_separate_from_transcript_edition(self):
        for source in self.sources:
            if source["id"] in ORIGINALS:
                kind = ("trial_transcript_edition" if source["id"] ==
                        "SRC-DE-STAMMHEIM-HEROLD-184-19770315"
                        else "trial_attachment_facsimile")
                self.assertEqual(source["type"], kind)
        self.assertIn("Prozessanlagen", self.study)
        self.assertIn("wissenschaftlich bereitgestellten Prozessedition", self.study)

    def test_claimed_media_contract_is_not_pretended_documented_payment(self):
        self.assertIn("Beweisbehauptung der Verteidigung", self.study)
        self.assertIn("Eduard Zimmermann", self.study)
        self.assertIn("kein eigenständiger Vertrags- oder Zahlungsnachweis", self.study)
        self.assertIn("Vertrags- und Zahlungsbefund", self.study)

    def test_buback_registration_and_bmi_limits_have_exact_document_locators(self):
        for fragment in ("3 ARP 74/75 I", "1 BJs 7/76",
                         "26. März 1976", "Dr. W. Krüger",
                         "mündliche Anordnung", "kein Vermerk",
                         "Z I 2 – 001 210 – 010/5", "§ 96 StPO",
                         "acht Themen", "Dr. Fröhlich", "S. 13620"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.study)
        self.assertIn("vom Bundesminister der Justiz", self.study)

    def test_generated_catalog_and_navigation_list_all_five_originals(self):
        self.assertIn(
            "quellen/raf-aktenanlage-aussagegenehmigung-1977.md",
            self.navigation)
        for source_id in ORIGINALS:
            with self.subTest(source_id=source_id):
                self.assertEqual(
                    self.index.count('<a id="' + source_id.lower() + '"></a>'),
                    1)


if __name__ == "__main__":
    unittest.main()
