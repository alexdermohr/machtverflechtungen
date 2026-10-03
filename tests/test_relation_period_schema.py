from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class RelationPeriodSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "relation.schema.json").read_text(encoding="utf-8")
        )
        cls.validator = Draft202012Validator(schema)

    @staticmethod
    def _relation() -> dict[str, object]:
        return {
            "id": "REL-TEST-PERIOD-001",
            "from": "PER-TEST-PERSON",
            "to": "ORG-TEST-ORG",
            "type": "documented_contact",
            "label": "dokumentierter Kontakt",
            "evidence_level": "established",
            "sources": ["SRC-TEST-PERIOD-001"],
        }

    def test_relation_without_period_remains_valid(self) -> None:
        self.validator.validate(self._relation())

    def test_relation_period_accepts_source_bound_interval(self) -> None:
        relation = self._relation()
        relation["period"] = {"start": "2016-09-26", "end": "2016-09-26"}
        self.validator.validate(relation)

    def test_relation_period_accepts_year_precision_and_open_end(self) -> None:
        relation = self._relation()
        relation["period"] = {"start": "2014", "end": None}
        self.validator.validate(relation)

    def test_relation_period_requires_start(self) -> None:
        relation = self._relation()
        relation["period"] = {"end": "2014"}
        self.assertTrue(list(self.validator.iter_errors(relation)))

    def test_relation_period_rejects_null_start(self) -> None:
        relation = self._relation()
        relation["period"] = {"start": None}
        self.assertTrue(list(self.validator.iter_errors(relation)))

    def test_relation_period_rejects_unsupported_date_shape(self) -> None:
        relation = self._relation()
        relation["period"] = {"start": "2014-Q1"}
        self.assertTrue(list(self.validator.iter_errors(relation)))

    def test_relation_period_rejects_unknown_fields(self) -> None:
        relation = self._relation()
        relation["period"] = {"start": "2014", "precision": "year"}
        self.assertTrue(list(self.validator.iter_errors(relation)))


if __name__ == "__main__":
    unittest.main()
