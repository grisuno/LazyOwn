"""Generic pass-through arguments for lazyaddons: ``--argN`` to ``{argN}``.

Contract: one module renders every ``execute_command`` template across
the CLI, the TUI plugin loader and the C2 surface. Runtime arguments
(``--arg1 value`` on the invocation line) map to ``{argN}`` placeholders
without declaring anything in the addon YAML. Resolution order is CLI
args, then the optional ``args`` defaults block in the YAML, then the
context mapping (payload keys). A token holding an unresolved ``{argN}``
is dropped entirely (never rendered empty, so no dangling flags);
classic ``{key}``/``{{key}}`` placeholders that cannot resolve stay
untouched so existing templates keep their exact behavior. Values
reaching the ``argN`` namespace are ``shlex.quote``-ed (one argument is
one shell word); classic placeholders keep the historical raw
substitution because existing templates pre-quote them.
"""

from __future__ import annotations

import re
import shlex
from collections.abc import Mapping

_NAME_RE = re.compile(r"^[a-z_][a-z0-9_]{0,31}$")
_DOUBLE_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-z_][a-z0-9_]*)\s*\}\}")
_PLACEHOLDER_RE = re.compile(r"\{\s*([a-z_][a-z0-9_]*)\s*\}")
_ARG_CANONICALISE_RE = re.compile(r"\{\{\s*(arg\d+)\s*\}\}|\{\s*(arg\d+)\s*\}")
_ARG_NAME_RE = re.compile(r"^arg\d+$")
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")
_WHITESPACE_RE = re.compile(r"\s{2,}")

_MISSING = object()

__all__ = [
    "ARG_NAME_RE",
    "extract_cli_args",
    "is_arg_name",
    "render_command",
]


def is_arg_name(name: str) -> bool:
    """Return whether *name* belongs to the runtime ``argN`` namespace.

    Args:
        name: Placeholder identifier.

    Returns:
        True for ``arg1``-style names.
    """
    return bool(_ARG_NAME_RE.fullmatch(name))


ARG_NAME_RE = _ARG_NAME_RE


def extract_cli_args(tokens: list[str]) -> tuple[list[str], dict[str, str]]:
    """Split ``--name value`` / ``--name=value`` pairs out of *tokens*.

    Last occurrence wins. ``--`` stops extraction and the remaining
    tokens pass through untouched. Tokens that do not look like a
    generic flag are returned in the rest list unchanged.

    Args:
        tokens: Invocation tokens (already shell-split).

    Returns:
        Tuple of (remaining tokens, extracted name to value mapping).
    """
    rest: list[str] = []
    args: dict[str, str] = {}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            rest.extend(tokens[index:])
            break
        if token.startswith("--"):
            body = token[2:]
            if "=" in body:
                name, value = body.split("=", 1)
                if _NAME_RE.fullmatch(name):
                    args[name] = value
                    index += 1
                    continue
            elif _NAME_RE.fullmatch(body):
                value = ""
                if index + 1 < len(tokens) and not tokens[index + 1].startswith("--"):
                    value = tokens[index + 1]
                    index += 1
                args[body] = value
                index += 1
                continue
        rest.append(token)
        index += 1
    return rest, args


def render_command(
    template: str,
    ctx: Mapping[str, object],
    cli_args: Mapping[str, str] | None = None,
    defaults: Mapping[str, str] | None = None,
) -> str:
    """Render one addon command template.

    Resolution order: CLI args, then the YAML ``args`` defaults block,
    then the context mapping. Tokens holding an unresolved ``{argN}``
    are dropped entirely (never rendered empty, so no dangling flags).
    Classic ``{key}`` / ``{{key}}`` placeholders that cannot resolve
    stay verbatim; classic substitutions are raw (existing templates
    pre-quote them), runtime ``argN`` values are ``shlex.quote``-ed.

    Args:
        template: Command template with placeholders.
        ctx: Context mapping (payload keys, declared params).
        cli_args: Runtime ``--argN`` mapping; highest precedence.
        defaults: Optional YAML ``args`` defaults block.

    Returns:
        The rendered command line.

    Raises:
        ValueError: If a supplied argument value contains control
            characters.
    """
    supplied = {**dict(defaults or {}), **dict(cli_args or {})}
    for key, value in supplied.items():
        if _CONTROL_CHARS_RE.search(str(value)):
            raise ValueError(f"argument '{key}': control characters not allowed")

    def _resolve(name: str) -> object:
        value = supplied.get(name)
        if value is not None:
            return value
        return ctx.get(name, _MISSING)

    def _sub_double(match: re.Match) -> str:
        name = match.group(1)
        value = _resolve(name)
        return match.group(0) if value is _MISSING else str(value)

    def _sub_single(match: re.Match) -> str:
        name = match.group(1)
        value = _resolve(name)
        if value is _MISSING:
            return match.group(0)
        if is_arg_name(name) and name in supplied:
            return shlex.quote(str(value))
        return str(value)

    def _drop_unresolved(tokens: list[str]) -> list[bool]:
        """Mark which tokens survive the unresolved-``{argN}`` token-drop.

        A token holding an unresolved runtime argument is dropped along
        with the pure flag token directly preceding it (``-w {arg1}``
        disappears as a unit); the cascade never crosses another
        placeholder token.

        Args:
            tokens: Canonical template tokens.

        Returns:
            Keep-mask aligned with *tokens*.
        """
        keep = [True] * len(tokens)
        for index, token in enumerate(tokens):
            names = set(_PLACEHOLDER_RE.findall(token))
            if not any(is_arg_name(name) and _resolve(name) is _MISSING for name in names):
                continue
            keep[index] = False
            previous = index - 1
            if (
                previous >= 0
                and keep[previous]
                and tokens[previous].startswith("-")
                and not _PLACEHOLDER_RE.search(tokens[previous])
            ):
                keep[previous] = False
        return keep

    tokens = _ARG_CANONICALISE_RE.sub(
        lambda m: "{" + (m.group(1) or m.group(2)) + "}", template
    ).split()
    keep = _drop_unresolved(tokens)
    dropped = " ".join(token for index, token in enumerate(tokens) if keep[index])
    rendered = _DOUBLE_PLACEHOLDER_RE.sub(_sub_double, dropped)
    rendered = _PLACEHOLDER_RE.sub(_sub_single, rendered)
    return _WHITESPACE_RE.sub(" ", rendered).strip()
