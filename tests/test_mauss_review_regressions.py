"""Regression checks for the Mauss/Schmücker source and graph corrections."""

from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {r["id"]: r for r in yaml.safe_load(
        (ROOT / "data" / (name + ".yml")).read_text(encoding="utf-8")
    )[name]}


class MaussReviewRegressions(unittest.TestCase):
    def test_historical_roles_remain_distinct(self):
        entities = records("entities")
        relations = records("relations")
        self.assertIn("Sponsor 2008/09", entities["ORG-DE-AUSWAERTIGES-AMT-2008"]["name"])
        for suffix in ("005", "008", "009"):
            edge = relations["REL-MAUSS-DIPLOMATIE-" + suffix]
            self.assertIn("ORG-DE-AUSWAERTIGES-AMT-1996", (edge["from"], edge["to"]))
            self.assertNotIn("ORG-DE-AUSWAERTIGES-AMT-2008", (edge["from"], edge["to"]))

    def test_report_dates_are_not_relationship_start_dates(self):
        relations = records("relations")
        for edge_id in (
            "REL-MAUSS-OFFSHORE-013", "REL-RAF-SCHMUECKER-NONNE-020",
            "REL-MAUSS-FINANZ-012", "REL-MAUSS-OFFSHORE-021",
            "REL-MAUSS-OFFSHORE-022", "REL-MAUSS-DIPLOMATIE-010",
        ):
            with self.subTest(edge_id=edge_id):
                self.assertFalse(relations[edge_id].get("period", {}).get("start"))
        edge = relations["REL-MAUSS-DIPLOMATIE-010"]
        self.assertEqual(edge["to"], "PER-DE-HELMUT-KOHL")
        self.assertEqual(edge["from"], "ORG-DE-BUNDESKANZLERAMT")

    def test_source_links_and_locators(self):
        sources = records("sources")
        self.assertEqual(
            sources["SRC-DE-BERLIN-UA-SCHMUECKER-1990"]["url"],
            "https://pardok.parlament-berlin.de/starweb/adis/citat/VT/11/DruckSachen/d11-1224.pdf",
        )
        self.assertIn("13275–13277", sources["SRC-DE-BT-MAUSS-PL147-1996"]["locator"])
        self.assertIn("13771–13776", sources["SRC-DE-BT-MAUSS-PL153-1997"]["locator"])


if __name__ == "__main__":
    unittest.main()
