"""Revisionssichere Quellenprüfung des CIA-LCPROWL-Amendments 3 (1952)."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/lcprowl-amendment3-1952.md"
NAV = ROOT / "mkdocs.yml"


class LCPROWLAmendment3Studies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = STUDY.read_text(encoding="utf-8")

    def test_primary_cia_record_and_content_digest(self):
        for marker in (
            "LCPROWL VOL. 1_0036",
            "20250220053745id_",
            "cf3f5edb13d77afa6559d392959f1e78bf6cb4213bf6271c913b0dbcc890a736",
            "Record Group 263",
            "Entry ZZ-19",
            "PDF-S. 5",
            "PDF-S. 7",
            "PDF-S. 9",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_budget_approval_request_and_payment_not_conflated(self):
        for marker in (
            "3. Juli 1951",
            "125.000 US-Dollar",
            "13 Monate",
            "1. Juni 1951",
            "27.656 US-Dollar",
            "32.000 US-Dollar",
            "beantragt",
            "verausgabt",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)
        self.assertNotIn("157.000 US-Dollar bewilligt", self.text)

    def test_reported_1952_strength_not_claimed_as_7000_actual_members(self):
        for marker in (
            "mehr als 3.000",
            "nicht rekrutiert",
            "125 Sicherheitsanfragen",
            "100 Freigaben",
            "mehr als 1.700",
            "50 Führungskräfte",
            "400 weitere Personen",
            "7.000",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)
        self.assertNotIn("7.000 ausgebildete", self.text)

    def test_industrial_cover_and_original_document_conflict(self):
        for marker in (
            "Sperrholzunternehmen",
            "15 Mitarbeiter",
            "Schallplattenfirma",
            "17. November 1950",
            "21. Dezember 1950",
            "unterschiedliche",
            "OPC",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_opc_financial_control_and_domestic_procurement(self):
        for marker in (
            "PDF-S. 9",
            "OPC-Zentrale",
            "Gesamtfinanzen",
            "400 deutschen Agenten",
            "35 hauptamtlich bezahlte Agenten",
            "DTSQUASH",
            "aus der deutschen Wirtschaft",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_planned_policy_handoff_remains_distinct_from_execution(self):
        for marker in (
            "Bonner Regierung",
            "Europäische Verteidigungsgemeinschaft",
            "westdeutsche Behörde",
            "Material, Anleitung und technisches Know-how",
            "amerikanische Politikoption",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_exact_navigation_once(self):
        entry = "quellen/lcprowl-amendment3-1952.md"
        self.assertEqual(NAV.read_text(encoding="utf-8").count(entry), 1)


if __name__ == "__main__":
    unittest.main()