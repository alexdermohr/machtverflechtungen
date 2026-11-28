"""Keep the two Cologne judgments distinct and preserve the counterevidence."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = "nsu-bfv-personalmassnahmen-vg-koeln-2012-2015.md"
ADVERSE = "REL-DE-NSU-VGK-BFV-DOPPELSPITZE-2015-001"
UPHELD = "REL-DE-NSU-VGK-BFV-UMSETZUNG-2015-001"


class NsuDienstrechtTests(unittest.TestCase):
    def test_judgments_are_not_conflated(self):
        relations = {
            r["id"]: r for r in yaml.safe_load(
                (ROOT / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            s["id"]: s for s in yaml.safe_load(
                (ROOT / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        for relation_id, kind, measure, source_id, docket in (
            (ADVERSE, "declared_personnel_measure_unlawful", "26.07.2013",
             "SRC-DE-VGK-NSU-15K706813-20150209", "15 K 7068/13"),
            (UPHELD, "upheld_personnel_measure", "25.11.2013",
             "SRC-DE-VGK-NSU-15K345814-20150209", "15 K 3458/14"),
        ):
            row = relations[relation_id]
            self.assertEqual((row["from"], row["to"]), ("ORG-DE-VG-KOELN", "ORG-DE-BFV"))
            self.assertEqual(row["type"], kind)
            self.assertEqual(str(row["period"]["start"]), "2015-02-09")
            self.assertIn(measure, row["label"])
            self.assertIn("Rechtskraft offen", row["label"])
            self.assertIn(source_id, row["sources"])
            self.assertIn(docket, sources[source_id]["title"])
            self.assertIn("Drittveröffentlichung", sources[source_id]["notes"])
            self.assertIn("Rechtskraft offen", sources[source_id]["notes"])
        registry = yaml.safe_load(
            (ROOT / "data/research-integrations.yml").read_text(encoding="utf-8")
        )["studies"][STUDY]
        self.assertIn(ADVERSE, registry["relation_ids"])
        self.assertIn(UPHELD, registry["relation_ids"])
        self.assertEqual(registry["status"], "network")
        text = (ROOT / "research" / STUDY).read_text(encoding="utf-8")
        self.assertIn("Parteivortrag", text)
        self.assertIn("Gegenindiz", text)


    def test_registered_receipt_is_not_full_production(self):
        rows = {r["id"]: r for r in yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]}
        req = rows["REL-DE-NSU-BT-NRW-GERICHTSAKTEN-2016-001"]
        receipt = rows["REL-DE-NSU-NRW-BT-AKTENEINGANG-2016-001"]
        self.assertEqual(str(req["period"]["start"]), "2016-10-20")
        self.assertEqual(str(receipt["period"]["start"]), "2016-12-13")
        self.assertIn("Vollständigkeit offen", req["label"])
        self.assertIn("Vollständigkeit und Inhalt offen", receipt["label"])
        self.assertIn("116/17 VS-V", receipt["label"])
        self.assertEqual(receipt["sources"], ["SRC-DE-BT-NSU-1812950-2017"])


if __name__ == "__main__":
    unittest.main()
