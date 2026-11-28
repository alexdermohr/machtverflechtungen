"""Keep the RED reform's outcomes and scope of oversight claims distinct."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = "nsu-rechtsextremismusdatei-reformwirkung-2012-2023.md"


class NsuRedTests(unittest.TestCase):
    def setUp(self):
        self.rows = {r["id"]: r for r in yaml.safe_load(
            (ROOT / "data/relations.yml").read_text()
        )["relations"]}
        self.registry = yaml.safe_load(
            (ROOT / "data/research-integrations.yml").read_text()
        )["studies"][STUDY]

    def test_file_boundaries_and_empirical_scope(self):
        self.assertEqual(self.rows["REL-DE-BFV-RED-FEHLBEFUELLUNG-2013-001"]["to"], "PRG-DE-RED")
        self.assertEqual(self.rows["REL-DE-BFDI-ATD-ABSCHAFFUNG-2023-001"]["to"], "PRG-DE-ATD")
        project = self.rows["REL-DE-BFV-BKA-PROJEKTDATEI-2015-001"]
        self.assertEqual(project["to"], "ORG-DE-BKA")
        self.assertIn("Nicht RED oder ATD", project["label"])
        self.assertEqual(len(set(self.registry["relation_ids"])), 10)
        evaluation = self.rows["REL-DE-BMI-RED-EVALUATION-2016-001"]["label"]
        self.assertIn("984 Bögen von elf Behörden", evaluation)
        self.assertIn("kein Wirkungsnachweis", evaluation)

    def test_remedies_are_not_general_clearance(self):
        positive = self.rows["REL-DE-BFDI-BFV-ATD-KONTROLLE-2019-001"]["label"]
        disputed = self.rows["REL-DE-BFDI-BFV-VERBUNDDATEIEN-2022-001"]["label"]
        repaired = self.rows["REL-DE-BFDI-BFV-VERBUNDDATEIEN-2023-001"]["label"]
        self.assertIn("keine Aussage über RED", positive)
        self.assertIn("jeweils eine zurückgenommen", disputed)
        self.assertIn("nicht nachweislich behoben", disputed)
        self.assertIn("Einzelmängel", repaired)
        self.assertIn("nicht erneut geprüft", repaired)
        self.assertIn("Bundesbehörden bis dahin ungenutzt", self.rows[
            "REL-DE-BMI-RED-NUTZUNG-2022-001"]["label"])

if __name__ == "__main__":
    unittest.main()
