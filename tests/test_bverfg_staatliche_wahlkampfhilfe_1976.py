"""Regression for 1976 constitutional court ruling and two Bundestag source records."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/bverfg-staatliche-wahlkampfhilfe-1976.md"
SOURCE = ROOT / "data/sources.yml"
NAV = ROOT / "mkdocs.yml"
INDEX = ROOT / "docs/quellen/index.md"
IDS = {
    "SRC-DE-BVERFG-2BVE1-76-19770302",
    "SRC-DE-BT-PLENAR-06135-BPA-19710923",
    "SRC-DE-BT-PLENAR-08164-MOBIL-19790628",
}

class Bundeswahlkampfhilfe1976(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))["sources"]
        cls.doc = STUDY.read_text(encoding="utf-8")
        cls.nav = NAV.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")

    def test_three_unique_primary_sources_and_catalog_links(self):
        ids = [x["id"] for x in self.entries]
        self.assertEqual(len(ids), len(set(ids)))
        for sid in IDS:
            with self.subTest(sid=sid):
                self.assertEqual(ids.count(sid), 1)
                source = next(x for x in self.entries if x["id"] == sid)
                self.assertTrue(source["primary"])
                self.assertEqual(source["tier"], "A")
                self.assertEqual(source["accessed"], "2026-10-14")
                self.assertIn("index.md#" + sid.lower(), self.doc)
                self.assertEqual(self.index.count('<a id="' + sid.lower() + '"></a>'), 1)

    def test_judicial_finding_is_not_confused_with_cash_transfer(self):
        s = next(x for x in self.entries if x["id"] == "SRC-DE-BVERFG-2BVE1-76-19770302")
        self.assertEqual(s["date"], "1977-03-02")
        self.assertEqual(s["type"], "court_judgment")
        for phrase in ("10 Mio. DM", "22 Druckschriften", "sechs Millionen Exemplaren",
                       "59,5 %", "0,26 %", "kein Geldanteil",
                       "keine Parteikasseneinzahlung", "Art. 20", "Art. 38",
                       "keine DM-Schätzung"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.doc)

    def test_court_locator_covers_ruling_and_all_referenced_reasons(self):
        source = next(x for x in self.entries if x["id"] == "SRC-DE-BVERFG-2BVE1-76-19770302")
        self.assertEqual(source["locator"], "Entscheidungsformel; Tatbestand Rn. 2–9; Gründe Rn. 86–138 (Anzeigen), 139–167 (Druckschriften)")
        self.assertIn("Entscheidungsformel, Tatbestand Rn. 2–9, Gründe Rn. 86–138 (Anzeigen) und 139–167 (Druckschriften)", self.doc)
        self.assertIn("Fundstelle: Entscheidungsformel; Tatbestand Rn. 2–9; Gründe Rn. 86–138 (Anzeigen), 139–167 (Druckschriften)", self.index)

    def test_1971_1979_claim_boundaries(self):
        self.assertIn("06135.pdf#page=53", self.doc)
        self.assertIn("08164.pdf#page=76", self.doc)
        for phrase in ("Titel 531 03", "160.000 DM", "kein testierter Ist-Abfluss",
                       "Mobil-Werbung", "noch nicht belegt", "nicht im Original eingesehen"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.doc)

    def test_advertising_and_party_leaflet_routes_remain_separate(self):
        self.assertIn("1976 – Anzeigenweg", self.doc)
        self.assertIn("1976 – Druckschriftenweg", self.doc)
        self.assertIn("Regierungsparteien sind **nicht** als Zwischenhändler", self.doc)
        self.assertIn("Weiterverwendung durch Regierungsparteien als zusätzliches Wahlkampfmaterial", self.doc)
        self.assertNotIn("Anzeigen bzw. gedruckte Regierungsinformationen → Empfängerkreis", self.doc)

    def test_adjudicated_ad_period_excludes_later_family_law_ads(self):
        self.assertIn("Anzeigenwerbung Mai–Juli 1976", self.doc)
        self.assertNotIn("Anzeigenwerbung Mai–September 1976", self.doc)
        self.assertIn("Eherechts-Informationsanzeigen vom 4. August bis 10. September 1976", self.doc)
        self.assertIn("nicht ungeprüft zugerechnet", self.doc)
        self.assertIn("Rn. 88–138", self.doc)

    def test_adk_and_bverfg_sources_survive_main_convergence(self):
        # Both studies modify data/sources.yml, the generated index and MkDocs navigation.
        # Their independently registered evidence must survive a PR-base convergence.
        by_id = {item["id"]: item for item in self.entries}
        preserved_adk_ids = (
            "SRC-DE-BT-ADK-HAUSHALT-19680315",
            "SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968",
            "SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968",
            "SRC-DE-ACDP-JAHN-NACHLASS-01753",
            "SRC-DE-KAS-FONDS-SPR-2003",
        )
        all_ids = [item["id"] for item in self.entries]
        for source_id in (*preserved_adk_ids, *sorted(IDS)):
            with self.subTest(source_id=source_id):
                self.assertEqual(all_ids.count(source_id), 1)
                self.assertEqual(
                    self.index.count('<a id="' + source_id.lower() + '"></a>'),
                    1,
                )
        for source_id in preserved_adk_ids[-2:]:
            with self.subTest(secondary_source_id=source_id):
                self.assertFalse(by_id[source_id]["primary"])
                self.assertEqual(by_id[source_id]["tier"], "B")
        self.assertIn(
            "quellen/adk-bundesmittel-haushaltsverhandlungen-1967-1968.md",
            self.nav,
        )
        self.assertIn("quellen/bverfg-staatliche-wahlkampfhilfe-1976.md", self.nav)

    def test_navigation_to_new_research(self):
        self.assertIn("quellen/bverfg-staatliche-wahlkampfhilfe-1976.md", self.nav)
        self.assertIn("https://www.servat.unibe.ch/dfr/bv044125.html", self.doc)

if __name__ == "__main__":
    unittest.main()
