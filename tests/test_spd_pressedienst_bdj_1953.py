"""Regression tests for contemporaneous FES BDJ reporting in 1953."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "sources.yml"
CASE = ROOT / "docs" / "faelle" / "de" / "technischer-dienst-bdj.md"
CATALOG = ROOT / "docs" / "quellen" / "index.md"

ORIGINALS = {
    "SRC-DE-FES-SPDPD-BDJ-19530124": {
        "date": "1953-01-24",
        "pdf": "530124.pdf",
        "sha256": "6d598917e6e56f264c844df9fd4b116d07eb54ebe4b077982007250c12ffe19c",
        "pages": "S. 1–2",
    },
    "SRC-DE-FES-SPDPD-BDJ-19530312": {
        "date": "1953-03-12",
        "pdf": "530312.pdf",
        "sha256": "873422812dcb9e6709a0b516aee19ab699086725b4e831c5efa97a37f28ec025",
        "pages": "S. 4–5",
    },
    "SRC-DE-FES-SPDPD-BDJ-19530717": {
        "date": "1953-07-17",
        "pdf": "530717.pdf",
        "sha256": "50eb71a849476e72d2ba390b1afb390b0ec59581761a1f638cef6d9ff4b58a06",
        "pages": "S. 5–6",
    },
}


class SPDPressedienstBDJ1953Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))["sources"]
        cls.metadata = yaml.safe_load(CASE.read_text(encoding="utf-8").split("\n---\n", 2)[0][4:])
        cls.case_text = CASE.read_text(encoding="utf-8")
        cls.catalog = CATALOG.read_text(encoding="utf-8")

    def test_three_archive_originals_have_distinct_verified_identity(self) -> None:
        ids = [entry.get("id") for entry in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for source_id, expected in ORIGINALS.items():
            with self.subTest(source_id=source_id):
                matched = [entry for entry in self.sources if entry.get("id") == source_id]
                self.assertEqual(len(matched), 1)
                entry = matched[0]
                self.assertEqual(entry["date"], expected["date"])
                self.assertEqual(entry["url"], "https://library.fes.de/spdpd/1953/" + expected["pdf"])
                self.assertEqual(entry["sha256"], expected["sha256"])
                self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(entry["primary"])
                self.assertEqual(entry["tier"], "A")
                self.assertIn(expected["pages"], entry["locator"])
                self.assertIn("400 dpi", entry["locator"])
                self.assertIn(source_id, self.catalog)
                self.assertIn(entry["url"], self.catalog)

    def test_source_aware_structured_claims_and_text(self) -> None:
        claims = {claim["id"]: claim for claim in self.metadata["claims"]}
        expected = {
            "CLM-DE-BDJ-029": "SRC-DE-FES-SPDPD-BDJ-19530124",
            "CLM-DE-BDJ-030": "SRC-DE-FES-SPDPD-BDJ-19530312",
            "CLM-DE-BDJ-031": "SRC-DE-FES-SPDPD-BDJ-19530312",
            "CLM-DE-BDJ-032": "SRC-DE-FES-SPDPD-BDJ-19530717",
        }
        for claim_id, source_id in expected.items():
            with self.subTest(claim_id=claim_id):
                claim = claims[claim_id]
                self.assertIn(source_id, claim["sources"])
                self.assertIn(source_id, self.metadata["sources"])
                self.assertEqual(claim["classification"], "fact")
                self.assertIn("counterevidence", claim)
                self.assertIn("alternatives", claim)
                self.assertIn("missing_evidence", claim)
                self.assertIn("falsification", claim)
                self.assertIn("supports", claim["scope"])
                self.assertIn("does_not_support", claim["scope"])
                self.assertIn(claim_id, self.case_text)
        self.assertIn("SPD-Originalausgaben 1953", self.case_text)

    def test_four_industrial_names_are_attributed_not_money_transfers(self) -> None:
        claims = {claim["id"]: claim for claim in self.metadata["claims"]}
        claim = claims["CLM-DE-BDJ-030"]
        for name in ("Salamander-Schuhfabrik", "Coca-Cola-GmbH", "Bosch-Auto-Licht", "Reemtsma"):
            with self.subTest(name=name):
                self.assertIn(name, claim["text"])
                self.assertIn(name, self.case_text)
        for amount in ("1,7 Mio. DM", "500.000 DM", "30.000 DM"):
            self.assertIn(amount, claim["text"])
        self.assertIn("SPD-Pressedienst", claim["text"])
        self.assertIn("nicht verbucht", claim["scope"]["does_not_support"].lower())
        self.assertNotIn("finanzierte den BDJ nachweislich", self.case_text)

    def test_july_interview_not_confused_with_official_committee_report(self) -> None:
        self.assertIn("vier Wochen", self.metadata["claims"][-1]["text"])
        self.assertIn("BT-Drs. 1/4644", self.case_text)
        self.assertIn("im Plenum", self.case_text)
        self.assertIn("nicht mehr behandelt", self.case_text)
        self.assertIn("SRC-DE-BT-04644-1953", self.metadata["sources"])
        self.assertIn("CLM-DE-BDJ-001", self.case_text)

    def test_original_company_issue_is_linked_to_cia_not_summed(self) -> None:
        self.assertIn("FRAN 1551", self.case_text)
        self.assertIn("12.02.1953", self.case_text)
        self.assertIn("15.04.1953", self.case_text)
        self.assertIn("40.000-DM-Fehlbetrag", self.case_text)
        self.assertIn("CLM-DE-BDJ-025", self.case_text)


if __name__ == "__main__":
    unittest.main()