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

    def test_visible_list_link_parser_honors_implicit_li_end(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a>'
            '<li>SRC-B <a href="https://example.invalid/b">B</a></ul>'
        )
        parser.close()

        self.assertEqual(
            [
                ("SRC-A A", [("https://example.invalid/a", "A")]),
                ("SRC-B B", [("https://example.invalid/b", "B")]),
            ],
            parser.visible_items,
        )

    def test_nested_select_start_exposes_following_source_list(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<select><select></select><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_select_input_exposes_following_source_list(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<select><input><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_select_textarea_keeps_following_source_list_hidden(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<select><textarea></textarea><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()

        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_honors_implicit_paragraph_end_before_list(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<p hidden>intro'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_visible_list_link_parser_closes_implicit_paragraph_through_phrasing(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<p hidden>intro<span>format'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_closed_disclosure_after_paragraph_keeps_source_list_hidden(self) -> None:
        for tag in ("details", "dialog"):
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    f"<p>intro<{tag}><ul><li>SRC-A "
                    '<a href="https://example.invalid/a">A</a>'
                    f"</li></ul></{tag}>"
                )
                parser.close()

                self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_implicit_li_does_not_cross_special_table_scope(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li hidden>outer<table><tr><td>'
            '<li>SRC-A <a href="https://example.invalid/a">A</a></li>'
            '</td></tr></table></li></ul>'
        )
        parser.close()

        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_honors_implicit_table_row_end(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr hidden><td>old</td>'
            '<tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></td></tr></table>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_visible_list_link_parser_implicit_tr_does_not_cross_nested_table_scope(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr hidden><td>outer<table>'
            '<tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></td></tr>'
            '</table></td></tr></table>'
        )
        parser.close()

        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_honors_implicit_container_ends(self) -> None:
        samples = (
            (
                "td",
                '<table><tr><td hidden>old<td><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a></li></ul></td></tr></table>',
            ),
            (
                "th",
                '<table><tr><th hidden>old<th><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a></li></ul></th></tr></table>',
            ),
            (
                "dt",
                '<dl><dt hidden>old<dt><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a></li></ul></dt></dl>',
            ),
            (
                "dd",
                '<dl><dd hidden>old<dd><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a></li></ul></dd></dl>',
            ),
            (
                "button",
                '<button hidden>old<button><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a></li></ul></button>',
            ),
        )
        for tag, markup in samples:
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(markup)
                parser.close()
                self.assertEqual(
                    [("SRC-A A", [("https://example.invalid/a", "A")])],
                    parser.visible_items,
                )

    def test_nested_table_start_closes_hidden_outer_table_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table hidden><table><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></td></tr></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_nested_table_inside_hidden_cell_stays_hidden_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr><td hidden><table><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></table></td></tr></table>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_table_foster_parenting_exposes_non_table_source_content(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table hidden><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_hidden_table_cell_still_hides_source_content(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table hidden><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></td></tr></table>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_in_table_form_start_does_not_hide_source_row(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><form hidden><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></td></tr></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_form_inside_table_cell_still_hides_source_content(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr><td><form hidden><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></form></td></tr></table>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_honors_implicit_table_section_end(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tbody hidden><tr><td>old</td></tr>'
            '<tbody><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_omitted_colgroup_closes_before_visible_source_section(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><colgroup hidden><col>'
            '<tbody><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_plain_colgroup_does_not_hide_visible_source_section(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><colgroup><col>'
            '<tbody><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_explicitly_closed_hidden_colgroup_does_not_hide_source_section(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><colgroup hidden><col></colgroup>'
            '<tbody><tr><td><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_implicit_table_section_close_does_not_cross_nested_table_scope(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tbody hidden><tr><td><table><tbody><tr><td>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></tbody></table></td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_closes_open_heading_on_heading_start(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<h1 hidden>intro<h2><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_heading_start_does_not_pop_through_phrasing(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<h1 hidden>intro<span>format<h2><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_div_end_does_not_cross_table_cell_scope_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div hidden><table><tr><td></div>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_div_end_closes_in_scope_through_section_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div hidden><section></div>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_explicit_li_end_does_not_cross_list_item_scope_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<li hidden><ul></li><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_li_end_closes_in_scope_through_div_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<li hidden><div></li><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_explicit_heading_end_does_not_cross_html_scope_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<h1 hidden><table><tr><td></h1><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_heading_end_closes_in_scope_through_phrasing_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<h1 hidden><span></h1><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_explicit_table_end_tag_scope_target_respects_nested_table(self) -> None:
        positive = {
            "tr": ["table", "tbody", "tr", "td"],
            "td": ["table", "tbody", "tr", "td", "span"],
            "tbody": ["table", "tbody", "tr", "td"],
        }
        for tag, tags in positive.items():
            with self.subTest(tag=tag, mode="in-scope"):
                elements = [{"tag": item} for item in tags]
                self.assertEqual(
                    tag,
                    validate.explicit_end_tag_scope_target(elements, tag),
                )
        for tag, tags in positive.items():
            with self.subTest(tag=tag, mode="nested-table-blocks"):
                elements = [{"tag": item} for item in [*tags, "table"]]
                self.assertIsNone(
                    validate.explicit_end_tag_scope_target(elements, tag)
                )

    def test_explicit_tr_end_does_not_cross_nested_table_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr hidden><td><table></tr></table>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_td_end_does_not_cross_nested_table_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr><td hidden><table></td></table>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_explicit_tbody_end_does_not_cross_nested_table_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tbody hidden><tr><td><table></tbody></table>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_foreign_scope_boundaries_block_normal_scope_end_tags(self) -> None:
        boundaries = (
            ("mi", "math"),
            ("mo", "math"),
            ("mn", "math"),
            ("ms", "math"),
            ("mtext", "math"),
            ("annotation-xml", "math"),
            ("foreignobject", "svg"),
            ("desc", "svg"),
            ("title", "svg"),
        )
        for boundary, namespace in boundaries:
            with self.subTest(boundary=boundary):
                self.assertIsNone(
                    validate.explicit_end_tag_scope_target(
                        [
                            {"tag": "div", "namespace": "html"},
                            {"tag": boundary, "namespace": namespace},
                        ],
                        "div",
                    )
                )

    def test_html_custom_foreign_names_do_not_block_normal_scope_end_tags(self) -> None:
        boundaries = (
            "mi",
            "mo",
            "mn",
            "ms",
            "mtext",
            "annotation-xml",
            "foreignobject",
            "desc",
            "title",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(
                    "div",
                    validate.explicit_end_tag_scope_target(
                        [
                            {"tag": "div", "namespace": "html"},
                            {"tag": boundary, "namespace": "html"},
                        ],
                        "div",
                    ),
                )

    def test_html_title_remains_generic_special_element(self) -> None:
        self.assertIsNone(
            validate.explicit_end_tag_scope_target(
                [
                    {"tag": "span", "namespace": "html"},
                    {"tag": "title", "namespace": "html"},
                ],
                "span",
            )
        )

    def test_html_title_remains_implicit_special_boundary(self) -> None:
        title = {"tag": "title", "namespace": "html"}
        self.assertTrue(
            validate.element_matches_boundary(
                title, validate.LI_IMPLICIT_SCOPE_BOUNDARIES
            )
        )
        self.assertTrue(
            validate.element_matches_boundary(
                title, validate.DESCRIPTION_IMPLICIT_SCOPE_BOUNDARIES
            )
        )
        self.assertFalse(
            validate.element_matches_boundary(
                title, validate.HTML_SCOPE_BOUNDARY_TAGS
            )
        )

    def test_foreignobject_scope_boundary_keeps_source_hidden(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div hidden><svg><foreignObject></div><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_html_mi_does_not_block_normal_scope_end_tag_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div hidden><mi></div><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_html_mi_does_not_block_generic_end_tag_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<span hidden><mi></span><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_dialog_blocks_generic_end_tag_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<span hidden><dialog open></span><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_generic_end_tag_stops_at_html_special_element_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<span hidden><div></span><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_generic_end_tag_closes_through_phrasing_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<span hidden><em></span><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_form_end_preserves_open_hidden_descendant_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<form><div hidden></form><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_form_end_closes_empty_form_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<form hidden></form><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_nested_form_start_is_ignored_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<form hidden><form></form><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_foreign_form_end_does_not_clear_html_form_pointer_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<form hidden><svg><form></form><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul></svg></form>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_document_level_hidden_attributes_persist_for_source(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    f"<{tag} hidden></{tag}><ul><li>SRC-A "
                    '<a href="https://example.invalid/a">A</a></li></ul>'
                )
                parser.close()
                self.assertEqual([], parser.visible_items)

    def test_document_level_plain_tags_do_not_hide_source(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    f"<{tag}></{tag}><ul><li>SRC-A "
                    '<a href="https://example.invalid/a">A</a></li></ul>'
                )
                parser.close()
                self.assertEqual(
                    [("SRC-A A", [("https://example.invalid/a", "A")])],
                    parser.visible_items,
                )

    def test_anchor_end_uses_adoption_agency_recovery_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>SRC-A <a href="https://example.invalid/a">'
            "<div></a>Visible label</div></li></ul>"
        )
        parser.close()
        self.assertEqual(
            [("SRC-A Visible label", [("https://example.invalid/a", "")])],
            parser.visible_items,
        )

    def test_new_anchor_finalizes_stale_formatting_anchor_for_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>SRC-A <b><a href="https://registered.invalid"></b>'
            '<a href="https://other.invalid"></a>Visible label</li></ul>'
        )
        parser.close()
        self.assertEqual(
            [
                (
                    "SRC-A Visible label",
                    [
                        ("https://registered.invalid", ""),
                        ("https://other.invalid", ""),
                    ],
                )
            ],
            parser.visible_items,
        )

    def test_document_level_hidden_attributes_apply_retroactively_for_source(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    '<ul><li>SRC-A <a href="https://example.invalid/a">'
                    f"A</a></li></ul><{tag} hidden></{tag}>"
                )
                parser.close()
                self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_finalizes_open_anchor_and_item_at_eof(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>SRC-A <a href="https://example.invalid/a">Quelle'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A Quelle", [("https://example.invalid/a", "Quelle")])],
            parser.visible_items,
        )

    def test_foreign_content_html_breakout_restores_visible_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<svg><p><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_self_closing_foreign_html_breakout_restores_visible_source(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<svg><p/><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a></li></ul>'
        )
        parser.close()
        self.assertEqual(
            [("SRC-A A", [("https://example.invalid/a", "A")])],
            parser.visible_items,
        )

    def test_visible_list_link_parser_implicit_cell_does_not_cross_nested_table_scope(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr><td hidden>outer<table><tr><td>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
            '</td></tr></table></td></tr></table>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_implicit_description_does_not_cross_nested_dl_scope(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<dl><dt hidden>outer<dl><dt>'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
            '</dt></dl></dt></dl>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

    def test_visible_list_link_parser_implicit_container_finalizes_open_item(self) -> None:
        samples = (
            (
                "tr",
                '<table><tr><td><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a>'
                '<tr><td>next</td></tr></table>',
            ),
            (
                "td",
                '<table><tr><td><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a>'
                '<td>next</td></tr></table>',
            ),
            (
                "th",
                '<table><tr><th><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a>'
                '<th>next</th></tr></table>',
            ),
            (
                "button",
                '<button><ul><li>SRC-A '
                '<a href="https://example.invalid/a">A</a>'
                '<button>next</button>',
            ),
        )
        for tag, markup in samples:
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(markup)
                parser.close()
                self.assertEqual(
                    [("SRC-A A", [("https://example.invalid/a", "A")])],
                    parser.visible_items,
                )

    def test_implicit_container_close_does_not_lend_later_anchor_to_source_item(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<table><tr><td><ul><li>SRC-A<td>next</td></tr></table>'
            '<a href="https://example.invalid/a">Outside</a></li>'
        )
        parser.close()
        self.assertEqual([("SRC-A", [])], parser.visible_items)

    def test_hidden_or_nonrendered_element_does_not_split_visible_source_id(self) -> None:
        hidden_or_nonrendered = (
            '<input type="hidden">',
            "<wbr>",
            "<br hidden>",
            "<img hidden>",
            '<meta name="x" content="y">',
        )
        for gap in hidden_or_nonrendered:
            with self.subTest(gap=gap):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    '<ul><li>SRC-TEST'
                    + gap
                    + '-001 <a href="https://example.test/source">Quelle</a></li></ul>'
                )
                parser.close()
                self.assertEqual(1, len(parser.visible_items))
                visible_text, links = parser.visible_items[0]
                self.assertTrue(
                    validate.exact_visible_id(visible_text, "SRC-TEST-001"),
                    visible_text,
                )
                self.assertEqual(
                    [("https://example.test/source", "Quelle")],
                    links,
                )

    def test_rendered_element_splits_visible_source_id(self) -> None:
        rendered = (
            "<br>",
            '<input type="text">',
            "<video controls></video>",
            '<image src="gap.png">',
            '<image src="gap.png"/>',
        )
        for gap in rendered:
            with self.subTest(gap=gap):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    '<ul><li>SRC-TEST'
                    + gap
                    + '-001 <a href="https://example.test/source">Quelle</a></li></ul>'
                )
                parser.close()
                self.assertEqual(1, len(parser.visible_items))
                visible_text, _links = parser.visible_items[0]
                self.assertFalse(
                    validate.exact_visible_id(visible_text, "SRC-TEST-001"),
                    visible_text,
                )

    def test_inert_ancestor_keeps_source_text_but_not_clickable_link(self) -> None:
        samples = (
            '<div inert><ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul></div>',
            '<ul><li>SRC-A <a inert href="https://example.invalid/a">A</a></li></ul>',
        )
        for markup in samples:
            with self.subTest(markup=markup):
                parser = validate.VisibleListLinkParser()
                parser.feed(markup)
                parser.close()

                self.assertEqual(
                    [("SRC-A A", [])],
                    parser.visible_items,
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

    def test_self_closing_svg_root_splits_visible_source_id(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>SRC-TEST<svg/>-001 '
            '<a href="https://example.invalid/source">Quelle</a></li></ul>'
        )
        parser.close()

        self.assertEqual(1, len(parser.visible_items))
        visible_text, links = parser.visible_items[0]
        self.assertFalse(
            validate.exact_visible_id(visible_text, "SRC-TEST-001"),
            visible_text,
        )
        self.assertEqual(
            [("https://example.invalid/source", "Quelle")],
            links,
        )

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
            '<svg><text display="none">HIDDEN-SVG-TEXT</text>'
            '<text>UNPOSITIONED-SVG-TEXT</text></svg><p>VISIBLE</p>'
        )
        self.assertNotIn("HIDDEN-SVG-TEXT", visible)
        self.assertNotIn("UNPOSITIONED-SVG-TEXT", visible)
        self.assertIn("VISIBLE", visible)

    def test_unpositioned_svg_text_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<svg><text>HIDDEN-UNPOSITIONED-SVG-TEXT</text></svg>"
            "<p>VISIBLE</p>"
        )

        self.assertNotIn("HIDDEN-UNPOSITIONED-SVG-TEXT", visible)
        self.assertIn("VISIBLE", visible)

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
                    "<text>UNPOSITIONED-SVG-TEXT</text></svg><p>VISIBLE</p>"
                )
                self.assertNotIn("HIDDEN-SVG-RESOURCE", visible)
                self.assertNotIn("UNPOSITIONED-SVG-TEXT", visible)
                self.assertIn("VISIBLE", visible)

    def test_pathless_svg_textpath_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<svg><text><textPath>HIDDEN-PATHLESS-TEXTPATH</textPath></text>"
            "<text>UNPOSITIONED-SVG-TEXT</text></svg><p>VISIBLE</p>"
        )

        self.assertNotIn("HIDDEN-PATHLESS-TEXTPATH", visible)
        self.assertNotIn("UNPOSITIONED-SVG-TEXT", visible)
        self.assertIn("VISIBLE", visible)

    def test_svg_switch_unselected_branch_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<svg><switch>"
            "<text>UNPOSITIONED-FIRST-BRANCH</text>"
            "<text>HIDDEN-SECOND-BRANCH</text>"
            "</switch><text>UNPOSITIONED-OUTSIDE-SWITCH</text></svg>"
            "<p>VISIBLE</p>"
        )

        self.assertNotIn("UNPOSITIONED-FIRST-BRANCH", visible)
        self.assertNotIn("HIDDEN-SECOND-BRANCH", visible)
        self.assertNotIn("UNPOSITIONED-OUTSIDE-SWITCH", visible)
        self.assertIn("VISIBLE", visible)

    def test_self_closing_foreign_child_does_not_make_svg_text_visible(self) -> None:
        visible = validate.visible_markdown_text(
            '<svg><circle hidden /> <text>UNPOSITIONED-SVG-TEXT</text></svg>'
            '<p>VISIBLE</p>'
        )
        self.assertNotIn("UNPOSITIONED-SVG-TEXT", visible)
        self.assertIn("VISIBLE", visible)

    def test_foreign_content_html_breakout_restores_visible_text(self) -> None:
        visible = validate.visible_markdown_text("<svg><div>VISIBLE</div>")
        self.assertIn("VISIBLE", visible)

    def test_mathml_text_after_self_closing_foreign_child_remains_visible(self) -> None:
        visible = validate.visible_markdown_text(
            '<math><mi hidden /> <mtext>VISIBLE-MATH-TEXT</mtext></math>'
        )
        self.assertIn("VISIBLE-MATH-TEXT", visible)

    def test_mathml_mphantom_does_not_satisfy_text_visibility(self) -> None:
        visible = validate.visible_markdown_text(
            "<math><mphantom><mtext>HIDDEN-MATH-TEXT</mtext></mphantom>"
            "<mtext>VISIBLE-MATH-TEXT</mtext></math>"
        )

        self.assertNotIn("HIDDEN-MATH-TEXT", visible)
        self.assertIn("VISIBLE-MATH-TEXT", visible)

    def test_mathml_mphantom_does_not_satisfy_visible_source_link(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<math><mphantom><mtext><ul><li>SRC-A '
            '<a href="https://example.invalid/a">A</a>'
            '</li></ul></mtext></mphantom></math>'
        )
        parser.close()

        self.assertEqual([], parser.visible_items)

    def test_mathml_annotation_metadata_does_not_satisfy_text_visibility(self) -> None:
        for tag in ("annotation", "annotation-xml"):
            with self.subTest(tag=tag):
                visible = validate.visible_markdown_text(
                    f"<math><semantics><mrow><mtext>VISIBLE-MATH-TEXT</mtext></mrow>"
                    f"<{tag}><mtext>HIDDEN-MATH-METADATA</mtext></{tag}>"
                    "</semantics></math>"
                )

                self.assertNotIn("HIDDEN-MATH-METADATA", visible)
                self.assertIn("VISIBLE-MATH-TEXT", visible)

    def test_mathml_annotation_metadata_does_not_satisfy_visible_source_link(self) -> None:
        for tag in ("annotation", "annotation-xml"):
            with self.subTest(tag=tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    f"<math><semantics><{tag}><mtext><ul><li>SRC-A "
                    '<a href="https://example.invalid/a">A</a>'
                    f"</li></ul></mtext></{tag}></semantics></math>"
                )
                parser.close()

                self.assertEqual([], parser.visible_items)

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

    def test_duplicate_class_preserves_first_hidden_source_class(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div class="visually-hidden" class="admonition note">'
            '<ul><li>SRC-A <a href="https://example.invalid/a">A</a></li></ul>'
            '</div>'
        )
        parser.close()
        self.assertEqual([], parser.visible_items)

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
            '\n<div><audio src="about:blank"><ul><li>'
            f'<a href="{source_url}">Quelle</a> {source_id}'
            "</li></ul></audio></div>\n"
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

    def test_nested_anchor_does_not_lend_visible_text_to_registered_source_link(self) -> None:
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
            f'- {source_id} <a href="{source_url}">'
            '<a href="https://example.invalid/other"></a>'
            "Quelle</a>"
        )
        path.write_text(text.replace(source_line, replacement, 1), encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            f"source {source_id} must be visibly listed with a clickable link to its registered URL",
            output,
        )

    def test_stale_formatting_anchor_does_not_satisfy_clickable_source_link(self) -> None:
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
            f'- {source_id} <b><a href="{source_url}"></b>'
            '<a href="https://example.invalid/other"></a>Quelle'
        )
        path.write_text(text.replace(source_line, replacement, 1), encoding="utf-8")

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

    def test_strong_claim_context_only_support_is_rejected(self) -> None:
        self._mutate_first_claim(
            evidence_level="strong",
            evidence=[
                {
                    "source": "SRC-DE-NI-MJ-CELLER-2015",
                    "directness": "context",
                    "note": "Diese Quelle liefert im Test nur Kontext und keine tragende Stütze.",
                }
            ],
        )

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "with strong evidence requires at least one direct or indirect support record",
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

    def test_duplicate_class_preserves_first_hidden_claim_class(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div class="visually-hidden" class="admonition note">'
            f'{claim_id} {claim_text}</div>'
        )
        parser.close()
        self.assertNotIn(claim_id, parser.text())
        self.assertNotIn(claim_text, parser.text())

    def test_duplicate_class_preserves_first_visible_claim_class(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div class="admonition note" class="visually-hidden">'
            f'{claim_id}</div>'
        )
        parser.close()
        self.assertIn(claim_id, parser.text())

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

    def test_hidden_or_nonrendered_element_does_not_split_visible_claim_id(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        hidden_or_nonrendered = (
            '<input type="hidden">',
            "<wbr>",
            "<br hidden>",
            "<img hidden>",
            '<meta name="x" content="y">',
        )
        prefix, suffix = claim_id.rsplit("-", 1)
        for gap in hidden_or_nonrendered:
            with self.subTest(gap=gap):
                parser = validate.VisibleTextParser()
                parser.feed(f"{prefix}{gap}-{suffix}")
                parser.close()
                self.assertTrue(
                    validate.exact_visible_id(parser.text(), claim_id),
                    parser.text(),
                )

    def test_rendered_element_splits_visible_claim_id(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        prefix, suffix = claim_id.rsplit("-", 1)
        for gap in (
            "<br>",
            '<input type="text">',
            "<video controls></video>",
            '<image src="gap.png">',
            '<image src="gap.png"/>',
        ):
            with self.subTest(gap=gap):
                parser = validate.VisibleTextParser()
                parser.feed(f"{prefix}{gap}-{suffix}")
                parser.close()
                self.assertFalse(
                    validate.exact_visible_id(parser.text(), claim_id),
                    parser.text(),
                )

    def test_void_end_tags_follow_browser_recovery_for_visible_claim_id(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        prefix, suffix = claim_id.rsplit("-", 1)
        for end_tag in ("</input>", "</img>", "</embed>", "</hr>"):
            with self.subTest(end_tag=end_tag):
                parser = validate.VisibleTextParser()
                parser.feed(f"{prefix}{end_tag}-{suffix}")
                parser.close()
                self.assertTrue(
                    validate.exact_visible_id(parser.text(), claim_id),
                    parser.text(),
                )

        parser = validate.VisibleTextParser()
        parser.feed(f"{prefix}</br>-{suffix}")
        parser.close()
        self.assertFalse(
            validate.exact_visible_id(parser.text(), claim_id),
            parser.text(),
        )

    def test_void_end_tags_follow_browser_recovery_for_visible_source_id(self) -> None:
        source_id = "SRC-TEST-001"
        prefix, suffix = source_id.rsplit("-", 1)
        for end_tag in ("</input>", "</img>", "</embed>", "</hr>"):
            with self.subTest(end_tag=end_tag):
                parser = validate.VisibleListLinkParser()
                parser.feed(
                    '<ul><li>'
                    + prefix
                    + end_tag
                    + '-'
                    + suffix
                    + ' <a href="https://example.test/source">Quelle</a></li></ul>'
                )
                parser.close()
                visible_text, _links = parser.visible_items[0]
                self.assertTrue(
                    validate.exact_visible_id(visible_text, source_id),
                    visible_text,
                )

        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<ul><li>'
            + prefix
            + '</br>-'
            + suffix
            + ' <a href="https://example.test/source">Quelle</a></li></ul>'
        )
        parser.close()
        visible_text, _links = parser.visible_items[0]
        self.assertFalse(
            validate.exact_visible_id(visible_text, source_id),
            visible_text,
        )

    def test_claim_binding_stops_at_visible_section_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"## Ereigniskern\n{claim_id} ohne Wortlaut\n\n"
            f"## Spätere Analyse\n{claim_text}"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_stops_at_visible_block_start_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(f"<span>{claim_id}</span><div>{claim_text}</div>")
        parser.close()
        visible = parser.claim_binding_text()

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_rejects_lexically_empty_wording(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        visible = validate.visible_markdown_claim_binding_text(
            f"<p>{claim_id}</p>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                visible, claim_id, "----------"
            )
        )

    def test_claim_heading_binds_immediately_following_statement_paragraph(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<h3><code>{claim_id}</code></h3>"
            f"<p><strong>Aussage:</strong> {claim_text}</p>"
        )
        parser.close()

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_ignores_hidden_intervening_element(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        hidden_variants = (
            "<span hidden>ignored</span>",
            '<span aria-hidden="true">ignored</span>',
            '<span style="display: none">ignored</span>',
            "<p hidden>ignored</p>",
        )
        for hidden_html in hidden_variants:
            with self.subTest(hidden_html=hidden_html):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<h3>{claim_id}</h3>{hidden_html}<p>{claim_text}</p>"
                )
                parser.close()
                self.assertTrue(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_heading_binding_ignores_nonrendered_void_elements(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for hidden_html in (
            '<input type="hidden">',
            '<meta name="x" content="y">',
            "<wbr>",
        ):
            with self.subTest(hidden_html=hidden_html):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<h3>{claim_id}</h3>{hidden_html}<p>{claim_text}</p>"
                )
                parser.close()
                self.assertTrue(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_heading_binding_stops_at_rendered_void_element(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h3>{claim_id}</h3><input type="text"><p>{claim_text}</p>'
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_stops_at_html_image_alias(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for image in ('<image src="gap.png">', '<image src="gap.png"/>'):
            with self.subTest(image=image):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<h3>{claim_id}</h3>{image}<p>{claim_text}</p>"
                )
                parser.close()
                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_heading_binding_ignores_empty_inline_element(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h3>{claim_id}</h3><a id="bookmark"></a><p>{claim_text}</p>'
        )
        parser.close()
        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_stops_at_self_closing_rendered_void(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h3>{claim_id}</h3><input type="text"/><p>{claim_text}</p>'
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_stops_at_self_closing_svg_root(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<h3>{claim_id}</h3><svg/><p>{claim_text}</p>"
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_attributed_svg_root_stops_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h3>{claim_id}</h3>'
            '<svg width="100" height="100">'
            '<rect width="100" height="100"/></svg>'
            f'<p>{claim_text}</p>'
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_visible_text_parser_closes_open_heading_on_heading_start(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h1 hidden>intro<h3>{claim_id}</h3><p>{claim_text}</p>'
        )
        parser.close()
        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_visible_text_heading_start_does_not_pop_through_phrasing(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h1 hidden>intro<span>format<h3>{claim_id}</h3><p>{claim_text}</p>'
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_nested_table_start_closes_hidden_outer_table_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table hidden><table><tr><td><p>VISIBLE</p></td></tr></table>'
        )
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_nested_table_inside_hidden_cell_stays_hidden_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><tr><td hidden><table><tr><td><p>VISIBLE</p>'
            '</td></tr></table></td></tr></table>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_omitted_colgroup_closes_before_visible_text_section(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><colgroup hidden><col>'
            '<tbody><tr><td><p>VISIBLE_ROW</p></td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual("VISIBLE_ROW", parser.text())

    def test_plain_colgroup_does_not_hide_visible_text_section(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><colgroup><col>'
            '<tbody><tr><td><p>VISIBLE_ROW</p></td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual("VISIBLE_ROW", parser.text())

    def test_explicitly_closed_hidden_colgroup_does_not_hide_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><colgroup hidden><col></colgroup>'
            '<tbody><tr><td><p>VISIBLE_ROW</p></td></tr></tbody></table>'
        )
        parser.close()
        self.assertEqual("VISIBLE_ROW", parser.text())

    def test_hidden_table_select_does_not_break_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<h3>{claim_id}</h3><table hidden><select><option>X</option></select>'
            f'</table><p>{claim_text}</p>'
        )
        parser.close()
        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_table_foster_parenting_exposes_non_table_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<table hidden><p>VISIBLE</p></table>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_hidden_table_cell_still_hides_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<table hidden><tr><td><p>VISIBLE</p></td></tr></table>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_in_table_rawtext_elements_remain_hidden_for_visible_text(self) -> None:
        for tag in ("style", "script"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(f"<table><{tag}>HIDDEN_RAWTEXT</{tag}></table>")
                parser.close()
                self.assertEqual("", parser.text())

    def test_in_table_form_start_does_not_hide_visible_text_row(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><form hidden><tr><td><p>VISIBLE</p></td></tr></table>'
        )
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_form_inside_table_cell_still_hides_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><tr><td><form hidden><p>VISIBLE</p></form></td></tr></table>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_div_end_does_not_cross_table_cell_scope_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<div hidden><table><tr><td></div><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_div_end_closes_in_scope_through_section_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<div hidden><section></div><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_explicit_li_end_does_not_cross_list_item_scope_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<li hidden><ul></li><li>VISIBLE</li>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_li_end_closes_in_scope_through_div_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<li hidden><div></li><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_explicit_heading_end_does_not_cross_html_scope_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<h1 hidden><table><tr><td></h1><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_heading_end_closes_in_scope_through_phrasing_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<h1 hidden><span></h1><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_explicit_tr_end_does_not_cross_nested_table_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><tr hidden><td><table></tr></table><span>VISIBLE</span>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_td_end_does_not_cross_nested_table_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><tr><td hidden><table></td></table><span>VISIBLE</span>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_explicit_tbody_end_does_not_cross_nested_table_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<table><tbody hidden><tr><td><table></tbody></table>'
            '<span>VISIBLE</span>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_foreignobject_scope_boundary_keeps_visible_text_hidden(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div hidden><svg><foreignObject></div><span>VISIBLE</span>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_html_mi_does_not_block_normal_scope_end_tag_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<div hidden><mi></div><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_html_mi_does_not_block_generic_end_tag_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<span hidden><mi></span><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_dialog_blocks_generic_end_tag_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<span hidden><dialog open></span><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_generic_end_tag_stops_at_html_special_element_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<span hidden><div></span><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_generic_end_tag_closes_through_phrasing_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<span hidden><em></span><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_form_end_preserves_open_hidden_descendant_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<form><div hidden></form><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_form_end_closes_empty_form_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<form hidden></form><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_nested_form_start_is_ignored_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<form hidden><form></form><span>VISIBLE</span>')
        parser.close()
        self.assertEqual("VISIBLE", parser.text())

    def test_foreign_form_end_does_not_clear_html_form_pointer_for_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed('<form hidden><svg><form></form><p>VISIBLE</p></svg></form>')
        parser.close()
        self.assertEqual("", parser.text())

    def test_document_level_hidden_attributes_persist_for_visible_text(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(f"<{tag} hidden></{tag}><p>VISIBLE</p>")
                parser.close()
                self.assertEqual("", parser.text())

    def test_document_level_plain_tags_do_not_hide_visible_text(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(f"<{tag}></{tag}><p>VISIBLE</p>")
                parser.close()
                self.assertEqual("VISIBLE", parser.text())

    def test_document_level_hidden_attributes_apply_retroactively_for_visible_text(self) -> None:
        for tag in ("html", "body"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(f"<p>VISIBLE</p><{tag} hidden></{tag}>")
                parser.close()
                self.assertEqual("", parser.text())

    def test_styled_rendered_separator_stops_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f'<span>{claim_id} </span><hr style="color:red">'
            f'<span> {claim_text}</span>'
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_stops_at_rendered_hidden_text_controls(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        rendered_controls = (
            "<video controls></video>",
            "<select><option>eins</option></select>",
            '<meter value="1" max="2"></meter>',
            '<progress value="1" max="2"></progress>',
            "<canvas></canvas>",
            "<iframe></iframe>",
            '<object data="about:blank"></object>',
            "<audio controls></audio>",
        )
        for control in rendered_controls:
            with self.subTest(control=control):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<h3>{claim_id}</h3>{control}<p>{claim_text}</p>"
                )
                parser.close()
                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_heading_binding_ignores_hidden_or_nonrendered_controls(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        hidden_controls = (
            "<audio></audio>",
            "<video controls hidden></video>",
            "<select hidden><option>eins</option></select>",
        )
        for control in hidden_controls:
            with self.subTest(control=control):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<h3>{claim_id}</h3>{control}<p>{claim_text}</p>"
                )
                parser.close()
                self.assertTrue(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_heading_rendered_gap_delimits_raw_following_wording(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        rendered_gaps = (
            '<input type="text">',
            "<br>",
            "<video controls></video>",
            "<span>sichtbar</span>",
        )
        for gap in rendered_gaps:
            with self.subTest(gap=gap):
                parser = validate.VisibleTextParser()
                parser.feed(f"<h3>{claim_id}</h3>{gap}{claim_text}")
                parser.close()
                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    ),
                    parser.claim_binding_text(),
                )

    def test_claim_heading_raw_text_requires_statement_paragraph(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(f"<h3>{claim_id}</h3>{claim_text}")
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_binding_stops_at_visible_intervening_inline(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<h3>{claim_id}</h3><span>visible</span><p>{claim_text}</p>"
        )
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_inline_claim_id_does_not_bind_following_paragraph(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(f"<span>{claim_id}</span><p>{claim_text}</p>")
        parser.close()

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_heading_exception_does_not_cross_intervening_block(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<h3>{claim_id}</h3><div>Zwischenblock</div><p>{claim_text}</p>"
        )
        parser.close()

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_claim_binding_stops_at_visible_list_record_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"- {claim_id} ohne Wortlaut\n- {claim_text}"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_stops_at_visible_paragraph_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"{claim_id} ohne Wortlaut\n\n{claim_text}"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_stops_at_thematic_break(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<span>{claim_id} ohne Wortlaut</span>"
            f"<hr><span>{claim_text}</span>"
        )
        parser.close()

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_closed_details_without_summary_splits_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<span>{claim_id} </span><details>collapsed</details>"
            f"<span>{claim_text}</span>"
        )
        parser.close()

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_named_details_splits_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for details in (
            '<details name="group" open><summary>sichtbar</summary>ignored</details>',
            '<details name="group"><summary>sichtbar</summary>ignored</details>',
        ):
            with self.subTest(details=details):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<span>{claim_id} </span>{details}<span>{claim_text}</span>"
                )
                parser.close()
                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    ),
                    parser.claim_binding_text(),
                )

    def test_end_br_stops_claim_heading_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(f"<h3>{claim_id}</h3></br><p>{claim_text}</p>")
        parser.close()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            ),
            parser.claim_binding_text(),
        )

    def test_hidden_closed_details_does_not_split_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(
            f"<span>{claim_id} </span><details hidden>collapsed</details>"
            f"<span>{claim_text}</span>"
        )
        parser.close()

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(
                parser.claim_binding_text(), claim_id, claim_text
            )
        )

    def test_hidden_thematic_break_does_not_split_claim_binding(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        hidden_breaks = (
            "<hr hidden>",
            "<hr hidden/>",
            '<hr aria-hidden="true">',
            '<hr style="display:none">',
            '<hr class="visually-hidden">',
            "<hr popover>",
        )
        for hr in hidden_breaks:
            with self.subTest(hr=hr):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<span>{claim_id} </span>{hr}<span>{claim_text}</span>"
                )
                parser.close()

                self.assertTrue(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_binding_stops_at_remaining_preformatted_and_menu_blocks(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for tag in ("listing", "menu", "xmp"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<span>{claim_id} ohne Wortlaut </span>"
                    f"<{tag}>{claim_text}</{tag}>"
                )
                parser.close()

                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_implicit_paragraph_closes_before_browser_block_starts(self) -> None:
        samples = {
            "center": "<p hidden>intro<center>VISIBLE-center</center>",
            "details": "<p hidden>intro<details open>VISIBLE-details</details>",
            "dialog": "<p hidden>intro<dialog open>VISIBLE-dialog</dialog>",
            "dir": "<p hidden>intro<dir>VISIBLE-dir</dir>",
            "figcaption": "<p hidden>intro<figcaption>VISIBLE-figcaption</figcaption>",
            "figure": "<p hidden>intro<figure>VISIBLE-figure</figure>",
            "listing": "<p hidden>intro<listing>VISIBLE-listing</listing>",
            "summary": "<p hidden>intro<summary>VISIBLE-summary</summary>",
            "xmp": "<p hidden>intro<xmp>VISIBLE-xmp</xmp>",
        }
        for tag, markup in samples.items():
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(markup)
                parser.close()

                self.assertIn(f"VISIBLE-{tag}", parser.text())

    def test_claim_binding_stops_at_visible_block_container_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for tag in ("div", "article", "section"):
            with self.subTest(tag=tag):
                visible = validate.visible_markdown_claim_binding_text(
                    f"<{tag}>{claim_id} ohne Wortlaut</{tag}>"
                    f"<{tag}>{claim_text}</{tag}>"
                )

                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        visible, claim_id, claim_text
                    )
                )

    def test_claim_binding_stops_at_legacy_block_container_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for tag in ("center", "dir", "search"):
            with self.subTest(tag=tag):
                parser = validate.VisibleTextParser()
                parser.feed(
                    f"<span>{claim_id} ohne Wortlaut </span>"
                    f"<{tag}>{claim_text}</{tag}>"
                )
                parser.close()

                self.assertFalse(
                    validate.claim_occurrences_bound_to_wording(
                        parser.claim_binding_text(), claim_id, claim_text
                    )
                )

    def test_claim_binding_accepts_wording_before_id_in_same_record(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"{claim_text} ({claim_id})"
        )

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_honors_implicit_paragraph_end(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<p>{claim_id} ohne Wortlaut<p>{claim_text}"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_honors_implicit_button_end(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<button>{claim_id} ohne Wortlaut<button>{claim_text}"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_accepts_wording_across_cells_in_same_table_row(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            "| Claim | Aussage |\n"
            "| --- | --- |\n"
            f"| {claim_id} | {claim_text} |"
        )

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_stops_between_table_rows(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            "| Claim | Aussage |\n"
            "| --- | --- |\n"
            f"| {claim_id} | ohne Wortlaut |\n"
            f"| anderer Claim | {claim_text} |"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_honors_implicit_li_end_in_same_list_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<ul><li>{claim_id} ohne Wortlaut<li>{claim_text}</ul>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_li_does_not_cross_nested_list_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<ul><li hidden>outer<ul><li>{claim_id} {claim_text}</li></ul></li></ul>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_honors_implicit_dt_end_in_same_dl_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<dl><dt>{claim_id} ohne Wortlaut<dt>{claim_text}</dl>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_dt_does_not_cross_nested_dl_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<dl><dt hidden>outer<dl><dt>{claim_id} {claim_text}</dt></dl></dt></dl>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_honors_implicit_tr_end_in_same_table_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<table><tr><td>{claim_id} ohne Wortlaut<tr><td>{claim_text}</table>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_tr_does_not_cross_nested_table_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<table><tr hidden><td>outer<table><tr><td>{claim_id} {claim_text}</td></tr></table></td></tr></table>"
        )

        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_accepts_wording_across_implicitly_closed_table_cells(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        for cell_tag in ("td", "th"):
            with self.subTest(cell_tag=cell_tag):
                visible = validate.visible_markdown_claim_binding_text(
                    f"<table><tr><{cell_tag}>{claim_id}"
                    f"<{cell_tag}>{claim_text}</tr></table>"
                )
                self.assertTrue(
                    validate.claim_occurrences_bound_to_wording(
                        visible, claim_id, claim_text
                    )
                )

    def test_claim_binding_implicit_button_does_not_cross_scope_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<button hidden>outer<table><tr><td>"
            f"<button>{claim_id} {claim_text}</button>"
            f"</td></tr></table></button>"
        )
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_orphan_paragraph_end_inserts_claim_binding_boundary(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        parser = validate.VisibleTextParser()
        parser.feed(f"<span>{claim_id} </span></p><span>{claim_text}</span>")
        parser.close()
        visible = parser.claim_binding_text()
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_paragraph_does_not_cross_button_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<p hidden>outer<button>inside<ul>"
            f"<li>{claim_id} {claim_text}</li>"
            f"</ul></button></p>"
        )
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_li_does_not_cross_special_table_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<ul><li hidden>outer<table><tr><td>"
            f"<li>{claim_id} {claim_text}</li>"
            f"</td></tr></table></li></ul>"
        )
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_binding_implicit_dt_does_not_cross_special_table_scope(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"<dl><dt hidden>outer<table><tr><td>"
            f"<dt>{claim_id} {claim_text}</dt>"
            f"</td></tr></table></dt></dl>"
        )
        self.assertFalse(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
        )

    def test_claim_heading_binds_wording_within_same_section(self) -> None:
        claim_id = "CLM-DE-CELLER-001"
        claim_text = (
            "Der niedersächsische Verfassungsschutz ließ am 25. Juli 1978 "
            "die Außenmauer der JVA Celle sprengen."
        )
        visible = validate.visible_markdown_claim_binding_text(
            f"### `{claim_id}`\n\n**Aussage:** {claim_text}\n\n### Nächster Abschnitt"
        )

        self.assertTrue(
            validate.claim_occurrences_bound_to_wording(visible, claim_id, claim_text)
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

    def test_nested_select_start_exposes_following_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed("<select><select></select><p>VISIBLE-AFTER-SELECT</p>")
        parser.close()

        self.assertEqual("VISIBLE-AFTER-SELECT", parser.text())

    def test_select_input_exposes_following_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed("<select><input><p>VISIBLE-AFTER-SELECT</p>")
        parser.close()

        self.assertEqual("VISIBLE-AFTER-SELECT", parser.text())

    def test_select_textarea_keeps_following_visible_text_hidden(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            "<select><textarea></textarea><p>HIDDEN-AFTER-TEXTAREA</p>"
        )
        parser.close()

        self.assertEqual("", parser.text())

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
            "svg": "Alpha<svg><text>Ignored</text></svg>Beta",
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

    def test_claim_text_requires_lexical_tokens(self) -> None:
        self._mutate_first_claim(text="----------")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "claim CLM-DE-CELLER-001 text must contain lexical tokens",
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

    def test_event_core_checks_second_visible_matching_section(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "\n## Rekonstruktion",
            "\n## Rekonstruktion\n\nZwischentext.\n\n"
            "## Gesicherter Ereigniskern\n\n"
            "- CLM-DE-CELLER-NON-EVENT\n\n"
            "## Fortsetzung",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(1, code)
        self.assertIn(
            "Gesicherter Ereigniskern includes non-event claim CLM-DE-CELLER-NON-EVENT",
            output,
        )

    def test_event_core_section_recovers_previous_unclosed_heading(self) -> None:
        parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
        parser.feed(
            "<h2>Previous"
            "<h2>Gesicherter Ereigniskern</h2>"
            "<p>CLM-X visible claim</p>"
            "<h2>Next</h2>"
        )
        parser.close()
        self.assertEqual("CLM-X visible claim", parser.text())

    def test_event_core_section_recovers_mismatched_heading_end_tags(self) -> None:
        for closing_tag in ("h1", "h3", "h4", "h5", "h6"):
            with self.subTest(closing_tag=closing_tag):
                parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
                parser.feed(
                    f"<h2>Gesicherter Ereigniskern</{closing_tag}>"
                    "<p>CLM-X visible claim</p>"
                    "<h2>Next</h2><p>later</p>"
                )
                parser.close()
                self.assertEqual("CLM-X visible claim", parser.text())

    def test_event_core_separates_adjacent_matching_sections(self) -> None:
        parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
        parser.feed(
            "<h2>Gesicherter Ereigniskern</h2>canonical"
            "<h2>Gesicherter Ereigniskern</h2>CLM-DE-CELLER-NON-EVENT"
        )
        parser.close()
        visible = parser.text()
        self.assertRegex(
            visible,
            r"canonical\s+CLM-DE-CELLER-NON-EVENT",
        )
        self.assertRegex(
            visible,
            r"(?<![\w-])CLM-DE-CELLER-NON-EVENT(?![\w-])",
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

    def test_event_core_ignores_unpositioned_svg_text(self) -> None:
        path = self._case_path()
        text = path.read_text(encoding="utf-8").replace(
            "\n## Rekonstruktion",
            "\n<svg><circle hidden /><text>CLM-DE-CELLER-NON-EVENT</text></svg>\n\n## Rekonstruktion",
            1,
        )
        path.write_text(text, encoding="utf-8")

        code, output = self._run_validator()

        self.assertEqual(0, code, output)

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