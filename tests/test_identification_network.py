from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
def records(name):
    return {r["id"]: r for r in yaml.safe_load((ROOT / "data" / f"{name}.yml").read_text())[name]}

class IdentificationNetwork(unittest.TestCase):
    def test_contractors_are_distinct_and_no_inferred_dates(self):
        r = records("relations")
        for i in ("001", "002"):
            edge = r["REL-CO-IDNET-" + i]
            self.assertEqual(edge["from"], "ORG-CO-IDEMIA-900060799")
            self.assertEqual(edge["to"], "ORG-IDNET-TGS")
            self.assertNotIn("period", edge)
        self.assertEqual(r["REL-CO-IDNET-004"]["from"], "ORG-IDNET-SAS")
        for edge in r.values():
            if edge["id"].startswith("REL-CO-IDNET-") and edge["type"] == "reported_consortium_participation":
                self.assertNotIn("period", edge)
                self.assertIn("Eintrittsdatum offen", edge["label"])

    def test_acquisition_and_disciplinary_dates(self):
        r = records("relations")
        self.assertEqual(r["REL-CO-IDNET-005"]["period"]["start"], "2011-04-27")
        self.assertEqual(r["REL-MAUSS-PMT-028"]["period"]["start"], "2026-03-16")
        self.assertIn("SRC-IDNET-FALLO", r["REL-MAUSS-PMT-028"]["sources"])
        self.assertIn("erstinstanzlich", r["REL-MAUSS-PMT-028"]["label"])

    def test_preliminary_inquiry_and_contract_scope(self):
        r = records("relations")
        inquiry = r["REL-CO-IDNET-024"]
        self.assertEqual(inquiry["type"], "documented_preliminary_inquiry_subject")
        self.assertNotIn("period", inquiry)
        self.assertIn("Kein förmliches Verfahren gegen TGS", inquiry["label"])
        self.assertIn("SRC-IDNET-FALLO-COPY", inquiry["sources"])
        for i, contract, year in (("026", "052/2017", "2017"), ("027", "038/2019", "2019")):
            edge = r["REL-CO-IDNET-" + i]
            self.assertEqual(edge["from"], "ORG-CO-RNEC")
            self.assertIn(contract, edge["label"])
            self.assertEqual(edge["period"]["start"], year)
            self.assertIn("SRC-IDNET-RNEC-SECTOR-2026", edge["sources"])
