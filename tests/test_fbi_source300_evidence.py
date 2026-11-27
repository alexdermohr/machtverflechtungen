"""Guard the narrow provenance, chronology and oversight findings."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class FBISource300EvidenceTests(unittest.TestCase):
    def test_provenance_is_not_generalized_to_other_reports(self):
        rel = records("relations")
        source = "PRG-US-FBI-BUREAU-SOURCE-300"
        legat = "ORG-US-FBI-LEGAT-BONN"
        for n in (2, 6):
            row = rel[f"REL-US-DDR-LIAISON-{n:03}"]
            self.assertEqual((source, legat), (row["from"], row["to"]))
            self.assertEqual("reported_information_transfer", row["type"])
            if n == 2:
                self.assertNotIn("period", row)
            else:
                self.assertEqual("1972", row["period"]["start"])
        row = rel["REL-US-DDR-LIAISON-010"]
        self.assertEqual(("ORG-US-ARMY", source), (row["from"], row["to"]))
        self.assertEqual("reported_origin_of_specific_records", row["type"])
        self.assertIn("keine pauschale Zuordnung", row["label"])
        self.assertNotIn("period", row)
        self.assertNotIn("period", rel["REL-US-DDR-LIAISON-004"])
        self.assertEqual(["SRC-US-NARA-FBI-HSC-AFSC-1975"], row["sources"])
        comparator = rel["REL-US-DDR-LIAISON-008"]
        self.assertIn("DGR-Feld unmarkiert", comparator["label"])
        self.assertNotEqual(source, comparator["from"])

    def test_oversight_and_book_order_are_distinct(self):
        rel = records("relations")
        request = rel["REL-US-DDR-LIAISON-011"]
        omission = rel["REL-US-DDR-LIAISON-012"]
        self.assertEqual("1975-11-03", request["period"]["start"])
        self.assertEqual("reported_nondisclosure_request", request["type"])
        self.assertEqual("1975-11-06", omission["period"]["start"])
        self.assertEqual("documented_omission_from_response", omission["type"])
        self.assertIn("spätere Freigabe und Rechtsgrundlage ungeklärt", omission["label"])
        order = rel["REL-US-DDR-LIAISON-005"]
        self.assertEqual("reported_book_order", order["type"])
        self.assertIn("Einlösung, Lieferung", order["label"])
        self.assertNotIn("period", rel["REL-US-DDR-LIAISON-013"])
        self.assertIn("keine Straftat festgestellt", rel["REL-US-DDR-LIAISON-013"]["label"])

    def test_notley_amount_is_reported_not_established_payment(self):
        row = records("relations")["REL-DE-DDR-UK-005"]
        self.assertEqual("reported_public_relations_mandate", row["type"])
        self.assertIn("bis zu 20.000 GBP jährlich", row["label"])
        self.assertIn("Zahlungsbelege offen", row["label"])
        self.assertIn("SRC-GB-BERGER-LAPORTE-FRIENDLY-ENEMIES-2010", row["sources"])
        self.assertEqual("strong", row["evidence_level"])


if __name__ == "__main__":
    unittest.main()
