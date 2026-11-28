"""Preserve limits of reform evidence and distinguish motion from referral."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = "nsu-reformbilanz-sachsen-evaluation-2019-2026.md"


class NsuReformbilanzTests(unittest.TestCase):
    def setUp(self):
        self.rows = {r["id"]: r for r in yaml.safe_load(
            (ROOT / "data/relations.yml").read_text()
        )["relations"]}
        self.registry = yaml.safe_load(
            (ROOT / "data/research-integrations.yml").read_text()
        )["studies"][STUDY]

    def test_external_evaluation_and_official_statistics_have_distinct_scope(self):
        study = self.rows["REL-DE-IDZ-SN-SMJ-NSU-REFORMDEFIZITE-2025-001"]
        statistics = self.rows["REL-DE-SN-SMJ-GENSTA-VERLAUFSSTATISTIK-2025-001"]
        transfer = self.rows["REL-DE-GBA-GENSTA-DRESDEN-ZESA-2025-001"]
        self.assertIn("Stand der Erhebung 2024", study["label"])
        self.assertIn("keine fallbezogene Verlaufsstatistik", statistics["label"])
        self.assertIn("kein Beleg manipulierter Einzelfälle", statistics["label"])
        self.assertEqual(statistics["sources"], [
            "SRC-DE-SN-PSB2-20250408", "SRC-DE-SN-PSB2-LANG-20250408"])
        self.assertIn("keine Schuld- oder allgemeine Wirksamkeitsfeststellung", transfer["label"])
        self.assertIn("nicht RED oder ATD", self.rows[
            "REL-DE-MAD-BFV-VPVERBUND-2019-001"]["label"])

    def test_motion_and_referral_are_not_enacted_policy(self):
        motion = self.rows["REL-DE-LINKE-BUNDESTAG-NSU-EVALUATION-2026-001"]
        referral = self.rows["REL-DE-BT-INNENAUSSCHUSS-NSU-ANTRAG-2026-001"]
        self.assertEqual(str(motion["period"]["start"]), "2026-11-04")
        self.assertEqual(str(referral["period"]["start"]), "2026-11-05")
        self.assertIn("kein erteilter Auftrag", motion["label"])
        self.assertIn("keine Annahme der Forderungen", referral["label"])
        self.assertEqual(referral["from"], "ORG-DE-BUNDESTAG")
        self.assertEqual(referral["to"], "ORG-DE-BT-INNENAUSSCHUSS-21")
        self.assertEqual(len(set(self.registry["relation_ids"])), 8)


if __name__ == "__main__":
    unittest.main()
