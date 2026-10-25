"""Boy-scout contracts for critical shared surfaces.

SPEC-01 lazyown.py carries no unused imports. Dead imports accumulate
because commands migrate to cli/commands while the import block stays.
SPEC-02 the MCP playbook executor shell-quotes the substituted target so a
value such as 8.8.8.8;id cannot break out of the step command.
SPEC-03 utils.replace_placeholders matches replace_command_placeholders on
single-brace templates and leaves brace-containing values literal instead
of re-substituting them.
SPEC-04 DEPLOY.sh carries no dangling TODO markers.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "skills"))


def _bound_import_names(tree: ast.Module) -> list[str]:
    """Collect every top-level name bound by an import statement."""
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                names.append(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.asname or alias.name.split(".")[0])
    return names


def test_lazyown_has_no_unused_imports() -> None:
    """SPEC-01: every name bound by an import in lazyown.py is referenced."""
    source = (_ROOT / "lazyown.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    dead = [
        name for name in _bound_import_names(tree) if len(re.findall(r"\b{}\b".format(re.escape(name)), source)) == 1
    ]
    assert not dead, f"unused imports in lazyown.py: {sorted(set(dead))}"


def _load_mcp_module():
    """Import skills.lazyown_mcp with SDK stubs when the pinned SDK is stale."""
    try:
        import lazyown_mcp

        return lazyown_mcp
    except (ImportError, AttributeError):
        import types as std_types

        mcp = std_types.ModuleType("mcp")
        server_mod = std_types.ModuleType("mcp.server")
        stdio_mod = std_types.ModuleType("mcp.server.stdio")
        types_mod = std_types.ModuleType("mcp.types")

        class Tool:
            """Minimal Tool stand-in."""

            def __init__(self, **kwargs):
                """Store every keyword as an attribute."""
                self.__dict__.update(kwargs)

        class TextContent:
            """Minimal TextContent stand-in."""

            def __init__(self, **kwargs):
                """Store every keyword as an attribute."""
                self.__dict__.update(kwargs)

        types_mod.Tool = Tool
        types_mod.TextContent = TextContent

        class Server:
            """Minimal Server stand-in."""

            def __init__(self, *args, **kwargs):
                """Accept and ignore constructor arguments."""

            def list_tools(self):
                """Return an identity decorator."""
                return lambda func: func

            def call_tool(self):
                """Return an identity decorator."""
                return lambda func: func

        server_mod.Server = Server
        stdio_mod.stdio_server = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("stub stdio server"))
        mcp.types = types_mod
        mcp.server = server_mod
        sys.modules["mcp"] = mcp
        sys.modules["mcp.types"] = types_mod
        sys.modules["mcp.server"] = server_mod
        sys.modules["mcp.server.stdio"] = stdio_mod
        import lazyown_mcp

        return lazyown_mcp


def test_playbook_target_is_shell_quoted() -> None:
    """SPEC-02: substituted target cannot break out of the step command."""
    mcp = _load_mcp_module()
    out = mcp.substitute_playbook_target("ping -c1 {target}", "8.8.8.8;id")
    assert out == "ping -c1 '8.8.8.8;id'"
    plain = mcp.substitute_playbook_target("ping -c1 {target}", "10.0.0.1")
    assert plain == "ping -c1 10.0.0.1"


def test_replace_placeholders_matches_single_pass_engine() -> None:
    """SPEC-03: legacy helper agrees with the canonical engine on sane input."""
    from utils import replace_command_placeholders, replace_placeholders

    cases = [
        ("nmap {rhost} -p {rport}", {"rhost": "10.0.0.5", "rport": "445"}),
        ("echo { missing }", {"missing": "x"}),
        ("no tokens here", {"rhost": "10.0.0.5"}),
        ("keep {unknown} intact", {"rhost": "10.0.0.5"}),
    ]
    for template, values in cases:
        assert replace_placeholders(template, values) == replace_command_placeholders(template, values)


def test_replace_placeholders_keeps_brace_values_literal() -> None:
    """SPEC-03: a value that looks like a placeholder is not re-substituted."""
    from utils import replace_placeholders

    out = replace_placeholders("pass={password}", {"password": "{lhost}", "lhost": "x"})
    assert out == "pass={lhost}"


def test_deploy_has_no_todo_markers() -> None:
    """SPEC-04: release script carries no dangling work markers."""
    text = (_ROOT / "DEPLOY.sh").read_text(encoding="utf-8")
    hits = re.findall(r"\b(TODO|FIXME|HACK|XXX)\b", text)
    assert not hits, f"dangling markers in DEPLOY.sh: {hits}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
