"""Viral adoption assets: GIFs, smoke script, drift CI, launch kit."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_demo_gifs_exist_and_nonempty():
    for name in (
        "golden-path.gif",
        "c2-collab.gif",
        "mcp-ai.gif",
        "c2-cli.gif",
        "issue-c2.gif",
        "first-steps.gif",
        "recon-loop.gif",
    ):
        p = REPO / "assets" / "demo" / name
        assert p.exists(), f"missing {p}"
        assert p.stat().st_size > 10_000, f"{p} too small"


def test_demo_gif_commands_exist_in_source():
    """Every command shown in a GIF must exist as do_* or addon."""
    import ast
    import glob as _glob

    commands = set()
    for path in _glob.glob(str(REPO / "cli" / "commands" / "*.py")):
        tree = ast.parse(open(path).read())
        commands.update(n.name[3:] for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("do_"))
    tree = ast.parse(open(REPO / "lazyown.py").read())
    commands.update(n.name[3:] for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("do_"))
    addons = {p.stem for p in (REPO / "lazyaddons").glob("*.yaml")}
    aliases = set()
    for alias_file in ("user_aliases.json",):
        alias_path = REPO / alias_file
        if alias_path.exists():
            import json as _json
            aliases.update(_json.loads(alias_path.read_text()).keys())
    known = commands | addons | aliases
    for shown in (
        "c2_quickstart", "c2_status", "c2_implant", "c2_beacons",
        "c2_beacon_cmd", "c2_keygen", "issue_command_to_c2", "download_c2",
        "doctor", "wizard", "assign", "scope", "ping", "lazynmap",
        "auto_populate", "facts_show", "recommend_next", "gobuster",
        "hunt", "engage", "auto_pwn", "blacksandbeacon", "collab_join",
        "campaign", "pentest_report",
    ):
        assert shown in known, f"GIF shows unknown command: {shown}"


def test_readme_links_viral_assets():
    text = (REPO / "README.md").read_text()
    assert "assets/demo/golden-path.gif" in text
    assert "ghcr.io/grisuno/lazyown" in text
    assert "COMPARISON.md" in text
    assert "ESSENTIALS.md" in text


def test_smoke_script_covers_onboarding():
    text = (REPO / "scripts" / "smoke_onboarding.sh").read_text()
    for needle in ("payload.example.json", "auto_populate", "htb-lame", "golden-path.gif"):
        assert needle in text


def test_docs_drift_workflow_exists():
    text = (REPO / ".github" / "workflows" / "docs-drift.yml").read_text()
    assert "build_command_index.py" in text
    assert "smoke_onboarding" in text


def test_marketplace_template_exists():
    p = REPO / ".github" / "ISSUE_TEMPLATE" / "marketplace_contribution.yml"
    assert p.exists()
    assert "yara_marketplace" in p.read_text()


def test_launch_kit_exists():
    p = REPO / "docs" / "launch_kit" / "POSTS.md"
    assert p.exists()
    text = p.read_text()
    assert "Show HN" in text
    assert "ghcr.io/grisuno/lazyown" in text
