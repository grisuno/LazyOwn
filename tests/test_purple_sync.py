"""Purple Sync tests: spool, adapters, redaction, config persistence."""

from __future__ import annotations

import json

import pytest

from modules import purple_sync
from modules.purple_sync import PurpleSync, PurpleSyncConfig


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    """Isolate the shared engine and its files per test."""
    monkeypatch.setattr(purple_sync, "SPOOL_PATH", tmp_path / "spool.jsonl")
    monkeypatch.setattr(purple_sync, "AUDIT_PATH", tmp_path / "sent.jsonl")
    monkeypatch.setattr(purple_sync, "_SYNC", None)
    return tmp_path


class TestRedactSecret:
    def test_masks_password_argument(self):
        assert purple_sync.redact_secret("sshpass -p hunter2 ssh user@x") == "sshpass -p [REDACTED] ssh user@x"

    def test_masks_named_token(self):
        assert "hunter2" not in purple_sync.redact_secret("curl -H 'Authorization: token=abc123def456'")
        assert "[REDACTED]" in purple_sync.redact_secret("curl -H 'Authorization: token=abc123def456'")

    def test_plain_command_untouched(self):
        cmd = "nmap -sV -p 22,80 10.0.0.5"
        assert purple_sync.redact_secret(cmd) == cmd


class TestSpool:
    def test_emit_disabled_keeps_spool_and_does_not_send(self, isolated):
        sender_calls = []
        sync = PurpleSync(
            PurpleSyncConfig(enabled=False),
            sender=lambda *a: sender_calls.append(a) or (200, ""),
            spool_path=isolated / "spool.jsonl",
        )
        assert sync.emit_command("nmap -sV 10.0.0.5") is False
        assert sender_calls == []
        assert len(sync._read_spool()) == 1

    def test_emit_enabled_forwards_and_drains_spool(self, isolated):
        calls = []

        def sender(url, headers, body, timeout):
            calls.append((url, headers, body))
            return 200, ""

        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="elastic", endpoint="https://siem:9200"),
            sender=sender,
            spool_path=isolated / "spool.jsonl",
        )
        sync.emit_command("nmap -sV 10.0.0.5")
        assert len(calls) == 1
        url, headers, body = calls[0]
        assert url == "https://siem:9200/_bulk"
        assert json.loads(headers)["Content-Type"] == "application/x-ndjson"
        assert "nmap -sV 10.0.0.5" in body
        assert sync._read_spool() == []

    def test_failed_forward_keeps_spool(self, isolated):
        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="elastic", endpoint="https://siem:9200"),
            sender=lambda *a: (500, "boom"),
            spool_path=isolated / "spool.jsonl",
        )
        sync.emit_command("nmap -sV 10.0.0.5")
        assert len(sync._read_spool()) == 1

    def test_splunk_envelope_shape(self, isolated):
        calls = []

        def sender(url, headers, body, timeout):
            calls.append((url, headers, body))
            return 200, ""

        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="splunk", endpoint="https://siem:8088", token="hec-token"),
            sender=sender,
            spool_path=isolated / "spool.jsonl",
        )
        sync.emit_command("id")
        url, headers, body = calls[0]
        assert url.endswith("/services/collector/event")
        assert json.loads(headers)["Authorization"] == "Splunk hec-token"
        first = json.loads(body.splitlines()[0])
        assert "event" in first and "sourcetype" in first

    def test_webhook_envelope_shape(self, isolated):
        calls = []

        def sender(url, headers, body, timeout):
            calls.append((url, headers, body))
            return 200, ""

        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="webhook", endpoint="http://siem/hook"),
            sender=sender,
            spool_path=isolated / "spool.jsonl",
        )
        sync.emit_command("id")
        url, headers, body = calls[0]
        assert url == "http://siem/hook"
        assert "events" in json.loads(body)

    def test_transport_error_keeps_spool(self, isolated):
        def sender(url, headers, body, timeout):
            raise ConnectionError("refused")

        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="webhook", endpoint="http://siem/hook"),
            sender=sender,
            spool_path=isolated / "spool.jsonl",
        )
        sync.emit_command("id")
        assert len(sync._read_spool()) == 1


class TestEventShape:
    def test_event_carries_command_target_outcome(self, isolated, monkeypatch):
        monkeypatch.setattr(
            purple_sync, "load_payload", lambda: {"rhost": "10.0.0.5", "lhost": "10.0.0.9", "phase": "exploit"}
        )
        sync = PurpleSync(PurpleSyncConfig(enabled=False), spool_path=isolated / "spool.jsonl")
        event = sync.build_event("mimikatz sekurlsa::logonpasswords", exit_code=0, category="credential")
        assert event["lazyown"]["target"] == "10.0.0.5"
        assert event["lazyown"]["operator_host"] == "10.0.0.9"
        assert event["lazyown"]["phase"] == "exploit"
        assert event["event"]["outcome"] == "success"
        assert "mimikatz" in event["lazyown"]["command"]

    def test_redaction_applied_by_default(self, isolated):
        sync = PurpleSync(PurpleSyncConfig(enabled=False, redact=True), spool_path=isolated / "spool.jsonl")
        event = sync.build_event("sshpass -p hunter2 ssh x")
        assert "hunter2" not in event["lazyown"]["command"]

    def test_status_counters(self, isolated):
        sync = PurpleSync(
            PurpleSyncConfig(enabled=False), spool_path=isolated / "spool.jsonl", audit_path=isolated / "sent.jsonl"
        )
        sync.emit_command("id")
        status = sync.status()
        assert status["enabled"] is False
        assert status["pending"] == 1
        assert status["sent"] == 0


class TestConfig:
    def test_defaults_disabled(self):
        config = (
            purple_sync.load_config.__wrapped__
            if hasattr(purple_sync.load_config, "__wrapped__")
            else purple_sync.load_config
        )
        cfg = PurpleSyncConfig()
        assert cfg.enabled is False
        assert cfg.siem_type == "elastic"

    def test_unknown_siem_type_falls_back(self, monkeypatch):
        monkeypatch.setattr(purple_sync, "load_payload", lambda: {"purple_sync": {"siem_type": "wrong"}})
        cfg = purple_sync.load_config()
        assert cfg.siem_type == "elastic"

    def test_configure_persists_and_updates_shared(self, isolated, monkeypatch):
        saved = {}

        def fake_save(config):
            saved.update(config.as_dict())
            return saved

        monkeypatch.setattr(purple_sync, "save_config", fake_save)
        data = purple_sync.configure("webhook", "http://siem/hook", "tok", enabled=True)
        assert data["siem_type"] == "webhook"
        assert data["enabled"] is True
        assert purple_sync.get_sync().config.enabled is True


class TestBackfill:
    def test_backfill_forwards_history(self, isolated):
        src = isolated / "history.jsonl"
        src.write_text(json.dumps({"lazyown": {"command": "nmap"}}) + "\n" + "not-json\n")
        calls = []

        def sender(url, headers, body, timeout):
            calls.append(body)
            return 200, ""

        sync = PurpleSync(
            PurpleSyncConfig(enabled=True, siem_type="webhook", endpoint="http://siem/hook"),
            sender=sender,
            spool_path=isolated / "spool.jsonl",
        )
        purple_sync._SYNC = sync
        total = purple_sync.backfill([str(src)])
        assert total >= 1
