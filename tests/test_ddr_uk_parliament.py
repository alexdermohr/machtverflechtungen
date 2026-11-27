"""Keep parliamentary statements, commercial links and press allegations distinct."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class DDRUKParliamentTests(unittest.TestCase):
    def test_self_disclosures_are_not_payments_or_precise_dates(self):
        rel = records("relations")
        ownership = rel["REL-DE-DDR-UK-013"]
        self.assertEqual("reported_ownership", ownership["type"])
        self.assertIn("Beteiligung und Dauer nicht nachgewiesen", ownership["label"])
        advocacy = rel["REL-DE-DDR-UK-014"]
        self.assertEqual(("PER-GB-ARTHUR-LEWIS", "PER-GB-BURNABY-DRAYSON"),
                         (advocacy["from"], advocacy["to"]))
        self.assertNotIn("period", advocacy)
        self.assertIn("Vergütung offen", advocacy["label"])
        disclosure = rel["REL-DE-DDR-UK-015"]
        self.assertEqual("declared_industry_affiliation", disclosure["type"])
        self.assertEqual("1961-04-24", disclosure["period"]["start"])
        self.assertIn("kein Firmenname oder persönlicher Zahlungsbetrag", disclosure["label"])
        for n in (16, 17):
            meeting = rel[f"REL-DE-DDR-UK-{n:03}"]
            self.assertEqual("reported_meeting", meeting["type"])
            self.assertEqual("1961", meeting["period"]["start"])

    def test_trade_association_not_intelligence_agency(self):
        rel = records("relations")["REL-DE-DDR-UK-018"]
        self.assertEqual("ORG-GB-FEDERATION-BRITISH-INDUSTRIES", rel["from"])
        self.assertNotEqual("ORG-US-FBI", rel["from"])
        self.assertIn("Originalvertrag nicht eingesehen", rel["label"])

    def test_privilege_ruling_not_verdict_on_allegations(self):
        rel = records("relations")
        complaint = rel["REL-DE-DDR-UK-019"]
        ruling = rel["REL-DE-DDR-UK-020"]
        self.assertEqual("documented_privilege_complaint", complaint["type"])
        self.assertEqual("1962-03-12", complaint["period"]["start"])
        self.assertIn("nicht als Tatsachen bestätigt", complaint["label"])
        self.assertEqual("documented_procedural_ruling", ruling["type"])
        self.assertEqual("1962-03-13", ruling["period"]["start"])
        self.assertIn("kein Urteil über den Wahrheitsgehalt", ruling["label"])
        self.assertIn("Sachantrag weiterhin möglich", ruling["label"])
        src = records("sources")
        for key in ("SRC-DE-OSTPREUSSENBLATT-19620505", "SRC-GB-SPECTATOR-STERNBERG-1978"):
            self.assertFalse(src[key]["primary"])


if __name__ == "__main__":
    unittest.main()
