"""MITRE ATT&CK <-> Atomic Red Team translator contract."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.atomic_resolver import (  # noqa: E402
    AtomicResolver,
    build_variables,
    is_guid,
    is_mitre_id,
    normalize_guid,
    normalize_mitre_id,
    normalize_platform,
    render_command,
)

_GUID_A = "f3132740-55bc-48c4-bcc0-758a459cd027"
_GUID_B = "a21bb23e-0000-4000-8000-000000000001"


def _write_fixture_atomics(root: Path) -> Path:
    """Create a minimal synthetic atomics tree (no network, no real repo)."""
    atomics = root / "atomics"
    (atomics / "T1059.001").mkdir(parents=True)
    (atomics / "T1059.001" / "T1059.001.yaml").write_text(
        yaml.dump(
            {
                "attack_technique": "T1059.001",
                "atomic_tests": [
                    {
                        "auto_generated_guid": _GUID_A,
                        "name": "Mimikatz",
                        "description": "Dump creds",
                        "supported_platforms": ["windows"],
                        "executor": {"name": "powershell", "command": "mimikatz #{password}"},
                        "dependencies": [{"prereq_command": "whoami", "get_prereq_command": ""}],
                        "input_arguments": {"password": {"default": "secret"}},
                    },
                    {
                        "auto_generated_guid": _GUID_B,
                        "name": "Linux exec",
                        "description": "Run cmd",
                        "supported_platforms": ["linux"],
                        "executor": {"name": "sh", "command": "id #{username}"},
                        "input_arguments": {},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return atomics


def test_normalize_mitre_accepts_variants() -> None:
    """Lowercase and padded IDs normalize to canonical form."""
    assert normalize_mitre_id("t1078") == "T1078"
    assert normalize_mitre_id("  T1059.001 ") == "T1059.001"
    assert is_mitre_id("T1003")


def test_normalize_mitre_rejects_injection() -> None:
    """Shell metachars and malformed IDs are rejected."""
    for bad in ["", "X123", "T10", "T1078; rm -rf /", "T1078|evil", "T1078\nT1003", "../../etc"]:
        assert not is_mitre_id(bad)
        with pytest.raises(ValueError):
            normalize_mitre_id(bad)


def test_guid_validation_roundtrip() -> None:
    """Valid UUIDs pass; truncated or hostile strings fail."""
    assert normalize_guid(_GUID_A.upper()) == _GUID_A
    assert is_guid(_GUID_B)
    for bad in ["", "not-a-guid", _GUID_A[:-1], _GUID_A + ";evil"]:
        assert not is_guid(bad)


def test_platform_allowlist() -> None:
    """Only known platforms pass; unknown values raise."""
    assert normalize_platform("Linux") == "linux"
    with pytest.raises(ValueError):
        normalize_platform("mainframe; rm -rf /")


def test_resolver_lists_and_filters(tmp_path: Path) -> None:
    """Fixture index resolves by technique, GUID, and platform."""
    resolver = AtomicResolver(_write_fixture_atomics(tmp_path))
    assert resolver.guids_for_technique("T1059.001") == [_GUID_A, _GUID_B]
    linux_only = resolver.list_for_technique("T1059.001", platform="linux")
    assert [t.guid for t in linux_only] == [_GUID_B]
    by_guid = resolver.get_by_guid(_GUID_A)
    assert by_guid is not None and by_guid.mitre_id == "T1059.001"
    assert by_guid.mitre_url == "https://attack.mitre.org/techniques/T1059/001"


def test_resolver_prefix_and_unknown(tmp_path: Path) -> None:
    """Prefix T1059 matches subtechniques; unknown IDs return empty."""
    resolver = AtomicResolver(_write_fixture_atomics(tmp_path))
    assert len(resolver.resolve("T1059")) == 2
    assert resolver.resolve("T9999") == []
    assert resolver.resolve("") == []
    assert resolver.resolve("not-an-id") == []


def test_chain_skips_invalid(tmp_path: Path) -> None:
    """One bad ID never aborts an autonomous emulation chain."""
    resolver = AtomicResolver(_write_fixture_atomics(tmp_path))
    chain = resolver.chain(["T1059.001", "T9999", "garbage"], platform="linux")
    assert [t.guid for t in chain] == [_GUID_B]


def test_variables_and_render() -> None:
    """Unknown inputs fall back to defaults; render never shells out."""
    from modules.atomic_resolver import AtomicTest

    test = AtomicTest(
        guid=_GUID_A,
        mitre_id="T1059.001",
        input_arguments={"password": {"default": "secret"}, "custom": {}},
    )
    variables = build_variables(test, rhost="10.0.0.5", username="op", password="pw")
    assert variables["#{ip_address}"] == "10.0.0.5"
    assert variables["#{password}"] == "pw"
    assert render_command("run #{password} #{custom}", variables) == "run pw "
