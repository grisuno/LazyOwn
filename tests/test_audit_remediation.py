"""Audit-remediation contract tests (P0-P4).

Covers the HMAC default flip, rat_key bootstrap, beacon signature guard
wiring, noisy-pipeline flag gating, artifact identity cleanup and the
hygiene command/chain surfaces.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY_RAT_KEY = "82e672ae054aa4de6f042c888111686a"


def _spec_by_key(key: str):
    from core.payload_schema import SCHEMA

    spec = SCHEMA.get(key)
    assert spec is not None, f"spec {key} not found"
    return spec


def test_beacon_hmac_default_is_on():
    spec = _spec_by_key("c2_require_beacon_hmac")
    assert str(spec.default).lower() == "true"


def test_auto_pipeline_flags_default_off():
    assert str(_spec_by_key("auto_privesc_on_checkin").default).lower() == "false"
    assert str(_spec_by_key("auto_discover_on_checkin").default).lower() == "false"


def test_rat_key_spec_is_no_longer_published_secret():
    spec = _spec_by_key("rat_key")
    assert not spec.default


def _payload_loader(payload_path: Path):
    def _load(*_args, **_kwargs):
        return json.loads(payload_path.read_text())

    return _load


def _payload_writer(payload_path: Path):
    def _write(payload, *_args, **_kwargs):
        payload_path.write_text(json.dumps(payload))

    return _write


def test_ensure_rat_key_generates_and_persists(tmp_path, monkeypatch):
    import core.config as config_module

    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"rat_key": "CHANGE_ME"}))
    monkeypatch.setattr(config_module, "PAYLOAD_PATH", payload_path)
    monkeypatch.setattr(config_module, "load_payload", _payload_loader(payload_path))
    monkeypatch.setattr(config_module, "save_payload", _payload_writer(payload_path))
    key = config_module.ensure_rat_key()
    stored = json.loads(payload_path.read_text())["rat_key"]
    assert key == stored
    assert len(key) == 64 and key != LEGACY_RAT_KEY
    assert all(c in "0123456789abcdef" for c in key)


def test_ensure_rat_key_rotates_legacy_published_key(tmp_path, monkeypatch):
    import core.config as config_module

    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"rat_key": LEGACY_RAT_KEY}))
    monkeypatch.setattr(config_module, "PAYLOAD_PATH", payload_path)
    monkeypatch.setattr(config_module, "load_payload", _payload_loader(payload_path))
    monkeypatch.setattr(config_module, "save_payload", _payload_writer(payload_path))
    key = config_module.ensure_rat_key()
    assert key != LEGACY_RAT_KEY
    assert json.loads(payload_path.read_text())["rat_key"] == key


def test_ensure_rat_key_idempotent_for_fresh_key(tmp_path, monkeypatch):
    import core.config as config_module

    payload_path = tmp_path / "payload.json"
    fresh = "ab" * 32
    payload_path.write_text(json.dumps({"rat_key": fresh}))
    monkeypatch.setattr(config_module, "PAYLOAD_PATH", payload_path)
    monkeypatch.setattr(config_module, "load_payload", _payload_loader(payload_path))
    key = config_module.ensure_rat_key()
    assert key == fresh


def test_ensure_rat_key_mirrors_live_config(tmp_path, monkeypatch):
    import core.config as config_module

    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({}))
    monkeypatch.setattr(config_module, "PAYLOAD_PATH", payload_path)
    monkeypatch.setattr(config_module, "load_payload", _payload_loader(payload_path))
    monkeypatch.setattr(config_module, "save_payload", _payload_writer(payload_path))

    class _Live:
        pass

    live = _Live()
    key = config_module.ensure_rat_key(live)
    assert getattr(live, "rat_key") == key


def test_lazyown_set_config_persists_and_mirrors(tmp_path, monkeypatch):
    import utils

    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"rhost": "10.0.0.1"}))
    monkeypatch.setattr(utils, "PAYLOAD_PATH", payload_path)
    monkeypatch.setattr(utils, "load_payload", _payload_loader(payload_path))
    monkeypatch.setattr(utils, "save_payload", _payload_writer(payload_path))

    class _Live:
        pass

    live = _Live()
    utils.lazyown_set_config("test_key", "test_value", config_obj=live)
    assert json.loads(payload_path.read_text())["test_key"] == "test_value"
    assert getattr(live, "test_key") == "test_value"

    with pytest.raises(ValueError):
        utils.lazyown_set_config("", "x")


def test_c2_signature_guard_wired_into_routes():
    source = (REPO_ROOT / "lazyc2.py").read_text()
    assert "def _beacon_signature_guard(" in source
    assert source.count("_beacon_signature_guard()") >= 2
    assert "hashlib.sha256" in source
    assert "hmac.compare_digest" in source
    assert "auto_privesc_on_checkin" in source
    assert "auto_discover_on_checkin" in source


def test_c2_bootstraps_session_secrets_at_boot():
    source = (REPO_ROOT / "lazyc2.py").read_text()
    assert "ensure_session_secrets" in source
    assert "rotate_keys_on_boot" in source


def test_implant_signs_wire_body():
    source = (REPO_ROOT / "sessions/implant/implant_crypt.go").read_text()
    assert "func signWireBody(" in source
    assert "RAT_KEY_HMAC" in source
    assert "X-Signature" in source
    assert source.count("signWireBody(") >= 3
    assert "crypto/hmac" in source and "crypto/sha256" in source


def test_implant_seeds_defaults_and_pins_tls():
    source = (REPO_ROOT / "sessions/implant/implant_crypt.go").read_text()
    assert "func seedConfigDefaults(" in source
    assert "REV_SHELL_PORT_STR" in source
    assert "SCAN_PORTS_CSV" in source
    assert 'utls "github.com/refraction-networking/utls"' in source
    assert "DialTLSContext: dialTLS" in source
    assert "HelloChrome_Auto" in source
    assert "using baked-in defaults" in source


def test_builder_context_carries_beacon_keys():
    source = (REPO_ROOT / "modules/c2_builder.py").read_text()
    assert '"rat_key"' in source
    assert '"reverse_shell_port"' in source
    assert '"beacon_scan_ports"' in source


def test_rootkit_sources_free_of_operator_identity():
    for relative in (
        "modules/rootkit/rootkit.c",
        "modules/rootkit/rootkit.c.bkp.c",
        "modules/rootkit/mrhyde.c",
        "modules/rootkit/mrhyde2.c",
        "modules/rootkit/mrhyde3.c",
    ):
        text = (REPO_ROOT / relative).read_text()
        assert "10.10.14.10" not in text, relative
        assert '"grisun0"' not in text, relative


def test_rootkit_makefile_exposes_overrides():
    text = (REPO_ROOT / "modules/rootkit/Makefile").read_text()
    assert "LISTENER_IP ?=" in text and "LISTENER_PORT ?=" in text
    assert "ccflags-y" in text


def test_backdoor_neutralized():
    text = (REPO_ROOT / "modules/backdoor/backdoor.c").read_text()
    assert "TEXT(\"Hacked\")" not in text
    assert "MessageBox" not in text
    assert "RUNKEY_NAME" in text


def test_hygiene_findings_clean_on_current_tree():
    from cli.commands.audit import collect_hygiene_findings

    findings = collect_hygiene_findings(
        {"rat_key": "ab" * 32, "c2_require_beacon_hmac": "True"}
    )
    assert findings["beacon_hmac_required"] is True
    assert findings["rat_key_fresh"] is True
    assert not findings["artifact_leaks"]


def test_hygiene_findings_flag_dirty_payload():
    from cli.commands.audit import collect_hygiene_findings

    findings = collect_hygiene_findings(
        {"rat_key": LEGACY_RAT_KEY, "auto_privesc_on_checkin": "true"}
    )
    assert findings["rat_key_fresh"] is False
    assert findings["noisy_flags"]["auto_privesc_on_checkin"] is True
    assert findings["findings_count"] >= 2


def test_audit_hygiene_chain_loads_and_resolves():
    from modules.chain_registry import load_all

    chain = load_all().get("audit_hygiene")
    assert chain is not None and len(chain.steps) == 4
    resolved = chain.resolve({"target": "127.0.0.1"})
    assert [step["run"].split()[0] for step in resolved] == [
        "hygiene_audit",
        "set",
        "set",
        "set",
    ]


def test_orchestrator_exposes_new_fields():
    from cli.orchestrator_assets_tabs import CONFIG_FIELDS

    keys = {field.key for field in CONFIG_FIELDS}
    assert {"c2_require_beacon_hmac", "auto_privesc_on_checkin", "auto_discover_on_checkin"} <= keys


def test_command_index_contains_hygiene_audit():
    index = json.loads((REPO_ROOT / "cli" / "command_index.json").read_text())
    names = {entry.get("name") for entry in index.get("commands", [])} if isinstance(index, dict) else set()
    if not names:
        names = {entry.get("name") for entry in index} if isinstance(index, list) else set()
    names = {str(name).removeprefix("do_") for name in names}
    assert "hygiene_audit" in names
