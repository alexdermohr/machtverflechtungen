"""Regression: Federal ADK aid-finding aids and Bundestag 1957 original budget record."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/adk-bundesfinanzierung-1954-1957.md"
SOURCE = ROOT / "data/sources.yml"
NAV = ROOT / "mkdocs.yml"
INDEX = ROOT / "docs/quellen/index.md"
IDS = {
    "SRC-DE-BARCH-B145-810-ADK-1954-1956",
    "SRC-DE-BARCH-B136-1679-PARIS-1955-1956",
    "SRC-DE-BT-PLENAR-02225-EPL04-T309-19570706",
}

class ADKBundesfinanzierung1957(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))["sources"]
        cls.study = STUDY.read_text(encoding="utf-8")
        cls.nav = NAV.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")

    def test_three_unique_primary_source_ids(self):
        all_ids = [r["id"] for r in self.sources]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        for sid in IDS:
            with self.subTest(sid=sid):
                self.assertEqual(all_ids.count(sid), 1)
                r = next(r for r in self.sources if r["id"] == sid)
                self.assertEqual(r["tier"], "A")
                self.assertTrue(r["primary"])
                self.assertEqual(r["accessed"], "2026-10-14")

    def test_archival_provenance_not_misrepresented_as_payment(self):
        for sid in ("SRC-DE-BARCH-B145-810-ADK-1954-1956","SRC-DE-BARCH-B136-1679-PARIS-1955-1956"):
            r=next(r for r in self.sources if r["id"]==sid)
            self.assertEqual(r["type"],"archival_finding_aid")
            self.assertIn("nicht eingesehen",r["notes"])
        self.assertIn("ADK steht **nicht** im Titel",self.study)
        self.assertIn("noch nicht eingesehen",self.study)

    def test_title_309_total_is_not_adk_payment_or_title_300(self):
        r=next(r for r in self.sources if r["id"]=="SRC-DE-BT-PLENAR-02225-EPL04-T309-19570706")
        self.assertEqual(r["date"],"1957-07-06")
        self.assertIn("02225.pdf#page=22",r["url"])
        for word in ("Titel 309","Titel 300","7.349.300 DM","Gesamtansatz","sechsten Nachtragshaushalt 1956","Bad Godesberg"):
            with self.subTest(word=word): self.assertIn(word,self.study)
        self.assertIn("keine individuelle ADK-Zahlung",self.study)

    def test_navigation_and_catalog_generated(self):
        self.assertIn("quellen/adk-bundesfinanzierung-1954-1957.md",self.nav)
        for sid in IDS:
            self.assertIn("index.md#"+sid.lower(),self.study)
            self.assertEqual(self.index.count('<a id="'+sid.lower()+'"></a>'),1)
        for sign in ("1RP 12/1","1RP 233/3","1RP 1896/3"):
            self.assertIn(sign,self.study)
        self.assertEqual([r["id"] for r in self.sources].count("SRC-FR-MAE-1RP-FINDBUCH-2023"),1)

if __name__ == "__main__":
    unittest.main()
