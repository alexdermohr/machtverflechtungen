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


if __name__ == "__main__":
    unittest.main()
