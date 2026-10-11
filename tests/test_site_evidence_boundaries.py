"""Guard material historical counterfindings when simplifying the public website."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class WebsiteEvidenceBoundaryTests(unittest.TestCase):
    def test_causation_and_missing_evidence_stay_explicit(self) -> None:
        text = (ROOT / "METHODOLOGY.md").read_text(encoding="utf-8")
        self.assertIn("Politischer Nutzen nach einem Ereignis begründet für sich weder Absicht noch Urheberschaft.", text)
        self.assertIn("eigenständigen Kausalbehauptungen", text)
        self.assertIn("Eine dokumentierte Verbindung beweist keinen Einfluss", text)
        self.assertIn("bislang nicht registrierte Gegenbelege", text)
        self.assertIn("Ebene 1 oder 2 trägt noch keinen Schluss auf Ebene 3 oder 4", text)

    def test_critical_counterfindings_remain_in_readable_case_leads(self) -> None:
        nsu = (DOCS / "faelle/de/nsu-yozgat-temme.md").read_text(encoding="utf-8")
        lead = nsu.split("## Einzelclaim-Prüfung", 1)[0]
        self.assertIn("ohne Nachweis seiner Tatbeteiligung", lead)
        self.assertIn("Eine absichtliche Strafvereitelung folgt daraus bislang nicht", lead)
        labelle = (DOCS / "faelle/de/la-belle-1986.md").read_text(encoding="utf-8")
        self.assertIn("Eine gemeinsame Informationsquelle der beiden Warnketten ist bislang nicht dokumentiert", labelle)

    def test_sources_retain_substantive_negative_findings(self) -> None:
        wsg = (DOCS / "quellen/oktoberfestattentat-1980-spurenpruefung.md").read_text(encoding="utf-8")
        for marker in (
            "keinen fortdauernden Kontakt bis zum Anschlag 1980",
            "Ein zweiter Zünder war hier eine Arbeitshypothese",
            "weder einen MfS-Informanten innerhalb der Soko",
            "Zusammenhang dieser WSG-Asservate mit dem Oktoberfestsprengsatz ist offen",
            "weder staatliche WSG-Geldgeber noch einen konkreten staatlichen Geldtransfer",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, wsg)
        film = (DOCS / "quellen/panorama-1971-filmanalyse.md").read_text(encoding="utf-8")
        self.assertIn("Quellenstatus, Beleggrenze und Originalprüfung", film)
        self.assertIn("keine gerichtliche Feststellung oder Identifizierung eines Führungsoffiziers", film)
        self.assertIn("keine eigene Augenzeugenschaft", film)

    def test_mermaid_has_visible_page_not_collapsed_panel(self) -> None:
        table = (DOCS / "generated/network.md").read_text(encoding="utf-8")
        graph = (DOCS / "generated/network-graph.md").read_text(encoding="utf-8")
        self.assertIn("[Netzwerkdiagramm öffnen](network-graph.md)", table)
        self.assertNotIn("```mermaid", table)
        self.assertIn("```mermaid", graph)
        self.assertIn("flowchart LR", graph)
        self.assertNotIn("??? info", graph)


if __name__ == "__main__":
    unittest.main()
