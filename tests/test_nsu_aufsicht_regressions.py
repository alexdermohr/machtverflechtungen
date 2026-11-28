"""Preserve the distinction between oversight restrictions, remedies and reforms."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = "nsu-bfv-datenschutzkontrolle-quellenschutz-1997-2026.md"


class NsuAufsichtTests(unittest.TestCase):
    def setUp(self):
        rows = yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]
        self.rows = {r["id"]: r for r in rows}
        self.registry = yaml.safe_load(
            (ROOT / "data/research-integrations.yml").read_text()
        )["studies"][STUDY]

    def test_control_failure_and_improvement_remain_distinct(self):
        for suffix, kind, phrase in (
            ("KONTROLLABBRUCH", "reported_aborted_oversight_inspection", "Datei nicht bezeichnet"),
            ("KONTROLLVERBESSERUNG", "reported_improved_oversight_access", "zwei Folgekontrollen"),
        ):
            rid = f"REL-DE-BFV-BFD-{suffix}-2001-001"
            row = self.rows[rid]
            self.assertEqual(row["type"], kind)
            self.assertEqual((row["from"], row["to"]), ("ORG-DE-BFV", "ORG-DE-BFD"))
            self.assertEqual(row["sources"], ["SRC-DE-BFD-TB18-20010313"])
            self.assertEqual(str(row["period"]["start"]), "2001-03-13")
            self.assertIn(phrase, row["label"])
            self.assertIn(rid, self.registry["relation_ids"])

    def test_dispute_and_reform_are_not_proof_of_implementation(self):
        foreign = self.rows["REL-DE-BFV-BFDI-AND-2011-001"]
        self.assertIn("technischer Kompromiss noch offen", foreign["label"])
        self.assertEqual(foreign["to"], "ORG-DE-BFD")
        criticism = self.rows["REL-DE-BFDI-UKRAT-REFORMKRITIK-2026-001"]
        vote = self.rows["REL-DE-BFDI-UKRAT-BESCHLUSS-2026-001"]
        self.assertEqual(str(criticism["period"]["start"]), "2026-05-06")
        self.assertEqual(str(vote["period"]["start"]), "2026-11-13")
        self.assertIn("nicht an produktivem Vollzug", criticism["label"])
        self.assertIn("Verkündung, Inkrafttreten und tatsächliche Umsetzung nicht verifiziert", vote["label"])
        self.assertEqual(vote["sources"], [
            "SRC-DE-BT-NDREFORM-219161-20261111",
            "SRC-DE-BT-NDREFORM-BESCHLUSS-20261113",
        ])
        self.assertEqual(self.registry["status"], "network")
        self.assertEqual(len(set(self.registry["relation_ids"])), 8)


if __name__ == "__main__":
    unittest.main()
