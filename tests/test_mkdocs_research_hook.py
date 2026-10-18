"""Integration checks for virtual MkDocs research-page publication."""
from __future__ import annotations

import posixpath
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

from mkdocs.config import load_config
from mkdocs.structure.files import Files

from scripts import mkdocs_research_hook as hook

ROOT = Path(__file__).resolve().parents[1]


class ResearchPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(config_file=str(ROOT / "mkdocs.yml"))
        # File.generated() expects the active MkDocs plugin event context.
        cls.config.plugins._current_plugin = "hooks"

    def generated(self):
        return hook.on_files(Files([]), self.config)

    def test_every_canonical_study_is_published_exactly_once(self):
        sources = hook.research_sources()
        files = self.generated()
        uris = [file.src_uri for file in files]
        self.assertEqual(len(uris), len(set(uris)))
        self.assertEqual(
            set(uris),
            {"research/index.md", *(f"research/{source.name}" for source in sources)},
        )
        for source in sources:
            file = next(item for item in files if item.src_uri == f"research/{source.name}")
            self.assertEqual(Path(file.abs_src_path), source)
            self.assertEqual(file.edit_uri, f"research/{source.name}")
        self.assertFalse((ROOT / "docs" / "research").exists())

    def test_dynamic_index_contains_every_original_and_no_untracked_studies(self):
        index = next(
            file for file in self.generated() if file.src_uri == "research/index.md"
        ).content_string
        sources = hook.research_sources()
        self.assertIn(f"**{len(sources)} versionierte Studien**", index)
        for source in sources:
            self.assertIn(f"]({source.name})", index)
            self.assertIn(hook.GITHUB_RESEARCH + source.name, index)

    def test_every_relative_markdown_link_resolves_in_site(self):
        files = self.generated()
        uris = {file.src_uri for file in files}
        for file in files:
            if file.src_uri == "research/index.md":
                content = file.content_string
            else:
                content = hook.on_page_markdown(
                    file.content_string, SimpleNamespace(file=file)
                )
                self.assertIn(hook.GITHUB_RESEARCH + Path(file.src_uri).name, content)

            for url in re.findall(r"\]\(([^)]+)\)", content):
                url = url.split("#", 1)[0].split("?", 1)[0]
                if not url.endswith(".md") or "://" in url:
                    continue
                target = posixpath.normpath(
                    posixpath.join("research", url)
                )
                self.assertTrue(
                    target in uris or (ROOT / "docs" / target).is_file(),
                    f"Unresolvable link in {file.src_uri}: {url} => {target}",
                )

    def test_non_research_pages_are_unchanged(self):
        unchanged = hook.on_page_markdown(
            "# Source index", SimpleNamespace(file=SimpleNamespace(src_uri="quellen/index.md"))
        )
        self.assertIsNone(unchanged)


if __name__ == "__main__":
    unittest.main()
