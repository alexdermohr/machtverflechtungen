from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

import scripts.validate as validate


ROOT = Path(__file__).resolve().parents[1]


class GeminiRegressionTests(unittest.TestCase):
    def test_source_nul_cannot_create_claim_binding_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<p>{claim_id} Präfix{chr(0)} {claim_text}</p>"
        )

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                visible, claim_id, claim_text
            ),
            repr(visible),
        )

    def test_comparison_case_link_rejects_relation_id(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "case.schema.json").read_text(encoding="utf-8")
        )
        item_schema = schema["properties"]["case_links"]["items"]
        link = {
            "kind": "comparison",
            "target": "CASE-DE-THS-BRANDT",
            "basis": "Struktureller Testvergleich ohne Kausalbehauptung.",
            "relation_id": "REL-DE-GEHLEN-001",
        }

        errors = list(Draft202012Validator(item_schema).iter_errors(link))

        self.assertTrue(errors, "comparison links must reject relation_id")


if __name__ == "__main__":
    unittest.main()
