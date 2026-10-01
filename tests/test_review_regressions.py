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


if __name__ == "__main__":
    unittest.main()
