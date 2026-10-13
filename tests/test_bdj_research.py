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
    "SRC-DE-HHSTAW-502-17886",
    "SRC-US-CIA-LCPROWL-V1-0037",
    "SRC-US-CIA-LCPROWL-V1-0044",
    "SRC-US-CIA-LCPROWL-V2-0023",
    "SRC-DE-FES-SPDPD-BDJ-19530124",
    "SRC-DE-FES-SPDPD-BDJ-19530312",
    "SRC-DE-FES-SPDPD-BDJ-19530717",
    "SRC-DE-FES-SPDPD-BDJ-19521009",
    "SRC-DE-FES-SPDPD-BDJ-19521010",
    "SRC-DE-FES-SPDPD-BDJ-19521027",
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
    def test_36_prepared_claims_and_18_registered_source_ids(self):
        case = bdj_metadata()
        claims = {item["id"]: item for item in case["claims"]}
        self.assertEqual(set(claims), {f"CLM-DE-BDJ-{n:03d}" for n in range(1, 37)})
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

    def test_visible_event_evidence_labels_match_claim_levels(self):
        case = bdj_metadata()
        claims = {entry["id"]: entry for entry in case["claims"]}
        article = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        names = {"established": "belegt", "strong": "stark gestützt"}
        for cid in case["event_claims"]:
            claim = claims[cid]
            with self.subTest(claim=cid):
                self.assertIn(
                    f"- **`{cid}` — {names[claim['evidence_level']]}:** {claim['text']}",
                    article,
                )

    def test_archival_commission_record_does_not_pretend_to_be_read(self):
        claim = next(c for c in bdj_metadata()["claims"] if c["id"] == "CLM-DE-BDJ-017")
        self.assertIn("Untersuchungskommission", claim["text"])
        self.assertIn("SRC-DE-HELT-BDJ-186904-2013", claim["sources"])
        self.assertIn("Signatur", " ".join(claim["missing_evidence"]).lower().replace("signatur", "Signatur"))
        self.assertNotIn("Kommissionsbericht beweist", CASE.read_text(encoding="utf-8"))


    def test_hhstaw_502_17886_archival_catalog_record_scoped_to_finding_aid(self):
        case = bdj_metadata()
        claims = {c["id"]: c for c in case["claims"]}
        source = records("sources.yml", "sources")["SRC-DE-HHSTAW-502-17886"]
        claim = claims["CLM-DE-BDJ-019"]

        self.assertIn("SRC-DE-HHSTAW-502-17886", case["sources"])
        self.assertTrue(source["primary"])
        self.assertIsNone(source["date"], "Katalog-Publikationsdatum darf nicht durch Abrufdatum ersetzt werden")
        self.assertEqual(source["accessed"], "2026-10-12")
        self.assertEqual(source["url"],
                         "https://arcinsys.hessen.de/arcinsys/showArchivalDescriptionDetails?archivalDescriptionId=6991555")
        self.assertIn("HHStAW, 502, 17886", source["locator"])
        self.assertEqual(claim["evidence_level"], "established")
        self.assertEqual(claim["classification"], "fact")
        self.assertEqual(claim["sources"], ["SRC-DE-HHSTAW-502-17886"])
        self.assertIn("HHStAW, 502, 17886", claim["evidence"][0]["locator"])
        self.assertIn("1952", claim["text"])
        self.assertIn("Ermittlungsverfahren", claim["text"])
        self.assertIn("Originalaktenblätter", " ".join(claim["missing_evidence"]))
        self.assertNotIn("CLM-DE-BDJ-019", case["event_claims"])

        visible = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        for anchor in ("HHStAW, 502, 17886", "Deutsch-Amerikanischen Untersuchungskommission",
                       "Paul Lüth", "Otto Rietdorf", "Erhard Peters",
                       "03a-34-01", "Nr. 18 I (26) Geheim"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, visible)
        self.assertNotIn("Kommission bewies", visible)


    def test_cia_amendment2_primary_facsimile_claims_are_bounded(self):
        case = bdj_metadata()
        claims = {c["id"]: c for c in case["claims"]}
        src = records("sources.yml", "sources")["SRC-US-CIA-LCPROWL-V1-0037"]
        self.assertTrue(src["primary"])
        self.assertEqual(src["tier"], "A")
        self.assertEqual(src["sha256"],
                         "d46f15e7afc334c4496c579cf8be1401dc4412d446edba6a370cb4bc19027c17")
        self.assertIn("VOL.%201_0037.pdf", src["url"])
        self.assertIn("PDF-S.", src["locator"])
        self.assertIn("0037", src["title"])
        for num in (20, 21, 22, 23):
            cid = f"CLM-DE-BDJ-{num:03d}"
            with self.subTest(claim=cid):
                self.assertEqual(claims[cid]["sources"],
                                 ["SRC-US-CIA-LCPROWL-V1-0044"] if num == 20
                                 else ["SRC-US-CIA-LCPROWL-V1-0037"])
                self.assertEqual(claims[cid]["classification"], "fact")
                self.assertEqual(claims[cid]["evidence_level"], "established")
                self.assertIn("PDF-S.", claims[cid]["evidence"][0]["locator"])
                self.assertNotIn(cid, case["event_claims"])

        self.assertIn("OPC", claims["CLM-DE-BDJ-020"]["text"])
        self.assertIn("privaten", claims["CLM-DE-BDJ-020"]["text"])
        self.assertIn("13 Monate", claims["CLM-DE-BDJ-021"]["text"])
        self.assertIn("beantragte", claims["CLM-DE-BDJ-021"]["text"])
        self.assertIn("7.000", claims["CLM-DE-BDJ-022"]["text"])
        self.assertIn("3.000", claims["CLM-DE-BDJ-022"]["text"])
        self.assertIn("4.000", claims["CLM-DE-BDJ-022"]["text"])
        self.assertIn("530", claims["CLM-DE-BDJ-022"]["text"])
        self.assertIn("178", claims["CLM-DE-BDJ-022"]["text"])
        self.assertIn("Schallplatten", claims["CLM-DE-BDJ-023"]["text"])
        original = records("sources.yml", "sources")["SRC-US-CIA-LCPROWL-V1-0044"]
        self.assertEqual(original["sha256"],
                         "136f7683bd367e92a141f7a0a0d5fb6298c25cc804f17692ad2f8db80ef3b93f")
        self.assertIn("ORG-US-OPC", case["actors"])
        self.assertIn("ORG-US-OPC", records("entities.yml", "entities"))
        relation = records("relations.yml", "relations")["REL-DE-BDJ-015"]
        self.assertEqual((relation["from"], relation["to"]),
                         ("ORG-US-OPC", "ORG-DE-BDJ"))
        self.assertEqual(relation["sources"], ["SRC-US-CIA-LCPROWL-V1-0044"])
        self.assertEqual(relation["claim_ids"], ["CLM-DE-BDJ-020"])
        self.assertNotIn("70.000", relation["label"])
        self.assertIn("Tarn", claims["CLM-DE-BDJ-023"]["text"])
        article = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        for content in ("LCPROWL VOL. 1_0037", "7.000", "530", "178",
                        "13 Monate", "Schallplatten", "beantragte"):
            self.assertIn(content, article)
        self.assertIn("geplant", article)
        self.assertNotIn("7.000 ausgebildete", article)


    def test_april1953_cia_whitebook_attributions_and_internal_assessment(self):
        sources = records("sources.yml", "sources")
        source = sources["SRC-US-CIA-LCPROWL-V2-0023"]
        case = bdj_metadata()
        claims = {entry["id"]: entry for entry in case["claims"]}
        self.assertEqual(source["date"], "1953-04-15")
        self.assertTrue(source["primary"])
        self.assertEqual(source["tier"], "A")
        self.assertIn("VOL.%202_0023.pdf", source["url"])
        self.assertEqual(source["sha256"],
                         "ae20eeb19b43dddbb83ed3a213231104c315583f8af490274dcd8db014ace532")
        self.assertIn("SRC-US-CIA-LCPROWL-V2-0023", case["sources"])

        article = CASE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
        for number in range(24, 29):
            cid = f"CLM-DE-BDJ-{number:03d}"
            with self.subTest(claim=cid):
                claim = claims[cid]
                self.assertEqual(claim["classification"], "fact")
                self.assertEqual(claim["evidence_level"], "established")
                self.assertEqual(claim["sources"], ["SRC-US-CIA-LCPROWL-V2-0023"])
                self.assertIn("PDF-S.", claim["evidence"][0]["locator"])
                self.assertNotIn(cid, case["event_claims"])
                self.assertIn(f"- **`{cid}` — belegt:** {claim['text']}", article)

        self.assertIn("Home Office", claims["CLM-DE-BDJ-024"]["text"])
        self.assertIn("vier", claims["CLM-DE-BDJ-025"]["text"])
        self.assertIn("SPD-Weißbuch", claims["CLM-DE-BDJ-025"]["text"])
        self.assertIn("40.000 DM", claims["CLM-DE-BDJ-026"]["text"])
        self.assertIn("Peters", claims["CLM-DE-BDJ-026"]["text"])
        self.assertIn("300", claims["CLM-DE-BDJ-027"]["text"])
        self.assertIn("19. Mai 1952", claims["CLM-DE-BDJ-027"]["text"])
        self.assertIn("Decknamen", claims["CLM-DE-BDJ-028"]["text"])
        self.assertIn("geschwärzt", claims["CLM-DE-BDJ-028"]["text"])
        self.assertIn("0023", article)
        self.assertIn("SRC-US-CIA-LCPROWL-V2-0023", article)
        self.assertIn("Weißbuch", article)

        relations = records("relations.yml", "relations")
        self.assertFalse(any(
            source["id"] in relation.get("sources", [])
            and relation["type"] in {"documented_opc_subsidy", "reported_federal_grant"}
            for relation in relations.values()
        ), "Aus dem CIA-Kommentar von 1953 dürfen keine Unternehmens-Zahlungen konstruiert werden")



if __name__ == "__main__":
    unittest.main()