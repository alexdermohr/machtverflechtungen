"""Regression checks for the French 1RP BDJ/VFF archival finding aid."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/bdj-vff-franzoesische-archive-1946-1955.md"
SOURCE = "SRC-FR-MAE-1RP-FINDBUCH-2023"
FASCICLES = (
    "1RP 11/6",
    "1RP 34/2",
    "1RP 233/4",
    "1RP 233/7",
    "1RP 438/3",
    "1RP 2262/1",
    "1RP 2950/3",
)
PDF = "https://archivesdiplomatiques.diplomatie.gouv.fr/media/894739ac-3d8f-4abb-bd77-171965ecbeab.pdf"


class French1RPArchiveTests(unittest.TestCase):
    def test_exact_one_primary_finding_aid_not_historical_files(self):
        sources = yaml.safe_load((ROOT / "data/sources.yml").read_text(encoding="utf-8"))["sources"]
        matching = [s for s in sources if s["id"] == SOURCE]
        self.assertEqual(len(matching), 1)
        src = matching[0]
        self.assertEqual(src["type"], "archival_finding_aid")
        self.assertTrue(src["primary"])
        self.assertEqual(src["tier"], "A")
        self.assertEqual(src["url"], PDF)
        self.assertIn("nicht eingesehen", src["notes"])

    def test_complete_seven_fascicles_and_separate_intelligence_entry(self):
        study = STUDY.read_text(encoding="utf-8")
        for signature in FASCICLES:
            with self.subTest(signature=signature):
                self.assertIn(signature, study)
        self.assertIn("1RP 16/5", study)
        self.assertIn("nicht selbst eingesehen", study)
        for page in (17, 18, 23, 53, 85, 267, 343):
            self.assertIn(f"{PDF}#page={page}", study)

    def test_study_appears_in_site_navigation_and_catalog(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("quellen/bdj-vff-franzoesische-archive-1946-1955.md", nav)
        self.assertIn("index.md#src-fr-mae-1rp-findbuch-2023", STUDY.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
