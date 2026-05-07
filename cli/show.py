"""Pretty-print the live payload for the operator.

Tier 2.5 replaces ``do_show``'s unordered, unaligned dump with a stable,
deterministic rendering. Output is plain text (no ANSI) so the formatter is
easy to test and reusable for logs, reports or the dashboard.
"""

from __future__ import annotations

from typing import Any, Iterable


def format_payload(
    params: dict[str, Any],
    *,
    keys: Iterable[str] | None = None,
) -> str:
    """Render ``params`` as a sorted, aligned ``key = value`` block.

    Args:
        params: Payload dict.
        keys: Optional whitelist; when given, only those keys are rendered
            (in the same alphabetical order). Missing keys render as empty
            strings, matching the alias loader's behaviour.

    Returns:
        A multi-line string. Each line is ``"<key padded>  <value>"``. The
        column width is computed from the rendered key set so output stays
        aligned regardless of which keys are present.
    """
    if keys is None:
        selected = dict(params)
    else:
        selected = {k: params.get(k) for k in keys}
    if not selected:
        return ""
    width = max(len(str(k)) for k in selected)
    lines = []
    for key in sorted(selected, key=str):
        value = selected[key]
        rendered = "" if value is None else str(value)
        lines.append(f"{str(key).ljust(width)}  {rendered}")
    return "\n".join(lines)


__all__ = ["format_payload"]
