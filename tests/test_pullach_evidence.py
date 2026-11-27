"""Preserve attribution and source boundaries for Pullach intern."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class PullachEvidenceTests(unittest.TestCase):
    def test_self_report_is_not_cooperation_of_addressees(self):
        rel = records("relations")
        dispatch = rel["REL-DE-PULLACH-002"]
        self.assertEqual("reported_material_dispatch", dispatch["type"])
        self.assertEqual("ORG-DE-MFS", dispatch["from"])
        self.assertEqual("ORG-DE-BUNDESTAGSABGEORDNETE-PULLACH-1971", dispatch["to"])
        self.assertIn("keine daraus ableitbare Kooperation", dispatch["label"])
        self.assertEqual(["SRC-DE-BARCH-MFS-K121-1971"], dispatch["sources"])
        self.assertEqual("reported_letter", rel["REL-DE-PULLACH-004"]["type"])
        self.assertEqual("ORG-DE-DDR-PANORAMA-AUSLANDSPRESSEDIENST", rel["REL-DE-PULLACH-005"]["to"])
        self.assertIn(rel["REL-DE-PULLACH-005"]["to"], records("entities"))
        self.assertNotIn("period", rel["REL-DE-PULLACH-006"])
        self.assertIn("genauer Beginn hier nicht belegt", rel["REL-DE-PULLACH-006"]["label"])

    def test_historical_documents_are_distinct_from_research(self):
        src = records("sources")
        for key, date in (("K121", "1971-04-06"), ("K125", "1971-07-30")):
            row = src[f"SRC-DE-BARCH-MFS-{key}-1971"]
            self.assertTrue(row["primary"])
            self.assertEqual(date, row["date"])
        self.assertFalse(src["SRC-DE-UNI-KOELN-DUELFFER-PULLACH-2015"]["primary"])
        for row in records("relations").values():
            if row["id"].startswith("REL-DE-PULLACH-"):
                self.assertNotIn("SRC-DE-BARCH-MFS-K125-1971", row["sources"])
                if row["id"][-3:] in {"006", "007", "008", "009"}:
                    self.assertEqual(["SRC-DE-UNI-KOELN-DUELFFER-PULLACH-2015"], row["sources"])


if __name__ == "__main__":
    unittest.main()
