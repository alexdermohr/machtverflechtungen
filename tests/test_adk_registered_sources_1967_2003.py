"""Source registry and site-index consistency for ADK federal funding and budget negotiations 1966–2003."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/adk-bundesmittel-haushaltsverhandlungen-1967-1968.md"
INDEX = ROOT / "docs/quellen/index.md"
SOURCES_PATH = ROOT / "data/sources.yml"

ORIGINAL_IDS = (
    "SRC-DE-KGPARL-CDU-ADK-19670606",
    "SRC-DE-KGPARL-SPD-ADK-19670606",
    "SRC-DE-BT-ADK-PLENUM-19670607",
    "SRC-DE-KGPARL-CDU-ADK-19671205",
    "SRC-DE-KGPARL-CDU-ADK-19671212",
    "SRC-DE-BT-ADK-HAUSHALT-19680315",
    "SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968",
    "SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968",
    "SRC-DE-KGPARL-CDU-ADK-19680326",
    "SRC-DE-KGPARL-CDU-ADK-19680402",
    "SRC-DE-BVERFG-PARTEIENFINANZIERUNG-19660719",
)
FINDING_AID_ID = "SRC-DE-ACDP-JAHN-NACHLASS-01753"
FONDS_SELF_REPORT_ID = "SRC-DE-KAS-FONDS-SPR-2003"
SECONDARY_ID = "SRC-DE-ADENAUERHAUS-ADK-SPR-NACHFOLGE"
ALL_IDS = (*ORIGINAL_IDS, FINDING_AID_ID, FONDS_SELF_REPORT_ID, SECONDARY_ID)


class AdkRegisteredSourcesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = yaml.safe_load(SOURCES_PATH.read_text(encoding="utf-8"))["sources"]
        cls.study = STUDY.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")

    def test_existing_1950s_sources_preserved(self):
        for source_id in (
            "SRC-DE-BARCH-B145-810-ADK-1954-1956",
            "SRC-DE-BARCH-B136-1679-PARIS-1955-1956",
            "SRC-DE-BT-PLENAR-02225-EPL04-T309-19570706",
        ):
            with self.subTest(source_id=source_id):
                self.assertEqual(sum(s["id"] == source_id for s in self.sources), 1)

    def test_all_fourteen_sources_are_unique_and_catalogued(self):
        ids = [s["id"] for s in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for source_id in ALL_IDS:
            with self.subTest(source_id=source_id):
                self.assertEqual(ids.count(source_id), 1)
                self.assertIn(source_id, self.index)
        self.assertIn(f"{len(ids)} registrierte Quellen", self.index)

    def test_primary_vs_institutional_history_separated(self):
        by_id = {s["id"]: s for s in self.sources}
        for source_id in ORIGINAL_IDS:
            with self.subTest(source_id=source_id):
                s = by_id[source_id]
                self.assertTrue(s["primary"])
                self.assertEqual(s["tier"], "A")
        self.assertFalse(by_id[FINDING_AID_ID]["primary"])
        self.assertEqual(by_id[FINDING_AID_ID]["tier"], "B")
        self.assertIn("Konrad-Adenauer-Stiftung", by_id[FINDING_AID_ID]["institution"])
        self.assertIn("DDB als Nachweisportal", by_id[FINDING_AID_ID]["institution"])
        self.assertNotIn("Amtlicher Katalog", by_id[FINDING_AID_ID]["notes"])
        self.assertFalse(by_id[FONDS_SELF_REPORT_ID]["primary"])
        self.assertEqual(by_id[FONDS_SELF_REPORT_ID]["tier"], "B")
        self.assertIn("Retrospektive", by_id[FONDS_SELF_REPORT_ID]["notes"])
        self.assertIn("keine zeitgenössische Liquidationsurkunde", by_id[FONDS_SELF_REPORT_ID]["notes"])
        self.assertIn("keine voneinander unabhängigen Bestätigungen", self.study)
        self.assertEqual(by_id[SECONDARY_ID]["tier"], "B")
        self.assertFalse(by_id[SECONDARY_ID]["primary"])
        self.assertEqual(by_id[SECONDARY_ID]["type"], "research_overview")
        self.assertIn("konrad-adenauer.de/seite/arbeitsgemeinschaft-demokratischer-kreise/", by_id[SECONDARY_ID]["url"])
        self.assertIn("kas.de/de/unterstuetzen-sie-uns", by_id["SRC-DE-KAS-FONDS-SPR-2003"]["url"])
        self.assertEqual(by_id["SRC-DE-ACDP-JAHN-NACHLASS-01753"]["type"], "archival_finding_aid")
        self.assertEqual(by_id["SRC-DE-KAS-FONDS-SPR-2003"]["type"], "institution_self_report")
        self.assertIn("kein nachweis", by_id["SRC-DE-KAS-FONDS-SPR-2003"]["notes"].lower())

    def test_exact_annual_budget_and_institution_link(self):
        original = next(s for s in self.sources if s["id"] == "SRC-DE-BT-ADK-HAUSHALT-19680315")
        self.assertIn("0502704.pdf#page=4", original["url"])
        self.assertIn("weder adk-empfängerbetrag noch belegte direkte zweckumbuchung", original["notes"].lower())
        self.assertIn("Titel 300", original["locator"])
        self.assertIn("Titel 314", original["locator"])
        self.assertIn("KAS-FONDS-SPR-2003", self.index.upper())
        self.assertIn("2003 noch öffentliche ADK- oder BPA-Mittel", self.study)

    def test_new_committee_report_distinct_from_budget_table(self):
        by_id = {source["id"]: source for source in self.sources}
        report = by_id["SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968"]
        self.assertEqual(report["institution"], "Deutscher Bundestag / Haushaltsausschuss")
        self.assertEqual(report["type"], "parliamentary_budget_committee_report")
        self.assertTrue(report["primary"])
        self.assertEqual(report["tier"], "A")
        self.assertEqual(report["date"], "1968-03-27")
        self.assertIn("27.03.1968", report["locator"])
        self.assertIn("0502731zu.pdf#page=6", report["url"])
        self.assertIn("Gedruckte Seite 6", report["locator"])
        for text in ("Titel 300", "Titel 314", "kein Nachweis", "nicht gesichert", "V/2704"):
            self.assertIn(text, report["notes"])
        self.assertIn("SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968", self.study)
        self.assertNotEqual(report["url"], by_id["SRC-DE-BT-ADK-HAUSHALT-19680315"]["url"])
        oral_report = by_id["SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968"]
        self.assertEqual(oral_report["date"], "1968-03-15")
        self.assertEqual(oral_report["tier"], "A")
        self.assertTrue(oral_report["primary"])
        self.assertIn("0502731.pdf#page=1", oral_report["url"])
        self.assertIn("keine Einzelzahlung", oral_report["notes"])
        self.assertIn("SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968", self.study)
        self.assertNotEqual(oral_report["url"], report["url"])
        self.assertNotEqual(oral_report["url"], by_id["SRC-DE-BT-ADK-HAUSHALT-19680315"]["url"])
        self.assertEqual(len({by_id["SRC-DE-BT-ADK-HAUSHALT-19680315"]["url"], oral_report["url"], report["url"]}), 3)
        self.assertIn("Zehn zeitgenössische", self.study)
        self.assertIn("Vier historische Bundestagsoriginaldrucke", self.study)
        self.assertNotIn("Personalkontinuität", by_id["SRC-DE-KGPARL-CDU-ADK-19680326"]["title"])
        self.assertNotIn("Ausschussvermerk", by_id["SRC-DE-KGPARL-CDU-ADK-19680402"]["title"])

    def test_site_navigation_links_both_periods(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("quellen/adk-bundesfinanzierung-1954-1957.md", nav)
        self.assertIn("quellen/adk-bundesmittel-haushaltsverhandlungen-1967-1968.md", nav)
        self.assertIn("ADK / Bundesmittel, Wahlkampfhilfe und Haushaltsverhandlungen 1967–1968", nav)


if __name__ == "__main__":
    unittest.main()
