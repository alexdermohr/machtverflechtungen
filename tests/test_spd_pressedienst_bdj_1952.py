"""Protect the October 1952 SPD Pressedienst originals and claim attribution."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "docs" / "faelle" / "de" / "technischer-dienst-bdj.md"
SOURCE_PATH = ROOT / "data" / "sources.yml"
CATALOG_PATH = ROOT / "docs" / "quellen" / "index.md"

ORIGINALS = {
    "SRC-DE-FES-SPDPD-BDJ-19521009": (
        "1952-10-09", "521009.pdf",
        "8bd2ad84ce155b30dd463a100e8b4d61ad05908d73f4e896d2038a715ab32b17",
        "S. 1–2", "00000244.tif",
    ),
    "SRC-DE-FES-SPDPD-BDJ-19521010": (
        "1952-10-10", "521010.pdf",
        "05e1ec3061b0c2e35565afc0f4eedc6f27847c513f849b260fa78e4c382674f6",
        "S. 6–7", "00000255.tif",
    ),
    "SRC-DE-FES-SPDPD-BDJ-19521027": (
        "1952-10-27", "521027.pdf",
        "12e0da64ad637156d45cc2ae2f99fcff76cb964dd3ad9c9347b4b45f03ffc3e1",
        "S. 6–7", "00000339.tif",
    ),
}

CLAIM_SOURCES = {
    "CLM-DE-BDJ-033": "SRC-DE-FES-SPDPD-BDJ-19521009",
    "CLM-DE-BDJ-034": "SRC-DE-FES-SPDPD-BDJ-19521010",
    "CLM-DE-BDJ-035": "SRC-DE-FES-SPDPD-BDJ-19521010",
    "CLM-DE-BDJ-036": "SRC-DE-FES-SPDPD-BDJ-19521027",
}


class SPDPressedienstBDJ1952Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = yaml.safe_load(SOURCE_PATH.read_text(encoding="utf-8"))["sources"]
        cls.case_text = CASE_PATH.read_text(encoding="utf-8")
        cls.frontmatter = yaml.safe_load(cls.case_text.split("\n---\n", 1)[0][4:])
        cls.catalog = CATALOG_PATH.read_text(encoding="utf-8")

    def test_immutable_archive_identity_and_source_registration(self) -> None:
        ids = [x["id"] for x in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for key, (date, file, sha, pages, tiff) in ORIGINALS.items():
            with self.subTest(source_id=key):
                found = [x for x in self.sources if x["id"] == key]
                self.assertEqual(len(found), 1)
                original = found[0]
                self.assertEqual(original["date"], date)
                self.assertEqual(original["url"], "https://library.fes.de/spdpd/1952/" + file)
                self.assertEqual(original["sha256"], sha)
                self.assertRegex(sha, r"^[0-9a-f]{64}$")
                self.assertIn(pages, original["locator"])
                self.assertIn(tiff, original["locator"])
                self.assertTrue(original["primary"])
                self.assertEqual(original["tier"], "A")
                self.assertIn(key, self.catalog)
                self.assertIn(original["url"], self.catalog)

    def test_four_explicit_claims_have_visible_source_bindings(self) -> None:
        claims = {c["id"]: c for c in self.frontmatter["claims"]}
        for claim_id, source_id in CLAIM_SOURCES.items():
            with self.subTest(claim_id=claim_id):
                claim = claims[claim_id]
                self.assertEqual(claim["classification"], "fact")
                self.assertEqual(claim["evidence_level"], "established")
                self.assertEqual(claim["sources"], [source_id])
                self.assertEqual([e["source"] for e in claim["evidence"]], [source_id])
                self.assertIn(source_id, self.frontmatter["sources"])
                for field in ("counterevidence", "alternatives", "missing_evidence", "falsification"):
                    self.assertIn(field, claim)
                self.assertIn("supports", claim["scope"])
                self.assertIn("does_not_support", claim["scope"])
                self.assertIn(f"- **`{claim_id}` — belegt:** {claim['text']}", self.case_text)

    def test_government_contacts_are_source_allegations_not_payments(self) -> None:
        claims = {c["id"]: c for c in self.frontmatter["claims"]}
        a = claims["CLM-DE-BDJ-034"]
        b = claims["CLM-DE-BDJ-035"]
        self.assertIn("Bundesministeriums für gesamtdeutsche Fragen", a["text"])
        self.assertIn("Bundesinnenministerium", a["text"])
        self.assertIn("Pfälzische Industrie- und Handelsblatt", b["text"])
        self.assertIn("Deutsche Industrie- und Handelstag", b["text"])
        for claim in (a, b):
            self.assertTrue(claim["missing_evidence"])
            self.assertTrue(claim["scope"]["does_not_support"])
        self.assertNotIn("DIHT überwies nachweislich", self.case_text)
        self.assertNotIn("BMI zahlte dem Technischen Dienst nachweislich", self.case_text)

    def test_confidential_memo_quote_is_not_confused_with_original_manuscript(self) -> None:
        claim = next(x for x in self.frontmatter["claims"] if x["id"] == "CLM-DE-BDJ-036")
        self.assertIn("streng vertraulich", claim["text"])
        self.assertIn("Technischen Dienst", claim["text"])
        self.assertIn("Lehrs Trennungsdarstellung", claim["text"])
        self.assertIn("Denkschrift im Original", " ".join(claim["missing_evidence"]))
        self.assertIn("SRC-DE-BT-BDJ-19521023", [x["source"] for x in claim["counterevidence"]])
        self.assertIn("23.10.1952", self.case_text)

    def test_october_1952_and_january_1953_book_title_forms_are_distinct(self) -> None:
        self.assertIn("Bürger und Partisan", self.case_text)
        self.assertIn("Bürger und Partisanen", self.case_text)
        self.assertIn("1952", self.case_text)
        self.assertIn("1953", self.case_text)
        self.assertIn("SRC-DE-FES-SPDPD-BDJ-19530124", self.frontmatter["sources"])


if __name__ == "__main__":
    unittest.main()