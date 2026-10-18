"""Integration and adversarial checks for Git-revision-bound MkDocs pages."""
from __future__ import annotations

import posixpath
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from mkdocs.config import load_config
from mkdocs.structure.files import Files, InclusionLevel

from scripts import mkdocs_research_hook as hook

ROOT = Path(__file__).resolve().parents[1]


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def committed_study_names(repo: Path = ROOT) -> set[str]:
    """An independent Git-tree oracle, not the hook's selection function."""
    entries = git(repo, "ls-tree", "-r", "-z", "HEAD", "--", "research")
    names = set()
    for entry in entries.split(b"\0"):
        if not entry:
            continue
        metadata, filename = entry.split(b"\t", 1)
        mode, object_type, _oid = metadata.split()
        path = filename.decode("utf-8")
        if (
            path.startswith("research/")
            and path.count("/") == 1
            and path.endswith(".md")
            and mode in (b"100644", b"100755")
            and object_type == b"blob"
        ):
            names.add(path.removeprefix("research/"))
    return names


class ResearchPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(config_file=str(ROOT / "mkdocs.yml"))
        # File.generated() expects the active MkDocs plugin event context.
        cls.config.plugins._current_plugin = "hooks"

    def generated(self):
        return hook.on_files(Files([]), self.config)

    def test_every_committed_study_is_published_exactly_once(self):
        expected = committed_study_names()
        self.assertGreater(len(expected), 0)
        files = self.generated()
        uris = [file.src_uri for file in files]
        self.assertEqual(len(uris), len(set(uris)))
        self.assertEqual(
            set(uris),
            {"research/index.md", *(f"research/{name}" for name in expected)},
        )
        revision = git(ROOT, "rev-parse", "HEAD").decode().strip()
        for name in expected:
            file = next(item for item in files if item.src_uri == f"research/{name}")
            # Confirm independently that the site reads Git's blob bytes, not
            # a path which could contain staged or uncommitted changes.
            self.assertEqual(file.content_string, git(ROOT, "show", f"HEAD:research/{name}").decode())
            self.assertEqual(file.edit_uri, f"blob/{revision}/research/{name}")
            self.assertEqual(file.inclusion, InclusionLevel.NOT_IN_NAV)
        self.assertFalse((ROOT / "docs" / "research").exists())

    def test_dynamic_index_contains_every_committed_original(self):
        index = next(
            file for file in self.generated() if file.src_uri == "research/index.md"
        ).content_string
        expected = committed_study_names()
        self.assertIn(f"**{len(expected)} versionierte Studien**", index)
        revision = git(ROOT, "rev-parse", "HEAD").decode().strip()
        self.assertIn(f"**Git-Revision:** `{revision}`", index)
        for name in expected:
            self.assertIn(f"]({name})", index)
            self.assertIn(hook.GITHUB_ROOT + f"blob/{revision}/research/{name}", index)

    def test_untracked_staged_dirty_nested_and_symlink_studies_are_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            research = repo / "research"
            research.mkdir()
            (research / "tracked.md").write_text("# Committed title\n\nCommitted body\n")
            nested = research / "nested"
            nested.mkdir()
            (nested / "not-top-level.md").write_text("# Nested\n")
            (research / "symlink.md").symlink_to("tracked.md")
            git(repo, "init", "-q")
            git(repo, "add", "research")
            git(
                repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "Committed research",
            )
            # These inputs are deliberately *not* part of HEAD:
            (research / "draft.md").write_text("# Untracked draft\n")
            (research / "staged.md").write_text("# Staged draft\n")
            git(repo, "add", "research/staged.md")
            (research / "tracked.md").write_text("# Dirty title\n\nLocally modified body\n")

            self.assertEqual(committed_study_names(repo), {"tracked.md"})
            with patch.object(hook, "ROOT", repo):
                files = self.generated()
            self.assertEqual(
                {file.src_uri for file in files},
                {"research/index.md", "research/tracked.md"},
            )
            study = next(file for file in files if file.src_uri == "research/tracked.md")
            index = next(file for file in files if file.src_uri == "research/index.md")
            self.assertEqual(study.content_string, "# Committed title\n\nCommitted body\n")
            self.assertEqual(study.inclusion, InclusionLevel.NOT_IN_NAV)
            self.assertEqual(study.edit_uri, f"blob/{git(repo, 'rev-parse', 'HEAD').decode().strip()}/research/tracked.md")
            self.assertIn("**1 versionierte Studien**", index.content_string)
            self.assertIn("Committed title", index.content_string)
            for excluded in ("draft", "staged", "symlink", "not-top-level", "Dirty"):
                self.assertNotIn(excluded, index.content_string)
            self.assertNotIn("Locally modified body", study.content_string)

    def test_no_git_revision_fails_closed_instead_of_publishing_local_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "research").mkdir()
            (repo / "research" / "draft.md").write_text("# Private draft\n")
            with patch.object(hook, "ROOT", repo):
                with self.assertRaises(RuntimeError):
                    self.generated()

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
                self.assertIn(hook.GITHUB_ROOT + file.edit_uri, content)

            for url in re.findall(r"\]\(([^)]+)\)", content):
                url = url.split("#", 1)[0].split("?", 1)[0]
                if not url.endswith(".md") or "://" in url:
                    continue
                target = posixpath.normpath(posixpath.join("research", url))
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