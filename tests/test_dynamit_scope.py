"""Guard the evidence and temporal boundaries of the Dynamit study."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    return {row["id"]: row for row in yaml.safe_load(
        (ROOT / "data" / f"{name}.yml").read_text(encoding="utf-8")
    )[name]}


class DynamitScopeTests(unittest.TestCase):
    def test_historical_institution_scopes_stay_distinct(self):
        entities = records("entities")
        relations = records("relations")
        pairs = (
            ("ORG-DE-BMVG-PSV-1981-1990", "ORG-DE-BMVG-1966", "1981–1990"),
            ("ORG-DE-AUSWAERTIGES-AMT-2008", "ORG-DE-AUSWAERTIGES-AMT-1966", "2008/09"),
            ("ORG-DE-BUNDESPRESSEAMT-1953", "ORG-DE-BUNDESPRESSEAMT-1966", "1953"),
        )
        film = [r for key, r in relations.items() if key.startswith("REL-DE-BND-DYNAMIT-")]
        endpoints = {r[k] for r in film for k in ("from", "to")}
        for historical, current, qualifier in pairs:
            with self.subTest(historical=historical):
                self.assertIn(qualifier, entities[historical]["name"])
                self.assertIn("1966", entities[current]["name"])
                self.assertIn(current, endpoints)
                self.assertNotIn(historical, endpoints)

    def test_staff_role_and_editorial_source_are_not_overstated(self):
        relation = records("relations")["REL-DE-BND-DYNAMIT-014"]
        self.assertEqual("employed_by", relation["type"])
        source = records("sources")["SRC-DE-STASI-PULLACH-INTERN-1971-ED"]
        self.assertIn(source["id"], relation["sources"])
        self.assertEqual("1971-07-30", source["date"])
        self.assertFalse(source["primary"])
        self.assertIn("unbekannte Publikationsdatum", source["notes"])
        self.assertNotIn("SRC-DE-STASI-PULLACH-INTERN-1968-ED", records("sources"))


if __name__ == "__main__":
    unittest.main()
