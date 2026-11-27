"""Guard the documented procedural scope of Langemann II."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class LangemannIIEvidenceTests(unittest.TestCase):
    def test_objection_and_denials_remain_distinct(self):
        rel = records("relations")
        ua = "ORG-DE-BAYLT-UA-LANGEMANN-II-1983-1985"
        objection = rel["REL-DE-LANG-II-002"]
        self.assertEqual("reported_secrecy_objection", objection["type"])
        self.assertEqual("ORG-DE-BND", objection["from"])
        self.assertEqual("ORG-DE-GBA", objection["to"])
        for n, sender, date in ((3, "ORG-DE-GBA", "1983-04-28"),
                                (6, "ORG-DE-BAYOBLG-1983", "1983-08-05"),
                                (8, "ORG-DE-BAYOBLG-1983", "1983-11-22")):
            row = rel[f"REL-DE-LANG-II-{n:03}"]
            self.assertEqual((sender, ua), (row["from"], row["to"]))
            self.assertEqual("reported_file_access_denial", row["type"])
            self.assertEqual(date, row["period"]["start"])

    def test_source_and_procedural_boundaries(self):
        source = records("sources")["SRC-DE-BAYLT-LANGEMANN-II-6288-1985"]
        self.assertTrue(source["primary"])
        self.assertIn("Faksimileseiten aktuell nicht abrufbar", source["notes"])
        self.assertIn("Kein Beleg einer rechtswidrigen Vertuschung", source["notes"])
        rows = [r for r in records("relations").values()
                if r["id"].startswith("REL-DE-LANG-II-")]
        self.assertEqual(8, len(rows))
        self.assertTrue(all(r["sources"] == [source["id"]] for r in rows))
        self.assertTrue(all(r["type"].startswith("reported_") for r in rows))


if __name__ == "__main__":
    unittest.main()
