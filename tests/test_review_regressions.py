from __future__ import annotations

import unittest

import scripts.validate as validate


class ReviewRegressionTests(unittest.TestCase):
    def test_section_heading_ignored_inside_select_does_not_capture_following_text(self) -> None:
        rendered = validate.render_site_markdown(
            "<h2>Gesicherter Ereigniskern</h2>"
            "<select><h2>ignored</select>"
            "<p>CLM-X wording</p>"
        )
        parser = validate.VisibleSectionTextParser(
            "Gesicherter Ereigniskern",
            validate.has_author_stylesheet(rendered),
        )
        parser.feed(rendered)
        parser.close()

        self.assertEqual("CLM-X wording", parser.text())

    def test_raw_text_containers_do_not_create_source_links(self) -> None:
        samples = (
            "<xmp><ul><li>SRC-A <a href=\"u\">A</a></li></ul></xmp>",
            "<plaintext><ul><li>SRC-A <a href=\"u\">A</a></li></ul>",
            "<plaintext>raw</plaintext><ul><li>SRC-A <a href=\"u\">A</a></li></ul>",
        )
        for markup in samples:
            with self.subTest(markup=markup):
                parser = validate.VisibleListLinkParser()
                parser.feed(markup)
                parser.close()
                self.assertEqual([], parser.visible_items)

    def test_xmp_closer_resumes_normal_link_parsing(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            "<xmp><a href=\"ignored\">ignored</a></xmp>"
            "<ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        parser.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], parser.visible_items)

    def test_plaintext_fake_closer_remains_literal_visible_text(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            "<plaintext>before</plaintext>"
            "<span>CLM-X wording</span>"
        )
        parser.close()

        self.assertIn("</plaintext><span>CLM-X wording</span>", parser.text())

    def test_table_start_is_ignored_inside_ordinary_select(self) -> None:
        markup = (
            "<select><table></select>"
            "<ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertEqual("SRC-A A", text.text())

    def test_template_end_pops_open_descendants(self) -> None:
        markup = (
            "<template><div></template>"
            "<ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertEqual("SRC-A A", text.text())


    def test_document_tags_are_ignored_while_template_is_in_scope(self) -> None:
        markup = (
            "<template><body hidden></body></template>"
            "<ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertEqual("SRC-A A", text.text())

    def test_template_form_does_not_clear_outer_form_pointer(self) -> None:
        markup = (
            "<form><template><form></form></template>"
            "<form hidden><ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertEqual("SRC-A A", text.text())

if __name__ == "__main__":
    unittest.main()
