"""Regression: Hamburger Senatsantwort 22/10312 nicht überinterpretieren."""
import hashlib
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "SRC-DE-HH-NSU-AKTEN-2210312"
STUDY = "nsu-hamburg-aktenmoratorium-2012-2022.md"
RELATIONS = {
    "REL-DE-NSU-HH-BIS-LFV-MORATORIUM-2017-001",
    "REL-DE-NSU-HH-LFV-AKTEN-2017-001",
    "REL-DE-NSU-HH-BIS-POL-MORATORIUM-2017-001",
    "REL-DE-NSU-HH-POL-AKTEN-2017-001",
    "REL-DE-NSU-HH-STA-GBA-AKTEN-001",
}

class HamburgRecordsTest(unittest.TestCase):
    def test_source_links_and_limits(self):
        rels = {r["id"]: r for r in yaml.safe_load(
            (ROOT / "data/relations.yml").read_text())["relations"]}
        self.assertTrue(RELATIONS <= rels.keys())
        for rid in RELATIONS:
            self.assertIn(SOURCE, rels[rid]["sources"])
        self.assertEqual(rels["REL-DE-NSU-HH-BIS-POL-MORATORIUM-2017-001"]["period"]["start"], "2017-12-07")
        self.assertNotIn("period", rels["REL-DE-NSU-HH-BIS-LFV-MORATORIUM-2017-001"])
        self.assertNotIn("period", rels["REL-DE-NSU-HH-LFV-AKTEN-2017-001"])
        self.assertNotIn("period", rels["REL-DE-NSU-HH-POL-AKTEN-2017-001"])
        self.assertNotIn("period", rels["REL-DE-NSU-HH-STA-GBA-AKTEN-001"])
        self.assertEqual(rels["REL-DE-NSU-HH-STA-GBA-AKTEN-001"]["to"], "ORG-DE-GBA")
        self.assertNotIn("period", rels["REL-DE-NSU-HH-GBA-2026-001"])
        self.assertIn("nicht zuvor", rels["REL-DE-NSU-HH-LFV-AKTEN-2017-001"]["label"])
        self.assertIn("Übermittlung offen", rels["REL-DE-NSU-HH-POL-AKTEN-2017-001"]["label"])

    def test_study_exact_integration(self):
        reg = yaml.safe_load((ROOT / "data/research-integrations.yml").read_text())
        entry = reg["studies"][STUDY]
        self.assertEqual(set(entry["relation_ids"]), RELATIONS | {"REL-DE-NSU-HH-GBA-2026-001"})
        self.assertEqual(entry["sha256"], hashlib.sha256((ROOT / "research" / STUDY).read_bytes()).hexdigest())

if __name__ == "__main__":
    unittest.main()
