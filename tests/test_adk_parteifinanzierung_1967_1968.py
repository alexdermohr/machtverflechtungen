"""Primary source and claim-boundary regression for ADK state-funding research, 1967–68."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/adk-parteifinanzierung-bundeskasse-1967-1968.md"
SOURCES = {
    "SRC-DE-KGPARL-CDU-ADK-19670606": "cdu-csu-05_1967-06-06-t1505_WZ.html",
    "SRC-DE-KGPARL-SPD-ADK-19670606": "spd-05_1967-06-06-t1705_EP.html",
    "SRC-DE-BT-ADK-PLENUM-19670607": "dserver.bundestag.de/btp/05/05111.pdf#page=35",
    "SRC-DE-KGPARL-CDU-ADK-19671205": "cdu-csu-05_1967-12-05-t1507_WZ.html",
    "SRC-DE-KGPARL-CDU-ADK-19671212": "cdu-csu-05_1967-12-12-t1507_WZ.html",
    "SRC-DE-BT-ADK-HAUSHALT-19680315": "dserver.bundestag.de/btd/05/027/0502704.pdf#page=4",
    "SRC-DE-KGPARL-CDU-ADK-19680326": "cdu-csu-05_1968-03-26-t1832_WZ.html",
    "SRC-DE-KGPARL-CDU-ADK-19680402": "cdu-csu-05_1968-04-02-t0805_WZ.html",
}


class AdkPrimary1967To1968Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study = STUDY.read_text(encoding="utf-8")

    def test_original_sources_with_direct_links(self):
        for identifier, url_suffix in SOURCES.items():
            with self.subTest(source=identifier):
                self.assertIn(url_suffix, self.study)

    def test_money_claims_do_not_treat_budget_titles_as_adk_payments(self):
        for amount in (
            "8.000.000 DM", "7.000.000 DM", "6.000.000 DM",
            "1.000.000 DM", "2 Mio. auf 1,8 Mio. DM",
        ):
            with self.subTest(amount=amount):
                self.assertIn(amount, self.study)
        self.assertIn("kein", self.study.lower())
        self.assertIn("keine belegte Zweckumbuchung", self.study)
        self.assertIn("kein** ADK-Empfängerbetrag", self.study)
        self.assertIn("hypothetisches Kabinettsbeispiel", self.study)

    def test_1967_quarter_fraction_is_only_proposed_financing(self):
        self.assertIn("6/12", self.study)
        self.assertIn("6/24", self.study)
        self.assertIn("9/12 = 75 %", self.study)
        self.assertIn("sofern der Plan umgesetzt", self.study)
        self.assertIn("nicht der Nachweis", self.study)

    def test_primary_and_editorial_provenance_are_distinguished(self):
        for marker in (
            "PDF-Bildseiten", "nicht eigenständig eingesehen",
            "editorische Fußnote 7", "nur eine editorische Sekundärangabe",
            "Antrag des Ausschusses an den Bundestag",
            "keine hier nachgewiesene verfassungsgerichtliche Entscheidung",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.study)

    def test_adk_person_identity_and_archive_followup(self):
        self.assertIn("Hans Edgar Jahn", self.study)
        self.assertNotIn("Werner Jahn", self.study)
        self.assertIn("ACDP-Bestand 01-753", self.study)
        self.assertIn("ACDP 01-226-010", self.study)
        self.assertIn("BArch B 145", self.study)
        self.assertIn("Studiengesellschaft Public Relations e.V.", self.study)
        self.assertIn("kein vorweggenommener Nachweis", self.study)


if __name__ == "__main__":
    unittest.main()
