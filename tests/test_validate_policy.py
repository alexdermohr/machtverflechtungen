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

    def _add_test_source(
        self,
        source_id: str,
        *,
        tier: str,
        institution: str,
        primary: bool = False,
    ) -> str:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"].append(
            {
                "id": source_id,
                "title": f"Testquelle {source_id}",
                "institution": institution,
                "date": "2026-09-28",
                "type": "test_source",
                "primary": primary,
                "tier": tier,
                "url": f"https://example.invalid/{source_id.lower()}",
                "accessed": "2026-09-28",
            }
        )
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        return source_id

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

    def test_case_source_must_be_directly_linked_in_visible_body(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        self.assertIn(f"]({source_url})", text)
        path.write_text(text.replace(f"]({source_url})", "](https://example.invalid/not-the-source)", 1), encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_claim_source_must_also_appear_in_case_sources(self) -> None:
        self._mutate_first_claim(sources=["SRC-DE-BT-04644-1953"])

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim source SRC-DE-BT-04644-1953 must also appear in case.sources",
            output,
        )

    def test_html_comment_does_not_satisfy_visible_source_link(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in text.splitlines()
            if source_id in line and f"]({source_url})" in line
        )
        path.write_text(
            text.replace(source_line, f"<!-- {source_id} ]({source_url}) -->", 1),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_empty_anchor_does_not_satisfy_clickable_source_link(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in text.splitlines()
            if source_id in line and f"]({source_url})" in line
        )
        path.write_text(
            text.replace(
                source_line,
                f"- {source_id} []({source_url})",
                1,
            ),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_prefixed_longer_source_id_does_not_satisfy_exact_id(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in text.splitlines()
            if source_id in line and f"]({source_url})" in line
        )
        path.write_text(
            text.replace(
                source_line,
                source_line.replace(source_id, f"{source_id}-APPENDIX", 1),
                1,
            ),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_image_destination_does_not_satisfy_clickable_source_link(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in text.splitlines()
            if source_id in line and f"]({source_url})" in line
        )
        path.write_text(
            text.replace(source_line, f"- ![{source_id}]({source_url})", 1),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_organization_source_must_be_directly_linked_in_visible_body(self) -> None:
        path = self._organization_path()
        text = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-ATLANTIKBRUECKE-YL"
        source_url = "https://www.atlantik-bruecke.org/nachwuchsfoerderung/"
        self.assertIn(f"]({source_url})", text)
        path.write_text(text.replace(f"]({source_url})", "](https://example.invalid/not-the-source)", 1), encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_source_accessed_rejects_invalid_calendar_date(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"][0]["accessed"] = "2026-02-31"
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn("accessed must use a valid YYYY-MM-DD date", output)

    def test_source_publication_date_rejects_invalid_calendar_date(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"][0]["date"] = "2026-02-31"
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn("date must use a valid YYYY-MM-DD date", output)

    def test_source_publication_date_preserves_supported_non_iso_values(self) -> None:
        path = self.root / "data" / "sources.yml"
        for value in ("2011", "current", None):
            with self.subTest(value=value):
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
                payload["sources"][0]["date"] = value
                path.write_text(
                    yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
                    encoding="utf-8",
                )

                code, output = self._run_validator()

                self.assertEqual(0, code, output)

    def test_source_url_requires_https_host(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"][0]["url"] = "https://"
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn("url must be a valid HTTPS URL with a host", output)

    def test_source_archive_url_requires_https_host(self) -> None:
        path = self.root / "data" / "sources.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["sources"][0]["archive_url"] = "https://"
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn("archive_url must be a valid HTTPS URL with a host", output)

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
        payload["relations"][0]["evidence_level"] = "strong"
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
        self._mutate_organization(evidence_level="strong", sources=[lead])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "non-speculative organization evidence may not rely solely on Tier-E leads",
            output,
        )

    def test_established_case_rejects_single_tier_d_source(self) -> None:
        source_id = self._add_test_source(
            "SRC-TEST-TIER-D",
            tier="D",
            institution="Testinstitut D",
        )
        self._mutate_case(evidence_level="established", sources=[source_id])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "established case evidence requires a Tier-A primary source",
            output,
        )

    def test_established_claim_rejects_single_tier_b_source(self) -> None:
        self._mutate_first_claim(
            classification="fact",
            evidence_level="established",
            sources=["SRC-DE-BPB-BND-2026"],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "with established evidence requires a Tier-A primary source",
            output,
        )

    def test_established_claim_accepts_two_independent_high_quality_sources(self) -> None:
        source_id = self._add_test_source(
            "SRC-TEST-TIER-C-INDEPENDENT",
            tier="C",
            institution="Unabhängiges Testinstitut",
        )
        claim_sources = ["SRC-DE-BPB-BND-2026", source_id]
        self._mutate_first_claim(
            classification="fact",
            evidence_level="established",
            sources=claim_sources,
        )
        self._mutate_case(
            sources=["SRC-DE-NI-MJ-CELLER-2015", *claim_sources],
        )

        path = self._case_path()
        text = path.read_text(encoding="utf-8").replace("## Quelle\n", "## Quellen\n", 1)
        text += (
            "\n- [BND-Hintergrund der bpb]"
            "(https://www.bpb.de/kurz-knapp/hintergrund-aktuell/576795/"
            "april-1956-gruendung-des-bundesnachrichtendienstes/) "
            "— SRC-DE-BPB-BND-2026\n"
            f"- [Unabhängige Testquelle](https://example.invalid/{source_id.lower()}) "
            f"— {source_id}\n"
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_established_claim_rejects_two_high_quality_sources_from_same_institution(self) -> None:
        source_id = self._add_test_source(
            "SRC-TEST-TIER-C-SAME-INSTITUTION",
            tier="C",
            institution="Bundeszentrale für politische Bildung",
        )
        self._mutate_first_claim(
            classification="fact",
            evidence_level="established",
            sources=["SRC-DE-BPB-BND-2026", source_id],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("different institutions", output)

    def test_established_relation_rejects_single_tier_d_source(self) -> None:
        source_id = self._add_test_source(
            "SRC-TEST-RELATION-TIER-D",
            tier="D",
            institution="Testinstitut Relation",
        )
        path = self.root / "data" / "relations.yml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["relations"][0]["evidence_level"] = "established"
        payload["relations"][0]["sources"] = [source_id]
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "established relation evidence requires a Tier-A primary source",
            output,
        )

    def test_established_organization_rejects_single_tier_b_source(self) -> None:
        self._mutate_organization(
            evidence_level="established",
            sources=["SRC-DE-BPB-BND-2026"],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "established organization evidence requires a Tier-A primary source",
            output,
        )

    def test_duplicate_organization_profile_id_is_rejected(self) -> None:
        source = self._organization_path()
        duplicate = source.with_name("atlantik-bruecke-duplicate.md")
        duplicate.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "organization profiles: duplicate id ORG-DE-ATLANTIK-BRUECKE",
            output,
        )

    def test_nested_organization_profile_is_validated(self) -> None:
        source = self._organization_path()
        nested_dir = source.parent / "de"
        nested_dir.mkdir()
        nested = nested_dir / source.name
        source.replace(nested)

        text = nested.read_text(encoding="utf-8")
        nested.write_text(
            text.replace("SRC-DE-ATLANTIKBRUECKE-YL", "SRC-UNKNOWN-NESTED"),
            encoding="utf-8",
        )

        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("docs/organisationen/de/atlantik-bruecke.md: unknown source SRC-UNKNOWN-NESTED", output)

    def test_nested_directory_index_organization_profile_is_validated(self) -> None:
        source = self._organization_path()
        nested_dir = source.parent / "de" / "atlantik-bruecke"
        nested_dir.mkdir(parents=True)
        nested = nested_dir / "index.md"
        source.replace(nested)

        text = nested.read_text(encoding="utf-8")
        nested.write_text(
            text.replace("SRC-DE-ATLANTIKBRUECKE-YL", "SRC-UNKNOWN-DIRECTORY-INDEX"),
            encoding="utf-8",
        )

        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "docs/organisationen/de/atlantik-bruecke/index.md: unknown source SRC-UNKNOWN-DIRECTORY-INDEX",
            output,
        )

    def test_nested_directory_index_case_is_validated(self) -> None:
        source = self._case_path()
        nested_dir = source.parent / "celler-loch"
        nested_dir.mkdir()
        nested = nested_dir / "index.md"
        source.replace(nested)

        text = nested.read_text(encoding="utf-8")
        nested.write_text(
            text.replace("SRC-DE-NI-MJ-CELLER-2015", "SRC-UNKNOWN-DIRECTORY-INDEX"),
            encoding="utf-8",
        )

        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "docs/faelle/de/celler-loch/index.md: unknown source SRC-UNKNOWN-DIRECTORY-INDEX",
            output,
        )

    def test_case_period_rejects_end_year_before_start_year(self) -> None:
        self._mutate_case(period={"start": "2000", "end": "1900"})
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("period.end precedes period.start", output)

    def test_case_period_rejects_end_date_before_start_date(self) -> None:
        self._mutate_case(period={"start": "2000-12-31", "end": "2000-01-01"})
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("period.end precedes period.start", output)

    def test_case_period_allows_ambiguous_same_year_mixed_precision(self) -> None:
        self._mutate_case(period={"start": "2000-12-31", "end": "2000"})
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_case_period_rejects_invalid_calendar_date(self) -> None:
        self._mutate_case(period={"start": "2000-02-31", "end": "2001"})
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("period.start must use a valid YYYY or YYYY-MM-DD value", output)

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

    def test_established_open_question_requires_a_source(self) -> None:
        self._mutate_first_claim(
            classification="open_question",
            evidence_level="established",
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("requires at least one source", output)

    def test_speculative_open_question_may_remain_unsourced(self) -> None:
        self._mutate_first_claim(
            classification="open_question",
            evidence_level="speculative",
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_contradicted_hypothesis_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="hypothesis",
            evidence_level="contradicted",
            sources=[lead],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("may not rely solely on Tier-E leads", output)

    def test_contradicted_open_question_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="open_question",
            evidence_level="contradicted",
            sources=[lead],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("may not rely solely on Tier-E leads", output)

    def test_strong_open_question_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="open_question",
            evidence_level="strong",
            sources=[lead],
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("may not rely solely on Tier-E leads", output)

    def test_contradicted_case_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_case(evidence_level="contradicted", sources=[lead])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "non-speculative case evidence may not rely solely on Tier-E leads",
            output,
        )

    def test_contradicted_organization_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_organization(evidence_level="contradicted", sources=[lead])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "non-speculative organization evidence may not rely solely on Tier-E leads",
            output,
        )

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
