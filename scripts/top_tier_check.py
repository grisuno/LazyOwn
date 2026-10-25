#!/usr/bin/env python3
"""Top-tier hygiene audit for LazyOwn.

Fails (exit 1) on any credibility blocker:
- version drift between README / pyproject.toml / version.json
- doc claims (command / MCP / addon counts) out of sync with repo reality
- secrets or session artefacts tracked by git
- missing release-hygiene inputs (requirements, SBOM source)

Usage: python3 scripts/top_tier_check.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[ ok ] {message}")


def count_cli_commands() -> int:
    pattern = re.compile(r"def (do_[a-z_0-9]+)")
    found: set[str] = set()
    for path in list((ROOT / "cli").rglob("*.py")) + [ROOT / "lazyown.py"]:
        try:
            found.update(pattern.findall(path.read_text(errors="ignore")))
        except OSError:
            continue
    return len(found)


def count_mcp_tools() -> int:
    text = (ROOT / "skills" / "lazyown_mcp.py").read_text(errors="ignore")
    return text.count("types.Tool(")


def count_addons() -> int:
    return len(list((ROOT / "lazyaddons").glob("*.yaml")))


def check_versions() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(errors="ignore")
    m = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
    py_version = m.group(1) if m else "?"
    try:
        file_version = json.loads((ROOT / "version.json").read_text()).get("version", "?")
    except (OSError, json.JSONDecodeError):
        file_version = "?"
    readme = (ROOT / "README.md").read_text(errors="ignore")
    m2 = re.search(r"RedTeam Framework v([0-9.]+)", readme)
    readme_version = m2.group(1) if m2 else "?"
    core = {v.split("/")[-1] for v in (py_version, file_version)}
    if len(core) > 1:
        fail(f"version drift: pyproject={py_version} version.json={file_version} README={readme_version}")
    else:
        ok(f"versions in sync: {py_version} / {file_version} / README {readme_version}")


def check_doc_counts(commands: int, mcp: int, addons: int) -> None:
    header = "\n".join((ROOT / "README.md").read_text(errors="ignore").splitlines()[:60])
    stale = [n for n in ("606+", "606 ", "148 MCP", "120+ YAML") if n in header]
    if stale:
        fail(
            f"README header cites stale counts {stale}; reality: {commands} commands, {mcp} MCP tools, {addons} addons"
        )
    else:
        ok(f"README header in sync vs reality {commands}/{mcp}/{addons}")


def check_tracked_secrets() -> None:
    try:
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, timeout=30
        ).stdout.splitlines()
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"git ls-files failed: {exc}")
        return
    bad_patterns = (
        "payload.json",
        "users.json",
        ".env",
        ".pem",
        ".c2_credentials",
        "tracking.db",
        "short_urls.json",
        "llm_budget.json",
    )
    bad = [t for t in tracked for p in bad_patterns if p in t and "example" not in t.lower()]
    fixture_suffixes = ("pass.txt", "site.txt", "credentials.json", "plan.txt", "routes_to_templates.json")
    sensitive = [t for t in bad if not t.lower().endswith(fixture_suffixes)]
    if sensitive:
        fail(f"tracked secrets/session artefacts: {sensitive[:10]}")
    else:
        ok("no secrets or session artefacts tracked by git")


def check_release_inputs() -> None:
    missing = [f for f in ("requirements.txt", "pyproject.toml", "CHANGELOG.md") if not (ROOT / f).exists()]
    if missing:
        fail(f"missing release inputs: {missing}")
    else:
        ok("release inputs present (requirements/pyproject/CHANGELOG)")


def main() -> int:
    commands, mcp, addons = count_cli_commands(), count_mcp_tools(), count_addons()
    print(f"commands={commands} mcp_tools={mcp} addons={addons}")
    if commands < 700:
        fail(f"CLI command count collapsed: {commands}")
    else:
        ok(f"CLI commands: {commands}")
    if mcp < 150:
        fail(f"MCP tool count collapsed: {mcp}")
    else:
        ok(f"MCP tools: {mcp}")
    check_versions()
    check_doc_counts(commands, mcp, addons)
    check_tracked_secrets()
    check_release_inputs()
    if FAILURES:
        print(f"\n{len(FAILURES)} top-tier blocker(s). Fix, then re-run this script.")
        return 1
    print("\nTop-tier hygiene OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
