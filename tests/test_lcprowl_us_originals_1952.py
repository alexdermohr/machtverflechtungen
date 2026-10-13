"""Exact-facsimile source regressions for LCPROWL US intervention reports (1952–53)."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "docs/quellen/lcprowl-1952-1953-us-ermittlungen.md"
PREVIOUS = ROOT / "docs/quellen/lcprowl-1950-opc-planung.md"

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

    def test_existing_public_1950_entry_point_links_new_originals(self):
        self.assertIn(
            "(lcprowl-1952-1953-us-ermittlungen.md)",
            PREVIOUS.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
