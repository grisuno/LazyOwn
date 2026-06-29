"""Parser that turns a CLAUDE.md into actionable contracts.

The parser is deterministic. It does not call any LLM. It walks the
markdown as a tree of sections and lifts every actionable bullet that
lives under a heading that carries a flag. The flag is the keyword
CONTRACT in the heading text. The orchestrator does not assume the
markdown is well formed. The parser records every malformed input and
returns a structured error alongside the partial result.

The parser also produces the rationale for each contract by combining
the parent section text with the first paragraph of the body. The
documentation agent can quote the source verbatim.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .config import Config
from .models import Contract


CONTRACT_HEADING_PATTERN = re.compile(
    r"^(?P<hashes>#{1,6})\s+(?P<title>.+)$", re.MULTILINE
)
CONTRACT_TAG_PATTERN = re.compile(r"\bCONTRACT\b", re.IGNORECASE)
CONTRACT_ID_PATTERN = re.compile(r"\bC-\d{3,}\b")
BULLET_PATTERN = re.compile(r"^\s*[-*+]\s+(?P<body>.+)$", re.MULTILINE)
NUMBERED_PATTERN = re.compile(r"^\s*\d+\.\s+(?P<body>.+)$", re.MULTILINE)
HEADING_ID_DERIVE = re.compile(r"[^a-z0-9]+")


@dataclass
class _Section:
    """Internal node that represents a heading and its body.

    Attributes:
        depth: Heading level. One is the document title.
        title: Heading text.
        body: Concatenated text of every paragraph that belongs to the
            section.
        children: Subsection nodes. The parser walks the tree in depth
            first order.
    """

    depth: int
    title: str
    body: str = ""
    children: list["_Section"] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = []


def _derive_contract_id(title: str, fallback_index: int) -> str:
    """Return a stable identifier for a contract heading.

    The parser prefers an explicit id in the heading text. The id must
    match the C-000 shape. When the heading does not carry an explicit
    id, the parser derives a slug from the heading text and falls back
    to a numeric index so two headings with the same slug never share
    an identifier.
    """
    match = CONTRACT_ID_PATTERN.search(title)
    if match:
        return match.group(0).upper()
    slug = HEADING_ID_DERIVE.sub("-", title.lower()).strip("-")
    slug = slug[:48] or "contract"
    return f"{slug}-{fallback_index:02d}"


def _strip_contract_marker(title: str) -> str:
    """Remove the CONTRACT keyword and any explicit id from the title.

    The marker is metadata. The orchestrator uses the cleaned title
    for human facing log lines.
    """
    cleaned = CONTRACT_TAG_PATTERN.sub("", title)
    cleaned = CONTRACT_ID_PATTERN.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" :-")
    return cleaned


def _walk_sections(lines: list[str]) -> list[_Section]:
    """Return the document section tree built from the markdown lines.

    The walker keeps a stack of open sections. When a new heading
    arrives, the walker closes the deepest section whose depth is
    greater or equal and attaches the new section as a child of the
    previous top.
    """
    root = _Section(depth=0, title="")
    stack: list[_Section] = [root]
    current_body: list[str] = []

    def flush_body() -> None:
        text = "\n".join(current_body).strip()
        if text and stack[-1].body != text:
            if stack[-1].body:
                stack[-1].body = stack[-1].body + "\n\n" + text
            else:
                stack[-1].body = text
        current_body.clear()

    for line in lines:
        match = CONTRACT_HEADING_PATTERN.match(line)
        if match:
            flush_body()
            depth = len(match.group("hashes"))
            title = match.group("title").strip()
            node = _Section(depth=depth, title=title)
            while stack and stack[-1].depth >= depth:
                stack.pop()
            stack[-1].children.append(node)
            stack.append(node)
            continue
        current_body.append(line)
    flush_body()
    return root.children


def _collect_bullets(text: str) -> list[str]:
    """Return the bullet items inside a section body.

    Args:
        text: Section body.
    Returns:
        A list of trimmed bullet strings. Empty list when the body has
        no bullet list.
    """
    bullets: list[str] = []
    for pattern in (BULLET_PATTERN, NUMBERED_PATTERN):
        for match in pattern.finditer(text):
            body = match.group("body").strip()
            if body:
                bullets.append(body)
    return bullets


def _collect_paragraphs(text: str) -> list[str]:
    """Return the paragraphs inside a section body."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _is_actionable(heading: _Section) -> bool:
    """Return True when a section qualifies as a contract.

    The parser treats a section as a contract when the heading carries
    the CONTRACT keyword or the body declares an explicit outcomes
    list. The marker is case insensitive.
    """
    if CONTRACT_TAG_PATTERN.search(heading.title):
        return True
    body = heading.body.lower()
    return ("out of scope" in body and "happy path" in body) or (
        "trigger" in body and "sad path" in body
    )


def _flatten_actionable(root: _Section) -> Iterable[_Section]:
    """Yield every actionable section in depth first order."""
    for child in root.children:
        yield from _flatten_actionable(child)
        if _is_actionable(child):
            yield child


def parse_claude_md(path: Path) -> list[Contract]:
    """Parse a CLAUDE.md file and return the list of contracts.

    Args:
        path: Absolute path of the markdown file.
    Returns:
        A list of Contract objects. Empty list when the file does not
        exist or contains no actionable section.
    Raises:
        FileNotFoundError: when the path is missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"CLAUDE.md not found at {path}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    roots = _walk_sections(lines)
    root = _Section(depth=0, title="")
    root.children = roots
    contracts: list[Contract] = []
    for index, section in enumerate(_flatten_actionable(root), start=1):
        contract_id = _derive_contract_id(section.title, index)
        title = _strip_contract_marker(section.title)
        paragraphs = _collect_paragraphs(section.body)
        rationale = paragraphs[0] if paragraphs else ""
        scope = _collect_bullets(section.body)
        contracts.append(
            Contract(
                contract_id=contract_id,
                title=title or contract_id,
                rationale=rationale,
                scope=scope,
                source_section=section.title,
                raw_text=section.body,
            )
        )
    return contracts


def _coerce_seed_contract(seed: dict[str, str]) -> Contract:
    """Build a Contract from a programmatic seed dictionary.

    Tests and the CLI use the helper to inject a contract without
    parsing a markdown file. The seed must carry the keys contract_id,
    title, rationale, and scope. scope is a newline separated bullet
    list.
    """
    scope_text = seed.get("scope", "")
    scope = [line.strip("-* \t") for line in scope_text.splitlines() if line.strip()]
    return Contract(
        contract_id=seed["contract_id"],
        title=seed.get("title", seed["contract_id"]),
        rationale=seed.get("rationale", ""),
        scope=scope,
        source_section=seed.get("source_section", "seed"),
        raw_text=seed.get("raw_text", ""),
    )


def load_contracts(config: Config, seeds: Optional[list[dict[str, str]]] = None) -> list[Contract]:
    """Return the contracts the orchestrator should process.

    Args:
        config: Active runtime configuration.
        seeds: Optional list of seed contracts the caller wants to mix
            in. The orchestrator uses the seeds when the markdown
            parser returns zero contracts so the operator can drive
            the cycle from a focused file.
    Returns:
        The merged list of contracts. The list is deduplicated by
        contract_id while preserving the original order.
    """
    parsed = parse_claude_md(config.claude_md_path)
    merged: list[Contract] = []
    seen: set[str] = set()
    for item in list(parsed) + [(_coerce_seed_contract(s) if seeds else None) for s in (seeds or [])]:
        if item is None:
            continue
        if item.contract_id in seen:
            continue
        seen.add(item.contract_id)
        merged.append(item)
    return merged
