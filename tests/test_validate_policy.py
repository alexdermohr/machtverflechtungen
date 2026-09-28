from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import scripts.validate as validate


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class EvidencePolicyValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="machtverflechtungen-validator-")
        self.root = Path(self.tempdir.name)
        shutil.copytree(SOURCE_ROOT / "data", self.root / "data")
        shutil.copytree(SOURCE_ROOT / "schemas", self.root / "schemas")
        shutil.copytree(SOURCE_ROOT / "docs" / "faelle", self.root / "docs" / "faelle")
        shutil.copytree(
            SOURCE_ROOT / "docs" / "organisationen",
            self.root / "docs" / "organisationen",
        )
        self.original_paths = (
            validate.ROOT,
            validate.DOCS,
            validate.CASE_DIR,
            validate.DATA,
            validate.SCHEMAS,
        )
        validate.ROOT = self.root
        validate.DOCS = self.root / "docs"
        validate.CASE_DIR = validate.DOCS / "faelle"
        validate.DATA = self.root / "data"
        validate.SCHEMAS = self.root / "schemas"

    def tearDown(self) -> None:
        (
            validate.ROOT,
            validate.DOCS,
            validate.CASE_DIR,
            validate.DATA,
            validate.SCHEMAS,
        ) = self.original_paths
        self.tempdir.cleanup()

    def _run_validator(self) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = validate.main()
        return code, output.getvalue()

    def _case_path(self) -> Path:
        return self.root / "docs" / "faelle" / "de" / "celler-loch.md"

    def _mutate_case(self, **updates: object) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        frontmatter.update(updates)
        body = "\n".join(lines[end + 1 :]).lstrip("\n")
        rendered = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")

    def _mutate_first_claim(self, **updates: object) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        frontmatter["claims"][0].update(updates)
        body = "\n".join(lines[end + 1 :]).lstrip("\n")
        rendered = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")

    def _organization_path(self) -> Path:
        return self.root / "docs" / "organisationen" / "atlantik-bruecke.md"

    def _mutate_organization(self, **updates: object) -> None:
        path = self._organization_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        frontmatter.update(updates)
        body = "\n".join(lines[end + 1 :]).lstrip("\n")
        rendered = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")

    def _add_tier_e_source(self) -> str:
        source_id = "SRC-TEST-LEAD"
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"].append(
            {
                "id": source_id,
                "title": "Unbestätigter Testhinweis",
                "institution": "Test",
                "date": "2026-09-28",
                "type": "lead",
                "primary": False,
                "tier": "E",
                "url": "https://example.invalid/lead",
                "accessed": "2026-09-28",
            }
        )
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        return source_id

    def test_speculative_fact_still_requires_a_source(self) -> None:
        self._mutate_first_claim(
            classification="fact",
            evidence_level="speculative",
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("requires at least one source", output)

    def test_fact_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="fact",
            evidence_level="speculative",
            sources=[lead],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("may not rely solely on Tier-E leads", output)

    def test_relation_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        path = self.root / "data" / "relations.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["relations"][0]["sources"] = [lead]
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("relation may not rely solely on Tier-E leads", output)

    def test_established_organization_requires_a_source(self) -> None:
        self._mutate_organization(sources=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("should be non-empty", output)

    def test_organization_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_organization(sources=[lead])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "non-speculative organization evidence may not rely solely on Tier-E leads",
            output,
        )

    def test_malformed_catalog_row_is_reported_without_crashing(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"].append("not-a-mapping")
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("expected mapping", output)

    def test_invalid_case_sources_type_is_reported_without_crashing(self) -> None:
        self._mutate_case(sources=None)
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not of type 'array'", output)

    def test_invalid_relation_node_type_is_reported_without_crashing(self) -> None:
        path = self.root / "data" / "relations.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["relations"][0]["from"] = {"invalid": "node"}
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not of type 'string'", output)

    def test_invalid_relation_sources_type_is_reported_without_crashing(self) -> None:
        path = self.root / "data" / "relations.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["relations"][0]["sources"] = None
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not of type 'array'", output)

    def test_invalid_case_evidence_level_container_is_reported_without_crashing(self) -> None:
        self._mutate_case(evidence_level=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not one of", output)

    def test_invalid_claim_classification_container_is_reported_without_crashing(self) -> None:
        self._mutate_first_claim(classification=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not one of", output)

    def test_invalid_claim_evidence_level_container_is_reported_without_crashing(self) -> None:
        self._mutate_first_claim(
            classification="hypothesis",
            evidence_level=[],
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not one of", output)

    def test_invalid_organization_evidence_level_container_is_reported_without_crashing(self) -> None:
        self._mutate_organization(evidence_level=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not one of", output)

    def test_speculative_hypothesis_may_remain_an_unsourced_open_lead(self) -> None:
        self._mutate_first_claim(
            classification="hypothesis",
            evidence_level="speculative",
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)


    def test_schema_invalid_catalog_row_does_not_block_valid_row_semantics(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"].append({"id": "SRC-BROKEN"})
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )

        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="fact",
            evidence_level="speculative",
            sources=[lead],
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn("is a required property", output)
        self.assertIn("may not rely solely on Tier-E leads", output)

if __name__ == "__main__":
    unittest.main()
