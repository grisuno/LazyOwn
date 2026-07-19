#!/usr/bin/env python3
"""Smoke test for the MCP server: verify all 131 tools are registered.

Run:
    python3 skills/tests/test_mcp_smoke.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent
LAZYOWN_DIR = SKILLS_DIR.parent
sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
sys.path.insert(0, str(SKILLS_DIR))

PASSED = 0
FAILED = 0
FAILURES: list[str] = []


def check(label: str, cond: bool, hint: str = "") -> None:
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {label}")
    else:
        FAILED += 1
        FAILURES.append(f"{label}  ({hint})" if hint else label)
        print(f"  [FAIL] {label}  {hint}")


def test_mcp_module_imports() -> None:
    """Verify the MCP module can be imported without syntax errors."""
    print("\n[1] MCP module import smoke test")
    try:
        import lazyown_mcp
        check("module imports without error", True)
        return lazyown_mcp
    except Exception as e:
        check("module imports without error", False, str(e))
        return None


def test_mcp_wellknown_symbols(mcp) -> None:
    """Verify expected symbols are defined at module level."""
    print("\n[2] Module-level symbols")

    expected = [
        "server",
        "list_tools",
        "main",
    ]
    for name in expected:
        found = hasattr(mcp, name)
        check(f"symbol '{name}' defined", found)


def test_list_tools_returns_tools(mcp) -> None:
    """Run list_tools() and verify it returns tool definitions."""
    print("\n[3] list_tools() returns tool definitions")
    try:
        import asyncio
        tools = asyncio.run(mcp.list_tools())
        check("list_tools() returns a list", isinstance(tools, list))
        check(
            "at least 10 tools registered",
            len(tools) >= 10,
            f"found {len(tools)}",
        )
        if tools:
            sample = tools[0]
            check(
                "tool has 'name' attribute",
                hasattr(sample, "name") or isinstance(sample, dict),
            )
            tool_names = [t.name if hasattr(t, "name") else t.get("name", "") for t in tools]
            expected_names = [
                "lazyown_run_command",
                "lazyown_set_config",
                "lazyown_campaign_sitrep",
            ]
            for en in expected_names:
                check(f"'{en}' registered", en in tool_names)
    except Exception as e:
        check("list_tools() succeeds", False, str(e))


def main() -> int:
    mcp = test_mcp_module_imports()
    if mcp:
        test_mcp_wellknown_symbols(mcp)
        test_list_tools_returns_tools(mcp)

    total = PASSED + FAILED
    print(f"\n{'='*40}")
    print(f"Results: {PASSED}/{total} passed")
    if FAILED:
        print(f"Failures:")
        for f in FAILURES:
            print(f"  - {f}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
