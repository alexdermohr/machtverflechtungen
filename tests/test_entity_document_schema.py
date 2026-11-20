from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocumentEntitySchemaTests(unittest.TestCase):
    def test_document_ids_are_allowed_for_entities_and_case_actors(self) -> None:
        entity = json.loads((ROOT / "schemas/entity.schema.json").read_text())
        case = json.loads((ROOT / "schemas/case.schema.json").read_text())
        entity_pattern = entity["properties"]["id"]["pattern"]
        actor_pattern = case["properties"]["actors"]["items"]["pattern"]
        for pattern in (entity_pattern, actor_pattern):
            for value in (
                "ORG-DE-TEST", "PER-DE-TEST", "PRG-DE-TEST",
                "DOC-IT-RIZZOLI-P2-AGREEMENT-1980",
            ):
                self.assertIsNotNone(re.fullmatch(pattern, value), value)
            for invalid in ("FAKE-IT-NODE", "doc-it-lower", "DOC-", "ORG spaces"):
                self.assertIsNone(re.fullmatch(pattern, invalid), invalid)

    def test_document_nodes_are_not_mislabeled_as_organizations(self) -> None:
        import yaml

        entities = yaml.safe_load(
            (ROOT / "data/entities.yml").read_text(encoding="utf-8")
        )["entities"]
        contracts = [e for e in entities if e["id"].startswith("DOC-")]
        self.assertGreaterEqual(len(contracts), 2)
        self.assertIn(
            "DOC-IT-DOCUMENTO-BOLOGNA-1982",
            {record["id"] for record in contracts},
        )
        for record in contracts:
            self.assertIn("document", record["type"])
            self.assertGreater(len(record["notes"]), 70)
            self.assertTrue(record["name"])


if __name__ == "__main__":
    unittest.main()