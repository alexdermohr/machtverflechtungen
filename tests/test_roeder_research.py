"""Source-bound regression checks for distinct Roeder organisations and transactions."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "docs/faelle/de/deutsche-aktionsgruppen-roeder-1980-1998.md"


def case_metadata() -> dict:
    text = CASE.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    data, sep, _body = text[4:].partition("\n---\n")
    assert sep
    return yaml.safe_load(data)


class RoederSourceBoundaryTests(unittest.TestCase):
    def test_dbinitiative_money_and_1994_state_material_are_distinct(self) -> None:
        meta = case_metadata()
        claims = {claim["id"]: claim for claim in meta["claims"]}
        funding = claims["CLM-DE-DA-003"]
        material = claims["CLM-DE-DA-006"]
        self.assertIn("84.000 DM", funding["text"])
        self.assertIn("1979 und 1980", funding["text"])
        self.assertEqual(funding["sources"], ["SRC-DE-BT-09066-1981"])
        self.assertIn("1994", material["text"])
        vehicle_people = claims["CLM-DE-DA-007"]["text"]
        for marker in ("Vissing", "Manfred Roeder", "eine weitere Person", "Vissings Elektriker"):
            self.assertIn(marker, vehicle_people)
        self.assertEqual(material["sources"], ["SRC-DE-BT-1311005-1998"])
        self.assertIn("keine Bundeswehrfinanzierung von Anschlägen des Jahres 1980", material["scope"]["does_not_support"])

    def test_case_preserves_material_counterevidence_and_judgment_date_conflict(self) -> None:
        meta = case_metadata()
        claims = {claim["id"]: claim for claim in meta["claims"]}
        self.assertEqual(claims["CLM-DE-DA-005"]["classification"], "counterevidence")
        denial = claims["CLM-DE-DA-005"]
        for marker in ("Oktoberfestattentat", "Shlomo Lewin", "Frida Poeschke"):
            self.assertIn(marker, denial["text"])
        self.assertNotIn("damals angesprochenen rechtsterroristischen Taten", denial["text"])
        self.assertIn("Deutschen Aktionsgruppen", denial["scope"]["does_not_support"])
        self.assertIn("SRC-DE-ERLANGEN-LEWIN-2026", denial["sources"])
        self.assertEqual(claims["CLM-DE-DA-010"]["classification"], "hypothesis")
        self.assertIn("darunter den tödlichen Hamburger Brandanschlag", claims["CLM-DE-DA-001"]["text"])
        self.assertNotIn("sowie den tödlichen Hamburger Brandanschlag", claims["CLM-DE-DA-001"]["text"])
        synthesis = next(rec for rec in meta["what_follows"] if "84.000 DM" in rec["text"])
        self.assertIn("CLM-DE-DA-012", synthesis["claim_ids"])
        self.assertTrue(claims["CLM-DE-DA-010"]["counterevidence"])
        prose = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[-1]
        self.assertIn("24. Juni 1982", prose)
        self.assertIn("28. Juni 1982", prose)
        self.assertIn("Verfassungsschutzbericht 1982", prose)
        self.assertIn("5 – 1 StE 3/81", prose)

    def test_source_register_and_relations_are_claim_bound(self) -> None:
        sources = {
            s["id"]: s for s in yaml.safe_load((ROOT / "data/sources.yml").read_text())["sources"]
        }
        self.assertTrue(sources["SRC-DE-BT-09066-1981"]["primary"])
        self.assertTrue(sources["SRC-DE-BT-1311005-1998"]["primary"])
        original_locator = sources["SRC-DE-BT-1311005-1998"]["locator"]
        self.assertIn("460", original_locator)
        self.assertIn("66–76", original_locator)
        self.assertTrue(sources["SRC-DE-HE-VSBER-1982"]["primary"])
        self.assertIn("gedruckte S. 15", sources["SRC-DE-HE-VSBER-1982"]["locator"])
        self.assertFalse(sources["SRC-DE-ARCHIVPORTAL-DA-2026"]["primary"])
        self.assertEqual(sources["SRC-DE-ERLANGEN-LEWIN-2026"]["institution"], "Stadt Erlangen")
        relations = {
            rel["id"]: rel for rel in yaml.safe_load((ROOT / "data/relations.yml").read_text())["relations"]
        }
        self.assertEqual(relations["REL-DE-DA-002"]["to"], "ORG-DE-DEUTSCHE-BUERGERINITIATIVE")
        self.assertEqual(relations["REL-DE-DA-002"]["type"], "documented_association")
        self.assertEqual(relations["REL-DE-DA-006"]["to"], "ORG-DE-DEUTSCH-RUSS-GEMEINSCHAFTSWERK")
        self.assertEqual(relations["REL-DE-DA-006"]["period"]["start"], "1994-06-15")
        self.assertEqual(relations["REL-DE-DA-005"]["claim_ids"], ["CLM-DE-DA-012"])
        self.assertEqual(relations["REL-DE-DA-005"]["period"]["start"], "1993-02-20")
        self.assertEqual(relations["REL-DE-DA-005"]["to"], "ORG-DE-DEUTSCH-RUSS-GEMEINSCHAFTSWERK")
        self.assertNotEqual(relations["REL-DE-DA-002"]["to"], relations["REL-DE-DA-006"]["to"])
        for rid, person in (
            ("REL-DE-DA-008", "PER-DE-NGUYEN-NGOC-CHAU"),
            ("REL-DE-DA-009", "PER-DE-DO-ANH-LAN"),
        ):
            with self.subTest(relation=rid):
                self.assertEqual(relations[rid]["from"], person)
                self.assertEqual(relations[rid]["to"], "ORG-DE-DEUTSCHE-AKTIONSGRUPPEN")
                self.assertEqual(relations[rid]["type"], "victim_of_violent_attack")

    def test_public_case_includes_source_discovery_paths(self) -> None:
        text = CASE.read_text(encoding="utf-8")
        for locator in ("B 106/101969", "B 136/46243", "N Hepp Nr. 18", "EL 317 VII"):
            with self.subTest(locator=locator):
                self.assertIn(locator, text)


if __name__ == "__main__":
    unittest.main()