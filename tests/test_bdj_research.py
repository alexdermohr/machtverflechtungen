"""Exact-source regressions for the BDJ/Technischer-Dienst case (1950–1953)."""

from __future__ import annotations

from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "docs/faelle/de/technischer-dienst-bdj.md"
SOURCE_IDS = (
    "SRC-DE-FRAK-BDJ-19521021",
    "SRC-DE-BARCH-KAB-BDJ-19521010",
    "SRC-DE-BT-BDJ-19521023",
    "SRC-DE-BYLT-TD-19521029",
    "SRC-DE-BYMR-TD-19530113",
    "SRC-DE-BYMR-TD-19530120",
    "SRC-DE-HE-LAGIS-BDJ-19530108",
    "SRC-DE-HELT-BDJ-186904-2013",
)


def records(name: str, key: str) -> dict:
    data = yaml.safe_load((ROOT / "data" / name).read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in data[key]}


def bdj_metadata() -> dict:
    raw = CASE.read_text(encoding="utf-8")
    self_boundary = raw.split("\n---\n", 1)
    assert raw.startswith("---\n") and len(self_boundary) == 2
    return yaml.safe_load(self_boundary[0][4:])


class BDJResearchRegressions(unittest.TestCase):
    def test_18_prepared_claims_and_8_registered_original_source_ids(self):
        case = bdj_metadata()
        claims = {item["id"]: item for item in case["claims"]}
        self.assertEqual(set(claims), {f"CLM-DE-BDJ-{n:03d}" for n in range(1, 19)})
        sources = records("sources.yml", "sources")
        for sid in SOURCE_IDS:
            with self.subTest(source=sid):
                self.assertIn(sid, sources)
                self.assertIn(sid, case["sources"])
                self.assertTrue(sources[sid]["url"].startswith("https://"))
                self.assertTrue(sources[sid]["locator"])
        self.assertTrue(sources["SRC-DE-HELT-BDJ-186904-2013"]["primary"])
        self.assertFalse(sources["SRC-DE-HE-LAGIS-BDJ-19530108"]["primary"])

    def test_egidi_lehr_conflicting_bfv_chronologies_visible(self):
        claims = {c["id"]: c for c in bdj_metadata()["claims"]}
        claim = claims["CLM-DE-BDJ-003"]
        self.assertIn("September 1951", claim["text"])
        self.assertIn("SRC-DE-BT-BDJ-19521023", bdj_metadata()["sources"])
        rivals = [entry for entry in claim["counterevidence"]
                  if entry["source"] == "SRC-DE-BT-BDJ-19521023"]
        self.assertEqual(len(rivals), 1)
        self.assertEqual(rivals[0]["directness"], "direct")
        self.assertIn("10805", rivals[0]["locator"])
        self.assertIn("10806", rivals[0]["locator"])
        self.assertIn("Februar 1951", rivals[0]["note"])
        self.assertIn("September 1952", rivals[0]["note"])
        article = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        self.assertIn("**`CLM-DE-BDJ-003`", article)
        self.assertIn("Februar 1951", article)
        self.assertIn("September 1952", article)
        self.assertIn("Lehr", article)
        self.assertIn("Egidi", article)

    def test_distinct_federal_grants_us_inflow_and_seized_cash(self):
        claims = {item["id"]: item for item in bdj_metadata()["claims"]}
        self.assertIn("10.000 DM", claims["CLM-DE-BDJ-004"]["text"])
        self.assertIn("6.000 DM", claims["CLM-DE-BDJ-004"]["text"])
        self.assertIn("70.000 DM", claims["CLM-DE-BDJ-007"]["text"])
        self.assertIn("30.000 DM", claims["CLM-DE-BDJ-007"]["text"])
        self.assertIn("keine 100.000-DM-Gesamtsumme", claims["CLM-DE-BDJ-007"]["scope"]["does_not_support"])
        relations = records("relations.yml", "relations")
        self.assertEqual(relations["REL-DE-BDJ-002"]["from"], "ORG-DE-BMG")
        self.assertEqual(relations["REL-DE-BDJ-003"]["from"], "ORG-DE-BMI")
        for rid, amount in (("REL-DE-BDJ-002", "10.000 DM"), ("REL-DE-BDJ-003", "6.000 DM")):
            self.assertEqual(relations[rid]["to"], "ORG-DE-BDJ")
            self.assertIn(amount, relations[rid]["label"])
        self.assertFalse(any("100.000 DM" in x["label"] for x in relations.values()))

    def test_organizations_and_cic_phone_reference_are_distinct(self):
        entities = records("entities.yml", "entities")
        ids = ("ORG-DE-BDJ", "ORG-DE-BDJ-TD", "ORG-DE-DHS",
               "ORG-DE-STOSSTRUPP-BZ", "ORG-US-CIC", "ORG-US-US-ARMY-GERMANY", "ORG-US-CIA")
        for ent in ids:
            self.assertIn(ent, entities)
        self.assertEqual(len({entities[s]["name"] for s in ids}), len(ids))
        relations = records("relations.yml", "relations")
        self.assertEqual(relations["REL-DE-BDJ-006"]["from"], "ORG-DE-STOSSTRUPP-BZ")
        self.assertEqual(relations["REL-DE-BDJ-006"]["to"], "ORG-DE-DHS")
        self.assertEqual(relations["REL-DE-BDJ-008"]["from"], "ORG-DE-DHS")
        self.assertEqual(relations["REL-DE-BDJ-008"]["to"], "ORG-US-CIC")
        self.assertEqual(relations["REL-DE-BDJ-008"]["claim_ids"], ["CLM-DE-BDJ-011"])
        self.assertFalse(any(
            r["to"] == "ORG-US-CIC" and r["from"] == "ORG-DE-BDJ-TD"
            for r in relations.values()
        ))

    def test_23_people_is_bavarian_count_not_total_strength(self):
        claim = next(c for c in bdj_metadata()["claims"] if c["id"] == "CLM-DE-BDJ-014")
        self.assertIn("23", claim["text"])
        self.assertIn("Bayern", claim["text"])
        self.assertIn("Gesamtstärke", claim["scope"]["does_not_support"])

    def test_federalism_and_prosecution_counterclaims(self):
        claims = {c["id"]: c for c in bdj_metadata()["claims"]}
        relations = records("relations.yml", "relations")
        self.assertEqual(claims["CLM-DE-BDJ-006"]["classification"], "counterevidence")
        self.assertEqual(claims["CLM-DE-BDJ-010"]["classification"], "counterevidence")
        self.assertEqual(relations["REL-DE-BDJ-009"]["period"]["start"], "1953-01-08")
        for rid in ("REL-DE-BDJ-010", "REL-DE-BDJ-011"):
            self.assertEqual(relations[rid]["period"]["start"], "1953-01-13")
        self.assertEqual(relations["REL-DE-BDJ-012"]["period"]["start"], "1953-01-20")
        self.assertEqual(relations["REL-DE-BDJ-013"]["type"], "reported_dismissal_considered")
        self.assertEqual(relations["REL-DE-BDJ-014"]["type"], "reported_preliminary_investigation_requested")

    def test_archival_commission_record_does_not_pretend_to_be_read(self):
        claim = next(c for c in bdj_metadata()["claims"] if c["id"] == "CLM-DE-BDJ-017")
        self.assertIn("Untersuchungskommission", claim["text"])
        self.assertIn("SRC-DE-HELT-BDJ-186904-2013", claim["sources"])
        self.assertIn("Signatur", " ".join(claim["missing_evidence"]).lower().replace("signatur", "Signatur"))
        self.assertNotIn("Kommissionsbericht beweist", CASE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()