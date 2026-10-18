"""Publish tracked research studies in MkDocs without copying their source files.

Only the research/*.md files present in the checked-out revision are published.
"""
from __future__ import annotations

from pathlib import Path

from mkdocs.structure.files import File, Files

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
GITHUB_RESEARCH = (
    "https://github.com/alexdermohr/machtverflechtungen/blob/main/research/"
)


def research_sources() -> list[Path]:
    """Select only the canonical top-level Markdown studies of this revision."""
    return sorted(
        (path for path in RESEARCH.glob("*.md") if path.is_file() and not path.is_symlink()),
        key=lambda path: path.name,
    )


def study_title(source: Path) -> str:
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("[", r"\[").replace("]", r"\]")
    raise ValueError(f"Research study is missing a title: {source.name}")


def on_files(files: Files, config, **kwargs) -> Files:
    """Register main's studies and a generated portal index as virtual MkDocs pages."""
    sources = research_sources()
    if not sources:
        raise ValueError("No versioned research studies found")

    known = {file.src_uri for file in files}
    generated = {"research/index.md", *(f"research/{p.name}" for p in sources)}
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
        study = File.generated(config, src_uri, abs_src_path=str(source))
        study.edit_uri = src_uri
        files.append(study)
        lines.append(
            f"- [{study_title(source)}]({source.name})"
            f" · [Originaldatei auf GitHub]({GITHUB_RESEARCH}{source.name})"
        )

    files.append(
        File.generated(config, "research/index.md", content="\n".join(lines) + "\n")
    )
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
        + f"[Originaldatei dieser Studie auf GitHub]({GITHUB_RESEARCH}{Path(uri).name})\n"
    )
