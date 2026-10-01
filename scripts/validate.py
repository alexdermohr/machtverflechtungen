#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import markdown
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CASE_DIR = DOCS / "faelle"
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"

SITE_MARKDOWN_EXTENSIONS = [
    "admonition",
    "attr_list",
    "tables",
    "pymdownx.details",
    "pymdownx.superfences",
]


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    payload = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(payload, dict):
        raise ValueError("frontmatter must be a mapping")
    return payload


def schema_errors(instance: Any, schema_file: str, label: str) -> list[str]:
    validator = Draft202012Validator(load_json(SCHEMAS / schema_file))
    out: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        out.append(f"{label}: {location}: {error.message}")
    return out


def unique_ids(items: list[dict[str, Any]], label: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            errors.append(f"{label}: duplicate id {item_id}")
        seen.add(item_id)
    return seen


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def mapping_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def lexical_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", normalized))


def contains_lexical_sequence(haystack: str, needle: str) -> bool:
    if not needle:
        return False
    return f" {needle} " in f" {haystack} "


def period_bounds(value: Any) -> tuple[date, date] | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if re.fullmatch(r"\d{4}", text):
        year = int(text)
        if not 1 <= year <= 9999:
            return None
        return (date(year, 1, 1), date(year, 12, 31))
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", text)
    if not match:
        return None
    try:
        exact = date(*(int(part) for part in match.groups()))
    except ValueError:
        return None
    return (exact, exact)


def valid_https_url(value: Any) -> bool:
    if not isinstance(value, str) or not value or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.netloc or not hostname:
        return False
    try:
        ascii_host = hostname.rstrip(".").encode("idna").decode("ascii")
    except UnicodeError:
        return False
    if not ascii_host or len(ascii_host) > 253:
        return False
    labels = ascii_host.split(".")
    host_label = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
    return all(host_label.fullmatch(label) for label in labels)


def markdown_body(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return ""
    return "\n".join(lines[end + 1 :])


def has_visible_text(value: str) -> bool:
    return any(
        unicodedata.category(char)[0] in {"L", "N", "P", "S"}
        for char in value
    )


def render_site_markdown(value: str) -> str:
    return markdown.markdown(value, extensions=SITE_MARKDOWN_EXTENSIONS)


FOREIGN_ROOT_TAGS = frozenset({"math", "svg"})
SVG_HTML_INTEGRATION_TAGS = frozenset({"desc", "foreignobject", "title"})
MATHML_TEXT_INTEGRATION_TAGS = frozenset({"mi", "mn", "mo", "ms", "mtext"})
FOREIGN_HTML_BREAKOUT_START_TAGS = frozenset(
    {
        "b", "big", "blockquote", "body", "br", "center", "code", "dd",
        "div", "dl", "dt", "em", "embed", "h1", "h2", "h3", "h4", "h5",
        "h6", "head", "hr", "i", "img", "li", "listing", "menu", "meta",
        "nobr", "ol", "p", "pre", "ruby", "s", "small", "span", "strong",
        "strike", "sub", "sup", "table", "tt", "u", "ul", "var",
    }
)
FOREIGN_HTML_BREAKOUT_FONT_ATTRS = frozenset({"color", "face", "size"})
MATHML_INELIGIBLE_SUBTREE_TAGS = frozenset({"annotation", "annotation-xml", "mphantom"})
SVG_METADATA_TAGS = frozenset({"desc", "metadata", "title"})
SVG_NON_RENDERING_CONTAINER_TAGS = frozenset(
    {
        "clippath",
        "defs",
        "filter",
        "lineargradient",
        "marker",
        "mask",
        "pattern",
        "radialgradient",
        "symbol",
    }
)
SVG_INELIGIBLE_SUBTREE_TAGS = (
    SVG_METADATA_TAGS
    | SVG_NON_RENDERING_CONTAINER_TAGS
    | frozenset({"foreignobject", "switch", "textpath"})
)
PYMDOWN_DETAILS_CLASSES = frozenset(
    {
        "abstract", "attention", "bug", "caution", "check", "cite", "danger",
        "done", "error", "example", "fail", "failure", "faq", "help", "hint",
        "important", "info", "missing", "note", "question", "quote", "success",
        "summary", "tip", "tldr", "todo", "warning",
    }
)


class AuthorStylesheetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        if tag == "style":
            self.found = True
            return
        if tag != "link":
            return
        rel = next(
            (value for name, value in attrs if name.casefold() == "rel"),
            None,
        )
        if isinstance(rel, str) and "stylesheet" in {
            token.casefold() for token in rel.split()
        }:
            self.found = True

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)


def has_author_stylesheet(rendered: str) -> bool:
    parser = AuthorStylesheetParser()
    parser.feed(rendered)
    parser.close()
    return parser.found


def element_namespace(element: dict[str, Any]) -> str:
    namespace = element.get("namespace")
    return str(namespace) if namespace in {"html", "svg", "math"} else "html"


def is_foreign_html_integration_point(element: dict[str, Any]) -> bool:
    tag = element.get("tag")
    namespace = element_namespace(element)
    return (
        namespace == "svg" and tag in SVG_HTML_INTEGRATION_TAGS
    ) or (
        namespace == "math" and tag in MATHML_TEXT_INTEGRATION_TAGS
    )


def foreign_context(elements: list[dict[str, Any]]) -> str | None:
    for element in reversed(elements):
        if is_foreign_html_integration_point(element):
            return None
        namespace = element_namespace(element)
        if namespace in {"svg", "math"}:
            return namespace
    return None


def namespace_for_start_tag(
    elements: list[dict[str, Any]], tag: str
) -> str:
    current_foreign_context = foreign_context(elements)
    if current_foreign_context is not None:
        return current_foreign_context
    if tag == "svg":
        return "svg"
    if tag == "math":
        return "math"
    return "html"


def active_foreign_root_index(elements: list[dict[str, Any]]) -> int | None:
    for index in range(len(elements) - 1, -1, -1):
        element = elements[index]
        if is_foreign_html_integration_point(element):
            return None
        tag = element.get("tag")
        namespace = element_namespace(element)
        if tag in FOREIGN_ROOT_TAGS and namespace == tag:
            return index
    return None


def is_foreign_scope_boundary(element: dict[str, Any]) -> bool:
    tag = element.get("tag")
    namespace = element_namespace(element)
    if namespace == "svg":
        return tag in SVG_HTML_INTEGRATION_TAGS
    if namespace == "math":
        return (
            tag in MATHML_TEXT_INTEGRATION_TAGS
            or tag == "annotation-xml"
        )
    return False


def element_matches_boundary(
    element: dict[str, Any], boundaries: frozenset[str]
) -> bool:
    tag = element.get("tag")
    if tag not in boundaries:
        return False
    namespace = element_namespace(element)
    if namespace == "html":
        if tag == "title":
            return boundaries in (
                LI_IMPLICIT_SCOPE_BOUNDARIES,
                DESCRIPTION_IMPLICIT_SCOPE_BOUNDARIES,
            )
        return tag not in FOREIGN_HTML_SCOPE_BOUNDARY_TAGS
    return is_foreign_scope_boundary(element)


def element_is_special(element: dict[str, Any]) -> bool:
    tag = element.get("tag")
    namespace = element_namespace(element)
    if namespace == "html":
        return tag in HTML_SPECIAL_TAGS and (
            tag not in FOREIGN_HTML_SCOPE_BOUNDARY_TAGS or tag == "title"
        )
    return is_foreign_scope_boundary(element)


def element_is_foreign_root_or_integration_boundary(
    element: dict[str, Any],
) -> bool:
    tag = element.get("tag")
    namespace = element_namespace(element)
    if namespace == "svg":
        return tag == "svg" or tag in SVG_HTML_INTEGRATION_TAGS
    if namespace == "math":
        return tag == "math" or tag in MATHML_TEXT_INTEGRATION_TAGS
    return False


def foreign_html_breakout_start_tag(
    tag: str, attrs: list[tuple[str, str | None]]
) -> bool:
    if tag in FOREIGN_HTML_BREAKOUT_START_TAGS:
        return True
    if tag != "font":
        return False
    return any(
        name.casefold() in FOREIGN_HTML_BREAKOUT_FONT_ATTRS
        for name, _value in attrs
    )


def foreign_text_visible(elements: list[dict[str, Any]]) -> bool:
    # Ordinary SVG text is not reliable visibility evidence without layout
    # geometry. HTML/MathML integration points leave foreign context above.
    return foreign_context(elements) is None

def foreign_attributes_ineligible(
    tag: str,
    attrs: list[tuple[str, str | None]],
    current_foreign_context: str | None,
) -> bool:
    # Rendering visibility for arbitrary SVG/MathML attributes is not
    # reproducible here. Treat attributed foreign elements as ineligible
    # visibility evidence; ordinary SVG text is also fail-closed above.
    return bool(attrs) and (
        tag in FOREIGN_ROOT_TAGS or current_foreign_context is not None
    )


CLAIM_BINDING_BOUNDARY = "\x00"
CLAIM_SECTION_BOUNDARY_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
P_IMPLICIT_END_START_TAGS = frozenset(
    {
        "address",
        "article",
        "aside",
        "blockquote",
        "center",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hgroup",
        "hr",
        "listing",
        "main",
        "menu",
        "nav",
        "ol",
        "p",
        "pre",
        "search",
        "section",
        "summary",
        "table",
        "ul",
        "xmp",
    }
)
CLAIM_IMPLICIT_CLOSE_GROUPS = {
    "li": frozenset({"li"}),
    "dt": frozenset({"dt", "dd"}),
    "dd": frozenset({"dt", "dd"}),
    "tr": frozenset({"tr"}),
    "td": frozenset({"td", "th"}),
    "th": frozenset({"td", "th"}),
    "tbody": frozenset({"tbody", "thead", "tfoot"}),
    "thead": frozenset({"tbody", "thead", "tfoot"}),
    "tfoot": frozenset({"tbody", "thead", "tfoot"}),
    "button": frozenset({"button"}),
}

# HTML tree-building algorithms use different backward-scan scopes for
# implicit closes. Keep only the element categories needed by the concrete
# recovery paths below instead of treating every open ancestor as closable.
FOREIGN_HTML_SCOPE_BOUNDARY_TAGS = frozenset(
    {
        "mi",
        "mo",
        "mn",
        "ms",
        "mtext",
        "annotation-xml",
        "foreignobject",
        "desc",
        "title",
    }
)
HTML_SCOPE_BOUNDARY_TAGS = frozenset(
    {
        "applet",
        "caption",
        "html",
        "marquee",
        "object",
        "select",
        "table",
        "td",
        "template",
        "th",
    }
) | FOREIGN_HTML_SCOPE_BOUNDARY_TAGS
HTML_BUTTON_SCOPE_BOUNDARY_TAGS = HTML_SCOPE_BOUNDARY_TAGS | frozenset({"button"})
HTML_LIST_ITEM_SCOPE_BOUNDARY_TAGS = HTML_SCOPE_BOUNDARY_TAGS | frozenset({"ol", "ul"})
HTML_TABLE_SCOPE_BOUNDARY_TAGS = frozenset({"html", "table", "template"})
HTML_TABLE_SCOPE_EXPLICIT_END_TAGS = frozenset(
    {"table", "tbody", "td", "tfoot", "th", "thead", "tr"}
)
HTML_NORMAL_SCOPE_EXPLICIT_END_TAGS = CLAIM_SECTION_BOUNDARY_TAGS | frozenset(
    {
        "address",
        "applet",
        "article",
        "aside",
        "blockquote",
        "button",
        "center",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "header",
        "hgroup",
        "listing",
        "main",
        "marquee",
        "menu",
        "nav",
        "object",
        "ol",
        "pre",
        "search",
        "section",
        "select",
        "summary",
        "ul",
    }
)


def explicit_end_tag_scope_target(
    elements: list[dict[str, Any]], tag: str
) -> str | None:
    if tag in HTML_TABLE_SCOPE_EXPLICIT_END_TAGS:
        scope_boundaries = HTML_TABLE_SCOPE_BOUNDARY_TAGS
        target_tags = frozenset({tag})
    elif tag == "li":
        scope_boundaries = HTML_LIST_ITEM_SCOPE_BOUNDARY_TAGS
        target_tags = frozenset({"li"})
    elif tag == "p":
        scope_boundaries = HTML_BUTTON_SCOPE_BOUNDARY_TAGS
        target_tags = frozenset({"p"})
    elif tag in HTML_NORMAL_SCOPE_EXPLICIT_END_TAGS:
        scope_boundaries = HTML_SCOPE_BOUNDARY_TAGS
        target_tags = (
            CLAIM_SECTION_BOUNDARY_TAGS
            if tag in CLAIM_SECTION_BOUNDARY_TAGS
            else frozenset({tag})
        )
    else:
        for element in reversed(elements):
            element_tag = element.get("tag")
            if element_tag == tag:
                return tag
            if element_is_special(element):
                return None
        return None

    for element in reversed(elements):
        element_tag = element.get("tag")
        if element_tag in target_tags:
            return str(element_tag)
        if element_matches_boundary(element, scope_boundaries):
            return None
    return None


def explicit_form_end_index(elements: list[dict[str, Any]]) -> int | None:
    for index in range(len(elements) - 1, -1, -1):
        element = elements[index]
        element_tag = element.get("tag")
        if element_tag == "form" and element_namespace(element) == "html":
            return index
        if element_matches_boundary(element, HTML_SCOPE_BOUNDARY_TAGS):
            return None
    return None


def explicit_anchor_end_index(elements: list[dict[str, Any]]) -> int | None:
    for index in range(len(elements) - 1, -1, -1):
        element = elements[index]
        if element.get("tag") == "a" and element_namespace(element) == "html":
            return index
        if element_matches_boundary(element, HTML_SCOPE_BOUNDARY_TAGS):
            return None
    return None


def active_html_select_index(elements: list[dict[str, Any]]) -> int | None:
    """Return the active HTML select for the concrete in-select recovery path."""
    for index in range(len(elements) - 1, -1, -1):
        element = elements[index]
        namespace = element_namespace(element)
        tag = element.get("tag")
        if tag == "select" and namespace == "html":
            return index
        if namespace != "html" or tag == "template":
            return None
    return None


HTML_SELECT_EXIT_REPROCESS_START_TAGS = frozenset({"input", "textarea"})


def first_html_attribute_values(
    attrs: list[tuple[str, str | None]],
) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for name, value in attrs:
        key = name.casefold()
        if key not in values:
            values[key] = value.casefold() if isinstance(value, str) else value
    return values


HTML_TABLE_FOSTER_CONTEXT_BLOCKERS = frozenset(
    {"caption", "script", "select", "style", "td", "th", "template"}
)
HTML_TABLE_FOSTER_EXEMPT_START_TAGS = frozenset(
    {
        "caption",
        "col",
        "colgroup",
        "form",
        "script",
        "select",
        "style",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "template",
        "tr",
    }
)


def active_html_table_insertion_index(
    elements: list[dict[str, Any]],
) -> int | None:
    """Return the active HTML table when tokens use in-table recovery.

    Cells, captions and templates switch to insertion modes where ordinary
    descendants are not foster-parented out of the table.
    """
    for index in range(len(elements) - 1, -1, -1):
        element = elements[index]
        if element_namespace(element) != "html":
            return None
        tag = element.get("tag")
        if tag in HTML_TABLE_FOSTER_CONTEXT_BLOCKERS:
            return None
        if tag == "table":
            return index
    return None


HTML_COLGROUP_IMPLICIT_END_START_TAGS = frozenset({"tbody", "thead", "tfoot", "tr"})


def active_html_colgroup_transition_index(
    elements: list[dict[str, Any]], tag: str
) -> int | None:
    """Return an omitted-end colgroup only in the active HTML table context."""
    if tag not in HTML_COLGROUP_IMPLICIT_END_START_TAGS:
        return None
    table_index = active_html_table_insertion_index(elements)
    if table_index is None or len(elements) <= table_index + 1:
        return None
    colgroup_index = len(elements) - 1
    colgroup = elements[colgroup_index]
    if (
        colgroup_index <= table_index
        or colgroup.get("tag") != "colgroup"
        or element_namespace(colgroup) != "html"
    ):
        return None
    return colgroup_index


def foster_parent_context_elements(
    elements: list[dict[str, Any]], table_index: int
) -> list[dict[str, Any]]:
    """Project the effective ancestry of content foster-parented before table."""
    return [
        *elements[:table_index],
        *[
            element
            for element in elements[table_index + 1 :]
            if element.get("foster_parented") is True
        ],
    ]


def effective_html_visibility_elements(
    elements: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    table_index = active_html_table_insertion_index(elements)
    if table_index is None:
        return elements
    fostered = [
        element
        for element in elements[table_index + 1 :]
        if element.get("foster_parented") is True
    ]
    if not fostered:
        return elements
    return [*elements[:table_index], *fostered]


def html_start_tag_foster_parent_index(
    elements: list[dict[str, Any]],
    tag: str,
    attrs: list[tuple[str, str | None]],
) -> int | None:
    table_index = active_html_table_insertion_index(elements)
    if table_index is None:
        return None
    if tag in HTML_TABLE_FOSTER_EXEMPT_START_TAGS:
        return None
    if (
        tag == "input"
        and first_html_attribute_values(attrs).get("type") == "hidden"
    ):
        return None
    return table_index


HTML_SPECIAL_TAGS = frozenset(
    {
        "address",
        "applet",
        "area",
        "article",
        "aside",
        "base",
        "basefont",
        "bgsound",
        "blockquote",
        "body",
        "br",
        "button",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "embed",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hgroup",
        "hr",
        "html",
        "iframe",
        "img",
        "input",
        "keygen",
        "li",
        "link",
        "listing",
        "main",
        "marquee",
        "menu",
        "meta",
        "nav",
        "noembed",
        "noframes",
        "noscript",
        "object",
        "ol",
        "p",
        "param",
        "plaintext",
        "pre",
        "script",
        "search",
        "section",
        "select",
        "source",
        "style",
        "summary",
        "table",
        "tbody",
        "td",
        "template",
        "textarea",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
        "wbr",
        "xmp",
    }
) | FOREIGN_HTML_SCOPE_BOUNDARY_TAGS
LI_IMPLICIT_SCOPE_BOUNDARIES = HTML_SPECIAL_TAGS - frozenset(
    {"address", "div", "p", "li"}
)
DESCRIPTION_IMPLICIT_SCOPE_BOUNDARIES = HTML_SPECIAL_TAGS - frozenset(
    {"address", "div", "p", "dt", "dd"}
)
CLAIM_IMPLICIT_SCOPE_BOUNDARIES = {
    "li": LI_IMPLICIT_SCOPE_BOUNDARIES,
    "dt": DESCRIPTION_IMPLICIT_SCOPE_BOUNDARIES,
    "dd": DESCRIPTION_IMPLICIT_SCOPE_BOUNDARIES,
    "tr": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "td": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "th": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "tbody": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "thead": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "tfoot": HTML_TABLE_SCOPE_BOUNDARY_TAGS,
    "button": HTML_SCOPE_BOUNDARY_TAGS,
}


CLAIM_RECORD_END_BOUNDARY_TAGS = frozenset(
    {
        "address",
        "article",
        "aside",
        "blockquote",
        "button",
        "center",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "header",
        "hgroup",
        "li",
        "listing",
        "main",
        "math",
        "menu",
        "nav",
        "ol",
        "p",
        "pre",
        "search",
        "section",
        "summary",
        "svg",
        "table",
        "tbody",
        "tfoot",
        "thead",
        "textarea",
        "tr",
        "ul",
        "xmp",
    }
)
CLAIM_RECORD_START_BOUNDARY_TAGS = (
    CLAIM_RECORD_END_BOUNDARY_TAGS | frozenset({"hr"})
)


VISIBLE_TEXT_BOUNDARY_TAGS = frozenset(
    {
        "address",
        "article",
        "aside",
        "audio",
        "blockquote",
        "br",
        "button",
        "canvas",
        "center",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "embed",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hgroup",
        "hr",
        "iframe",
        "img",
        "input",
        "li",
        "listing",
        "main",
        "math",
        "menu",
        "meter",
        "nav",
        "object",
        "ol",
        "p",
        "progress",
        "pre",
        "search",
        "section",
        "select",
        "summary",
        "svg",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "textarea",
        "tr",
        "ul",
        "video",
        "xmp",
    }
)

NONRENDERED_VOID_TAGS = frozenset(
    {"area", "base", "col", "link", "meta", "param", "source", "track", "wbr"}
)
RENDERED_ELEMENT_BOUNDARY_TAGS = frozenset(
    {"canvas", "iframe", "meter", "object", "progress", "select", "video"}
)


class VisibleListLinkParser(HTMLParser):
    VOID_TAGS = frozenset(
        {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }
    )
    ALWAYS_HIDDEN_TAGS = frozenset(
        {
            "audio",
            "canvas",
            "datalist",
            "head",
            "iframe",
            "meter",
            "noembed",
            "noframes",
            "noscript",
            "object",
            "progress",
            "rp",
            "script",
            "select",
            "style",
            "template",
            "title",
            "video",
        }
    )

    def __init__(self, author_stylesheet_present: bool = False) -> None:
        super().__init__(convert_charrefs=True)
        self._author_stylesheet_present = author_stylesheet_present
        self._items: list[dict[str, Any]] = []
        self._anchors: list[dict[str, Any]] = []
        self._elements: list[dict[str, Any]] = []
        self._document_hidden = False
        self._document_inert = False
        self._form_element_active = False
        self.visible_items: list[tuple[str, list[tuple[str, str]]]] = []

    def close(self) -> None:
        super().close()
        while self._items:
            self._finalize_current_item()
        while self._anchors:
            self._finalize_anchor()
        if self._document_hidden:
            self.visible_items.clear()
        elif self._document_inert:
            self.visible_items = [
                (text, []) for text, _links in self.visible_items
            ]

    @staticmethod
    def _declares_hidden(
        tag: str,
        attrs: list[tuple[str, str | None]],
        author_stylesheet_present: bool = False,
        *,
        include_intrinsic_tag: bool = True,
    ) -> bool:
        lowered = first_html_attribute_values(attrs)
        class_value = lowered.get("class")
        class_tokens = (
            set(class_value.split()) if isinstance(class_value, str) else set()
        )
        safe_pymdown_details_class = (
            not author_stylesheet_present
            and tag == "details"
            and bool(class_tokens)
            and class_tokens.issubset(PYMDOWN_DETAILS_CLASSES)
        )
        safe_admonition_class = (
            not author_stylesheet_present
            and (
                (
                    tag == "div"
                    and len(class_tokens) == 2
                    and "admonition" in class_tokens
                    and bool(class_tokens & PYMDOWN_DETAILS_CLASSES)
                )
                or (
                    tag == "p"
                    and class_tokens == {"admonition-title"}
                )
            )
        )
        # CSS-affectable evidence is deliberately fail-closed. Reimplementing
        # the browser cascade here would leave bypasses through escapes,
        # stylesheet selectors, importance, inheritance, or theme rules.
        # The allowlisted class paths are MkDocs/Pymdown's standard details
        # and admonition renderings when the page itself supplies no stylesheet
        # override.
        return (
            (include_intrinsic_tag and tag in VisibleListLinkParser.ALWAYS_HIDDEN_TAGS)
            or "hidden" in lowered
            or lowered.get("aria-hidden") == "true"
            or "style" in lowered
            or "popover" in lowered
            or (tag == "details" and "name" in lowered)
            or (
                "class" in lowered
                and not safe_pymdown_details_class
                and not safe_admonition_class
            )
        )

    @staticmethod
    def _has_attribute(
        attrs: list[tuple[str, str | None]], name: str
    ) -> bool:
        wanted = name.casefold()
        return any(attr_name.casefold() == wanted for attr_name, _value in attrs)

    @staticmethod
    def _renders_boundary(
        tag: str,
        attrs: list[tuple[str, str | None]],
        author_stylesheet_present: bool = False,
        current_foreign_context: str | None = None,
    ) -> bool:
        lowered = first_html_attribute_values(attrs)
        if tag in NONRENDERED_VOID_TAGS or (
            tag == "input" and lowered.get("type") == "hidden"
        ):
            return False
        style_value = lowered.get("style")
        if isinstance(style_value, str) and "display:none" in re.sub(
            r"\s+", "", style_value
        ):
            return False
        class_value = lowered.get("class")
        if (
            isinstance(class_value, str)
            and "visually-hidden" in class_value.split()
        ):
            return False
        # CSS-affectable descendants remain ineligible visibility evidence,
        # but an ambiguous styled/classed element must conservatively keep
        # rendered records separated rather than silently merging them.
        ignored_boundary_attrs = {"style", "class"}
        if tag == "details":
            ignored_boundary_attrs.add("name")
        boundary_attrs = [
            (name, value)
            for name, value in attrs
            if name.casefold() not in ignored_boundary_attrs
        ]
        if VisibleListLinkParser._declares_hidden(
            tag,
            boundary_attrs,
            author_stylesheet_present,
            include_intrinsic_tag=False,
        ):
            return False
        if (
            current_foreign_context is not None
            and foreign_attributes_ineligible(tag, attrs, current_foreign_context)
        ):
            return False
        if (
            current_foreign_context == "svg"
            and tag in SVG_INELIGIBLE_SUBTREE_TAGS
        ) or (
            current_foreign_context == "math"
            and tag in MATHML_INELIGIBLE_SUBTREE_TAGS
        ):
            return False
        if tag == "dialog" and not VisibleListLinkParser._has_attribute(
            attrs, "open"
        ):
            return False
        if tag == "audio":
            return VisibleListLinkParser._has_attribute(attrs, "controls")
        if tag in VisibleListLinkParser.ALWAYS_HIDDEN_TAGS:
            return tag in RENDERED_ELEMENT_BOUNDARY_TAGS
        return True

    def _regular_hidden(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        return bool(active and active[-1]["hidden"])

    def _current_inert(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        return self._document_inert or any(
            element.get("inert") is True for element in active
        )

    def _text_visible(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        return (
            not self._author_stylesheet_present
            and not self._document_hidden
            and not self._current_hidden(active)
            and foreign_text_visible(active)
        )

    def _current_hidden(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        if self._regular_hidden(active):
            return True
        for index, element in enumerate(active):
            if element.get("tag") != "details" or element.get("closed") is not True:
                continue
            descendants = active[index + 1 :]
            if (
                not descendants
                or descendants[0].get("summary_for_closed_details") is not True
            ):
                return True
        return False

    def _close_element(self, tag: str) -> None:
        for index in range(len(self._elements) - 1, -1, -1):
            if self._elements[index].get("tag") == tag:
                del self._elements[index:]
                return

    def _pop_elements_from(self, index: int) -> None:
        removed = self._elements[index:]
        for _ in range(sum(element.get("tag") == "a" for element in removed)):
            self._finalize_anchor()
        for _ in range(sum(element.get("tag") == "li" for element in removed)):
            self._finalize_current_item()
        del self._elements[index:]

    def _close_active_table_for_nested_start(self) -> None:
        table_index = active_html_table_insertion_index(self._elements)
        if table_index is not None:
            self._pop_elements_from(table_index)

    def _append_text_boundary(self) -> None:
        if self._items:
            self._items[-1]["text"].append(" ")
        if self._anchors:
            self._anchors[-1]["text"].append(" ")

    def _current_list_item_open(self) -> bool:
        for element in reversed(self._elements):
            tag = element.get("tag")
            if tag == "li" and element_namespace(element) == "html":
                return True
            if (
                element_matches_boundary(element, LI_IMPLICIT_SCOPE_BOUNDARIES)
                or element_is_foreign_root_or_integration_boundary(element)
            ):
                return False
        return False

    def _finalize_anchor(self) -> None:
        if not self._anchors:
            return
        anchor = self._anchors.pop()
        href = anchor.get("href")
        visible_anchor_text = " ".join("".join(anchor["text"]).split())
        if (
            self._items
            and anchor.get("hidden") is not True
            and anchor.get("inert") is not True
            and isinstance(href, str)
        ):
            self._items[-1]["links"].append((href, visible_anchor_text))

    def _finalize_current_item(self) -> None:
        if not self._items:
            return
        item_depth = len(self._items)
        while (
            self._anchors
            and self._anchors[-1].get("item_depth") == item_depth
        ):
            self._finalize_anchor()
        item = self._items.pop()
        if item.get("hidden") is not True:
            visible_text = " ".join("".join(item["text"]).split())
            self.visible_items.append((visible_text, list(item["links"])))

    def _close_implicit_list_item(self) -> None:
        if not self._current_list_item_open():
            return
        self._finalize_current_item()
        self._close_element("li")

    def _close_implicit_paragraph(self, tag: str) -> None:
        if tag not in P_IMPLICIT_END_START_TAGS:
            return
        for index in range(len(self._elements) - 1, -1, -1):
            element = self._elements[index]
            element_tag = element.get("tag")
            if (
                element_matches_boundary(element, HTML_BUTTON_SCOPE_BOUNDARY_TAGS)
                or element_is_foreign_root_or_integration_boundary(element)
            ):
                return
            if element_tag == "p" and element_namespace(element) == "html":
                del self._elements[index:]
                return

    def _close_implicit_container(self, tag: str) -> None:
        if tag not in {"button", "dt", "dd", "tr", "td", "th", "tbody", "thead", "tfoot"}:
            return
        close_tags = CLAIM_IMPLICIT_CLOSE_GROUPS[tag]
        scope_boundaries = CLAIM_IMPLICIT_SCOPE_BOUNDARIES[tag]
        for index in range(len(self._elements) - 1, -1, -1):
            element = self._elements[index]
            element_tag = element.get("tag")
            if (
                element_matches_boundary(element, scope_boundaries)
                or element_is_foreign_root_or_integration_boundary(element)
            ):
                return
            if (
                element_tag in close_tags
                and element_namespace(element) == "html"
            ):
                removed_list_items = sum(
                    element.get("tag") == "li"
                    for element in self._elements[index:]
                )
                for _ in range(removed_list_items):
                    self._finalize_current_item()
                del self._elements[index:]
                return

    def _close_implicit_heading(self, tag: str) -> None:
        if (
            tag in CLAIM_SECTION_BOUNDARY_TAGS
            and self._elements
            and self._elements[-1].get("tag") in CLAIM_SECTION_BOUNDARY_TAGS
        ):
            self.handle_endtag(str(self._elements[-1]["tag"]))

    def _exit_foreign_context_for_html_breakout(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> bool:
        if not foreign_html_breakout_start_tag(tag, attrs):
            return False
        root_index = active_foreign_root_index(self._elements)
        if root_index is None:
            return False
        removed = self._elements[root_index:]
        for _ in range(sum(element.get("tag") == "a" for element in removed)):
            self._finalize_anchor()
        for _ in range(sum(element.get("tag") == "li" for element in removed)):
            self._finalize_current_item()
        del self._elements[root_index:]
        return True

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        current_foreign_context = foreign_context(self._elements)
        if current_foreign_context is not None:
            self._exit_foreign_context_for_html_breakout(tag, attrs)
            current_foreign_context = foreign_context(self._elements)
        if tag == "image" and current_foreign_context is None:
            tag = "img"
        namespace = namespace_for_start_tag(self._elements, tag)
        if tag in {"html", "body"} and namespace == "html":
            self._document_hidden = (
                self._document_hidden
                or self._declares_hidden(
                    tag, attrs, self._author_stylesheet_present
                )
            )
            self._document_inert = (
                self._document_inert or self._has_attribute(attrs, "inert")
            )
            return
        if tag == "table" and namespace == "html":
            self._close_active_table_for_nested_start()
        if tag == "form" and namespace == "html":
            if self._form_element_active:
                return
            self._form_element_active = True
            if active_html_table_insertion_index(self._elements) is not None:
                return
        if tag == "select" and namespace == "html":
            select_index = active_html_select_index(self._elements)
            if select_index is not None:
                self._pop_elements_from(select_index)
                return
        if (
            tag in HTML_SELECT_EXIT_REPROCESS_START_TAGS
            and namespace == "html"
        ):
            select_index = active_html_select_index(self._elements)
            if select_index is not None:
                self._pop_elements_from(select_index)
        colgroup_index = active_html_colgroup_transition_index(
            self._elements, tag
        )
        if colgroup_index is not None:
            self._pop_elements_from(colgroup_index)
        if tag == "a" and namespace == "html":
            if self._anchors and self._anchors[-1].get("namespace") == "html":
                self._finalize_anchor()
            if any(
                element.get("tag") == "a"
                and element_namespace(element) == "html"
                for element in self._elements
            ):
                self._close_element("a")
        self._close_implicit_paragraph(tag)
        self._close_implicit_heading(tag)
        if current_foreign_context is None:
            self._close_implicit_container(tag)
        if tag == "li":
            self._close_implicit_list_item()
        foster_table_index = (
            html_start_tag_foster_parent_index(self._elements, tag, attrs)
            if current_foreign_context is None and namespace == "html"
            else None
        )
        visibility_elements = (
            foster_parent_context_elements(self._elements, foster_table_index)
            if foster_table_index is not None
            else self._elements
        )
        boundary_visible_before = self._text_visible(visibility_elements)
        parent = visibility_elements[-1] if visibility_elements else None
        summary_for_closed_details = (
            tag == "summary"
            and isinstance(parent, dict)
            and parent.get("tag") == "details"
            and parent.get("closed") is True
            and parent.get("summary_seen") is not True
        )
        if summary_for_closed_details:
            parent["summary_seen"] = True

        current_foreign_context = foreign_context(visibility_elements)
        element_renders_boundary = (
            boundary_visible_before
            and self._renders_boundary(
                tag,
                attrs,
                self._author_stylesheet_present,
                current_foreign_context,
            )
        )
        text_boundary_visible = (
            boundary_visible_before
            and tag in VISIBLE_TEXT_BOUNDARY_TAGS
            and (
                tag not in self.VOID_TAGS
                or element_renders_boundary
            )
        )
        if text_boundary_visible:
            self._append_text_boundary()
        hidden = (
            self._regular_hidden(visibility_elements)
            or self._declares_hidden(
                tag, attrs, self._author_stylesheet_present
            )
            or foreign_attributes_ineligible(tag, attrs, current_foreign_context)
            or (
                current_foreign_context == "svg"
                and tag in SVG_INELIGIBLE_SUBTREE_TAGS
            )
            or (
                current_foreign_context == "math"
                and tag in MATHML_INELIGIBLE_SUBTREE_TAGS
            )
        )
        closed = tag == "details" and not self._has_attribute(attrs, "open")
        if tag == "dialog" and not self._has_attribute(attrs, "open"):
            hidden = True
        if tag not in self.VOID_TAGS:
            self._elements.append(
                {
                    "tag": tag,
                    "namespace": namespace,
                    "foster_parented": foster_table_index is not None,
                    "hidden": hidden,
                    "inert": self._has_attribute(attrs, "inert"),
                    "closed": closed,
                    "summary_seen": False if tag == "details" else None,
                    "summary_for_closed_details": summary_for_closed_details,
                    "renders_boundary": element_renders_boundary,
                    "text_boundary_visible": text_boundary_visible,
                }
            )

        effective_hidden = not self._text_visible()
        effective_inert = self._current_inert()
        if tag == "li":
            self._items.append(
                {"text": [], "links": [], "hidden": effective_hidden}
            )
            return
        if tag == "a" and self._items:
            href = next(
                (value for name, value in attrs if name.casefold() == "href"),
                None,
            )
            self._anchors.append(
                {
                    "href": href if isinstance(href, str) else None,
                    "namespace": namespace,
                    "text": [],
                    "hidden": effective_hidden,
                    "inert": effective_inert,
                    "item_depth": len(self._items),
                }
            )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        # HTML ignores self-closing syntax on ordinary non-void elements.
        # In SVG/MathML foreign content the self-closing flag is real,
        # including for child elements, so those tags must not leak onto
        # the HTML visibility stack.
        tag = tag.casefold()
        current_foreign_context = foreign_context(self._elements)
        if tag == "image" and current_foreign_context is None:
            tag = "img"
        if tag in self.VOID_TAGS:
            self.handle_starttag(tag, attrs)
            return
        if tag in FOREIGN_ROOT_TAGS:
            if current_foreign_context is None:
                self.handle_starttag(tag, attrs)
                self.handle_endtag(tag)
            return
        if current_foreign_context is not None:
            if foreign_html_breakout_start_tag(tag, attrs):
                self.handle_starttag(tag, attrs)
            return
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        visibility_elements = self._elements
        if data.strip():
            table_index = active_html_table_insertion_index(self._elements)
            if table_index is not None:
                visibility_elements = foster_parent_context_elements(
                    self._elements, table_index
                )
        if not self._text_visible(visibility_elements):
            return
        if self._items:
            self._items[-1]["text"].append(data)
        if self._anchors:
            self._anchors[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag in self.VOID_TAGS:
            if tag == "br" and foreign_context(self._elements) is None:
                self.handle_starttag(tag, [])
            return
        current_foreign_context = foreign_context(self._elements)
        if tag in {"html", "body"} and current_foreign_context is None:
            return
        if (
            tag == "p"
            and current_foreign_context is None
            and explicit_end_tag_scope_target(self._elements, "p") is None
            and active_html_select_index(self._elements) is None
        ):
            self.handle_starttag("p", [])
            self.handle_endtag("p")
            return
        if tag == "a" and current_foreign_context is None:
            anchor_index = explicit_anchor_end_index(self._elements)
            if anchor_index is None:
                return
            if self._anchors:
                self._finalize_anchor()
            del self._elements[anchor_index]
            return
        html_form_end = (
            tag == "form" and current_foreign_context is None
        )
        if html_form_end:
            if not self._form_element_active:
                return
            self._form_element_active = False
            form_index = explicit_form_end_index(self._elements)
            if form_index is None:
                return
            close_tag = "form"
        else:
            form_index = None
            close_tag = explicit_end_tag_scope_target(self._elements, tag)
        if close_tag is None:
            return
        boundary_visible_before = self._text_visible()
        closing_renders_boundary = False
        closing_text_boundary_visible = False
        for element in reversed(self._elements):
            if element.get("tag") == close_tag:
                closing_renders_boundary = element.get("renders_boundary") is True
                closing_text_boundary_visible = (
                    element.get("text_boundary_visible") is True
                )
                break
        if tag in {"ul", "ol", "menu"}:
            self._close_implicit_list_item()
        if tag == "a" and self._anchors:
            self._finalize_anchor()
        elif tag == "li" and self._items:
            self._finalize_current_item()
        if html_form_end:
            assert form_index is not None
            del self._elements[form_index]
        elif close_tag == "table":
            table_index = next(
                (
                    index
                    for index in range(len(self._elements) - 1, -1, -1)
                    if self._elements[index].get("tag") == "table"
                    and element_namespace(self._elements[index]) == "html"
                ),
                None,
            )
            if table_index is not None:
                self._pop_elements_from(table_index)
        else:
            self._close_element(close_tag)
        if close_tag in VISIBLE_TEXT_BOUNDARY_TAGS and (
            boundary_visible_before or closing_text_boundary_visible
        ):
            self._append_text_boundary()


def rendered_list_links(path: Path) -> list[tuple[str, list[tuple[str, str]]]]:
    rendered = render_site_markdown(markdown_body(path))
    parser = VisibleListLinkParser(has_author_stylesheet(rendered))
    parser.feed(rendered)
    parser.close()
    return parser.visible_items


class VisibleTextParser(HTMLParser):
    VOID_TAGS = VisibleListLinkParser.VOID_TAGS
    TEXT_BOUNDARY_TAGS = VISIBLE_TEXT_BOUNDARY_TAGS
    RENDERED_HIDDEN_CONTENT_RECORD_TAGS = RENDERED_ELEMENT_BOUNDARY_TAGS

    def __init__(self, author_stylesheet_present: bool = False) -> None:
        super().__init__(convert_charrefs=True)
        self._author_stylesheet_present = author_stylesheet_present
        self._elements: list[dict[str, Any]] = []
        self._document_hidden = False
        self._form_element_active = False
        self._text: list[str] = []
        self._claim_heading_tag: str | None = None
        self._claim_heading_text: list[str] = []
        self._pending_claim_statement_paragraph = False

    def _regular_hidden(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        return bool(active and active[-1]["hidden"])

    def _text_visible(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        return (
            not self._author_stylesheet_present
            and not self._document_hidden
            and not self._current_hidden(active)
            and foreign_text_visible(active)
        )

    def _current_hidden(
        self, elements: list[dict[str, Any]] | None = None
    ) -> bool:
        active = (
            effective_html_visibility_elements(self._elements)
            if elements is None
            else elements
        )
        if self._regular_hidden(active):
            return True
        for index, element in enumerate(active):
            if element.get("tag") != "details" or element.get("closed") is not True:
                continue
            descendants = active[index + 1 :]
            if (
                not descendants
                or descendants[0].get("summary_for_closed_details") is not True
            ):
                return True
        return False

    def _close_element(self, tag: str) -> None:
        for index in range(len(self._elements) - 1, -1, -1):
            if self._elements[index].get("tag") == tag:
                del self._elements[index:]
                return

    def _pop_elements_from(self, index: int) -> None:
        removed = self._elements[index:]
        heading_was_removed = (
            self._claim_heading_tag is not None
            and any(
                element.get("tag") == self._claim_heading_tag
                for element in removed
            )
        )
        heading_was_visible = heading_was_removed and self._text_visible()
        heading_text = (
            " ".join("".join(self._claim_heading_text).split())
            if heading_was_removed
            else ""
        )
        del self._elements[index:]
        if heading_was_removed:
            self._claim_heading_tag = None
            self._claim_heading_text = []
            self._pending_claim_statement_paragraph = bool(
                heading_was_visible
                and re.fullmatch(r"CLM-[A-Z0-9-]+", heading_text)
            )

    def _close_active_table_for_nested_start(self) -> None:
        table_index = active_html_table_insertion_index(self._elements)
        if table_index is not None:
            self._pop_elements_from(table_index)

    @staticmethod
    def _has_attribute(
        attrs: list[tuple[str, str | None]], name: str
    ) -> bool:
        wanted = name.casefold()
        return any(attr_name.casefold() == wanted for attr_name, _value in attrs)

    def _close_implicit_group(
        self,
        close_tags: frozenset[str],
        scope_boundaries: frozenset[str],
    ) -> None:
        for index in range(len(self._elements) - 1, -1, -1):
            element = self._elements[index]
            element_tag = element.get("tag")
            if (
                element_matches_boundary(element, scope_boundaries)
                or element_is_foreign_root_or_integration_boundary(element)
            ):
                return
            if (
                element_tag in close_tags
                and element_namespace(element) == "html"
            ):
                if (
                    element_tag in CLAIM_RECORD_END_BOUNDARY_TAGS
                    and self._text_visible()
                ):
                    self._append_claim_binding_boundary()
                del self._elements[index:]
                return

    def _close_implicit_record(self, tag: str) -> None:
        close_tags = CLAIM_IMPLICIT_CLOSE_GROUPS.get(tag)
        if close_tags:
            self._close_implicit_group(
                close_tags,
                CLAIM_IMPLICIT_SCOPE_BOUNDARIES.get(tag, frozenset()),
            )
        if tag in P_IMPLICIT_END_START_TAGS:
            self._close_implicit_group(
                frozenset({"p"}),
                HTML_BUTTON_SCOPE_BOUNDARY_TAGS,
            )

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        current_foreign_context = foreign_context(self._elements)
        if (
            current_foreign_context is not None
            and foreign_html_breakout_start_tag(tag, attrs)
        ):
            root_index = active_foreign_root_index(self._elements)
            if root_index is not None:
                del self._elements[root_index:]
            current_foreign_context = foreign_context(self._elements)
        if tag == "image" and current_foreign_context is None:
            tag = "img"
        namespace = namespace_for_start_tag(self._elements, tag)
        if tag in {"html", "body"} and namespace == "html":
            self._document_hidden = (
                self._document_hidden
                or VisibleListLinkParser._declares_hidden(
                    tag, attrs, self._author_stylesheet_present
                )
            )
            return
        if tag == "table" and namespace == "html":
            self._close_active_table_for_nested_start()
        if tag == "form" and namespace == "html":
            if self._form_element_active:
                return
            self._form_element_active = True
            if active_html_table_insertion_index(self._elements) is not None:
                return
        if tag == "select" and namespace == "html":
            select_index = active_html_select_index(self._elements)
            if select_index is not None:
                self._pop_elements_from(select_index)
                return
        if (
            tag in HTML_SELECT_EXIT_REPROCESS_START_TAGS
            and namespace == "html"
        ):
            select_index = active_html_select_index(self._elements)
            if select_index is not None:
                self._pop_elements_from(select_index)
        colgroup_index = active_html_colgroup_transition_index(
            self._elements, tag
        )
        if colgroup_index is not None:
            self._pop_elements_from(colgroup_index)
        if (
            tag == "a"
            and namespace == "html"
            and any(
                element.get("tag") == "a"
                and element_namespace(element) == "html"
                for element in self._elements
            )
        ):
            self._close_element("a")
        wants_claim_heading_join = (
            tag == "p" and self._pending_claim_statement_paragraph
        )
        if (
            tag in CLAIM_SECTION_BOUNDARY_TAGS
            and self._elements
            and self._elements[-1].get("tag") in CLAIM_SECTION_BOUNDARY_TAGS
        ):
            self.handle_endtag(str(self._elements[-1]["tag"]))
        self._close_implicit_record(tag)
        foster_table_index = (
            html_start_tag_foster_parent_index(self._elements, tag, attrs)
            if current_foreign_context is None and namespace == "html"
            else None
        )
        visibility_elements = (
            foster_parent_context_elements(self._elements, foster_table_index)
            if foster_table_index is not None
            else self._elements
        )
        boundary_visible_before = self._text_visible(visibility_elements)
        parent = visibility_elements[-1] if visibility_elements else None
        summary_for_closed_details = (
            tag == "summary"
            and isinstance(parent, dict)
            and parent.get("tag") == "details"
            and parent.get("closed") is True
            and parent.get("summary_seen") is not True
        )
        if summary_for_closed_details:
            parent["summary_seen"] = True

        current_foreign_context = foreign_context(visibility_elements)
        element_renders_boundary = (
            boundary_visible_before
            and VisibleListLinkParser._renders_boundary(
                tag,
                attrs,
                self._author_stylesheet_present,
                current_foreign_context,
            )
        )
        text_boundary_visible = (
            boundary_visible_before
            and tag in self.TEXT_BOUNDARY_TAGS
            and (
                tag not in self.VOID_TAGS
                or element_renders_boundary
            )
        )
        hidden = (
            self._regular_hidden(visibility_elements)
            or VisibleListLinkParser._declares_hidden(
                tag, attrs, self._author_stylesheet_present
            )
            or foreign_attributes_ineligible(tag, attrs, current_foreign_context)
            or (
                current_foreign_context == "svg"
                and tag in SVG_INELIGIBLE_SUBTREE_TAGS
            )
            or (
                current_foreign_context == "math"
                and tag in MATHML_INELIGIBLE_SUBTREE_TAGS
            )
        )
        closed = tag == "details" and not self._has_attribute(attrs, "open")
        if tag == "dialog" and not self._has_attribute(attrs, "open"):
            hidden = True
        if tag not in self.VOID_TAGS:
            self._elements.append(
                {
                    "tag": tag,
                    "namespace": namespace,
                    "foster_parented": foster_table_index is not None,
                    "hidden": hidden,
                    "closed": closed,
                    "summary_seen": False if tag == "details" else None,
                    "summary_for_closed_details": summary_for_closed_details,
                    "renders_boundary": element_renders_boundary,
                    "text_boundary_visible": text_boundary_visible,
                }
            )
        if tag in CLAIM_SECTION_BOUNDARY_TAGS and self._text_visible():
            self._claim_heading_tag = tag
            self._claim_heading_text = []
        joins_claim_heading = (
            wants_claim_heading_join and element_renders_boundary
        )
        if joins_claim_heading:
            self._pending_claim_statement_paragraph = False

        heading_gap_visible = (
            element_renders_boundary
            and (
                tag in CLAIM_SECTION_BOUNDARY_TAGS
                | CLAIM_RECORD_START_BOUNDARY_TAGS
                or tag in self.VOID_TAGS
                or tag in self.RENDERED_HIDDEN_CONTENT_RECORD_TAGS
                or (
                    tag == "audio"
                    and self._has_attribute(attrs, "controls")
                )
            )
        )
        pending_gap_boundary_added = False
        if (
            self._pending_claim_statement_paragraph
            and not joins_claim_heading
            and heading_gap_visible
        ):
            self._pending_claim_statement_paragraph = False
            self._append_claim_binding_boundary()
            pending_gap_boundary_added = True

        if (
            tag in CLAIM_SECTION_BOUNDARY_TAGS | CLAIM_RECORD_START_BOUNDARY_TAGS
            and element_renders_boundary
            and not joins_claim_heading
            and not pending_gap_boundary_added
        ):
            self._append_claim_binding_boundary()
        if text_boundary_visible:
            self._append_text(" ")

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        # Match the browser split between ordinary HTML and foreign content.
        tag = tag.casefold()
        current_foreign_context = foreign_context(self._elements)
        if tag == "image" and current_foreign_context is None:
            tag = "img"
        if tag in self.VOID_TAGS:
            self.handle_starttag(tag, attrs)
            return
        if tag in FOREIGN_ROOT_TAGS:
            if current_foreign_context is None:
                self.handle_starttag(tag, attrs)
                self.handle_endtag(tag)
            return
        if current_foreign_context is not None:
            if foreign_html_breakout_start_tag(tag, attrs):
                self.handle_starttag(tag, attrs)
            return
        self.handle_starttag(tag, attrs)

    def _append_text(self, data: str) -> None:
        self._text.append(data)

    def _append_claim_binding_boundary(self) -> None:
        # NUL cannot originate as rendered HTML text: browsers replace source
        # NULs during parsing. Keep it internal so lexical checks ignore it.
        self._text.append(CLAIM_BINDING_BOUNDARY)

    def handle_data(self, data: str) -> None:
        visibility_elements = self._elements
        if data.strip():
            table_index = active_html_table_insertion_index(self._elements)
            if table_index is not None:
                visibility_elements = foster_parent_context_elements(
                    self._elements, table_index
                )
        if not self._text_visible(visibility_elements):
            return
        if self._claim_heading_tag is not None:
            self._claim_heading_text.append(data)
        elif self._pending_claim_statement_paragraph and data.strip():
            self._pending_claim_statement_paragraph = False
            self._append_claim_binding_boundary()
        self._append_text(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag in self.VOID_TAGS:
            if tag == "br" and foreign_context(self._elements) is None:
                self.handle_starttag(tag, [])
            return
        current_foreign_context = foreign_context(self._elements)
        if tag in {"html", "body"} and current_foreign_context is None:
            return
        if (
            tag == "p"
            and current_foreign_context is None
            and explicit_end_tag_scope_target(self._elements, "p") is None
            and active_html_select_index(self._elements) is None
        ):
            self.handle_starttag("p", [])
            self.handle_endtag("p")
            return
        if tag == "a" and current_foreign_context is None:
            anchor_index = explicit_anchor_end_index(self._elements)
            if anchor_index is None:
                return
            del self._elements[anchor_index]
            return
        html_form_end = (
            tag == "form" and current_foreign_context is None
        )
        if html_form_end:
            if not self._form_element_active:
                return
            self._form_element_active = False
            form_index = explicit_form_end_index(self._elements)
            if form_index is None:
                return
            close_tag = "form"
        else:
            form_index = None
            close_tag = explicit_end_tag_scope_target(self._elements, tag)
        if close_tag is None:
            return
        boundary_visible_before = self._text_visible()
        closing_renders_boundary = False
        closing_text_boundary_visible = False
        for element in reversed(self._elements):
            if element.get("tag") == close_tag:
                closing_renders_boundary = element.get("renders_boundary") is True
                closing_text_boundary_visible = (
                    element.get("text_boundary_visible") is True
                )
                break
        closes_claim_heading = close_tag == self._claim_heading_tag
        claim_heading_text = (
            " ".join("".join(self._claim_heading_text).split())
            if closes_claim_heading
            else ""
        )
        if html_form_end:
            assert form_index is not None
            del self._elements[form_index]
        elif close_tag == "table":
            table_index = next(
                (
                    index
                    for index in range(len(self._elements) - 1, -1, -1)
                    if self._elements[index].get("tag") == "table"
                    and element_namespace(self._elements[index]) == "html"
                ),
                None,
            )
            if table_index is not None:
                self._pop_elements_from(table_index)
        else:
            self._close_element(close_tag)
        if close_tag in CLAIM_RECORD_END_BOUNDARY_TAGS and (
            boundary_visible_before or closing_renders_boundary
        ):
            self._append_claim_binding_boundary()
        if close_tag in self.TEXT_BOUNDARY_TAGS and (
            boundary_visible_before or closing_text_boundary_visible
        ):
            self._append_text(" ")
        if closes_claim_heading:
            self._claim_heading_tag = None
            self._claim_heading_text = []
            self._pending_claim_statement_paragraph = bool(
                boundary_visible_before
                and re.fullmatch(r"CLM-[A-Z0-9-]+", claim_heading_text)
            )

    def _normalized_text(self) -> str:
        if self._document_hidden:
            return ""
        return " ".join("".join(self._text).split())

    def text(self) -> str:
        return " ".join(
            self._normalized_text().replace(CLAIM_BINDING_BOUNDARY, " ").split()
        )

    def claim_binding_text(self) -> str:
        return self._normalized_text()


def visible_markdown_text(value: str) -> str:
    rendered = render_site_markdown(value)
    parser = VisibleTextParser(has_author_stylesheet(rendered))
    parser.feed(rendered)
    parser.close()
    return parser.text()


def visible_markdown_claim_binding_text(value: str) -> str:
    rendered = render_site_markdown(value)
    parser = VisibleTextParser(has_author_stylesheet(rendered))
    parser.feed(rendered)
    parser.close()
    return parser.claim_binding_text()


class VisibleSectionTextParser(VisibleTextParser):
    def __init__(
        self, heading: str, author_stylesheet_present: bool = False
    ) -> None:
        super().__init__(author_stylesheet_present)
        self._wanted_heading = " ".join(heading.split())
        self._in_h2 = False
        self._h2_text: list[str] = []
        self._h2_visible = False
        self._capture = False
        self._capture_before_h2 = False
        self._section_text: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        super().handle_starttag(tag, attrs)
        if tag == "h1":
            if self._text_visible():
                self._capture = False
        elif tag == "h2":
            self._capture_before_h2 = self._capture
            self._in_h2 = True
            self._h2_text = []
            self._h2_visible = self._text_visible()

    def _append_text(self, data: str) -> None:
        if self._in_h2:
            self._h2_text.append(data)
            return
        if self._capture:
            self._section_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        recovered_heading = (
            explicit_end_tag_scope_target(self._elements, tag)
            if self._in_h2 and tag in CLAIM_SECTION_BOUNDARY_TAGS
            else None
        )
        if recovered_heading == "h2":
            heading_text = " ".join("".join(self._h2_text).split())
            is_target = heading_text == self._wanted_heading
            capture_after_heading = (
                is_target
                if self._h2_visible
                else self._capture_before_h2
            )
            super().handle_endtag(tag)
            if is_target and self._h2_visible and self._section_text:
                self._section_text.append(" ")
            self._in_h2 = False
            self._h2_text = []
            self._h2_visible = False
            self._capture_before_h2 = False
            self._capture = capture_after_heading
            return
        super().handle_endtag(tag)

    def text(self) -> str:
        if self._document_hidden:
            return ""
        return " ".join("".join(self._section_text).split())


def rendered_visible_text(path: Path) -> str:
    return visible_markdown_text(markdown_body(path))


def rendered_claim_binding_text(path: Path) -> str:
    return visible_markdown_claim_binding_text(markdown_body(path))


def rendered_visible_section(path: Path, heading: str) -> str:
    rendered = render_site_markdown(markdown_body(path))
    parser = VisibleSectionTextParser(
        heading, has_author_stylesheet(rendered)
    )
    parser.feed(rendered)
    parser.close()
    return parser.text()


def exact_visible_id(text: str, identifier: str) -> bool:
    pattern = rf"(?<![\w-]){re.escape(identifier)}(?![\w-])"
    return re.search(pattern, text) is not None


def visible_claim_segments(text: str) -> list[tuple[str, str]]:
    matches = list(
        re.finditer(r"(?<![\w-])CLM-[A-Z0-9-]+(?![\w-])", text)
    )
    segments: list[tuple[str, str]] = []
    for match in matches:
        start_boundary = text.rfind(
            CLAIM_BINDING_BOUNDARY, 0, match.start()
        )
        start = 0 if start_boundary == -1 else start_boundary + 1
        end = text.find(CLAIM_BINDING_BOUNDARY, match.end())
        if end == -1:
            end = len(text)
        segments.append((match.group(), text[start:end]))
    return segments


def claim_occurrences_bound_to_wording(
    text: str,
    claim_id: str,
    claim_text: str,
) -> bool:
    canonical = lexical_text(claim_text)
    if not canonical:
        return False
    segments = [
        segment
        for visible_id, segment in visible_claim_segments(text)
        if visible_id == claim_id
    ]
    return bool(segments) and all(
        contains_lexical_sequence(lexical_text(segment), canonical)
        for segment in segments
    )


def direct_source_link_errors(
    path: Path,
    source_ids: list[str],
    source_by_id: dict[str, dict[str, Any]],
    label: str,
) -> list[str]:
    items = rendered_list_links(path)
    out: list[str] = []
    for source_id in source_ids:
        source = source_by_id.get(source_id)
        if not isinstance(source, dict):
            continue
        url = source.get("url")
        if not isinstance(url, str):
            continue
        if not any(
            exact_visible_id(visible_text, source_id)
            and any(
                href == url and has_visible_text(anchor_text)
                for href, anchor_text in links
            )
            for visible_text, links in items
        ):
            out.append(
                f"{label}: source {source_id} must be visibly listed with a "
                "clickable link to its registered URL"
            )
    return out


def established_supports(
    source_ids: list[str],
    source_by_id: dict[str, dict[str, Any]],
) -> bool:
    if not source_ids or any(source_id not in source_by_id for source_id in source_ids):
        return False
    resolved = [source_by_id[source_id] for source_id in source_ids]
    if any(
        source.get("tier") == "A" and source.get("primary") is True
        for source in resolved
    ):
        return True
    high_quality = [
        source for source in resolved if source.get("tier") in {"B", "C"}
    ]
    institutions = {
        source["institution"].strip().casefold()
        for source in high_quality
        if isinstance(source.get("institution"), str) and source["institution"].strip()
    }
    return len(high_quality) >= 2 and len(institutions) >= 2


def established_claim_supports(
    value: Any,
    source_by_id: dict[str, dict[str, Any]],
) -> bool:
    resolved: list[tuple[dict[str, Any], str]] = []
    for record in mapping_list(value):
        source_id = record.get("source")
        directness = record.get("directness")
        if (
            isinstance(source_id, str)
            and source_id in source_by_id
            and isinstance(directness, str)
            and directness in {"direct", "indirect"}
        ):
            resolved.append((source_by_id[source_id], directness))

    if any(
        directness == "direct"
        and source.get("tier") == "A"
        and source.get("primary") is True
        for source, directness in resolved
    ):
        return True

    high_quality = [
        source
        for source, _directness in resolved
        if source.get("tier") in {"B", "C"}
    ]
    institutions = {
        source["institution"].strip().casefold()
        for source in high_quality
        if isinstance(source.get("institution"), str)
        and source["institution"].strip()
    }
    return len(high_quality) >= 2 and len(institutions) >= 2


def load_catalog(
    filename: str,
    key: str,
    schema_file: str,
    errors: list[str],
) -> list[dict[str, Any]]:
    path = DATA / filename
    payload = load_yaml(path)
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        errors.append(f"{path.relative_to(ROOT)}: expected top-level list '{key}'")
        return []
    rows = payload[key]
    valid_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{path.relative_to(ROOT)}[{index}]: expected mapping")
            continue
        row_errors = schema_errors(
            row, schema_file, f"{path.relative_to(ROOT)}[{index}]"
        )
        errors.extend(row_errors)
        if row_errors:
            continue
        valid_rows.append(row)
    return valid_rows


def evidence_sources(value: Any) -> list[str]:
    return [
        item["source"]
        for item in mapping_list(value)
        if isinstance(item.get("source"), str)
    ]


def main() -> int:
    errors: list[str] = []

    sources = load_catalog("sources.yml", "sources", "source.schema.json", errors)
    for source in sources:
        source_id = source.get("id", "<unknown-source>")
        publication_date = source.get("date")
        if (
            isinstance(publication_date, str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}", publication_date.strip())
            and period_bounds(publication_date) is None
        ):
            errors.append(
                f"sources:{source_id}: date must use a valid YYYY-MM-DD date"
            )

        accessed = source.get("accessed")
        if isinstance(accessed, str) and period_bounds(accessed) is None:
            errors.append(
                f"sources:{source_id}: accessed must use a valid YYYY-MM-DD date"
            )

        url = source.get("url")
        if isinstance(url, str) and not valid_https_url(url):
            errors.append(
                f"sources:{source_id}: url must be a valid HTTPS URL with a host"
            )
        archive_url = source.get("archive_url")
        if isinstance(archive_url, str) and not valid_https_url(archive_url):
            errors.append(
                f"sources:{source_id}: archive_url must be a valid HTTPS URL with a host"
            )

    entities = load_catalog("entities.yml", "entities", "entity.schema.json", errors)
    mechanisms = load_catalog(
        "mechanisms.yml", "mechanisms", "mechanism.schema.json", errors
    )
    relations = load_catalog(
        "relations.yml", "relations", "relation.schema.json", errors
    )

    source_ids = unique_ids(sources, "sources", errors)
    source_by_id = {
        item["id"]: item
        for item in sources
        if isinstance(item.get("id"), str)
    }
    source_tiers = {
        source_id: item.get("tier")
        for source_id, item in source_by_id.items()
    }
    entity_ids = unique_ids(entities, "entities", errors)
    mechanism_ids = unique_ids(mechanisms, "mechanisms", errors)
    unique_ids(relations, "relations", errors)
    relation_by_id = {
        item["id"]: item
        for item in relations
        if isinstance(item.get("id"), str)
    }

    case_ids: set[str] = set()
    claim_ids: set[str] = set()
    claim_case_by_id: dict[str, str] = {}
    claim_by_id: dict[str, dict[str, Any]] = {}
    cases: list[tuple[Path, dict[str, Any]]] = []

    for path in sorted(CASE_DIR.rglob("*.md")):
        if path == CASE_DIR / "index.md":
            continue
        label = str(path.relative_to(ROOT))
        try:
            meta = frontmatter(path)
        except Exception as exc:
            errors.append(f"{label}: {exc}")
            continue

        errors.extend(schema_errors(meta, "case.schema.json", label))
        case_id = meta.get("id")
        if isinstance(case_id, str):
            if case_id in case_ids or case_id in entity_ids:
                errors.append(f"global IDs: duplicate id {case_id}")
            case_ids.add(case_id)

        raw_claims = meta.get("claims", [])
        if isinstance(raw_claims, list):
            for claim in raw_claims:
                if not isinstance(claim, dict):
                    errors.append(f"{label}: claim must be a mapping")
                    continue
                claim_label = f"{label}:{claim.get('id', '<unknown-claim>')}"
                errors.extend(schema_errors(claim, "claim.schema.json", claim_label))
                claim_id = claim.get("id")
                if isinstance(claim_id, str):
                    if claim_id in claim_ids:
                        errors.append(f"claims: duplicate id {claim_id}")
                    claim_ids.add(claim_id)
                    claim_by_id.setdefault(claim_id, claim)
                    if isinstance(case_id, str):
                        claim_case_by_id[claim_id] = case_id
        cases.append((path, meta))

    for path, meta in cases:
        label = str(path.relative_to(ROOT))
        case_id = meta.get("id")
        period = meta.get("period")
        if isinstance(period, dict):
            start_raw = period.get("start")
            end_raw = period.get("end")
            start_bounds = period_bounds(start_raw)
            end_bounds = period_bounds(end_raw) if end_raw is not None else None
            if isinstance(start_raw, str) and start_bounds is None:
                errors.append(
                    f"{label}: period.start must use a valid YYYY or YYYY-MM-DD value"
                )
            if isinstance(end_raw, str) and end_bounds is None:
                errors.append(
                    f"{label}: period.end must use a valid YYYY or YYYY-MM-DD value"
                )
            if (
                start_bounds is not None
                and end_bounds is not None
                and start_bounds[0] > end_bounds[1]
            ):
                errors.append(f"{label}: period.end precedes period.start")

        case_sources = string_list(meta.get("sources"))
        for source_id in case_sources:
            if source_id not in source_ids:
                errors.append(f"{label}: unknown source {source_id}")
        errors.extend(
            direct_source_link_errors(path, case_sources, source_by_id, label)
        )

        for actor_id in string_list(meta.get("actors")):
            if actor_id not in entity_ids:
                errors.append(f"{label}: unknown actor {actor_id}")
        for mechanism_id in string_list(meta.get("mechanisms")):
            if mechanism_id not in mechanism_ids:
                errors.append(f"{label}: unknown mechanism {mechanism_id}")

        for event_claim_id in string_list(meta.get("event_claims")):
            event_claim = claim_by_id.get(event_claim_id)
            if event_claim is None:
                errors.append(f"{label}: event claim {event_claim_id} is unknown")
                continue
            owner_case = claim_case_by_id.get(event_claim_id)
            if isinstance(case_id, str) and owner_case != case_id:
                errors.append(
                    f"{label}: event claim {event_claim_id} belongs to case {owner_case}"
                )
                continue
            if event_claim.get("classification") != "fact":
                errors.append(
                    f"{label}: event claim {event_claim_id} must be classification fact"
                )
            event_level = event_claim.get("evidence_level")
            if not isinstance(event_level, str) or event_level not in {"established", "strong"}:
                errors.append(
                    f"{label}: event claim {event_claim_id} must be established or strong"
                )

        for synthesis_field in ("what_follows", "what_does_not_follow"):
            for synthesis in mapping_list(meta.get(synthesis_field)):
                for synthesis_claim_id in string_list(synthesis.get("claim_ids")):
                    synthesis_claim = claim_by_id.get(synthesis_claim_id)
                    if synthesis_claim is None:
                        errors.append(
                            f"{label}: {synthesis_field} references unknown claim {synthesis_claim_id}"
                        )
                        continue
                    owner_case = claim_case_by_id.get(synthesis_claim_id)
                    if isinstance(case_id, str) and owner_case != case_id:
                        errors.append(
                            f"{label}: {synthesis_field} claim {synthesis_claim_id} "
                            f"belongs to case {owner_case}"
                        )

        seen_links: set[tuple[str, str]] = set()
        for link in mapping_list(meta.get("case_links")):
            kind = link.get("kind")
            target = link.get("target")
            if isinstance(target, str):
                if target == case_id:
                    errors.append(f"{label}: case link may not target itself")
                if target not in case_ids:
                    errors.append(f"{label}: case link references unknown case {target}")
            if isinstance(kind, str) and isinstance(target, str):
                key = (kind, target)
                if key in seen_links:
                    errors.append(
                        f"{label}: duplicate {kind} case link to {target}"
                    )
                seen_links.add(key)
            if kind == "documented_connection":
                relation_id = link.get("relation_id")
                if not isinstance(relation_id, str):
                    continue
                relation = relation_by_id.get(relation_id)
                if relation is None:
                    errors.append(
                        f"{label}: documented case link requires known relation {relation_id}"
                    )
                elif isinstance(case_id, str) and isinstance(target, str):
                    if {relation.get("from"), relation.get("to")} != {case_id, target}:
                        errors.append(
                            f"{label}: relation {relation_id} does not directly connect "
                            f"{case_id} and {target}"
                        )

        visible_body = rendered_visible_text(path)
        claim_binding_body = rendered_claim_binding_text(path)
        body_lexical = lexical_text(visible_body)

        event_section = rendered_visible_section(path, "Gesicherter Ereigniskern")
        visible_event_claim_ids = list(
            dict.fromkeys(
                re.findall(
                    r"(?<![\w-])CLM-[A-Z0-9-]+(?![\w-])",
                    event_section,
                )
            )
        )
        declared_event_claim_ids = string_list(meta.get("event_claims"))
        for event_claim_id in declared_event_claim_ids:
            if event_claim_id not in visible_event_claim_ids:
                errors.append(
                    f"{label}: event claim {event_claim_id} must appear in Gesicherter Ereigniskern"
                )
        for visible_event_claim_id in visible_event_claim_ids:
            if visible_event_claim_id not in declared_event_claim_ids:
                errors.append(
                    f"{label}: Gesicherter Ereigniskern includes non-event claim {visible_event_claim_id}"
                )

        for claim in mapping_list(meta.get("claims")):
            claim_id = claim.get("id")
            claim_text = claim.get("text")
            classification = claim.get("classification")
            evidence_level = claim.get("evidence_level")

            claim_id_visible = False
            claim_wording_visible = False
            if isinstance(claim_id, str):
                claim_id_pattern = re.compile(
                    rf"(?<![\w-]){re.escape(claim_id)}(?![\w-])"
                )
                claim_id_visible = claim_id_pattern.search(visible_body) is not None
                if not claim_id_visible:
                    errors.append(
                        f"{label}: claim {claim_id} must be visibly represented by ID in case body"
                    )
            if isinstance(claim_id, str) and isinstance(claim_text, str):
                claim_lexical = lexical_text(claim_text)
                if not claim_lexical:
                    errors.append(
                        f"{label}: claim {claim_id} text must contain lexical tokens"
                    )
                else:
                    claim_wording_visible = contains_lexical_sequence(
                        body_lexical, claim_lexical
                    )
                    if not claim_wording_visible:
                        errors.append(
                            f"{label}: claim {claim_id} wording must be visibly represented in case body"
                        )
                if (
                    claim_id_visible
                    and claim_wording_visible
                    and not claim_occurrences_bound_to_wording(
                        claim_binding_body, claim_id, claim_text
                    )
                ):
                    errors.append(
                        f"{label}: claim {claim_id} must bind each visible ID occurrence to its own wording"
                    )
            claim_sources = string_list(claim.get("sources"))
            rich_support_sources = evidence_sources(claim.get("evidence"))
            counter_sources = evidence_sources(claim.get("counterevidence"))

            if set(claim_sources) != set(rich_support_sources):
                errors.append(
                    f"{label}: claim {claim_id} sources must exactly match evidence source IDs"
                )

            source_optional = (
                isinstance(classification, str)
                and classification in {"open_question", "hypothesis"}
                and evidence_level == "speculative"
            )
            if not source_optional and not claim_sources:
                errors.append(f"{label}: claim {claim_id} requires at least one source")

            all_claim_source_ids = list(
                dict.fromkeys([*claim_sources, *rich_support_sources, *counter_sources])
            )
            for source_id in all_claim_source_ids:
                if source_id not in source_ids:
                    errors.append(
                        f"{label}: claim {claim_id} references unknown source {source_id}"
                    )
                if source_id not in case_sources:
                    errors.append(
                        f"{label}: claim source {source_id} must also appear in case.sources "
                        f"(claim {claim_id})"
                    )

            non_lead_required = (
                isinstance(classification, str)
                and (
                    classification in {"fact", "counterevidence", "interpretation"}
                    or (
                        classification in {"hypothesis", "open_question"}
                        and isinstance(evidence_level, str)
                        and evidence_level
                        in {"established", "strong", "plausible", "contradicted"}
                    )
                )
            )
            support_directness = {
                record.get("directness")
                for record in mapping_list(claim.get("evidence"))
                if isinstance(record.get("directness"), str)
            }
            if (
                evidence_level == "strong"
                and claim_sources
                and not support_directness.intersection({"direct", "indirect"})
            ):
                errors.append(
                    f"{label}: claim {claim_id} with strong evidence requires "
                    "at least one direct or indirect support record"
                )

            if (
                evidence_level == "established"
                and claim_sources
                and all(source_id in source_by_id for source_id in claim_sources)
                and not established_claim_supports(claim.get("evidence"), source_by_id)
            ):
                errors.append(
                    f"{label}: claim {claim_id} with established evidence requires "
                    "a Tier-A primary source marked direct or at least two Tier-B/C "
                    "sources from different institutions using direct/indirect evidence"
                )
            elif (
                non_lead_required
                and claim_sources
                and all(source_id in source_tiers for source_id in claim_sources)
                and not any(
                    source_tiers[source_id] in {"A", "B", "C", "D"}
                    for source_id in claim_sources
                )
            ):
                errors.append(
                    f"{label}: claim {claim_id} may not rely solely on Tier-E leads"
                )

    node_ids = entity_ids | case_ids
    for relation in relations:
        relation_id = relation.get("id", "<unknown-relation>")
        from_id = relation.get("from")
        to_id = relation.get("to")
        if isinstance(from_id, str) and from_id not in node_ids:
            errors.append(f"{relation_id}: unknown from-node {from_id}")
        if isinstance(to_id, str) and to_id not in node_ids:
            errors.append(f"{relation_id}: unknown to-node {to_id}")
        relation_claim_ids = string_list(relation.get("claim_ids"))
        for claim_id in relation_claim_ids:
            if claim_id not in claim_ids:
                errors.append(f"{relation_id}: unknown claim {claim_id}")
        if from_id in case_ids and to_id in case_ids:
            if not relation_claim_ids:
                errors.append(
                    f"{relation_id}: case-to-case relation requires at least one claim_id"
                )
            for claim_id in relation_claim_ids:
                claim_case = claim_case_by_id.get(claim_id)
                if claim_case is not None and claim_case not in {from_id, to_id}:
                    errors.append(
                        f"{relation_id}: claim {claim_id} belongs to unrelated case {claim_case}"
                    )
        relation_sources = string_list(relation.get("sources"))
        for source_id in relation_sources:
            if source_id not in source_ids:
                errors.append(f"{relation_id}: unknown source {source_id}")
        relation_evidence = relation.get("evidence_level")
        if (
            relation_evidence == "established"
            and relation_sources
            and all(source_id in source_by_id for source_id in relation_sources)
            and not established_supports(relation_sources, source_by_id)
        ):
            errors.append(
                f"{relation_id}: established relation evidence requires a Tier-A "
                "primary source or at least two Tier-B/C sources from different institutions"
            )
        elif (
            relation_sources
            and all(source_id in source_tiers for source_id in relation_sources)
            and not any(
                source_tiers[source_id] in {"A", "B", "C", "D"}
                for source_id in relation_sources
            )
        ):
            errors.append(f"{relation_id}: relation may not rely solely on Tier-E leads")

    organization_dir = DOCS / "organisationen"
    organization_profile_ids: set[str] = set()
    if organization_dir.exists():
        for path in sorted(organization_dir.rglob("*.md")):
            if path == organization_dir / "index.md":
                continue
            label = str(path.relative_to(ROOT))
            try:
                meta = frontmatter(path)
            except Exception as exc:
                errors.append(f"{label}: {exc}")
                continue
            errors.extend(schema_errors(meta, "organization.schema.json", label))
            entity_id = meta.get("id")
            if isinstance(entity_id, str):
                if entity_id in organization_profile_ids:
                    errors.append(f"organization profiles: duplicate id {entity_id}")
                organization_profile_ids.add(entity_id)
                if entity_id not in entity_ids:
                    errors.append(f"{label}: unknown organization entity {entity_id}")
            organization_sources = string_list(meta.get("sources"))
            for source_id in organization_sources:
                if source_id not in source_ids:
                    errors.append(f"{label}: unknown source {source_id}")
            errors.extend(
                direct_source_link_errors(
                    path, organization_sources, source_by_id, label
                )
            )
            organization_evidence = meta.get("evidence_level")
            if (
                organization_evidence == "established"
                and organization_sources
                and all(source_id in source_by_id for source_id in organization_sources)
                and not established_supports(organization_sources, source_by_id)
            ):
                errors.append(
                    f"{label}: established organization evidence requires a Tier-A "
                    "primary source or at least two Tier-B/C sources from different institutions"
                )
            elif (
                isinstance(organization_evidence, str)
                and organization_evidence in {"strong", "plausible", "contradicted"}
                and organization_sources
                and all(source_id in source_tiers for source_id in organization_sources)
                and not any(
                    source_tiers[source_id] in {"A", "B", "C", "D"}
                    for source_id in organization_sources
                )
            ):
                errors.append(
                    f"{label}: non-speculative organization evidence may not rely solely on Tier-E leads"
                )

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "VALIDATION OK: "
        f"{len(case_ids)} cases, {len(claim_ids)} claims, "
        f"{len(source_ids)} sources, {len(entity_ids)} entities, "
        f"{len(mechanism_ids)} mechanisms, {len(relations)} relations"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())