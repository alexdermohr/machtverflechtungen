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

    def _sync_event_core_body(self, body: str, event_claims: list[str]) -> str:
        lines = body.splitlines()
        out: list[str] = []
        in_event_core = False
        for line in lines:
            stripped = line.strip()
            if stripped == "## Gesicherter Ereigniskern":
                in_event_core = True
            elif in_event_core and stripped.startswith("## "):
                in_event_core = False
            if (
                in_event_core
                and stripped.startswith("- ")
                and "`CLM-" in line
                and not any(f"`{claim_id}`" in line for claim_id in event_claims)
            ):
                continue
            out.append(line)
        return "\n".join(out)

    def _mutate_first_claim(self, **updates: object) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        claim = frontmatter["claims"][0]
        claim.update(updates)

        if "sources" in updates and "evidence" not in updates:
            sources = updates["sources"]
            if isinstance(sources, list):
                existing = {
                    record.get("source"): record
                    for record in claim.get("evidence", [])
                    if isinstance(record, dict) and isinstance(record.get("source"), str)
                }
                claim["evidence"] = [
                    existing.get(
                        source_id,
                        {
                            "source": source_id,
                            "directness": "direct",
                            "note": f"Testbeleg für {source_id}.",
                        },
                    )
                    for source_id in sources
                    if isinstance(source_id, str)
                ]

        if any(key in updates for key in ("classification", "evidence_level")):
            eligible = (
                claim.get("classification") == "fact"
                and claim.get("evidence_level") in {"established", "strong"}
            )
            if not eligible:
                claim_id = claim.get("id")
                frontmatter["event_claims"] = [
                    item
                    for item in frontmatter.get("event_claims", [])
                    if item != claim_id
                ]
                if not frontmatter["event_claims"]:
                    for candidate in frontmatter["claims"][1:]:
                        if (
                            candidate.get("classification") == "fact"
                            and candidate.get("evidence_level") in {"established", "strong"}
                        ):
                            frontmatter["event_claims"] = [candidate["id"]]
                            break

        body = "\n".join(lines[end + 1 :]).lstrip("\n")
        body = self._sync_event_core_body(
            body,
            [
                item
                for item in frontmatter.get("event_claims", [])
                if isinstance(item, str)
            ],
        )
        rendered = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")

    def _delete_first_claim_field(self, field: str) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        frontmatter["claims"][0].pop(field, None)
        body = "\n".join(lines[end + 1 :]).lstrip("\n")
        rendered = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")

    def _replace_case_body_text(self, old: str, new: str) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        frontmatter = yaml.safe_load("\n".join(lines[1:end]))
        event_claims = [
            item
            for item in frontmatter.get("event_claims", [])
            if isinstance(item, str)
        ]
        if old.startswith("CLM-") and old in event_claims and old != new:
            event_claims = [item for item in event_claims if item != old]
            frontmatter["event_claims"] = event_claims
        body = "\n".join(lines[end + 1 :]).replace(old, new)
        body = self._sync_event_core_body(body, event_claims)
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

    def test_collapsed_pymdown_details_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n??? note \"Verborgene Quelle\"\n"
            f"    - [Quelle]({source_url}) — `{source_id}`\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_standard_admonition_satisfies_visible_source_link(self) -> None:
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
        visible_source = (
            "\n!!! note \"Sichtbare Quelle\"\n"
            f"    - [Quelle]({source_url}) — " + chr(96) + source_id + chr(96) + "\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + visible_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

    def test_source_id_split_by_select_does_not_satisfy_visibility(self) -> None:
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
        split_source = (
            chr(10)
            + f'<ul><li><a href="{source_url}">Quelle</a> '
            + 'SRC-DE-NI-MJ-CELLER-<select><option>ignored</option></select>'
            + '2015</li></ul>'
            + chr(10)
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + split_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_named_details_group_does_not_satisfy_visible_source_link(self) -> None:
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
        grouped_source = (
            '\n<details name="evidence" open><summary>Erste Quelle</summary><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            '</li></ul></details>\n'
            '<details name="evidence" open><summary>Zweite Quelle</summary>'
            'Andere sichtbare Gruppe</details>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + grouped_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_source_id_split_by_self_closing_br_does_not_satisfy_visibility(self) -> None:
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
        split_source = (
            f'\n- <a href="{source_url}">Quelle</a> '
            "SRC-DE-NI-MJ-CELLER-<br/>2015\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + split_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_css_newline_hidden_source_link_does_not_satisfy_visibility(self) -> None:
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
        hidden_source = (
            '\n<ul><li style="visibility:\n hidden">'
            f'<a href="{source_url}">Quelle</a> {source_id}</li></ul>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_inline_style_never_satisfies_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n<ul><li style=\"display:\\6e one\">"
            f'<a href="{source_url}">Quelle</a> {source_id}</li></ul>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_self_closing_svg_does_not_hide_following_visible_content(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        claim_line = next(
            line
            for line in text.splitlines()
            if "`CLM-DE-CELLER-001` — belegt:" in line
        )
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in text.splitlines()
            if "SRC-DE-NI-MJ-CELLER-2015" in line and f"]({source_url})" in line
        )
        text = text.replace(
            claim_line,
            claim_line.replace("- **", '- <svg aria-hidden="true" /> **', 1),
            1,
        )
        text = text.replace(
            source_line,
            source_line.replace("- [", '- <svg aria-hidden="true" /> [', 1),
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

    def test_non_rendered_fallback_tags_do_not_satisfy_text_visibility(self) -> None:
        samples = {
            "noscript": "<noscript>HIDDEN-FALLBACK</noscript><p>VISIBLE</p>",
            "progress": "<progress>HIDDEN-FALLBACK</progress><p>VISIBLE</p>",
            "meter": "<meter>HIDDEN-FALLBACK</meter><p>VISIBLE</p>",
            "datalist": "<datalist><option>HIDDEN-FALLBACK</option></datalist><p>VISIBLE</p>",
            "rp": "<ruby>漢<rp>HIDDEN-FALLBACK</rp><rt>kan</rt></ruby>",
            "noembed": "<noembed>HIDDEN-FALLBACK</noembed><p>VISIBLE</p>",
            "noframes": "<noframes>HIDDEN-FALLBACK</noframes><p>VISIBLE</p>",
        }
        for tag, markup in samples.items():
            with self.subTest(tag=tag):
                visible = validate.visible_markdown_text(markup)
                self.assertNotIn("HIDDEN-FALLBACK", visible)

    def test_html_title_metadata_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<title>HIDDEN-TITLE-METADATA</title><p>VISIBLE</p>"
        )
        self.assertNotIn("HIDDEN-TITLE-METADATA", visible)
        self.assertIn("VISIBLE", visible)

    def test_linked_stylesheet_is_detected_as_author_stylesheet(self) -> None:
        self.assertTrue(
            validate.has_author_stylesheet(
                '<link href="theme.css" rel="stylesheet">'
            )
        )

    def test_svg_presentation_attribute_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            '<svg><text display="none">HIDDEN-SVG-TEXT</text><text>VISIBLE-SVG-TEXT</text></svg>'
        )
        self.assertNotIn("HIDDEN-SVG-TEXT", visible)
        self.assertIn("VISIBLE-SVG-TEXT", visible)

    def test_svg_resource_container_text_does_not_satisfy_text_visibility(self) -> None:
        containers = (
            "defs",
            "symbol",
            "clipPath",
            "mask",
            "pattern",
            "filter",
            "marker",
            "linearGradient",
            "radialGradient",
        )
        for tag in containers:
            with self.subTest(tag=tag):
                visible = validate.visible_markdown_text(
                    f"<svg><{tag}><text>HIDDEN-SVG-RESOURCE</text></{tag}>"
                    "<text>VISIBLE-SVG-TEXT</text></svg>"
                )
                self.assertNotIn("HIDDEN-SVG-RESOURCE", visible)
                self.assertIn("VISIBLE-SVG-TEXT", visible)

    def test_pathless_svg_textpath_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<svg><text><textPath>HIDDEN-PATHLESS-TEXTPATH</textPath></text>"
            "<text>VISIBLE-SVG-TEXT</text></svg>"
        )

        self.assertNotIn("HIDDEN-PATHLESS-TEXTPATH", visible)
        self.assertIn("VISIBLE-SVG-TEXT", visible)

    def test_svg_switch_unselected_branch_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<svg><switch>"
            "<text>VISIBLE-FIRST-BRANCH</text>"
            "<text>HIDDEN-SECOND-BRANCH</text>"
            "</switch><text>VISIBLE-OUTSIDE-SWITCH</text></svg>"
        )

        self.assertNotIn("HIDDEN-SECOND-BRANCH", visible)
        self.assertIn("VISIBLE-OUTSIDE-SWITCH", visible)

    def test_svg_text_after_self_closing_foreign_child_remains_visible(self) -> None:
        visible = validate.visible_markdown_text(
            '<svg><circle hidden /> <text>VISIBLE-SVG-TEXT</text></svg>'
        )
        self.assertIn("VISIBLE-SVG-TEXT", visible)

    def test_mathml_text_after_self_closing_foreign_child_remains_visible(self) -> None:
        visible = validate.visible_markdown_text(
            '<math><mi hidden /> <mtext>VISIBLE-MATH-TEXT</mtext></math>'
        )
        self.assertIn("VISIBLE-MATH-TEXT", visible)

    def test_svg_foreign_object_is_not_visibility_evidence(self) -> None:
        visible = validate.visible_markdown_text(
            '<svg><foreignObject><p>HIDDEN-HTML</p></foreignObject></svg>'
        )

        self.assertNotIn("HIDDEN-HTML", visible)

    def test_svg_foreign_object_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n<svg><foreignObject>"
            f'<li><a href="{source_url}">Quelle</a> — {source_id}</li>'
            "</foreignObject></svg>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code, output)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_self_closing_hidden_ancestor_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<div style="display:none" />\n'
            f'- [Quelle]({source_url}) — `{source_id}`\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_class_styled_hidden_content_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<style>.hidden-evidence { display: none; }</style>\n'
            '<div class="hidden-evidence"><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            '</li></ul></div>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_attributed_stylesheet_hides_open_details_source_evidence(self) -> None:
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
        hidden_source = (
            '\n<style type="text/css">.note { display: none; }</style>\n'
            '<details class="note" open><summary>Quellen</summary><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            '</li></ul></details>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_object_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<object data="about:blank"><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            '</li></ul></object>\n'
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_canvas_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n<canvas><ul><li>"
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></canvas>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_noscript_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n<noscript><ul><li>"
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></noscript>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_noembed_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            "\n<noembed><ul><li>"
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></noembed>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_popover_content_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<div popover><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></div>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_audio_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<audio src="about:blank"><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></audio>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_iframe_fallback_does_not_satisfy_visible_source_link(self) -> None:
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
        hidden_source = (
            '\n<iframe src="about:blank"><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></iframe>\n"
        )
        path.write_text(
            text.replace(source_line, "- Quelle im sichtbaren Text entfernt", 1)
            + hidden_source,
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
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

    def test_lowercase_or_underscore_suffix_does_not_satisfy_exact_id(self) -> None:
        path = self._case_path()
        original = path.read_text(encoding="utf-8")
        source_id = "SRC-DE-NI-MJ-CELLER-2015"
        source_url = (
            "https://www.mj.niedersachsen.de/startseite/aktuelles/"
            "presseinformationen/justizministerin-besucht-das-celler-loch-135720.html"
        )
        source_line = next(
            line
            for line in original.splitlines()
            if source_id in line and f"]({source_url})" in line
        )

        for suffix in ("oops", "_APPENDIX"):
            with self.subTest(suffix=suffix):
                path.write_text(
                    original.replace(
                        source_line,
                        source_line.replace(source_id, f"{source_id}{suffix}", 1),
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

        path.write_text(original, encoding="utf-8")

    def test_hidden_anchor_does_not_satisfy_clickable_source_link(self) -> None:
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
        replacement = (
            f"- {source_id} <a hidden href=\"{source_url}\">Quelle</a>"
        )
        path.write_text(text.replace(source_line, replacement, 1), encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_hidden_ancestor_does_not_satisfy_clickable_source_link(self) -> None:
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
        replacement = (
            f"- {source_id} <span hidden>"
            f"<a href=\"{source_url}\">Quelle</a></span>"
        )
        path.write_text(text.replace(source_line, replacement, 1), encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_format_only_anchor_text_does_not_satisfy_clickable_source_link(self) -> None:
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
                f"- {source_id} [&#8203;]({source_url})",
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

    def test_case_level_evidence_verdict_is_rejected(self) -> None:
        self._mutate_case(evidence_level="established")
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("Additional properties are not allowed", output)
        self.assertIn("evidence_level", output)

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

    def test_established_claim_context_only_source_does_not_meet_threshold(self) -> None:
        self._mutate_first_claim(
            evidence=[
                {
                    "source": "SRC-DE-NI-MJ-CELLER-2015",
                    "directness": "context",
                    "note": "Diese Quelle liefert im Test nur Kontext und keine tragende Stütze.",
                }
            ]
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "with established evidence requires a Tier-A primary source",
            output,
        )

    def test_schema_invalid_directness_is_reported_without_crashing(self) -> None:
        for invalid_directness in ([], {}):
            with self.subTest(directness=invalid_directness):
                self._mutate_first_claim(
                    evidence=[
                        {
                            "source": "SRC-DE-NI-MJ-CELLER-2015",
                            "directness": invalid_directness,
                            "note": "Diese absichtlich falsche Form muss als Schemafehler gemeldet werden.",
                        }
                    ]
                )

                code, output = self._run_validator()

                self.assertEqual(1, code)
                self.assertIn("is not one of", output)

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

    def test_case_level_evidence_container_is_rejected_without_crashing(self) -> None:
        self._mutate_case(evidence_level=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("Additional properties are not allowed", output)
        self.assertIn("evidence_level", output)

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

    def test_speculative_hypothesis_may_use_a_tier_e_lead(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_first_claim(
            classification="hypothesis",
            evidence_level="speculative",
            sources=[lead],
        )
        self._mutate_case(
            sources=["SRC-DE-NI-MJ-CELLER-2015", lead],
        )
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text += (
            "\n- [Unbestätigter Testhinweis](https://example.invalid/lead) "
            "— `SRC-TEST-LEAD`\n"
        )
        path.write_text(text, encoding="utf-8")

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

    def test_contradicted_organization_may_not_rely_only_on_tier_e_leads(self) -> None:
        lead = self._add_tier_e_source()
        self._mutate_organization(evidence_level="contradicted", sources=[lead])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "non-speculative organization evidence may not rely solely on Tier-E leads",
            output,
        )

    def test_speculative_hypothesis_may_remain_unsourced(self) -> None:
        self._mutate_first_claim(
            classification="hypothesis",
            evidence_level="speculative",
            sources=[],
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)


    def test_claim_id_must_be_visible_in_case_body(self) -> None:
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )

    def test_css_tab_hidden_claim_does_not_satisfy_case_body_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<span style="display:\tnone">CLM-DE-CELLER-001 {claim_text}</span>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_css_comment_hidden_claim_does_not_satisfy_case_body_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<span style="display:/**/none">CLM-DE-CELLER-001 {claim_text}</span>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_inline_style_never_satisfies_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<span style="display:\\6e one">CLM-DE-CELLER-001 {claim_text}</span>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_svg_metadata_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f"\n<svg><desc>CLM-DE-CELLER-001 {claim_text}</desc></svg>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_pathless_svg_textpath_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f"\n<svg><text><textPath>CLM-DE-CELLER-001 {claim_text}</textPath></text></svg>\n",
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_self_closing_hidden_ancestor_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<div style="display:none" />\nCLM-DE-CELLER-001 {claim_text}\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_class_styled_hidden_content_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + '\n<style>.hidden-evidence { display: none; }</style>\n'
            + f'<div class="hidden-evidence">CLM-DE-CELLER-001 {claim_text}</div>\n',
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_object_fallback_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<object data="about:blank">CLM-DE-CELLER-001 {claim_text}</object>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_canvas_fallback_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f"\n<canvas>CLM-DE-CELLER-001 {claim_text}</canvas>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_popover_content_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<div popover>CLM-DE-CELLER-001 {claim_text}</div>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_video_fallback_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<video src="about:blank">CLM-DE-CELLER-001 {claim_text}</video>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_iframe_fallback_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f'\n<iframe src="about:blank">CLM-DE-CELLER-001 {claim_text}</iframe>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_hidden_claim_id_does_not_satisfy_case_body_visibility(self) -> None:
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8") + "\n<!-- CLM-DE-CELLER-001 -->\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )

    def test_collapsed_pymdown_details_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n??? note \"Verborgener Claim\"\n"
            + f"    CLM-DE-CELLER-001 {claim_text}\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_open_pymdown_details_satisfies_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n???+ note \"Sichtbarer Claim\"\n"
            + f"    CLM-DE-CELLER-001 {claim_text}\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_standard_admonition_satisfies_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n!!! note \"Sichtbarer Claim\"\n"
            + f"    CLM-DE-CELLER-001 {claim_text}\n",
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

    def test_each_visible_claim_id_is_bound_to_its_own_wording(self) -> None:
        first = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        second = (
            "Die Operation sollte einen RAF-Befreiungsversuch vortäuschen; "
            "Öffentlichkeit und Strafverfolgungsbehörden wurden über die Urheber "
            "planmäßig getäuscht."
        )
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        body = chr(10).join(lines[end + 1 :])
        self.assertGreaterEqual(body.count(first), 2)
        self.assertGreaterEqual(body.count(second), 2)
        body = body.replace(first, "__CLAIM_ONE_WORDING__")
        body = body.replace(second, first)
        body = body.replace("__CLAIM_ONE_WORDING__", second)
        path.write_text(
            chr(10).join(lines[: end + 1]) + chr(10) + body + chr(10),
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must bind each visible ID occurrence to its own wording",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-002 must bind each visible ID occurrence to its own wording",
            output,
        )

    def test_inline_html_preserves_claim_wording_across_markup(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        formatted_claim = claim_text.replace(
            "Verfassungsschutz",
            "Verfassungs<b>schutz</b>",
            1,
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f"\n<p>CLM-DE-CELLER-001 {formatted_claim}</p>\n",
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

    def test_visible_text_parser_preserves_block_boundary(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed("<p>Alpha</p><p>Beta</p>")
        parser.close()

        self.assertEqual("Alpha Beta", parser.text())

    def test_disqualified_named_details_preserves_text_boundary(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            'Alpha<details name="group" open><summary>Hidden</summary>'
            "Ignored</details>Beta"
        )
        parser.close()

        self.assertEqual("Alpha Beta", parser.text())

    def test_self_closing_br_preserves_text_boundary(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed("Alpha<br/>Beta")
        parser.close()

        self.assertEqual("Alpha Beta", parser.text())

    def test_unselected_select_option_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<select><option selected>SELECTED-LABEL</option>"
            "<option>HIDDEN-UNSELECTED-OPTION</option></select>"
            "<p>VISIBLE-OUTSIDE</p>"
        )

        self.assertNotIn("HIDDEN-UNSELECTED-OPTION", visible)
        self.assertIn("VISIBLE-OUTSIDE", visible)

    def test_rendered_controls_and_replaced_elements_preserve_text_boundaries(self) -> None:
        hidden_content_samples = {
            "audio": "Alpha<audio>Ignored</audio>Beta",
            "canvas": "Alpha<canvas>Ignored</canvas>Beta",
            "iframe": "Alpha<iframe>Ignored</iframe>Beta",
            "meter": "Alpha<meter>Ignored</meter>Beta",
            "object": "Alpha<object>Ignored</object>Beta",
            "progress": "Alpha<progress>Ignored</progress>Beta",
            "video": "Alpha<video>Ignored</video>Beta",
        }
        for tag, markup in hidden_content_samples.items():
            with self.subTest(tag=tag):
                self.assertEqual("Alpha Beta", validate.visible_markdown_text(markup))

        void_samples = {
            "embed": "Alpha<embed>Beta",
            "img": "Alpha<img>Beta",
            "input": "Alpha<input>Beta",
        }
        for tag, markup in void_samples.items():
            with self.subTest(tag=tag):
                self.assertEqual("Alpha Beta", validate.visible_markdown_text(markup))

        visible_content_samples = {
            "button": ("Alpha<button>Control</button>Beta", "Alpha Control Beta"),
            "textarea": ("Alpha<textarea>Control</textarea>Beta", "Alpha Control Beta"),
            "svg": (
                "Alpha<svg><text>Visible</text></svg>Beta",
                "Alpha Visible Beta",
            ),
            "math": (
                "Alpha<math><mtext>Visible</mtext></math>Beta",
                "Alpha Visible Beta",
            ),
        }
        for tag, (markup, expected_text) in visible_content_samples.items():
            with self.subTest(tag=tag):
                self.assertEqual(expected_text, validate.visible_markdown_text(markup))

    def test_select_preserves_text_boundary(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed("Alpha<select><option>Ignored</option></select>Beta")
        parser.close()

        self.assertEqual("Alpha Beta", parser.text())

    def test_named_details_group_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details name=\"claims\" open><summary>Erster Claim</summary>\n"
            + f"CLM-DE-CELLER-001 {claim_text}\n</details>\n"
            + '<details name="claims" open><summary>Zweiter Claim</summary>'
            + "Andere sichtbare Gruppe</details>\n",
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_stylesheet_can_not_hide_open_pymdown_details_evidence(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<style>.note { display: none; }</style>\n"
            + "\n???+ note \"Versteckter offener Claim\"\n"
            + f"    CLM-DE-CELLER-001 {claim_text}\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_id_selector_stylesheet_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + '\n<style>#hidden-evidence { display: none; }</style>\n'
            + f'<div id="hidden-evidence">CLM-DE-CELLER-001 {claim_text}</div>\n',
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_attributed_stylesheet_can_not_hide_open_pymdown_details_evidence(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<style type=\"text/css\">.note { display: none; }</style>\n"
            + "\n???+ note \"Versteckter offener Claim\"\n"
            + f"    CLM-DE-CELLER-001 {claim_text}\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_closed_details_content_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details>\n<summary>Zusatz</summary>\n"
            + f"CLM-DE-CELLER-001 {claim_text}\n</details>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_closed_details_direct_summary_satisfies_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details>\n"
            + f"<summary>CLM-DE-CELLER-001 {claim_text}</summary>\n"
            + "Verborgener Zusatz\n</details>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_nested_summary_inside_closed_details_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details>\n<summary>Äußerer Titel</summary>\n"
            + "<details open>\n"
            + f"<summary>CLM-DE-CELLER-001 {claim_text}</summary>\n"
            + "</details>\n</details>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_second_direct_summary_inside_closed_details_is_hidden(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details>\n<summary>Erster Titel</summary>\n"
            + f"<summary>CLM-DE-CELLER-001 {claim_text}</summary>\n"
            + "</details>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_open_details_content_satisfies_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n<details open>\n<summary>Zusatz</summary>\n"
            + f"CLM-DE-CELLER-001 {claim_text}\n</details>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_closed_dialog_content_does_not_satisfy_claim_visibility(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text("CLM-DE-CELLER-001", "CLM-DE-CELLER-HIDDEN")
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich verändert.",
        )
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + f"\n<dialog>CLM-DE-CELLER-001 {claim_text}</dialog>\n",
            encoding="utf-8",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 must be visibly represented by ID in case body",
            output,
        )
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_claim_wording_must_be_visible_in_case_body(self) -> None:
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        self._replace_case_body_text(
            claim_text,
            "Die sichtbare Fassung wurde absichtlich von der kanonischen Claim-Aussage abweichend verändert.",
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_claim_wording_requires_lexical_token_boundaries(self) -> None:
        self._mutate_first_claim(text="Rat war geheim")
        path = self._case_path()
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\nCLM-DE-CELLER-001 Vorrat war geheim\n",
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 wording must be visibly represented in case body",
            output,
        )

    def test_claim_challenge_fields_are_structurally_required(self) -> None:
        for field in (
            "counterevidence",
            "alternatives",
            "missing_evidence",
            "scope",
            "falsification",
        ):
            with self.subTest(field=field):
                original = self._case_path().read_text(encoding="utf-8")
                self._delete_first_claim_field(field)
                code, output = self._run_validator()
                self.assertEqual(1, code)
                self.assertIn("is a required property", output)
                self._case_path().write_text(original, encoding="utf-8")

    def test_claim_sources_must_match_structured_support_evidence(self) -> None:
        self._mutate_first_claim(evidence=[])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("sources must exactly match evidence source IDs", output)

    def test_unknown_event_claim_is_rejected(self) -> None:
        self._mutate_case(event_claims=["CLM-UNKNOWN-EVENT"])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("event claim CLM-UNKNOWN-EVENT is unknown", output)

    def test_event_claim_must_belong_to_same_case(self) -> None:
        self._mutate_case(event_claims=["CLM-DE-GEHLEN-001"])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-GEHLEN-001 belongs to case CASE-DE-ORG-GEHLEN-1946",
            output,
        )

    def test_event_core_section_may_not_include_non_event_claim(self) -> None:
        self._mutate_case(event_claims=["CLM-DE-CELLER-001"])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "Gesicherter Ereigniskern includes non-event claim CLM-DE-CELLER-002",
            output,
        )

    def test_event_core_section_must_include_each_event_claim(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "- **`CLM-DE-CELLER-002` — belegt:**",
            "- **`CLM-DE-CELLER-HIDDEN` — belegt:**",
            1,
        )
        path.write_text(text, encoding="utf-8")
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-002 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_event_core_accepts_event_claim_in_visible_admonition(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        event_line = next(
            line
            for line in text.splitlines()
            if (chr(96) + "CLM-DE-CELLER-002" + chr(96) + " — belegt:") in line
        )
        event_wording = event_line.split(":** ", 1)[1]
        text = text.replace(
            event_line,
            "!!! note \"Sichtbarer Ereignisclaim\"\n"
            f"    CLM-DE-CELLER-002 {event_wording}",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

    def test_event_core_detects_non_event_claim_in_visible_svg_text(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8").replace(
            "\n## Rekonstruktion",
            "\n<svg><circle hidden /><text>CLM-DE-CELLER-NON-EVENT</text></svg>\n\n## Rekonstruktion",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "Gesicherter Ereigniskern includes non-event claim CLM-DE-CELLER-NON-EVENT",
            output,
        )

    def test_event_core_ignores_svg_text_with_presentation_attributes(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "- **`CLM-DE-CELLER-002` — belegt:** Die Operation sollte einen RAF-Befreiungsversuch vortäuschen; Öffentlichkeit und Strafverfolgungsbehörden wurden über die Urheber planmäßig getäuscht.\n",
            '<svg><text display="none">CLM-DE-CELLER-002</text></svg>\n',
            1,
        )
        path.write_text(text, encoding="utf-8")
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-002 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_event_core_ignores_html_title_metadata(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "- **`CLM-DE-CELLER-002` — belegt:** Die Operation sollte einen RAF-Befreiungsversuch vortäuschen; Öffentlichkeit und Strafverfolgungsbehörden wurden über die Urheber planmäßig getäuscht.\n",
            "<title>CLM-DE-CELLER-002</title>\n",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-002 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_hidden_event_core_ancestor_does_not_satisfy_visibility(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        start = text.index("## Gesicherter Ereigniskern")
        end = text.index("\n## Rekonstruktion", start)
        hidden_event_core = (
            '<div hidden>\n'
            '<h2>Gesicherter Ereigniskern</h2>\n'
            '<p>CLM-DE-CELLER-001 CLM-DE-CELLER-002</p>\n'
            '</div>\n'
        )
        path.write_text(
            text[:start] + hidden_event_core + text[end:],
            encoding="utf-8",
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-001 must appear in Gesicherter Ereigniskern",
            output,
        )
        self.assertIn(
            "event claim CLM-DE-CELLER-002 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_hidden_heading_fragment_does_not_identify_event_core(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8").replace(
            "## Gesicherter Ereigniskern",
            "## Gesicherter <span hidden>Ereigniskern</span>",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-001 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_hidden_following_heading_does_not_end_event_core_capture(self) -> None:
        path = (
            self.root
            / "docs"
            / "faelle"
            / "de"
            / "thueringer-heimatschutz-tino-brandt.md"
        )
        original = path.read_text(encoding="utf-8")
        for heading_tag in ("h1", "h2"):
            with self.subTest(heading_tag=heading_tag):
                text = original.replace(
                    "## Gegenbefund zur Gründungsthese",
                    f"<{heading_tag} hidden>Versteckte Zwischenüberschrift</{heading_tag}>",
                    1,
                )
                path.write_text(text, encoding="utf-8")

                code, output = self._run_validator()

                self.assertEqual(1, code)
                self.assertIn(
                    "Gesicherter Ereigniskern includes non-event claim CLM-DE-THS-001",
                    output,
                )
        path.write_text(original, encoding="utf-8")

    def test_event_core_capture_stops_at_following_h1(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "- **`CLM-DE-CELLER-002` — belegt:** Die Operation sollte einen RAF-Befreiungsversuch vortäuschen; Öffentlichkeit und Strafverfolgungsbehörden wurden über die Urheber planmäßig getäuscht.\n",
            "",
            1,
        )
        text = text.replace(
            "## Rekonstruktion",
            "# Rekonstruktion\n\nCLM-DE-CELLER-002",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-002 must appear in Gesicherter Ereigniskern",
            output,
        )

    def test_event_core_heading_may_use_attr_list(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8").replace(
            "## Gesicherter Ereigniskern",
            "## Gesicherter Ereigniskern {#ereigniskern}",
            1,
        )
        path.write_text(text, encoding="utf-8")
        code, output = self._run_validator()
        self.assertEqual(0, code, output)

    def test_event_claim_must_be_fact(self) -> None:
        self._mutate_first_claim(classification="hypothesis")
        self._mutate_case(event_claims=["CLM-DE-CELLER-001"])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-001 must be classification fact",
            output,
        )

    def test_event_claim_must_be_strong_or_established(self) -> None:
        self._mutate_first_claim(evidence_level="plausible")
        self._mutate_case(event_claims=["CLM-DE-CELLER-001"])
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "event claim CLM-DE-CELLER-001 must be established or strong",
            output,
        )

    def test_synthesis_must_reference_known_case_claim(self) -> None:
        self._mutate_case(
            what_follows=[
                {
                    "text": "Eine testweise Synthese mit absichtlich unbekanntem Claim.",
                    "claim_ids": ["CLM-UNKNOWN-SYNTHESIS"],
                }
            ]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn(
            "what_follows references unknown claim CLM-UNKNOWN-SYNTHESIS",
            output,
        )

    def test_legacy_free_event_core_is_rejected(self) -> None:
        self._mutate_case(
            event_core=["Freie Faktensätze dürfen nicht neben dem Claimmodell entstehen."]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("Additional properties are not allowed", output)
        self.assertIn("event_core", output)

    def test_unknown_comparison_case_is_rejected(self) -> None:
        self._mutate_case(
            case_links=[
                {
                    "kind": "comparison",
                    "target": "CASE-UNKNOWN-TARGET",
                    "basis": "Struktureller Testvergleich ohne Kausalbehauptung.",
                }
            ]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("case link references unknown case CASE-UNKNOWN-TARGET", output)

    def test_case_link_may_not_target_itself(self) -> None:
        self._mutate_case(
            case_links=[
                {
                    "kind": "comparison",
                    "target": "CASE-DE-CELLER-LOCH-1978",
                    "basis": "Ein Selbstvergleich ist methodisch nicht sinnvoll.",
                }
            ]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("case link may not target itself", output)

    def test_malformed_documented_relation_id_is_reported_without_crashing(self) -> None:
        self._mutate_case(
            case_links=[
                {
                    "kind": "documented_connection",
                    "target": "CASE-DE-THS-BRANDT",
                    "basis": "Test eines strukturell ungültigen Relationstyps.",
                    "relation_id": ["REL-DE-GEHLEN-001"],
                }
            ]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("not of type 'string'", output)

    def test_documented_connection_requires_direct_relation(self) -> None:
        self._mutate_case(
            case_links=[
                {
                    "kind": "documented_connection",
                    "target": "CASE-DE-THS-BRANDT",
                    "basis": "Test einer behaupteten dokumentierten Fallverbindung.",
                    "relation_id": "REL-DE-GEHLEN-001",
                }
            ]
        )
        code, output = self._run_validator()
        self.assertEqual(1, code)
        self.assertIn("does not directly connect", output)

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