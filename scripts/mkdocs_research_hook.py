"""Publish exactly the committed top-level research studies as virtual MkDocs pages.

The Git HEAD tree and blob contents, not the index or working tree, define the
published revision. Drafts, staged changes and dirty worktree edits are excluded.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from urllib.parse import quote

from mkdocs.structure.files import File, Files, InclusionLevel

ROOT = Path(__file__).resolve().parents[1]
GITHUB_ROOT = "https://github.com/alexdermohr/machtverflechtungen/"

# Curated *prefix* groups, not a second catalogue of research files: new studies
# automatically appear here or in "Weitere Studien". Individual source URLs stay stable.
STUDY_GROUPS = (
    ("Nachrichtendienste & verdeckte Operationen", "nachrichtendienste",
     ("cia-", "bnd-", "bdj-", "kgu-", "gehlen-", "organisation-gehlen-",
      "psb-", "suchasnist-", "weltforum-", "wirsing-", "searle-",
      "friedrich-wilhelm-", "aktion-blitz-", "ewk-bpa-")),
    ("Politische Gewalt & Ermittlungen", "gewalt-und-ermittlungen",
     ("strategie-der-spannung-", "piazza-fontana-", "peteano-",
      "raf-", "npd-", "nsu-", "bfv-", "corelli-", "piatto-",
      "brandenburg-", "berlin-lka-", "britische-neonazinetzwerke-",
      "ewk-kkk-", "aginter-")),
    ("Wirtschaft, Finanzen & öffentliche Mittel", "finanzen",
     ("bcci-", "p2-", "bologna-", "bpa-", "adk-", "erp-", "insm-", "warburg-",
      "biz-", "schroeder-",
      "verkehrsaufklaerung-")),
    ("Transatlantische & internationale Netzwerke", "internationale-netzwerke",
     ("acg-", "atlantik-bruecke-", "bilderberg-", "wef-", "msc-",
      "aspen-", "ecfr-", "dgap-", "lobbykontakte-",
      "anne-zetsche-")),
    ("Quellenkritik & historische Einordnung", "quellenkritik",
     ("rockefeller-", "monica-crowley-", "epstein-", "cromwell-",
      "okkultismus-", "wilhelm-classen-")),
)
OTHER_STUDIES = ("Weitere Studien", "weitere-studien")



@dataclass(frozen=True)
class ResearchSource:
    name: str
    content: str
    revision: str


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
            or quote(name, safe="-._~") != name
        ):
            raise ValueError(f"Unsafe committed research filename: {name!r}")
        markdown = _git_output("cat-file", "blob", object_id.decode("ascii")).decode(
            "utf-8"
        )
        sources.append(ResearchSource(name=name, content=markdown, revision=revision))
    return sorted(sources, key=lambda item: item.name)


def study_title(source: ResearchSource) -> str:
    for line in source.content.splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("[", r"\[").replace("]", r"\]")
    raise ValueError(f"Research study is missing a title: {source.name}")


def study_group(name: str) -> str:
    """Return a durable topic anchor, with a discoverable fallback for new files."""
    for _label, anchor, prefixes in STUDY_GROUPS:
        if name.startswith(prefixes):
            return anchor
    return OTHER_STUDIES[1]


def on_files(files: Files, config, **kwargs) -> Files:
    """Register the committed studies and their dynamically generated index."""
    sources = research_sources()
    if not sources:
        raise ValueError("No versioned research studies found")
    if any(source.name == "index.md" for source in sources):
        raise ValueError("Committed research/index.md conflicts with generated index")

    known = {file.src_uri for file in files}
    generated = {"research/index.md", *(f"research/{source.name}" for source in sources)}
    if known & generated:
        raise ValueError("Duplicate research page path in docs/")

    lines = [
        "# Forschungsstudien",
        "",
        f"**{len(sources)} versionierte Studien** aus dem Forschungsordner dieses Site-Builds.",
        "",
        "Die Studien sind nach Themen erschlossen; innerhalb eines Themas alphabetisch "
        "nach Titel sortiert. Der vollständige Volltext und die Originaldatei "
        "sind direkt verlinkt. Nicht integrierte Pull Requests erscheinen nicht.",
        "",
        "## Themenübersicht",
        "",
    ]
    by_group: dict[str, list[ResearchSource]] = {}
    for source in sources:
        by_group.setdefault(study_group(source.name), []).append(source)
    groups = [
        (label, anchor)
        for label, anchor, _prefixes in STUDY_GROUPS
        if by_group.get(anchor)
    ]
    if by_group.get(OTHER_STUDIES[1]):
        groups.append(OTHER_STUDIES)
    for label, anchor in groups:
        lines.append(f"- [{label}](#{anchor}) ({len(by_group[anchor])})")
    lines += ["", f"**Git-Revision:** `{sources[0].revision}`", ""]
    for source in sources:
        src_uri = f"research/{source.name}"
        # Content comes from the Git object database; abs_src_path would instead
        # read uncommitted edits and defeat revision-bound publication.
        study = File.generated(config, src_uri, content=source.content)
        study.inclusion = InclusionLevel.NOT_IN_NAV
        escaped_name = quote(source.name, safe="-._~")
        # A pinned blob URL resolves to the exact Markdown used for this build.
        study.edit_uri = f"blob/{source.revision}/research/{escaped_name}"
        files.append(study)

    for label, anchor in groups:
        lines += [f"## {label} {{ #{anchor} }}", ""]
        for source in sorted(by_group[anchor], key=lambda item: study_title(item).casefold()):
            escaped_name = quote(source.name, safe="-._~")
            original_url = f"{GITHUB_ROOT}blob/{source.revision}/research/{escaped_name}"
            lines.append(
                f"- [{study_title(source)}]({escaped_name})"
                f" · [Originaldatei auf GitHub]({original_url})"
            )
        lines.append("")

    lines += [
        "## Weitere Recherchewege",
        "",
        "- [Fallakten nach Themen](../faelle/index.md) — zusammengefasste Befunde.",
        "- [Quellenkatalog](../quellen/index.md) — Originalakten und Fundstellen.",
        "- [Akteure und Beziehungen](../generated/entities.md) — Namen und Netzwerke.",
        "- [Methodik](../methodik.md) — Evidenzstufen und Gegenprüfung.",
        "",
    ]
    files.append(File.generated(config, "research/index.md", content="\n".join(lines) + "\n"))
    return files


def on_page_markdown(markdown: str, page, **kwargs) -> str | None:
    """Adapt repository-relative cross-links without editing canonical research."""
    uri = page.file.src_uri
    if not uri.startswith("research/") or uri == "research/index.md":
        return None

    # Research lives beside docs/ in Git; its virtual MkDocs location lives
    # inside docs/. Resolve references accordingly at render time only.
    original_path = page.file.edit_uri
    if not isinstance(original_path, str) or not original_path.startswith("blob/"):
        raise ValueError(f"Missing pinned research original for {uri}")
    rendered = markdown.replace("](../METHODOLOGY.md", "](../methodik.md")
    rendered = rendered.replace("](../docs/", "](../")
    return (
        rendered
        + "\n\n---\n\n"
        + "[Zur Studienübersicht](index.md) · [Fallakten](../faelle/index.md)"
        + " · [Methodik](../methodik.md)\n\n"
        + f"[Originaldatei dieser Studie auf GitHub]({GITHUB_ROOT}{original_path})\n"
    )