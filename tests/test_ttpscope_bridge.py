"""TTPScope bridge contract: validators, fallbacks, addon schema."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules import ttpscope_bridge as bridge  # noqa: E402


def test_object_id_validation() -> None:
    """ATT&CK IDs pass; hostile strings are rejected."""
    assert bridge.validate_object_id("t1059.001") == "T1059.001"
    assert bridge.validate_object_id("G0016") == "G0016"
    for bad in ["", "X1", "T10", "T1078;evil", "T1078|sleep", "$(id)", "../x"]:
        with pytest.raises(ValueError):
            bridge.validate_object_id(bad)


def test_query_and_platform_validation() -> None:
    """Queries are capped; platforms come from an allowlist."""
    assert bridge.validate_query("credential dumping") == "credential dumping"
    with pytest.raises(ValueError):
        bridge.validate_query("")
    with pytest.raises(ValueError):
        bridge.validate_query("x" * 201)
    assert bridge.validate_platform("windows") == "Windows"
    assert bridge.validate_platform("") == ""
    with pytest.raises(ValueError):
        bridge.validate_platform("mainframe")


def test_unknown_action_rejected() -> None:
    """Dispatch allowlist blocks unexpected actions."""
    with pytest.raises(ValueError):
        bridge.run_action("tui")
    with pytest.raises(ValueError):
        bridge.run_action("show; rm -rf /", object_id="T1003")


def test_search_fallback_needs_no_binary(monkeypatch: pytest.MonkeyPatch) -> None:
    """Search degrades to parquets when the binary is absent."""
    monkeypatch.setattr(bridge, "locate_binary", lambda: None)
    result = bridge.run_action("search", query="mimikatz")
    assert result["backend"] in ("fallback-stix", "fallback-parquet")
    assert Path(result["staged"]).exists()


def test_show_fallback_technique(monkeypatch: pytest.MonkeyPatch) -> None:
    """Show answers T* IDs from cache without the binary."""
    monkeypatch.setattr(bridge, "locate_binary", lambda: None)
    result = bridge.run_action("show", object_id="T1003")
    assert result["object_id"] == "T1003"
    assert "T1003" in result["output"]
    assert Path(result["staged"]).exists()


def test_matrix_fallback_groups(monkeypatch: pytest.MonkeyPatch) -> None:
    """Matrix renders from cache without the binary."""
    monkeypatch.setattr(bridge, "locate_binary", lambda: None)
    result = bridge.run_action("matrix", platform="Linux")
    assert result["platform"] == "Linux"
    assert "T1003" in result["output"]


def test_notes_roundtrip_without_binary(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Notes append/read work fully offline in the XDG layout."""
    monkeypatch.setattr(bridge, "locate_binary", lambda: None)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    written = bridge.run_action("note", object_id="T1053.005", text="coverage check")
    assert written["backend"] == "fallback-notes"
    read_back = bridge.run_action("notes", object_id="T1053.005")
    assert "coverage check" in read_back["output"]


def test_chain_needs_no_binary(monkeypatch: pytest.MonkeyPatch) -> None:
    """Chain joins Atomic tests + parquet context without the binary."""
    monkeypatch.setattr(bridge, "locate_binary", lambda: None)
    result = bridge.run_action("chain", object_id="T1003", platform="windows", limit=2)
    assert result["object_id"] == "T1003"
    assert len(result["atomic_tests"]) >= 1
    assert result["atomic_tests"][0]["guid"]
    assert Path(result["staged"]).exists()


def test_addon_schema_agent_friendly() -> None:
    """ttpscope.yaml meets the lazyaddons contract for agents and CLI."""
    addon = yaml.safe_load((_ROOT / "lazyaddons" / "ttpscope.yaml").read_text(encoding="utf-8"))
    assert addon["name"] == "ttpscope"
    assert addon["enabled"] is True
    assert addon["tool"]["repo_url"] == "https://github.com/bl4ckr0ss3/ttpscope.git"
    assert addon["tool"]["install_path"] == "external/.exploit/ttpscope"
    assert "ttpscope_bridge.py" in addon["tool"]["execute_command"]
    assert addon["category"] == "01. Reconnaissance"
    params = {p["name"] for p in addon["params"]}
    assert {"action", "query", "technique_id", "platform", "note_text", "limit"} <= params
    assert "chain" in addon["description"] and "atomic" in addon["description"].lower()
