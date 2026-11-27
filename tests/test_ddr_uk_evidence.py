"""Guard distinctions between state funding, trade, disclosure and operations."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class DDRUKEvidenceTests(unittest.TestCase):
    def test_finance_and_public_disclosure_are_not_personal_payments(self):
        rel = records("relations")
        funding = rel["REL-DE-DDR-UK-001"]
        self.assertEqual("ORG-DE-DDR-STAAT", funding["from"])
        self.assertEqual("reported_public_funding", funding["type"])
        self.assertIn("Beträge nicht nachgewiesen", funding["label"])
        trade = rel["REL-DE-DDR-UK-009"]
        self.assertEqual("reported_trade_agreement", trade["type"])
        self.assertEqual("ORG-GB-DOMINION-EXPORT", trade["from"])
        self.assertIn("keine tatsächliche Zahlung", trade["label"])
        disclosure = rel["REL-DE-DDR-UK-010"]
        self.assertEqual("declared_business_interest", disclosure["type"])
        self.assertEqual("established", disclosure["evidence_level"])
        self.assertIn("nicht namentlich genannte Firma", disclosure["label"])
        self.assertEqual(["SRC-GB-HANSARD-DRAYSON-1962"], disclosure["sources"])

    def test_surveillance_and_plans_do_not_assert_agent_control(self):
        rel = records("relations")
        watched = rel["REL-DE-DDR-UK-003"]
        self.assertEqual("reported_surveillance", watched["type"])
        self.assertNotIn("period", watched)
        self.assertIn("nicht belegt", watched["label"])
        plan = rel["REL-DE-DDR-UK-012"]
        self.assertEqual("planned_disinformation", plan["type"])
        self.assertIn("keine konkret ausgeführte Maßnahme", plan["label"])
        self.assertEqual(["SRC-DE-BARCH-MFS-K121-1971"], plan["sources"])
        for row in rel.values():
            if row["id"].startswith("REL-DE-DDR-UK-"):
                self.assertNotEqual(
                    {row["from"], row["to"]},
                    {"ORG-DE-MFS", "PER-GB-BURNABY-DRAYSON"},
                )
        self.assertFalse(records("sources")[
            "SRC-DE-BSTU-ENGELMANN-JOESTEL-ZAIG-2009"]["primary"])


if __name__ == "__main__":
    unittest.main()
