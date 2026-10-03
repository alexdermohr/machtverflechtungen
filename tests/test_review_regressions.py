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


    def test_declarative_shadow_template_after_html_void_sibling_is_active(self) -> None:
        self.assertTrue(
            validate.has_author_executable_content(
                '<div><img><template shadowrootmode="open">'
                '<script>document.body.hidden=true</script>'
                '</template></div>'
            )
        )
        self.assertTrue(
            validate.has_author_stylesheet(
                '<div><input><template shadowrootmode="closed">'
                '<style>:host{display:none}</style>'
                '</template></div>'
            )
        )

    def test_search_is_not_a_declarative_shadow_host(self) -> None:
        self.assertFalse(
            validate.has_author_executable_content(
                '<search><template shadowrootmode="open">'
                '<script>document.body.hidden=true</script>'
                '</template></search>'
            )
        )

    def test_visible_text_uses_active_declarative_shadow_tree(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div><template shadowrootmode="open">'
            '<span>SHADOW-ONLY</span></template>'
            '<span>UNSLOTTED-LIGHT</span></div>'
        )
        parser.close()

        self.assertIn("SHADOW-ONLY", parser.text())
        self.assertNotIn("UNSLOTTED-LIGHT", parser.text())

    def test_visible_text_rolls_back_light_content_preceding_shadow_template(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div><span>BEFORE-SHADOW</span>'
            '<template shadowrootmode="open">'
            '<span>SHADOW-AFTER</span></template></div>'
        )
        parser.close()

        self.assertIn("SHADOW-AFTER", parser.text())
        self.assertNotIn("BEFORE-SHADOW", parser.text())

    def test_visible_text_applies_default_and_named_shadow_slots(self) -> None:
        default_slot = validate.VisibleTextParser()
        default_slot.feed(
            '<div><template shadowrootmode="open">'
            '<span>SHADOW-CONTENT</span><slot></slot></template>'
            '<span>DEFAULT-SLOTTED</span>'
            '<span slot="named">NAMED-WITHOUT-SLOT</span></div>'
        )
        default_slot.close()
        self.assertIn("SHADOW-CONTENT", default_slot.text())
        self.assertIn("DEFAULT-SLOTTED", default_slot.text())
        self.assertNotIn("NAMED-WITHOUT-SLOT", default_slot.text())

        named_slot = validate.VisibleTextParser()
        named_slot.feed(
            '<div><template shadowrootmode="open">'
            '<slot name="evidence"></slot></template>'
            '<span slot="evidence">NAMED-SLOTTED</span>'
            '<span>DEFAULT-WITHOUT-SLOT</span></div>'
        )
        named_slot.close()
        self.assertIn("NAMED-SLOTTED", named_slot.text())
        self.assertNotIn("DEFAULT-WITHOUT-SLOT", named_slot.text())

    def test_visible_list_links_use_active_declarative_shadow_tree(self) -> None:
        parser = validate.VisibleListLinkParser()
        parser.feed(
            '<div><template shadowrootmode="open">'
            '<ul><li>SRC-S <a href="shadow">Shadow</a></li></ul>'
            '</template>'
            '<ul><li>SRC-L <a href="light">Light</a></li></ul></div>'
        )
        parser.close()

        self.assertEqual(
            [("SRC-S Shadow", [("shadow", "Shadow")])],
            parser.visible_items,
        )

    def test_visibility_parsers_keep_rejected_shadow_templates_inert(self) -> None:
        markup = (
            '<div><template shadowrootmode="open">'
            '<span>FIRST-SHADOW</span></template>'
            '<template shadowrootmode="open">'
            '<span>REJECTED-SHADOW</span></template>'
            '<span>UNSLOTTED-LIGHT</span></div>'
        )
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertIn("FIRST-SHADOW", text.text())
        self.assertNotIn("REJECTED-SHADOW", text.text())
        self.assertNotIn("UNSLOTTED-LIGHT", text.text())


    def test_visible_text_handles_slot_fallback_and_pre_template_assignments(self) -> None:
        fallback = validate.VisibleTextParser()
        fallback.feed(
            '<div><template shadowrootmode="open">'
            '<slot><span>FALLBACK-VISIBLE</span></slot>'
            '</template></div>'
        )
        fallback.close()
        self.assertIn("FALLBACK-VISIBLE", fallback.text())

        assigned = validate.VisibleTextParser()
        assigned.feed(
            '<div><template shadowrootmode="open">'
            '<slot><span>FALLBACK-HIDDEN</span></slot>'
            '</template><span>ASSIGNED-VISIBLE</span></div>'
        )
        assigned.close()
        self.assertIn("ASSIGNED-VISIBLE", assigned.text())
        self.assertNotIn("FALLBACK-HIDDEN", assigned.text())

        pre_default = validate.VisibleTextParser()
        pre_default.feed(
            '<div><span>PRE-DEFAULT-VISIBLE</span>'
            '<template shadowrootmode="open"><slot></slot></template></div>'
        )
        pre_default.close()
        self.assertIn("PRE-DEFAULT-VISIBLE", pre_default.text())

        pre_named = validate.VisibleTextParser()
        pre_named.feed(
            '<div><span slot="evidence">PRE-NAMED-VISIBLE</span>'
            '<template shadowrootmode="open">'
            '<slot name="evidence"></slot></template></div>'
        )
        pre_named.close()
        self.assertIn("PRE-NAMED-VISIBLE", pre_named.text())

    def test_visible_list_links_handle_slot_fallback_and_pre_template_assignments(self) -> None:
        fallback = validate.VisibleListLinkParser()
        fallback.feed(
            '<div><template shadowrootmode="open"><slot>'
            '<ul><li>SRC-F <a href="fallback">Fallback</a></li></ul>'
            '</slot></template></div>'
        )
        fallback.close()
        self.assertEqual(
            [("SRC-F Fallback", [("fallback", "Fallback")])],
            fallback.visible_items,
        )

        assigned = validate.VisibleListLinkParser()
        assigned.feed(
            '<div><template shadowrootmode="open"><slot>'
            '<ul><li>SRC-F <a href="fallback">Fallback</a></li></ul>'
            '</slot></template>'
            '<ul><li>SRC-A <a href="assigned">Assigned</a></li></ul></div>'
        )
        assigned.close()
        self.assertEqual(
            [("SRC-A Assigned", [("assigned", "Assigned")])],
            assigned.visible_items,
        )

        pre_default = validate.VisibleListLinkParser()
        pre_default.feed(
            '<div><ul><li>SRC-D <a href="default">Default</a></li></ul>'
            '<template shadowrootmode="open"><slot></slot></template></div>'
        )
        pre_default.close()
        self.assertEqual(
            [("SRC-D Default", [("default", "Default")])],
            pre_default.visible_items,
        )

        pre_named = validate.VisibleListLinkParser()
        pre_named.feed(
            '<div><ul slot="evidence">'
            '<li>SRC-N <a href="named">Named</a></li></ul>'
            '<template shadowrootmode="open">'
            '<slot name="evidence"></slot></template></div>'
        )
        pre_named.close()
        self.assertEqual(
            [("SRC-N Named", [("named", "Named")])],
            pre_named.visible_items,
        )


    def test_shadow_preassignment_preserves_each_slot_name(self) -> None:
        text = validate.VisibleTextParser()
        text.feed(
            '<div><span slot="source">MULTI-SOURCE</span>'
            '<span slot="claim">MULTI-CLAIM</span>'
            '<template shadowrootmode="open">'
            '<slot name="source"></slot><slot name="claim"></slot>'
            '</template></div>'
        )
        text.close()
        self.assertIn("MULTI-SOURCE", text.text())
        self.assertIn("MULTI-CLAIM", text.text())

        links = validate.VisibleListLinkParser()
        links.feed(
            '<div><ul slot="source"><li>SRC-S '
            '<a href="source">Source</a></li></ul>'
            '<ul slot="claim"><li>SRC-C '
            '<a href="claim">Claim</a></li></ul>'
            '<template shadowrootmode="open">'
            '<slot name="source"></slot><slot name="claim"></slot>'
            '</template></div>'
        )
        links.close()
        self.assertEqual(
            [
                ("SRC-S Source", [("source", "Source")]),
                ("SRC-C Claim", [("claim", "Claim")]),
            ],
            links.visible_items,
        )

    def test_duplicate_named_shadow_slots_assign_only_the_first_slot(self) -> None:
        text = validate.VisibleTextParser()
        text.feed(
            '<div><span slot="evidence">DUP-ASSIGNED</span>'
            '<template shadowrootmode="open">'
            '<div hidden><slot name="evidence"></slot></div>'
            '<slot name="evidence"><span>DUP-FALLBACK</span></slot>'
            '</template></div>'
        )
        text.close()
        self.assertNotIn("DUP-ASSIGNED", text.text())
        self.assertIn("DUP-FALLBACK", text.text())

        links = validate.VisibleListLinkParser()
        links.feed(
            '<div><ul slot="evidence"><li>SRC-A '
            '<a href="assigned">Assigned</a></li></ul>'
            '<template shadowrootmode="open">'
            '<div hidden><slot name="evidence"></slot></div>'
            '<slot name="evidence"><ul><li>SRC-F '
            '<a href="fallback">Fallback</a></li></ul></slot>'
            '</template></div>'
        )
        links.close()
        self.assertEqual(
            [("SRC-F Fallback", [("fallback", "Fallback")])],
            links.visible_items,
        )

    def test_post_template_assigned_text_is_composed_at_slot_position(self) -> None:
        parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
        parser.feed(
            '<div><template shadowrootmode="open">'
            '<slot></slot><h2>Gesicherter Ereigniskern</h2>'
            '</template><p>CLM-LIGHT-BEFORE-HEADING</p></div>'
        )
        parser.close()
        self.assertEqual("", parser.text())

    def test_template_end_finalizes_implicitly_closed_shadow_slot(self) -> None:
        text = validate.VisibleTextParser()
        text.feed(
            '<div><template shadowrootmode="open"><slot>'
            '<span>IMPLICIT-FALLBACK</span></template>'
            '<span>IMPLICIT-ASSIGNED</span></div>'
        )
        text.close()
        self.assertIn("IMPLICIT-ASSIGNED", text.text())
        self.assertNotIn("IMPLICIT-FALLBACK", text.text())

        links = validate.VisibleListLinkParser()
        links.feed(
            '<div><template shadowrootmode="open"><slot>'
            '<ul><li>SRC-F <a href="fallback">Fallback</a></li></ul>'
            '</template><ul><li>SRC-A '
            '<a href="assigned">Assigned</a></li></ul></div>'
        )
        links.close()
        self.assertEqual(
            [("SRC-A Assigned", [("assigned", "Assigned")])],
            links.visible_items,
        )


    def test_implicit_close_preserves_preassigned_light_child(self) -> None:
        parser = validate.VisibleTextParser()
        parser.feed(
            '<div><p slot="evidence">PRECLOSE-ASSIGNED'
            '<div>PRECLOSE-UNSLOTTED-BRIDGE</div>'
            '<template shadowrootmode="open">'
            '<slot name="evidence"></slot></template></div>'
        )
        parser.close()
        self.assertIn("PRECLOSE-ASSIGNED", parser.text())
        self.assertNotIn("PRECLOSE-UNSLOTTED-BRIDGE", parser.text())

    def test_section_parser_uses_composed_slot_position_for_later_light_child(self) -> None:
        parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
        parser.feed(
            '<div><template shadowrootmode="open">'
            '<h2>Gesicherter Ereigniskern</h2>'
            '<slot></slot><h2>Andere Sektion</h2>'
            '</template><p>SECTION-SLOTTED-CLAIM</p></div>'
        )
        parser.close()
        self.assertEqual("SECTION-SLOTTED-CLAIM", parser.text())


    def test_section_parser_uses_composed_slot_position_for_preassigned_light_child(self) -> None:
        parser = validate.VisibleSectionTextParser("Gesicherter Ereigniskern")
        parser.feed(
            '<div><span slot="evidence">PRE-SECTION-SLOTTED</span>'
            '<template shadowrootmode="open">'
            '<h2>Gesicherter Ereigniskern</h2>'
            '<slot name="evidence"></slot>'
            '</template></div>'
        )
        parser.close()
        self.assertEqual("PRE-SECTION-SLOTTED", parser.text())


    def test_inline_style_attribute_disqualifies_static_visibility_evidence(self) -> None:
        rendered = validate.render_site_markdown(
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X wording</p>'
            '<div style="position:fixed;inset:0;background:white;'
            'z-index:2147483647"></div>'
        )
        self.assertTrue(validate.has_author_visibility_mutator(rendered))

        links = validate.VisibleListLinkParser(
            validate.has_author_visibility_mutator(rendered)
        )
        links.feed(rendered)
        links.close()
        text = validate.VisibleTextParser(
            validate.has_author_visibility_mutator(rendered)
        )
        text.feed(rendered)
        text.close()

        self.assertEqual([], links.visible_items)
        self.assertEqual("", text.text())

    def test_meta_refresh_disqualifies_static_visibility_evidence(self) -> None:
        rendered = validate.render_site_markdown(
            '<h2>META-SOURCE</h2>'
            '<ul><li>SRC-R <a href="u">R</a></li></ul>'
            '<meta http-equiv=" ReFrEsH " content="0;url=/elsewhere">'
        )
        self.assertTrue(validate.has_author_executable_content(rendered))
        self.assertTrue(validate.has_author_visibility_mutator(rendered))

        links = validate.VisibleListLinkParser(
            validate.has_author_visibility_mutator(rendered)
        )
        links.feed(rendered)
        links.close()
        text = validate.VisibleTextParser(
            validate.has_author_visibility_mutator(rendered)
        )
        text.feed(rendered)
        text.close()

        self.assertEqual([], links.visible_items)
        self.assertEqual("", text.text())


    def test_author_scanner_ignores_nested_html_node_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><html><template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )
        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_styled_div_inside_select_is_not_assumed_ignored_by_current_parser(self) -> None:
        markup = (
            '<select><div style="display:none"></select>'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
        )
        self.assertTrue(validate.has_author_stylesheet(markup))


    def test_self_closed_html_host_keeps_declarative_shadow_mutators_active(self) -> None:
        markup = (
            '<div/><template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )
        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_aria_hidden_content_remains_visual_evidence(self) -> None:
        markup = (
            '<ul><li aria-hidden="true">SRC-A <a href="u">A</a></li></ul>'
            '<p aria-hidden="true">CLM-X wording</p>'
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual(
            [("SRC-A A", [("u", "A")])],
            links.visible_items,
        )
        self.assertIn("CLM-X wording", text.text())

    def test_author_scanner_applies_implied_li_end_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><li>one<li>two</li>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><ul><li>SRC-A <a href="u">A</a></li></ul></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_zero_width_marquee_does_not_count_as_visual_evidence(self) -> None:
        markup = (
            '<marquee width="0">'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X wording</p>'
            '</marquee>'
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([], links.visible_items)
        self.assertNotIn("CLM-X wording", text.text())


    def test_author_scanner_ignores_nested_form_start_before_shadow_host_selection(self) -> None:
        markup = (
            '<form><div><form>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div></form>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_closes_nested_anchor_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><a><a></a>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))


    def test_author_scanner_inspects_in_table_form_before_stack_drop(self) -> None:
        markup = (
            '<table><form style="position:fixed;left:0;top:0;'
            'width:100vw;height:100vh;background:white"></form></table>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_pops_anchor_formatting_descendants_on_explicit_end(self) -> None:
        markup = (
            '<div><a><b></a>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_ignores_in_body_frameset_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><frameset>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))


    def test_author_scanner_preserves_special_block_during_nested_anchor_recovery(self) -> None:
        markup = (
            '<b><a><div><a></a>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div></b>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_generates_implied_end_tags_before_form_removal(self) -> None:
        markup = (
            '<div><form><li></form>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_marquee_legacy_zero_dimensions_match_browser_visibility(self) -> None:
        hidden_widths = ("00", "000", "0px", "0PX", "0%", "00%", "0foo", "0.0", " 0 ")
        visible_widths = ("0.5", "+0", "-0", "01", "1", "1px", "1%")

        for width in hidden_widths:
            with self.subTest(width=width, expected="hidden"):
                links = validate.VisibleListLinkParser()
                links.feed(
                    f'<marquee width="{width}"><ul><li>SRC-A '
                    '<a href="u">A</a></li></ul></marquee>'
                )
                links.close()
                self.assertEqual([], links.visible_items)

        for width in visible_widths:
            with self.subTest(width=width, expected="visible"):
                links = validate.VisibleListLinkParser()
                links.feed(
                    f'<marquee width="{width}"><ul><li>SRC-A '
                    '<a href="u">A</a></li></ul></marquee>'
                )
                links.close()
                self.assertEqual([("SRC-A A", [("u", "A")])], links.visible_items)


    def test_author_scanner_recovers_nested_nobr_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><nobr><nobr></nobr>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))


    def test_author_scanner_exits_select_for_input_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><select><input>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_zero_height_marquee_does_not_count_as_visual_evidence(self) -> None:
        markup = (
            '<marquee height="0">'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X wording</p>'
            '</marquee>'
        )
        links = validate.VisibleListLinkParser()
        links.feed(markup)
        links.close()
        text = validate.VisibleTextParser()
        text.feed(markup)
        text.close()

        self.assertEqual([], links.visible_items)
        self.assertNotIn("CLM-X wording", text.text())

    def test_author_scanner_ignores_in_body_head_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><head>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template></head><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_executable_scanner_matches_real_event_handler_attributes(self) -> None:
        self.assertFalse(
            validate.has_author_executable_content('<div once="historical"></div>')
        )
        self.assertFalse(
            validate.has_author_executable_content('<div online="historical"></div>')
        )
        self.assertTrue(
            validate.has_author_executable_content('<div onclick="x()"></div>')
        )
        self.assertTrue(
            validate.has_author_executable_content('<img onerror="x()">')
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<input autofocus onfocusin="x()">'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<input onfocusout="x()">'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content('<div ononline="x()"></div>')
        )
        self.assertTrue(
            validate.has_author_executable_content('<body ononline="x()"></body>')
        )
        self.assertTrue(
            validate.has_author_executable_content('<body onpageshow="x()"></body>')
        )
        for name in ("onpagereveal", "onpageswap"):
            for element in ("body", "div"):
                with self.subTest(name=name, element=element):
                    self.assertFalse(
                        validate.has_author_executable_content(
                            f'<{element} {name}="document.body.hidden=true"></{element}>'
                        )
                    )
        self.assertTrue(
            validate.has_author_executable_content('<video onencrypted="x()"></video>')
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<svg><animate onbegin="x()"></animate></svg>'
            )
        )


    def test_author_scanner_recovers_nested_select_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><select><select></select>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_marquee_legacy_event_names_are_not_executable_handlers(self) -> None:
        for name in ("onstart", "onfinish", "onbounce"):
            with self.subTest(name=name):
                self.assertFalse(
                    validate.has_author_executable_content(
                        f'<marquee {name}="document.body.hidden=true">X</marquee>'
                    )
                )


    def test_author_scanner_normalizes_image_alias_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><image>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_recovers_nested_table_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><table><table></table>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_javascript_url_detection_is_scoped_to_actionable_attributes(self) -> None:
        self.assertFalse(
            validate.has_author_executable_content(
                '<div href="javascript:window.x=1"></div>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<span src="javascript:window.x=1"></span>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<a href="javascript:window.x=1">go</a>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<iframe src="javascript:parent.window.x=1"></iframe>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<form action="javascript:window.x=1"></form>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<form><button formaction="javascript:window.x=1">go</button></form>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<svg><a href="javascript:window.x=1"><text>x</text></a></svg>'
            )
        )
        self.assertTrue(
            validate.has_author_executable_content(
                '<svg><a xlink:href="javascript:window.x=1"><text>x</text></a></svg>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<svg><rect href="javascript:window.x=1"></rect></svg>'
            )
        )


    def test_executable_url_detection_uses_first_duplicate_attribute(self) -> None:
        safe_first = (
            '<a href="https://example.test" href="javascript:window.x=1">A</a>',
            '<iframe src="https://example.test" src="javascript:parent.window.x=1"></iframe>',
            '<form action="https://example.test" action="javascript:window.x=1"></form>',
            '<button formaction="https://example.test" formaction="javascript:window.x=1">B</button>',
            '<svg><a href="https://example.test" href="javascript:window.x=1"><text>x</text></a></svg>',
        )
        executable_first = (
            '<a href="javascript:window.x=1" href="https://example.test">A</a>',
            '<iframe src="javascript:parent.window.x=1" src="https://example.test"></iframe>',
            '<form action="javascript:window.x=1" action="https://example.test"></form>',
            '<button formaction="javascript:window.x=1" formaction="https://example.test">B</button>',
            '<svg><a href="javascript:window.x=1" href="https://example.test"><text>x</text></a></svg>',
        )

        for markup in safe_first:
            with self.subTest(markup=markup, expected="safe-first"):
                self.assertFalse(validate.has_author_executable_content(markup))
        for markup in executable_first:
            with self.subTest(markup=markup, expected="executable-first"):
                self.assertTrue(validate.has_author_executable_content(markup))



    def test_author_scanner_respects_end_tag_scope_before_shadow_host_selection(self) -> None:
        markup = (
            '<div><table></div></table>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>HIDDEN-SLOTTED</span></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))


    def test_author_scanner_ignores_head_start_inside_shadow_template(self) -> None:
        markup = (
            '<div><template shadowrootmode="open">'
            '<span><head><template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template></head><em>HIDDEN-SLOTTED</em></span>'
            '</template></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_srcdoc_detection_is_scoped_to_html_iframes(self) -> None:
        self.assertTrue(
            validate.has_author_executable_content(
                '<iframe srcdoc="<p>active</p>"></iframe>'
            )
        )
        self.assertFalse(
            validate.has_author_executable_content(
                '<svg><iframe srcdoc="<p>foreign</p>"></iframe></svg>'
            )
        )

    def test_bdo_content_is_ineligible_visibility_evidence(self) -> None:
        links = validate.VisibleListLinkParser()
        links.feed(
            '<ul>'
            '<li><bdo dir="rtl">SRC-A <a href="a">Reversed</a></bdo></li>'
            '<li>SRC-B <a href="b">Visible</a></li>'
            '</ul>'
        )
        links.close()
        self.assertFalse(
            any("SRC-A" in text for text, _links in links.visible_items)
        )
        self.assertFalse(
            any(
                href == "a"
                for _text, item_links in links.visible_items
                for href, _label in item_links
            )
        )
        self.assertIn(
            ("SRC-B Visible", [("b", "Visible")]),
            links.visible_items,
        )

        text_parser = validate.VisibleTextParser()
        text_parser.feed(
            '<p><bdo dir="rtl">CLM-X canonical wording</bdo></p>'
            '<p>VISIBLE-TEXT</p>'
        )
        text_parser.close()
        self.assertNotIn("CLM-X", text_parser.text())
        self.assertNotIn("canonical wording", text_parser.text())
        self.assertIn("VISIBLE-TEXT", text_parser.text())


    def test_formaction_javascript_requires_submit_control(self) -> None:
        non_submit = (
            '<input formaction="javascript:window.x=1">',
            '<input type="text" formaction="javascript:window.x=1">',
            '<input type="button" formaction="javascript:window.x=1">',
            '<input type="reset" formaction="javascript:window.x=1">',
            '<button type="button" formaction="javascript:window.x=1">B</button>',
            '<button type="reset" formaction="javascript:window.x=1">R</button>',
        )
        submit = (
            '<input type="submit" formaction="javascript:window.x=1">',
            '<input type="image" formaction="javascript:window.x=1">',
            '<button formaction="javascript:window.x=1">D</button>',
            '<button type="submit" formaction="javascript:window.x=1">S</button>',
            '<button type="not-a-real-type" formaction="javascript:window.x=1">I</button>',
        )

        for markup in non_submit:
            with self.subTest(markup=markup, expected="non-submit"):
                self.assertFalse(validate.has_author_executable_content(markup))
        for markup in submit:
            with self.subTest(markup=markup, expected="submit"):
                self.assertTrue(validate.has_author_executable_content(markup))

    def test_foreign_executable_scanner_rejects_fake_on_prefixes(self) -> None:
        for markup in (
            '<svg once="historical"></svg>',
            '<svg><rect once="historical"></rect></svg>',
            '<math once="historical"></math>',
            '<math><mrow once="historical"></mrow></math>',
            '<svg ononline="x()"></svg>',
            '<math ononline="x()"></math>',
        ):
            with self.subTest(markup=markup):
                self.assertFalse(validate.has_author_executable_content(markup))

        for markup in (
            '<svg onclick="x()"></svg>',
            '<svg><rect onclick="x()"></rect></svg>',
            '<math onclick="x()"></math>',
            '<math><mrow onclick="x()"></mrow></math>',
            '<svg><animate onbegin="x()"></animate></svg>',
        ):
            with self.subTest(markup=markup):
                self.assertTrue(validate.has_author_executable_content(markup))


    def test_option_family_start_recovers_before_shadow_host_selection(self) -> None:
        option_markup = (
            '<div><option>one<option>two</option>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template>'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X wording</p></div>'
        )
        self.assertTrue(validate.has_author_stylesheet(option_markup))
        self.assertTrue(validate.has_author_visibility_mutator(option_markup))

        option_visibility = (
            '<div><option>one<option>two</option>'
            '<template shadowrootmode="open">'
            '<ul><li>SRC-S <a href="s">Shadow</a></li></ul>'
            '<p>SHADOW-TEXT</p></template>'
            '<ul><li>SRC-L <a href="l">Light</a></li></ul>'
            '<p>LIGHT-TEXT</p></div>'
        )
        links = validate.VisibleListLinkParser()
        links.feed(option_visibility)
        links.close()
        text_parser = validate.VisibleTextParser()
        text_parser.feed(option_visibility)
        text_parser.close()
        self.assertEqual(
            [("SRC-S Shadow", [("s", "Shadow")])],
            links.visible_items,
        )
        self.assertIn("SHADOW-TEXT", text_parser.text())
        self.assertNotIn("LIGHT-TEXT", text_parser.text())

        outside_optgroup = (
            '<div><optgroup><option>one'
            '<optgroup><option>two</option></optgroup>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template><span>LIGHT</span></div>'
        )
        self.assertFalse(validate.has_author_stylesheet(outside_optgroup))
        self.assertFalse(validate.has_author_visibility_mutator(outside_optgroup))

        outside_stack = [
            validate.parser_element_record("div", "html", []),
            validate.parser_element_record("optgroup", "html", []),
            validate.parser_element_record("option", "html", []),
        ]
        inside_stack = [
            validate.parser_element_record("select", "html", []),
            validate.parser_element_record("optgroup", "html", []),
            validate.parser_element_record("option", "html", []),
        ]
        self.assertEqual(
            2,
            validate.html_option_family_start_pop_index(
                outside_stack, "optgroup"
            ),
        )
        self.assertEqual(
            1,
            validate.html_option_family_start_pop_index(
                inside_stack, "optgroup"
            ),
        )


    def test_material_page_wrapper_hosts_top_level_declarative_shadow_root(self) -> None:
        markup = (
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template>'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X canonical wording</p>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_active_declarative_shadow_root_without_styles_is_visibility_mutator(self) -> None:
        markup = (
            '<template shadowrootmode="open"><p>SHADOW-ONLY</p></template>'
            '<p>LIGHT-ONLY</p>'
        )

        self.assertTrue(validate.has_author_declarative_shadow_root(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))
        self.assertEqual("", validate.visible_markdown_text(markup))
        self.assertFalse(
            validate.has_author_declarative_shadow_root(
                '<template><p>INERT</p></template>'
            )
        )
        self.assertFalse(
            validate.has_author_declarative_shadow_root(
                '<template shadowrootmode="bogus"><p>INERT</p></template>'
            )
        )

    def test_obsolete_void_tokens_do_not_shadow_declarative_host(self) -> None:
        for tag in ("basefont", "bgsound", "keygen"):
            markup = (
                f"<div><{tag}>"
                '<template shadowrootmode="open">'
                '<style>:host{display:none}</style><slot></slot>'
                "</template>"
                '<ul><li>SRC-A <a href="u">A</a></li></ul>'
                '<p>CLM-X canonical wording</p></div>'
            )
            with self.subTest(tag=tag):
                self.assertTrue(validate.has_author_declarative_shadow_root(markup))
                self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_material_wrapper_escape_declarative_shadow_root_fails_closed(self) -> None:
        markup = (
            '</article><template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template>'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X canonical wording</p>'
        )

        self.assertTrue(validate.has_author_declarative_shadow_root(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_author_scanner_exits_table_select_before_nested_table_recovery(self) -> None:
        markup = (
            '<div><table><select><table></table>'
            '<template shadowrootmode="open">'
            '<style>:host{display:none}</style><slot></slot>'
            '</template>'
            '<ul><li>SRC-A <a href="u">A</a></li></ul>'
            '<p>CLM-X canonical wording</p></div>'
        )

        self.assertTrue(validate.has_author_stylesheet(markup))
        self.assertTrue(validate.has_author_visibility_mutator(markup))

    def test_unicode_bidi_controls_are_ineligible_visibility_evidence(self) -> None:
        controls = (
            (chr(0x202E), chr(0x202C)),
            (chr(0x202D), chr(0x202C)),
            (chr(0x2067), chr(0x2069)),
            (chr(0x2066), chr(0x2069)),
            (chr(0x2068), chr(0x2069)),
        )
        for opener, closer in controls:
            markup = (
                f'<p>{opener}CLM-X canonical wording{closer}</p>'
                '<p>VISIBLE-TEXT</p>'
            )
            with self.subTest(opener=hex(ord(opener))):
                self.assertTrue(validate.has_author_visibility_mutator(markup))
                parser = validate.VisibleTextParser(
                    validate.has_author_visibility_mutator(markup)
                )
                parser.feed(markup)
                parser.close()
                self.assertNotIn("CLM-X", parser.text())
                self.assertNotIn("canonical wording", parser.text())


    def test_mermaid_fence_comments_are_not_visible_evidence(self) -> None:
        fence = chr(96) * 3
        body = (
            f"{fence}mermaid\n"
            "flowchart LR\n"
            "%% CLM-X canonical wording\n"
            "A --> B\n"
            f"{fence}"
        )

        rendered = validate.render_site_markdown(body)
        self.assertIn('class="mermaid"', rendered)
        self.assertEqual("", validate.visible_markdown_text(body))
        self.assertNotIn(
            "CLM-X",
            validate.visible_markdown_claim_binding_text(body),
        )


if __name__ == "__main__":
    unittest.main()
