"""Tests for core.config — Config wrapper, load_payload, save_payload, load_and_validate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


class TestLoadPayload:
    """Tests for :func:`core.config.load_payload`."""

    def test_returns_dict_with_expected_keys(self, tmp_path):
        """load_payload returns a dictionary containing the keys that were saved."""
        from core.config import load_payload, save_payload

        target = tmp_path / "payload.json"
        save_payload({"rhost": "10.0.0.1", "lport": 4444, "lhost": "127.0.0.1", "target_os": "1"}, target)
        result = load_payload(target)
        assert isinstance(result, dict)
        assert result["rhost"] == "10.0.0.1"
        assert result["lport"] == 4444

    def test_roundtrips_values_correctly(self, tmp_path):
        """Values survive a full save-then-load cycle unchanged."""
        from core.config import load_payload, save_payload

        target = tmp_path / "payload.json"
        original = {"rhost": "192.168.1.1", "lport": 9999, "nested": {"key": [1, 2, 3]}, "lhost": "10.0.0.1", "target_os": "1"}
        save_payload(original, target)
        loaded = load_payload(target)
        assert loaded == original

    def test_handles_malformed_json(self, tmp_path):
        """load_payload raises JSONDecodeError when the file is not valid JSON."""
        from core.config import load_payload

        target = tmp_path / "payload.json"
        target.write_text("{invalid json!!!")
        with pytest.raises(json.JSONDecodeError):
            load_payload(target)

    def test_copies_from_example_when_payload_missing(self, tmp_path):
        """When payload.json is missing but payload.example.json exists, copy from the example."""
        from core.config import load_payload, save_payload, _EXAMPLE_FILENAME

        example = tmp_path / _EXAMPLE_FILENAME
        save_payload({"rhost": "10.10.10.10", "lport": 1234, "lhost": "127.0.0.1", "target_os": "1"}, example)
        payload_path = tmp_path / "payload.json"
        assert not payload_path.exists()
        result = load_payload(payload_path)
        assert payload_path.exists()
        assert result["rhost"] == "10.10.10.10"
        assert result["lport"] == 1234

    def test_raises_when_both_payload_and_example_missing(self, tmp_path):
        """load_payload raises FileNotFoundError when neither payload nor example exists."""
        from core.config import load_payload

        target = tmp_path / "nonexistent" / "payload.json"
        with pytest.raises(FileNotFoundError):
            load_payload(target)


class TestSavePayload:
    """Tests for :func:`core.config.save_payload`."""

    def test_atomic_write_no_leftover_tmp(self, tmp_path):
        """save_payload writes atomically with no .tmp files left behind."""
        from core.config import save_payload

        target = tmp_path / "payload.json"
        save_payload({"k": "v"}, target)
        assert target.exists()
        assert json.loads(target.read_text(encoding="utf-8")) == {"k": "v"}
        for sibling in tmp_path.iterdir():
            assert not sibling.name.endswith(".tmp"), f"leftover tmp file: {sibling}"

    def test_creates_parent_directories(self, tmp_path):
        """save_payload creates intermediate directories that do not exist."""
        from core.config import save_payload

        target = tmp_path / "nested" / "path" / "payload.json"
        save_payload({"a": 1}, target)
        assert target.exists()


class TestConfig:
    """Tests for the :class:`core.config.Config` wrapper."""

    def test_attribute_access_for_known_keys(self):
        """Config attributes match the underlying dictionary keys."""
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lport": 9999, "lhost": "127.0.0.1", "target_os": "1"})
        assert cfg.rhost == "10.0.0.1"
        assert cfg.lport == 9999
        assert cfg.lhost == "127.0.0.1"

    def test_item_access_for_known_keys(self):
        """Config[...] delegates to attribute access."""
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "target_os": "1"})
        assert cfg["rhost"] == "10.0.0.1"

    def test_unknown_key_returns_none(self):
        """Missing keys return None instead of raising."""
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "target_os": "1"})
        assert cfg.nonexistent_key_12345 is None
        assert cfg["another_fake_key"] is None

    def test_as_params_returns_shallow_copy(self):
        """as_params returns a shallow copy of the underlying dict."""
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "target_os": "1"})
        params = cfg.as_params()
        assert params["rhost"] == "10.0.0.1"
        assert isinstance(params, dict)
        params["rhost"] = "changed"
        assert cfg.rhost == "10.0.0.1"

    def test_aes_key_is_resolved_and_hex(self):
        """Config resolves or generates a 64-char hex aes_key on construction."""
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "target_os": "1"})
        assert hasattr(cfg, "aes_key")
        assert isinstance(cfg.aes_key, bytes)
        assert len(cfg.aes_key) == 32
        assert isinstance(cfg.config["aes_key"], str)
        assert len(cfg.config["aes_key"]) == 64


class TestLoadAndValidate:
    """Tests for :func:`core.config.load_and_validate`."""

    def test_returns_validation_results_dict(self, tmp_path):
        """load_and_validate returns a dict with payload, valid, warnings, errors, issues."""
        from core.config import load_and_validate, save_payload
        from core.payload_schema import ValidationIssue

        target = tmp_path / "payload.json"
        save_payload({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "lport": 4444, "target_os": "1"}, target)
        result = load_and_validate(target)
        assert isinstance(result, dict)
        assert isinstance(result["payload"], dict)
        assert isinstance(result["valid"], bool)
        assert isinstance(result["warnings"], list)
        assert isinstance(result["errors"], list)
        assert isinstance(result["issues"], list)
        for issue in result["issues"]:
            assert isinstance(issue, ValidationIssue)

    def test_missing_required_fields_reported_as_errors(self, tmp_path):
        """Required fields missing from the payload yield error-level issues."""
        from core.config import load_and_validate, save_payload
        from core.payload_schema import Severity

        target = tmp_path / "payload.json"
        save_payload({"rhost": "10.0.0.1"}, target)
        result = load_and_validate(target)
        error_issues = [i for i in result["issues"] if i.severity == Severity.ERROR]
        assert len(error_issues) > 0

    def test_invalid_types_reported_as_warnings(self, tmp_path):
        """Malformed values produce warning-level issues."""
        from core.config import load_and_validate, save_payload
        from core.payload_schema import Severity

        target = tmp_path / "payload.json"
        save_payload({"rhost": "10.0.0.1", "lhost": "127.0.0.1", "lport": "not_a_port", "target_os": "1"}, target)
        result = load_and_validate(target)
        warning_issues = [i for i in result["issues"] if i.severity == Severity.WARNING]
        assert len(warning_issues) > 0
        assert any("lport" in i.key for i in warning_issues)
