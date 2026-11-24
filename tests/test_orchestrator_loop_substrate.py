"""Tests for orchestrator termination/leases/boundary/evidence sections."""

from __future__ import annotations

import pytest

from modules import orchestrator_config as oc


@pytest.fixture()
def payload_store(monkeypatch):
    """Back orchestrator_config reads with an in-memory payload."""
    store: dict = {}
    monkeypatch.setattr(oc, "_payload", lambda: dict(store))
    monkeypatch.setattr(oc, "profile_config", lambda name="": {})
    return store


def test_termination_defaults(payload_store):
    config = oc.termination()
    assert config["mode"] == "try_hard"
    assert config["max_tokens_per_task"] > 0
    assert config["wrapup_reserve_pct"] == 5.0


def test_termination_payload_override(payload_store):
    payload_store["orchestrator"] = {"termination": {"mode": "save_tokens", "max_tokens_per_task": 500}}
    config = oc.termination()
    assert config["mode"] == "save_tokens"
    assert config["max_tokens_per_task"] == 500


def test_termination_bad_mode_falls_back(payload_store):
    payload_store["orchestrator"] = {"termination": {"mode": "bogus"}}
    assert oc.termination()["mode"] == "try_hard"


def test_leases_defaults_and_override(payload_store):
    defaults = oc.leases_config()
    assert defaults["enabled"] is True
    assert defaults["ttl_sec"] == 900.0
    payload_store["orchestrator"] = {"leases": {"enabled": False, "ttl_sec": 30}}
    config = oc.leases_config()
    assert config["enabled"] is False
    assert config["ttl_sec"] == 30.0


def test_leases_bad_value_falls_back(payload_store):
    payload_store["orchestrator"] = {"leases": {"ttl_sec": "nonsense"}}
    assert oc.leases_config()["ttl_sec"] == 900.0


def test_boundary_default_on_and_disableable(payload_store):
    assert oc.boundary_config()["enabled"] is True
    payload_store["orchestrator"] = {"boundary": {"enabled": False}}
    assert oc.boundary_config()["enabled"] is False


def test_evidence_defaults_and_override(payload_store):
    assert oc.evidence_config()["citation_enabled"] is True
    payload_store["orchestrator"] = {"evidence": {"citation_enabled": False, "citation_max_age_sec": 60}}
    config = oc.evidence_config()
    assert config["citation_enabled"] is False
    assert config["citation_max_age_sec"] == 60.0


def test_validate_rejects_bad_termination_mode():
    errors = oc.validate_config({"version": 1, "profiles": {"a": {"termination": {"mode": "speedrun"}}}})
    assert any("termination mode" in error for error in errors)


def test_validate_rejects_negative_lease_ttl():
    errors = oc.validate_config({"version": 1, "profiles": {"a": {"leases": {"ttl_sec": -5}}}})
    assert any("ttl_sec" in error for error in errors)


def test_validate_rejects_bad_boundary_type():
    errors = oc.validate_config({"version": 1, "profiles": {"a": {"boundary": {"enabled": "yes"}}}})
    assert any("boundary enabled" in error for error in errors)


def test_validate_accepts_full_section():
    errors = oc.validate_config(
        {
            "version": 1,
            "profiles": {
                "a": {
                    "termination": {"mode": "save_tokens", "wrapup_reserve_pct": 10},
                    "leases": {"enabled": True, "ttl_sec": 300, "heartbeat_sec": 30},
                    "boundary": {"enabled": True},
                    "evidence": {"citation_enabled": True, "citation_max_age_sec": 7200},
                }
            },
        }
    )
    assert errors == []
