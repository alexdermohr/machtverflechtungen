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

    def test_document_tag_template_detection_crosses_foreign_integration_points(self) -> None:
        markup = (
            "<template><svg><foreignObject><body hidden></body></foreignObject></svg></template>"
            "<ul><li>SRC-A <a href=\"u\">A</a></li></ul>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertIn("SRC-A A", text.text())

    def test_frameset_start_is_ignored_in_body_fragment(self) -> None:
        markup = (
            "<p>BEFORE</p>"
            "<frameset hidden><ul><li>SRC-A <a href=\"u\">A</a></li></ul></frameset>"
            "<button>AFTER</button>"
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)
        self.assertIn("SRC-A A", text.text())

    def test_executable_author_content_is_a_visibility_mutator(self) -> None:
        samples = (
            "<script>document.body.hidden=true</script>",
            '<img src="missing" onerror="document.body.hidden=true">',
            '<iframe srcdoc="<script>parent.document.body.hidden=true</script>"></iframe>',
            '<a href="javascript:document.body.hidden=true">trigger</a>',
        )
        for markup in samples:
            with self.subTest(markup=markup):
                rendered = validate.render_site_markdown(markup)
                self.assertTrue(validate.has_author_visibility_mutator(rendered))

    def test_author_script_disqualifies_static_visibility_evidence(self) -> None:
        rendered = validate.render_site_markdown(
            '<ul id="evidence"><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X wording</p>'
            '<script>document.querySelector("#evidence").hidden=true</script>'
        )
        mutator_present = validate.has_author_visibility_mutator(rendered)

        links = validate.VisibleListLinkParser(mutator_present)
        links.feed(rendered)
        links.close()
        visible_text = validate.VisibleTextParser(mutator_present)
        visible_text.feed(rendered)
        visible_text.close()

        self.assertEqual([], links.visible_items)
        self.assertEqual("", visible_text.text())

    def test_executable_scanner_preserves_raw_text_contexts(self) -> None:
        script = '<script>document.querySelector("#evidence").hidden=true</script>'
        samples = (
            f"<xmp>{script}</xmp>",
            f"<iframe>{script}</iframe>",
            f"<noscript>{script}</noscript>",
            f"<noembed>{script}</noembed>",
            f"<noframes>{script}</noframes>",
            f"<plaintext>{script}",
            f"<textarea>{script}</textarea>",
        )
        for markup in samples:
            with self.subTest(markup=markup):
                rendered = validate.render_site_markdown(markup)
                self.assertFalse(validate.has_author_executable_content(rendered))

        self.assertTrue(validate.has_author_executable_content(script))
        self.assertTrue(
            validate.has_author_executable_content(f"<xmp>literal</xmp>{script}")
        )
        self.assertFalse(
            validate.has_author_executable_content(
                f"<plaintext>literal</plaintext>{script}"
            )
        )


    def test_stylesheet_scanner_preserves_raw_text_contexts(self) -> None:
        style = "<style>#evidence{display:none}</style>"
        samples = (
            f"<xmp>{style}</xmp>",
            f"<iframe>{style}</iframe>",
            f"<noscript>{style}</noscript>",
            f"<noembed>{style}</noembed>",
            f"<noframes>{style}</noframes>",
            f"<plaintext>{style}",
            f"<textarea>{style}</textarea>",
        )
        for markup in samples:
            with self.subTest(markup=markup):
                rendered = validate.render_site_markdown(markup)
                self.assertFalse(validate.has_author_stylesheet(rendered))

        self.assertTrue(validate.has_author_stylesheet(style))
        self.assertTrue(validate.has_author_stylesheet(f"<xmp>literal</xmp>{style}"))
        self.assertFalse(
            validate.has_author_stylesheet(
                f"<plaintext>literal</plaintext>{style}"
            )
        )

    def test_javascript_url_detection_removes_ascii_tab_and_newline(self) -> None:
        samples = (
            '<iframe src="java&#10;script:parent.document.body.hidden=true"></iframe>',
            '<iframe src="java&#13;script:parent.document.body.hidden=true"></iframe>',
            '<a href="java&#9;script:document.body.hidden=true">x</a>',
        )
        for markup in samples:
            with self.subTest(markup=markup):
                rendered = validate.render_site_markdown(markup)
                self.assertTrue(validate.has_author_executable_content(rendered))

    def test_self_closed_foreign_raw_text_tag_does_not_swallow_script(self) -> None:
        markup = (
            '<svg><iframe/>'
            '<script>document.body.hidden=true</script>'
            '</svg>'
        )
        rendered = validate.render_site_markdown(markup)
        self.assertTrue(validate.has_author_executable_content(rendered))

    def test_javascript_url_detection_strips_leading_ascii_c0_and_space(self) -> None:
        samples = (
            '<iframe src="\x01javascript:parent.document.body.hidden=true"></iframe>',
            '<iframe src="\x1fjavascript:parent.document.body.hidden=true"></iframe>',
            '<iframe src=" javascript:parent.document.body.hidden=true"></iframe>',
            '<iframe src="\x01java&#10;script:parent.document.body.hidden=true"></iframe>',
        )
        for markup in samples:
            with self.subTest(markup=repr(markup)):
                rendered = validate.render_site_markdown(markup)
                self.assertTrue(validate.has_author_executable_content(rendered))

    def test_script_detection_respects_mathml_namespace(self) -> None:
        self.assertFalse(
            validate.has_author_executable_content(
                '<math><script>document.body.hidden=true</script></math>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<svg><script>document.body.hidden=true</script></svg>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<script>document.body.hidden=true</script>'
            )
        )

    def test_foreign_breakout_reprocesses_script_as_html(self) -> None:
        self.assertTrue(
            validate.has_author_executable_content(
                '<math><p><script>document.body.hidden=true</script></p></math>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<math><script>document.body.hidden=true</script></math>'
            )
        )

    def test_annotation_xml_html_encoding_is_integration_point(self) -> None:
        for encoding in ("text/html", "application/xhtml+xml"):
            with self.subTest(encoding=encoding):
                self.assertTrue(
                    validate.has_author_executable_content(
                        '<math><annotation-xml encoding="'
                        + encoding
                        + '"><script>document.body.hidden=true</script>'
                        '</annotation-xml></math>'
                    )
                )

        self.assertFalse(
            validate.has_author_executable_content(
                '<math><annotation-xml encoding="application/xml">'
                '<script>document.body.hidden=true</script>'
                '</annotation-xml></math>'
            )
        )

    def test_stylesheet_detection_respects_namespace(self) -> None:
        self.assertFalse(
            validate.has_author_stylesheet(
                '<math><style>#evidence{display:none}</style></math>'
            )
        )
        self.assertTrue(
            validate.has_author_stylesheet(
                '<svg><style>#evidence{display:none}</style></svg>'
            )
        )
        self.assertTrue(
            validate.has_author_stylesheet(
                '<style>#evidence{display:none}</style>'
            )
        )
        self.assertFalse(
            validate.has_author_stylesheet(
                '<math><link rel="stylesheet" href="theme.css"></math>'
            )
        )
        self.assertTrue(
            validate.has_author_stylesheet(
                '<link rel="stylesheet" href="theme.css">'
            )
        )

    def test_mathml_text_integration_exceptions_remain_mathml(self) -> None:
        for tag in ("mglyph", "malignmark"):
            with self.subTest(tag=tag):
                self.assertFalse(
                    validate.has_author_executable_content(
                        '<math><mtext><'
                        + tag
                        + '><script>document.body.hidden=true</script></'
                        + tag
                        + '></mtext></math>'
                    )
                )

        self.assertTrue(
            validate.has_author_executable_content(
                '<math><mtext><div><script>document.body.hidden=true</script>'
                '</div></mtext></math>'
            )
        )

    def test_template_contents_are_inert_for_author_mutator_detection(self) -> None:
        self.assertFalse(
            validate.has_author_executable_content(
                '<template><script>document.body.hidden=true</script></template>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<template/><script>document.body.hidden=true</script>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<div><template></div><script>document.body.hidden=true</script>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<template><script>document.body.hidden=true</script></template>'
                '<script>document.body.hidden=true</script>'
            )
        )

    def test_declarative_shadow_template_contents_are_active_mutators(self) -> None:
        for mode in ("open", "closed"):
            with self.subTest(mode=mode):
                self.assertTrue(
                    validate.has_author_stylesheet(
                        '<div><template shadowrootmode="'
                        + mode
                        + '"><style>:host{display:none}</style><slot></slot>'
                        '</template><a href="#">A</a></div>'
                    )
                )
                self.assertTrue(
                    validate.has_author_executable_content(
                        '<div><template shadowrootmode="'
                        + mode
                        + '"><script>document.body.hidden=true</script>'
                        '</template><a href="#">A</a></div>'
                    )
                )

        self.assertFalse(
            validate.has_author_stylesheet(
                '<div><template shadowrootmode="bogus">'
                '<style>:host{display:none}</style></template></div>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<div><template shadowrootmode="bogus">'
                '<script>document.body.hidden=true</script></template></div>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<template><div><template shadowrootmode="open">'
                '<script>document.body.hidden=true</script></template></div></template>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<div><template shadowrootmode="open"><template>'
                '<script>document.body.hidden=true</script></template></template></div>'
            )
        )
        rejected_same_host = (
            '<div><template shadowrootmode="open"><slot></slot></template>'
            '<template shadowrootmode="open">{payload}</template></div>'
        )
        self.assertFalse(
            validate.has_author_stylesheet(
                rejected_same_host.format(
                    payload='<style>body{display:none}</style>'
                )
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                rejected_same_host.format(
                    payload='<script>document.body.hidden=true</script>'
                )
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<a><template shadowrootmode="open">'
                '<script>document.body.hidden=true</script></template></a>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<x-host><template shadowrootmode="open">'
                '<script>document.body.hidden=true</script></template></x-host>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<div><template shadowrootmode="open"><span>'
                '<template shadowrootmode="open">'
                '<script>document.body.hidden=true</script></template></span>'
                '</template></div>'
            )
        )

if __name__ == "__main__":
    unittest.main()
