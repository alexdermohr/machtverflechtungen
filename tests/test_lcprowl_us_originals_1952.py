"""Exact-facsimile source regressions for LCPROWL US intervention reports (1952–53)."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "docs/quellen/lcprowl-1952-1953-us-ermittlungen.md"
PREVIOUS = ROOT / "docs/quellen/lcprowl-1950-opc-planung.md"
BDJ_CASE = ROOT / "docs/faelle/de/technischer-dienst-bdj.md"
NAVIGATION = ROOT / "mkdocs.yml"

ORIGINALS = (
    ("VOL. 4_0030", "LCPROWLVOL4-0030", "VOL.%204_0030.pdf",
     "1051f9972fce044286d5cac74bec8c182ec25a4003411ccb96032467b0894a1c",
     "2b7459805f4353a7ea83e02ee97924b5"),
    ("VOL. 4_0039", "LCPROWLVOL4-0039", "VOL.%204_0039.pdf",
     "29bf5550072efd35871891ad057a232a32ee2cdc951f30520f7bc56fc78f5490",
     "07cb866066bdf9d5ce5d17b3d5a0ac95"),
    ("VOL. 3_0009", "LCPROWLVOL3-0009", "VOL.%203_0009.pdf",
     "29e740de9fb7b567a208dc5c72ed32ac5c91df8b92c4f741a793aa10b881929b",
     "f90afea98cfc61da449af8a19b511d91"),
    ("VOL. 4_0040", "LCPROWLVOL4-0040", "VOL.%204_0040.pdf",
     "79c540aab4ca4093b4767899e9b6a45f8a03f1204242ed3952d03e518ced6204",
     "02fbcf3199e1ff4c9987c81fff2c36ce"),
    ("VOL. 1_0033", "LCPROWLVOL1-0033", "VOL.%201_0033.pdf",
     "c04a0f51e7cbf5037d115b3f5efd6df007ad2b5e828dc8cd477f5708848c6747",
     "ae250501906762bd3772c921d0b96a6a"),
    ("VOL. 3_0017", "LCPROWLVOL3-0017", "VOL.%203_0017.pdf",
     "2a0c1acb3d13ab90c5c0f7f1b14f6ae16a354811d32190f40e3bd0bbd6a263a0",
     "2c28d8c402cc2c31f61f85a1e1622438"),
    ("VOL. 4_0054", "LCPROWLVOL4-0054", "VOL.%204_0054.pdf",
     "da76e303a7ce59ad477749d381c6436fae284840115ca6d299009031ec2c8c49",
     "98f26bd8f4b965c3483dc5aba3719202"),
    ("VOL. 2_0050", "LCPROWLVOL2-0050", "VOL.%202_0050.pdf",
     "d60c92a2b1df34fbe0055d622abe65db1b8d422a57d4b0de8fcab5c22b993c8e",
     "96475f631cd53e9233f83b02f0a8bdea"),
    ("VOL. 2_0049", "LCPROWLVOL2-0049", "VOL.%202_0049.pdf",
     "26e62a748bc0e3a454ce8e245058037121ed1dff64a1b6c4cd2dab43c12065f6",
     "3d8651f4861c886a2dc112e2e11ba95b"),
    ("VOL. 2_0046", "LCPROWLVOL2-0046", "VOL.%202_0046.pdf",
     "4f616e786c47556accfbc057984519f7be5235eea8514e23d8487c107f2c4c9d",
     "28e55576f0161da4953bec5ffba09a7d"),
    ("VOL. 2_0047", "LCPROWLVOL2-0047", "VOL.%202_0047.pdf",
     "3765f020b273d66106abe08eaa6c34cea292ca2187dc12d9b9b4c4dcd798e5d0",
     "333316d3bd00b48c1abd766b682ba942"),
    ("VOL. 2_0048", "LCPROWLVOL2-0048", "VOL.%202_0048.pdf",
     "64a74527c67fd42894abeea059044150aa1c4aeec82e0888e70fde951f2ad75e",
     "3782d5e9e9cf896aa2952b7ede30e185"),
)


class LcprowlUSOriginals1952(unittest.TestCase):
    def test_each_cia_archival_original_has_immutable_locator(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for label, item, file_part, sha, md5 in ORIGINALS:
            with self.subTest(label=label):
                self.assertIn(label, article)
                self.assertIn(f"https://archive.org/download/{item}/", article)
                self.assertIn(file_part, article)
                self.assertIn(sha, article)
                self.assertIn(md5, article)
        self.assertIn("NARA", article)
        self.assertIn("PDF-S.", article)

    def test_actual_claims_distinguish_sources_from_inference(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for key in ("Saxer", "Emil Peters", "Schallplatten", "18. September 1952",
                    "23. Oktober 1952", "Robert Lehr", "Zinn", "CIC",
                    "29. Januar 1953", "Franz Halder", "15. Januar 1951",
                    "Akten", "Zeugen", "nicht unwahrhaftig"):
            with self.subTest(key=key):
                self.assertIn(key, article)
        self.assertIn("Bericht", article)
        self.assertIn("Sponsoring", article)
        self.assertIn("Auszahlung", article)
        self.assertNotIn("Saxer überwies nachweislich", article)

    def test_saxer_press_translation_is_attributed_and_names_conflict(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for marker in (
            "Der Spiegel", "15. Oktober 1952",
            "PDF-S. 15", "PDF-S. 17",
            "Emil Peters", "Erwin Peters", "50.000 DM",
            "500–1.000 DM", "1. September 1952", "Worms",
            "Presseübersetzung", "unterschiedlichen Dateihashes",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article)
        self.assertNotIn("Saxer überwies nachweislich", article)

    def test_private_cover_contracts_and_later_cia_self_assessment(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for marker in (
            "23. Dezember 1952", "20. Juli 1951", "11. August 1951", "Otto Schill",
            "Johann Saxer", "Emil Peters", "20.000 DM", "18.000 DM",
            "40.000-DM-Darlehen", "35 m³", "126.000 DM", "4.450 DM",
            "91.000 DM", "QA 1328", "nicht genehmigt",
            "PDF-S. 16–17", "PDF-S. 21–22", "unwirksame Tarnung",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article)
        self.assertNotIn("Saxer überwies nachweislich", article)

    def test_hicog_apartment_cache_source_reconciliation(self):
        """Preserve the apartment location and separately sourced CIA employment."""
        article = ARTICLE.read_text(encoding="utf-8")
        row = next(
            line for line in article.splitlines()
            if line.startswith("| 25. September 1952 |")
        )
        for marker in (
            "fünf Kisten Waffen und Munition im Keller einer HICOG-Wohnung",
            "Schwester eines amerikanischen Stabsmitarbeiters",
            "CIA-Angestellte in Deutschland",
            "`VOL. 4_0039`",
            "`VOL. 4_0030`",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, row)
        self.assertNotIn("in einem Gebäude einer", row)

    def test_justice_ministry_negotiations_and_confidential_draft_1953(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for marker in (
            "10. Februar 1953", "11. Februar 1953", "12. Februar",
            "BONN 0507", "FRAN 1488", "EGQA 8969",
            "Bundesjustizministerium", "Kantor", "Zinn",
            "unterzeichnete Ausfertigung", "Erhard Peters",
            "Rücknahme des Verfahrens", "Erpressung",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article)

    def test_spd_whitebook_first_unpublished_copy_and_company_claim_attribution(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for marker in (
            "12. Februar 1953", "FRAN 1551", "FRAN 1552", "FRAN 1555",
            "noch unveröffentlichten SPD-Weißbuchs", "60 Seiten",
            "Sopade-Denkschriften Nr. 50", "Z 3015/50",
            "Coca-Cola", "Bosch Licht", "vermutlich Reemtsma",
            "500.000 DM", "keine Belege tatsächlicher Überweisungen",
            "Schlussfolgerungen des SPD-Manuskripts",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, article)
        self.assertNotIn("Coca-Cola überwies", article)
        self.assertNotIn("Bosch Licht überwies", article)

    def test_cia_originals_are_listed_exactly_once_in_site_navigation(self):
        self.assertEqual(
            NAVIGATION.read_text(encoding="utf-8").count(
                "quellen/lcprowl-1952-1953-us-ermittlungen.md"
            ), 1,
        )

    def test_february_scope_april_cia_memo_and_bdj_case_status_agree(self):
        article = ARTICLE.read_text(encoding="utf-8")
        case = BDJ_CASE.read_text(encoding="utf-8")
        self.assertIn("1951 bis Februar 1953", article)
        self.assertIn("15. April 1953, LCPROWL VOL. 2_0023", article)
        self.assertIn("VOL.%202_0023.pdf", article)
        self.assertIn("CIA-Originalaktenstudie 1952–1953", case)
        self.assertIn("lcprowl-1952-1953-us-ermittlungen.md", case)
        self.assertNotIn("bisher zugängliche Indextexte", case)

    def test_existing_public_1950_entry_point_links_new_originals(self):
        self.assertIn(
            "(lcprowl-1952-1953-us-ermittlungen.md)",
            PREVIOUS.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()