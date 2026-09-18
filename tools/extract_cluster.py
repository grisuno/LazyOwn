#!/usr/bin/env python3
"""Extract a named cluster of do_* methods from a CommandSet module.

Usage:
    python3 tools/extract_cluster.py <source.py> <target.py> <TargetClass>
        <phase> <category> <title> [--extra-imports "line1;line2"] <do_a> [do_b ...]

Copies each method including decorators, verbatim, into a new module
defining a pending ``PendingCommandSet`` subclass. The emitted module
mirrors the ``*_migrated.py`` runtime contract: a bottom-of-file injector
copies public ``utils`` names into module globals (bare-name references
inside migrated methods resolve through it, since PEP 562
``__getattr__`` does not fire for function-global lookups), plus a
``__getattr__`` fallback for attribute-style access.

Follow the dormancy protocol after generating: verify with a parity
test, delete the originals from the source module, then flip the base
class to ``LazyOwnCommandSet``.
"""

from __future__ import annotations

import ast
import sys
import textwrap
from pathlib import Path


def fragment_name(fragment: str) -> str:
    """Return the function name defined by an extracted source fragment.

    Args:
        fragment: Raw source text of one decorated method.

    Returns:
        The ``def`` name declared by the fragment.
    """
    return ast.parse(textwrap.dedent(fragment)).body[0].name


def collect_methods(source_text: str, wanted: set[str]) -> list[str]:
    """Collect verbatim source of wanted methods in class-definition order.

    Args:
        source_text: Full source of the origin module.
        wanted: Method names to extract.

    Returns:
        Raw source fragments, decorators included.
    """
    src_lines = source_text.splitlines()
    tree = ast.parse(source_text)
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name in wanted:
                start = item.lineno - 1
                for dec in item.decorator_list:
                    start = min(start, dec.lineno - 1)
                found.append("\n".join(src_lines[start:item.end_lineno]))
    return found


def build_module(
    target_class: str,
    phase: str,
    category: str,
    title: str,
    methods: list[str],
    extra_imports: tuple[str, ...] = (),
) -> str:
    """Render the new pending CommandSet module source.

    Args:
        target_class: Name of the generated ``CommandSet`` subclass.
        phase: Kill-chain phase slug for the ``phase`` attribute.
        category: cmd2 help category label.
        title: Short human description used in the docstring.
        methods: Verbatim method fragments in final order.
        extra_imports: Additional import lines (for underscore-aliased
            names the ``utils`` injector cannot provide).

    Returns:
        Complete module source text.
    """
    extra_block = "\n".join(extra_imports)
    if extra_block:
        extra_block += "\n"
    header = f'''"""{title} extracted from the miscellaneous cluster.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from the source
module.
"""

from __future__ import annotations

import base64

import cmd2

from cli.commands._dormancy import PendingCommandSet as _PendingBase
{extra_block}
__all__ = ["{target_class}"]


class {target_class}(_PendingBase):
    """{title} (pending)."""

    phase = "{phase}"
    category = "{category}"
'''
    chunks = []
    for method in methods:
        dedented = textwrap.dedent(method)
        indented = "\n".join(
            "    " + line if line.strip() else "" for line in dedented.splitlines()
        )
        chunks.append(indented)
    footer = '''

import utils as _lazy_utils

for _lazy_name in dir(_lazy_utils):
    if not _lazy_name.startswith('_'):
        globals().setdefault(_lazy_name, getattr(_lazy_utils, _lazy_name))
del _lazy_utils, _lazy_name


def __getattr__(name: str):
    """Fall back to ``utils`` for bare-name references used by migrated commands."""
    import utils as _utils
    try:
        return getattr(_utils, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
'''
    return header + "\n" + "\n\n".join(chunks) + "\n" + footer


def main() -> int:
    """Extract the requested cluster and write the target module."""
    args = sys.argv[1:]
    extra_imports: tuple[str, ...] = ()
    if "--extra-imports" in args:
        flag = args.index("--extra-imports")
        extra_imports = tuple(args[flag + 1].split(";"))
        del args[flag : flag + 2]
    (source, target, target_class, phase, category, title, *methods) = args
    wanted = set(methods)
    found = collect_methods(Path(source).read_text(encoding="utf-8"), wanted)
    missing = wanted - {fragment_name(f) for f in found}
    if missing:
        print(f"ERROR missing methods: {sorted(missing)}")
        return 1
    order = {name: i for i, name in enumerate(methods)}
    found.sort(key=lambda f: order[fragment_name(f)])
    Path(target).write_text(
        build_module(target_class, phase, category, title, found, extra_imports),
        encoding="utf-8",
    )
    print(f"WROTE {len(found)} methods -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
