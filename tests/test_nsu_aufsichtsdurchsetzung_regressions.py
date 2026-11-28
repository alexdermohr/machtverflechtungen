"""Guard against confusing procedural rejection with a merits decision."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY = "nsu-aufsichtsdurchsetzung-bfv-bnd-2023-2026.md"


class NsuAufsichtsdurchsetzungTests(unittest.TestCase):
    def setUp(self):
        self.rows = {r["id"]: r for r in yaml.safe_load(
            (ROOT / "data/relations.yml").read_text()
        )["relations"]}
        self.registry = yaml.safe_load(
            (ROOT / "data/research-integrations.yml").read_text()
        )["studies"][STUDY]

    def test_distinct_oversight_conflict_and_procedural_disposition(self):
        for rid, date, actor in (
            ("REL-DE-BND-BFDI-EINSICHTSVERWEIGERUNG-2024-001", "2024-03-22", "ORG-DE-BND"),
            ("REL-DE-BKAMT-BFDI-BEANSTANDUNG-2024-001", "2024-04-11", "ORG-DE-BUNDESKANZLERAMT"),
            ("REL-DE-BVERWG-BFDI-KLAGEUNZULAESSIG-2026-001", "2026-03-04", "ORG-DE-BVERWG"),
        ):
            row = self.rows[rid]
            self.assertEqual(str(row["period"]["start"]), date)
            self.assertEqual((row["from"], row["to"]), (actor, "ORG-DE-BFD"))
            self.assertEqual(row["sources"], ["SRC-DE-BVERWG-BFDI-BND-6A224-20260304"])
            self.assertIn(rid, self.registry["relation_ids"])
        verdict = self.rows["REL-DE-BVERWG-BFDI-KLAGEUNZULAESSIG-2026-001"]
        self.assertIn("keine materielle Entscheidung", verdict["label"])
        self.assertEqual(verdict["type"], "dismissed_oversight_action_as_inadmissible")

    def test_limited_positive_findings_do_not_erase_defects(self):
        self.assertIn("keine allgemeine Freigabe", self.rows[
            "REL-DE-BFDI-BFV-VERBUNDDATEIEN-2025-001"]["label"])
        self.assertIn("kein Nachweis bereits vollzogener Reform", self.rows[
            "REL-DE-BFDI-RED-REFORM-2025-001"]["label"])
        self.assertIn("erneut Dokumentationsdefizite", self.rows[
            "REL-DE-BFDI-BFV-DOKUMENTATION-2026-001"]["label"])
        self.assertIn("BfV-Prüfung bei Redaktionsschluss nicht abgeschlossen", self.rows[
            "REL-DE-BFDI-MAD-AUSLANDSUEBERMITTLUNG-2026-001"]["label"])
        self.assertEqual(len(set(self.registry["relation_ids"])), 10)


if __name__ == "__main__":
    unittest.main()
