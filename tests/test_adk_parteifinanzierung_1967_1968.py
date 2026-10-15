"""Primary source and claim-boundary regression for ADK state-funding research, 1967–68."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs/quellen/adk-bundesmittel-haushaltsverhandlungen-1967-1968.md"
SOURCES = {
    "SRC-DE-KGPARL-CDU-ADK-19670606": "cdu-csu-05_1967-06-06-t1505_WZ.html",
    "SRC-DE-KGPARL-SPD-ADK-19670606": "spd-05_1967-06-06-t1705_EP.html",
    "SRC-DE-BT-ADK-PLENUM-19670607": "dserver.bundestag.de/btp/05/05111.pdf#page=35",
    "SRC-DE-KGPARL-CDU-ADK-19671205": "cdu-csu-05_1967-12-05-t1507_WZ.html",
    "SRC-DE-KGPARL-CDU-ADK-19671212": "cdu-csu-05_1967-12-12-t1507_WZ.html",
    "SRC-DE-BT-ADK-HAUSHALT-19680315": "dserver.bundestag.de/btd/05/027/0502704.pdf#page=4",
    "SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968": "dserver.bundestag.de/btd/05/027/0502731zu.pdf#page=6",
    "SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968": "dserver.bundestag.de/btd/05/027/0502731.pdf#page=1",
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
        self.assertIn("Weder der Vollzug der Verlagerung noch der endgültige Ausschluss", self.study)
        self.assertIn("kein ADK-Empfängerbetrag", self.study)
        self.assertIn("hypothetisches Kabinettsbeispiel", self.study)

    def test_no_documented_staff_transfer_or_continued_payment_is_invented(self):
        # Editorial note 7 reports a proposal to examine a staff transfer, not its execution.
        self.assertIn("nur editorisch überlieferte Hinweis auf eine geplante Prüfung", self.study)
        self.assertIn("Weder eine tatsächlich erfolgte Personalübernahme", self.study)
        self.assertIn("Fortsetzung eines konkreten öffentlichen Zahlungsstroms", self.study)
        for unsupported in (
            "Vorschläge, den öffentlichen Geldfluss trotz Koalitionswiderstands organisatorisch weiterzuführen",
            "belegt die Fortsetzung öffentlicher ADK-Zahlungen",
            "vollzogene Übernahme von ADK-Personal",
        ):
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported, self.study)

    def test_kiesinger_adk_is_question_context_not_name_quote(self):
        self.assertIn("Burgemeister nennt die ADK in seiner Frage ausdrücklich", self.study)
        self.assertIn("Kiesinger nennt die ADK in seiner eigenen Antwort nicht erneut ausdrücklich", self.study)
        self.assertIn("mehrere frühere Wahlkampfunterstützer", self.study)
        for overstatement in (
            "die direkte Einordnung durch den Bundeskanzler",
            "Kiesinger nennt die ADK ausdrücklich",
            "Kiesinger bezeichnet die ADK ausdrücklich",
        ):
            self.assertNotIn(overstatement, self.study)

    def test_adk_budget_years_and_stages_are_explicitly_separated(self):
        for marker in (
            "am **06.06.1967**",
            "7 Mio. DM",
            "für 1967 von 13 Mio. auf 8 Mio. DM",
            "anderes Haushaltsjahr (1968)",
            "8 Mio. DM im Regierungsentwurf sowie 7 Mio. DM in der Ausschussfassung",
            "bleibt ohne weitere Haushalts- und Beratungsakten **ungeklärt**",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.study)
        self.assertNotIn("7 Mio. DM als tatsächlich an die ADK gezahlt", self.study)

    def test_secondary_opelland_is_not_mislabeled_as_kas_primary_source(self):
        self.assertIn("historischen Sekundärdarstellung", self.study)
        self.assertIn("institutionellen Eigenauskunft der KAS", self.study)
        self.assertIn("historische Sekundärdarstellung von Torsten Oppelland", self.study)
        self.assertIn("keine KAS-Eigenauskunft", self.study)
        self.assertNotIn("institutionelle KAS-Darstellung zur ADK", self.study)
        self.assertNotIn("zwei **institutionellen Eigenveröffentlichungen**", self.study)

    def test_constitutional_original_uses_registered_bpb_print(self):
        self.assertIn("www.bpb.de/shop/zeitschriften/apuz/archiv/527544/", self.study)
        self.assertIn("zeitgenössisch abgedruckt in *APuZ* 32/1966", self.study)
        self.assertNotIn("SharedDocs/Entscheidungen/EN/1966", self.study)

    def test_committee_proposal_is_in_report_zu_v2731_not_just_equal_numbers(self):
        self.assertIn("0502731zu.pdf#page=6", self.study)
        self.assertIn("SRC-DE-BT-ADK-BERICHT-ZU-V2731-1968", self.study)
        self.assertIn("SRC-DE-BT-HAUSHALTSGESETZ-V2731-1968", self.study)
        self.assertIn("V/2704", self.study)
        self.assertIn("von Titel 300 nach Titel 314 zu verlagern", self.study)
        self.assertIn("im selben Berichtsabschnitt unmittelbar nacheinander vorgeschlagen", self.study)
        self.assertIn("Welcher der beiden zuvor genannten Titel", self.study)
        self.assertNotIn("bewusste Verknüpfung beider Titeländerungen", self.study)
        self.assertIn("explizite ADK-bezogene Ausschussabsicht", self.study)
        self.assertIn("Weder der Vollzug der Verlagerung", self.study)
        self.assertIn("keinen fortgesetzten öffentlichen Zahlungsstrom an die ADK", self.study)
        self.assertNotIn("Verlagerung von 1 Mio. DM wurde 1968 ausgeführt", self.study)

    def test_editorial_sperrvermerk_explained_by_second_original_but_not_final_verification(self):
        self.assertIn("editorische Fußnote 20", self.study)
        self.assertIn("fünf Druckseiten den Ausschluss", self.study)
        self.assertIn("schriftlichen Bericht zur Gesamtvorlage zu V/2731", self.study)
        self.assertIn("alleinigen V/2704-Verweis", self.study)
        self.assertIn("schriftliche Berichterstattung zu V/2731", self.study)
        self.assertIn("förmlich verbindlicher", self.study)
        self.assertNotIn("V/2704 belegt einen ADK-Sperrvermerk", self.study)
        self.assertNotIn("sicher endgültig gestrichen", self.study)

    def test_evidence_table_separates_grant_plan_and_editorial_material(self):
        self.assertIn("regulären ADK-Jahreszuwendung 1967 (Plan)", self.study)
        self.assertIn("KGParl 26.03.1968, editorische Fußnote 7", self.study)
        self.assertIn("editorische Fußnote 20", self.study)
        self.assertNotIn("¾ eines Jahresansatzes 1967", self.study)
        self.assertNotIn("KGParl-Fußnote 26.03.1968 |", self.study)

    def test_section_headings_do_not_infer_illegal_party_payments(self):
        self.assertIn("Fraktionen verhandeln die ADK-Förderung", self.study)
        self.assertNotIn("Fraktionen benennen ihren Finanzierungsmechanismus", self.study)
        self.assertNotIn("institutionelle **historische Rückschau**", self.study)
        self.assertNotIn("nach institutioneller Rückschau", self.study)

    def test_1968_edition_citation_identifies_original_and_secondary_footnote(self):
        self.assertIn("08-001-1016/1", self.study)
        self.assertIn("10.82988/b995-sj37", self.study)
        self.assertIn("TOP 3 Bundeshaushalt 1968", self.study)
        self.assertIn("www.fraktionsprotokolle.de/cdu-csu-05_1968-04-02", self.study)

    def test_abstract_cannot_claim_named_restricted_title_or_finished_transfer(self):
        for marker in (
            "Drucksachenbeziehung:",
            "V/2704",
            "V/2731",
            "mündliche Bericht zum Haushaltsgesetz 1968",
            "schriftliche Ausschussbericht",
            "nicht** als unmittelbare schriftliche Begründung allein zu V/2704",
            "Titel 300 oder 314",
            "nicht mit Rafferts gesonderter Angabe",
            "keine voneinander unabhängigen Bestätigungen",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.study)
        self.assertNotIn("aus dem betreffenden Titel auszuschließen", self.study)
        self.assertNotIn("im endgültigen Haushalt umgewidmet", self.study)

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
            "mündliche Bericht und Ausschussantrag zu Einzelplan 04",
            "keine hier nachgewiesene verfassungsgerichtliche Entscheidung",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.study)

    def test_constitutional_court_1966_distinguishes_titles_and_legal_entities(self):
        for marker in (
            "19. Juli 1966", "2 BvF 1/65", "BVerfGE 20, 56",
            "38 Mio. DM", "Einzelplan 06 / Kapitel 02 / Titel 612",
            "Erstattung notwendiger angemessener Wahlkampfkosten",
            "06 02/612 statt 04 03/300",
            "Zweck-, Leistungs- und Empfängerprüfung",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.study)

    def test_kas_spr_liquidation_is_not_a_federal_money_trace(self):
        self.assertIn("www.kas.de/de/unterstuetzen-sie-uns", self.study)
        self.assertIn("Liquidationsbeschluss", self.study)
        self.assertIn("2003", self.study)
        self.assertIn("2001", self.study)
        self.assertIn("Fonds SPR", self.study)
        self.assertIn("1956", self.study)
        self.assertIn("Herkunft des übergegangenen Vermögens", self.study)
        self.assertIn("2003 noch öffentliche ADK- oder BPA-Mittel", self.study)
        self.assertIn("Vereinsregister/Abwicklungsakten", self.study)

    def test_adk_person_identity_and_archive_followup(self):
        self.assertIn("Hans Edgar Jahn", self.study)
        self.assertNotIn("Werner Jahn", self.study)
        self.assertIn("ACDP-Bestand 01-753", self.study)
        self.assertIn("ACDP-Archivfindbuch der Konrad-Adenauer-Stiftung", self.study)
        self.assertNotIn("Das amtliche [DDB-/ACDP-Findbuch", self.study)
        self.assertIn("ACDP 01-226-010", self.study)
        self.assertIn("BArch B 145", self.study)
        self.assertIn("Studiengesellschaft Public Relations e.V.", self.study)
        self.assertIn("kein vorweggenommener Nachweis", self.study)


if __name__ == "__main__":
    unittest.main()
