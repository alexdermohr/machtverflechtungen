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

    def test_earlier_sources_and_limits(self):
        rels = {r["id"]: r for r in yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]}
        original = rels["REL-DE-NSU-HH-BIS-LFV-MORATORIUM-2017-001"]
        self.assertIn("SRC-DE-HH-NSU-2014-2011661", original["sources"])
        self.assertIn("Verhältnis der Anordnungen offen", original["label"])
        self.assertIn("Zustimmung nicht dokumentiert", rels["REL-DE-NSU-HH-SENAT-PKA-2017-001"]["label"])
        self.assertNotIn("period", rels["REL-DE-NSU-HH-LFV-FORSCHUNG-BESTAND-2025-001"])
        self.assertIn("Zugang nicht belegt", rels["REL-DE-NSU-HH-LFV-FORSCHUNG-BESTAND-2025-001"]["label"])

    def test_selection_not_destruction_or_completed_transfer(self):
        rels = {r["id"]: r for r in yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]}
        sel = rels["REL-DE-NSU-HH-LFV-AUSWAHL-2025-001"]
        self.assertIn("im ausgewählten Bestand", sel["label"])
        self.assertEqual(sel["to"], "DOC-DE-NSU-HH-LFV-AUSWAHL-2025")
        self.assertIn("Vollzug nicht belegt", rels["REL-DE-NSU-HH-POL-ARCHIV-2025-001"]["label"])
        self.assertIn("noch ausstehend", rels["REL-DE-NSU-HH-POL-GBA-FREIGABE-2023-001"]["label"])
        self.assertIn("Anfang 2012", rels["REL-DE-NSU-HH-STA-GBA-AKTEN-001"]["label"])
        self.assertIn("kein Beweis", (ROOT / "research" / STUDY).read_text())

    def test_italian_tip_and_information_limits(self):
        rels = {r["id"]: r for r in yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]}
        first = rels["REL-IT-DE-NSU-SISDE-BFV-HINWEIS-2003-001"]
        self.assertNotIn("period", first)
        self.assertIn("kein erwiesener NSU-Bezug", first["label"])
        later = rels["REL-IT-DE-NSU-AISI-BFV-HINWEIS-2011-001"]
        self.assertEqual(later["period"]["start"], "2011-12-14")
        self.assertNotEqual(first["from"], later["from"])
        self.assertIn("Freigabeanfragen offen", rels["REL-DE-NSU-HH-SENAT-BUERGERSCHAFT-THIRD-PARTY-2023-001"]["label"])
        self.assertIn("anderweitige Überlieferung offen", rels["REL-DE-NSU-HH-POL-PMK-LUECKE-2023-001"]["label"])

    def test_study_exact_integration(self):
        reg = yaml.safe_load((ROOT / "data/research-integrations.yml").read_text())
        entry = reg["studies"][STUDY]
        self.assertEqual(set(entry["relation_ids"]), RELATIONS | {'REL-IT-DE-NSU-AISI-BFV-HINWEIS-2011-001', 'REL-IT-DE-NSU-SISDE-BFV-HINWEIS-2003-001', 'REL-DE-NSU-HH-SENAT-BUERGERSCHAFT-THIRD-PARTY-2023-001', 'REL-DE-NSU-HH-POL-PMK-LUECKE-2023-001'} | {'REL-DE-NSU-HH-POL-ARCHIV-2025-001', 'REL-DE-NSU-HH-POL-GBA-FREIGABE-2023-001', 'REL-DE-NSU-HH-LFV-AUSWAHL-2025-001'} | {'REL-DE-NSU-HH-SENAT-PKA-2017-001', 'REL-DE-NSU-HH-LFV-FORSCHUNG-BESTAND-2025-001', 'REL-DE-NSU-HH-BUERGERSCHAFT-FORSCHUNG-2023-001', 'REL-DE-NSU-HH-BUERGERSCHAFT-SENAT-SICHERUNG-2023-001', 'REL-DE-NSU-HH-GBA-2026-001', 'REL-DE-NSU-HH-DSB-PKA-2016-001'})
        self.assertEqual(entry["sha256"], hashlib.sha256((ROOT / "research" / STUDY).read_bytes()).hexdigest())

if __name__ == "__main__":
    unittest.main()
