"""Publish exactly the committed top-level research studies as virtual MkDocs pages.

The Git HEAD tree and blob contents, not the index or working tree, define the
published revision. Drafts, staged changes and dirty worktree edits are excluded.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from urllib.parse import quote

from mkdocs.structure.files import File, Files

ROOT = Path(__file__).resolve().parents[1]
GITHUB_RESEARCH = (
    "https://github.com/alexdermohr/machtverflechtungen/blob/main/research/"
)


@dataclass(frozen=True)
class ResearchSource:
    name: str
    content: str


def _git_output(*args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Cannot read the committed research revision: {detail}")
    return result.stdout


def research_sources() -> list[ResearchSource]:
    """Read regular root-level Markdown blobs from one immutable HEAD commit."""
    revision = _git_output("rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    entries = _git_output("ls-tree", "-z", f"{revision}:research")
    sources = []
    for entry in entries.split(b"\0"):
        if not entry:
            continue
        metadata, separator, name_bytes = entry.partition(b"\t")
        if not separator:
            raise ValueError("Malformed research Git tree entry")
        mode, object_type, object_id = metadata.split()
        name = name_bytes.decode("utf-8")
        if not name.endswith(".md"):
            continue
        # A Git tree lists immediate children only. Ignore symbolic links,
        # submodules and non-regular objects, never traverse filesystem paths.
        if mode not in (b"100644", b"100755") or object_type != b"blob":
            continue
        if (
            name.startswith(".")
            or any(character in name for character in "/\\\r\n\t()[]")
            or any(ord(character) < 32 or ord(character) == 127 for character in name)
        ):
            raise ValueError(f"Unsafe committed research filename: {name!r}")
        markdown = _git_output("cat-file", "blob", object_id.decode("ascii")).decode(
            "utf-8"
        )
        sources.append(ResearchSource(name=name, content=markdown))
    return sorted(sources, key=lambda item: item.name)


def study_title(source: ResearchSource) -> str:
    for line in source.content.splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("[", r"\[").replace("]", r"\]")
    raise ValueError(f"Research study is missing a title: {source.name}")


def on_files(files: Files, config, **kwargs) -> Files:
    """Register the committed studies and their dynamically generated index."""
    sources = research_sources()
    if not sources:
        raise ValueError("No versioned research studies found")

    known = {file.src_uri for file in files}
    generated = {"research/index.md", *(f"research/{source.name}" for source in sources)}
    if known & generated:
        raise ValueError("Duplicate research page path in docs/")

    lines = [
        "# Forschungsstudien",
        "",
        f"**{len(sources)} versionierte Studien** aus dem Forschungsordner dieses Site-Builds.",
        "",
        "Jeder Volltext enthält datierte Originalquellen, Beweisgrenzen und offene "
        "Forschungsfragen. Nicht integrierte Pull Requests erscheinen hier nicht. "
        "Die GitHub-Originaldateien bleiben die maßgebliche Fassung.",
        "",
    ]
    for source in sources:
        src_uri = f"research/{source.name}"
        # Content comes from the Git object database; abs_src_path would instead
        # read uncommitted edits and defeat revision-bound publication.
        study = File.generated(config, src_uri, content=source.content)
        study.edit_uri = src_uri
        files.append(study)
        escaped_name = quote(source.name, safe="-._~")
        lines.append(
            f"- [{study_title(source)}]({escaped_name})"
            f" · [Originaldatei auf GitHub]({GITHUB_RESEARCH}{escaped_name})"
        )

    files.append(File.generated(config, "research/index.md", content="\n".join(lines) + "\n"))
    return files


def on_page_markdown(markdown: str, page, **kwargs) -> str | None:
    """Adapt repository-relative cross-links without editing canonical research."""
    uri = page.file.src_uri
    if not uri.startswith("research/") or uri == "research/index.md":
        return None

    # Research lives beside docs/ in Git; its virtual MkDocs location lives
    # inside docs/. Resolve references accordingly at render time only.
    rendered = markdown.replace("](../METHODOLOGY.md", "](../methodik.md")
    rendered = rendered.replace("](../docs/", "](../")
    return (
        rendered
        + "\n\n---\n\n"
        + f"[Originaldatei dieser Studie auf GitHub]({GITHUB_RESEARCH}{quote(Path(uri).name, safe='-._~')})\n"
    )
