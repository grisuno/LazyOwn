"""Hardening round: quoting, hostname retarget, fail-closed sealing, fdopen modes.

Covers the fixes from the hardening review: ``shlex.join`` serialisation
in ``repair_worker_command`` (argument quoting survives), hostname
retargeting, ``safe_open_under`` read-write fd modes, fail-closed
``seal_secret``, per-operator token revocation plus one-time SSE tickets,
and the LLM playbook shape gate.
"""

from __future__ import annotations

import shlex

import pytest

from core.errors import SecurityViolation
from modules.loop.command_sanitize import (
    _HOSTNAME_RE,
    _host_from_token,
    repair_worker_command,
)

# ── command_sanitize: hostname retargeting ───────────────────────────


@pytest.mark.parametrize(
    "hostname",
    ["example.com", "scanme.nmap.org", "target.local", "vuln-web.corp", "dc01.corp.example.com"],
)
def test_hostname_regex_matches_real_hostnames(hostname: str) -> None:
    """The hostname grammar accepts dotted FQDNs, not only IP literals."""
    assert _HOSTNAME_RE.match(hostname)


@pytest.mark.parametrize("value", ["10.0.0.5", "-p", "80,443", "not a host"])
def test_host_from_token_rejects_non_hosts(value: str) -> None:
    """Non-host tokens yield an empty host so they are never retargeted."""
    if value in ("10.0.0.5",):
        assert _host_from_token(value) == value
    else:
        assert _host_from_token(value) == ""


def test_repair_retargets_foreign_hostname() -> None:
    """A hallucinated hostname is retargeted to the authorized intent target."""
    command, reason = repair_worker_command("nmap -sV scanme.nmap.org", "10.0.0.5")
    assert command == "nmap -sV 10.0.0.5"
    assert "retargeted" in reason


def test_repair_retargets_hostname_inside_url() -> None:
    """URL-embedded foreign hostnames are retargeted too."""
    command, reason = repair_worker_command("curl http://evil.example.com/shell.txt", "10.0.0.5")
    assert command == "curl http://10.0.0.5/shell.txt"
    assert "retargeted" in reason


def test_repair_extracts_user_at_host_forms() -> None:
    """``user@host`` tokens expose their host so the target is not appended twice."""
    command, reason = repair_worker_command("ssh admin@srv.corp.local id", "10.0.0.5")
    assert command == "ssh admin@10.0.0.5 id"
    assert "retargeted" in reason
    command, _reason = repair_worker_command("ssh admin@10.0.0.5 id", "10.0.0.5")
    assert command == "ssh admin@10.0.0.5 id"


def test_repair_keeps_authorized_hostname() -> None:
    """The authorized target hostname is never rewritten."""
    command, reason = repair_worker_command("nmap -sV corp.local", "corp.local")
    assert command == "nmap -sV corp.local"
    assert reason == ""


# ── command_sanitize: quoting survival ───────────────────────────────


def test_repair_preserves_quoted_argument_with_spaces() -> None:
    """Round-tripping through shlex must not destroy argument quoting."""
    raw = "nmap --script-args 'user=admin,pass=P@ss w0rd' 10.0.0.5"
    command, _reason = repair_worker_command(raw, "10.0.0.5")
    assert shlex.split(command) == shlex.split(raw)
    assert "user=admin,pass=P@ss w0rd" in command
    assert command != "nmap --script-args user=admin,pass=P@ss w0rd 10.0.0.5"


def test_repair_output_roundtrips_through_shlex() -> None:
    """Whatever the repair produces must parse back to the same argv."""
    for raw in (
        "nmap -sV 10.0.0.5",
        "curl 'http://10.0.0.5/a b/'",
        "ssh admin@10.0.0.5 id",
    ):
        command, _reason = repair_worker_command(raw, "10.0.0.5")
        assert shlex.split(command) == shlex.split(raw)


# ── core.paths: fdopen mode correctness ──────────────────────────────


def test_safe_open_under_read_write_mode(tmp_path) -> None:
    """``r+`` opens a readable-and-writable fd (O_RDWR, not O_WRONLY)."""
    from core.paths import safe_open_under

    target = tmp_path / "state.txt"
    target.write_text("seed")
    with safe_open_under(str(tmp_path), "state.txt", "r+") as handle:
        assert handle.read() == "seed"
        handle.seek(0)
        handle.write("RE")
    assert target.read_text() == "REed"


def test_safe_open_under_write_plus_mode(tmp_path) -> None:
    """``w+`` truncates yet yields a readable-and-writable handle."""
    from core.paths import safe_open_under

    with safe_open_under(str(tmp_path), "fresh.txt", "w+") as handle:
        handle.write("data")
        handle.seek(0)
        assert handle.read() == "data"


def test_safe_join_under_is_deprecated_alias(tmp_path) -> None:
    """``safe_join_under`` still works but emits a DeprecationWarning."""
    from core.paths import safe_join_under, safe_path_join

    with pytest.warns(DeprecationWarning):
        resolved = safe_join_under(str(tmp_path), "child/file.txt")
    assert resolved == safe_path_join(str(tmp_path), "child/file.txt")


# ── core.secrets: fail-closed sealing ────────────────────────────────


def test_seal_secret_fail_closed_on_key_failure(tmp_path, monkeypatch) -> None:
    """A sealing failure raises SecurityViolation instead of plaintext."""
    import core.secrets as secrets_module
    from core.secrets import seal_secret

    def _boom(_sessions_dir):
        raise ValueError("key unavailable")

    monkeypatch.setattr(secrets_module, "_seal_key", _boom)
    with pytest.raises(SecurityViolation):
        seal_secret("secret-value", sessions_dir=tmp_path)


def test_seal_secret_fail_closed_without_cryptography(tmp_path, monkeypatch) -> None:
    """A missing cryptography backend also fails closed."""
    import builtins

    from core.secrets import seal_secret

    real_import = builtins.__import__

    def _no_fernet(name, *args, **kwargs):
        if name.startswith("cryptography"):
            raise ImportError("cryptography unavailable")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _no_fernet)
    with pytest.raises(SecurityViolation):
        seal_secret("secret-value", sessions_dir=tmp_path)


def test_seal_secret_roundtrip(tmp_path) -> None:
    """Sealed values unseal to the original plaintext."""
    from core.secrets import SEALED_SECRET_PREFIX, seal_secret, unseal_secret

    sealed = seal_secret("hunter2", sessions_dir=tmp_path)
    assert sealed.startswith(SEALED_SECRET_PREFIX)
    assert unseal_secret(sealed, sessions_dir=tmp_path) == "hunter2"


def test_seal_secret_idempotent_on_sealed_value() -> None:
    """Already-sealed values pass through untouched."""
    from core.secrets import SEALED_SECRET_PREFIX, seal_secret

    assert seal_secret(f"{SEALED_SECRET_PREFIX}abc") == f"{SEALED_SECRET_PREFIX}abc"


# ── token_gate: per-operator tokens and one-time tickets ─────────────


def _gate():
    from lazyc2.security.token_gate import SessionTokenGate

    gate = SessionTokenGate()
    gate.rotate()
    return gate


def test_operator_token_authenticates_and_revokes() -> None:
    """Per-operator tokens authenticate until revoked."""
    gate = _gate()
    token = gate.issue_for_operator("alice")
    assert gate.check(token)
    assert gate.revoke_operator("alice") == 1
    assert not gate.check(token)


def test_operator_tokens_scoped_by_name() -> None:
    """Revoking one operator leaves another operator's token live."""
    gate = _gate()
    alice = gate.issue_for_operator("alice")
    bob = gate.issue_for_operator("bob")
    gate.revoke_operator("alice")
    assert not gate.check(alice)
    assert gate.check(bob)


def test_issue_for_operator_requires_name() -> None:
    """Empty operator names are rejected."""
    with pytest.raises(ValueError):
        _gate().issue_for_operator("  ")


def test_rotate_clears_operator_tokens_and_tickets() -> None:
    """A rotation is a global logout: operator tokens and tickets die."""
    gate = _gate()
    token = gate.issue_for_operator("alice")
    ticket = gate.issue_ticket()
    gate.rotate()
    assert not gate.check(token)
    assert not gate.check(ticket)


def test_ticket_one_time_and_short_lived() -> None:
    """Tickets authenticate exactly once and expire quickly."""
    gate = _gate()
    gate.ticket_ttl_seconds = 0
    ticket = gate.issue_ticket()
    assert not gate.check(ticket)

    gate = _gate()
    ticket = gate.issue_ticket()
    assert gate.check(ticket)
    assert not gate.check(ticket)


def test_ticket_cap_bounds_memory() -> None:
    """Outstanding tickets never exceed the configured cap."""
    from lazyc2.security.token_gate import MAX_OUTSTANDING_TICKETS

    gate = _gate()
    for _ in range(MAX_OUTSTANDING_TICKETS + 10):
        gate.issue_ticket()
    assert len(gate._tickets) <= MAX_OUTSTANDING_TICKETS


def test_cookie_secure_auto_detects_https() -> None:
    """Explicit secure=True is honoured; auto-detect works without a request context."""
    gate = _gate()
    kwargs = gate.issue_session_cookie_kwargs(secure=True)
    assert kwargs["secure"] is True
    auto = gate.issue_session_cookie_kwargs()
    assert auto["httponly"] is True
    assert auto["samesite"] == "Lax"


# ── llm_yaml_repair: playbook shape gate ─────────────────────────────


def test_save_playbook_rejects_non_mapping(tmp_path, monkeypatch) -> None:
    """Non-mapping documents never reach disk."""
    from modules import llm_yaml_repair

    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        llm_yaml_repair.save_playbook("not a mapping", "leak")


def test_save_playbook_rejects_traversal_name(tmp_path, monkeypatch) -> None:
    """Path segments in the playbook name are neutralised."""
    from modules import llm_yaml_repair

    monkeypatch.chdir(tmp_path)
    path = llm_yaml_repair.save_playbook({"phases": []}, "../../etc/evil")
    assert str(path).startswith("playbooks/")
    assert ".." not in str(path)


def test_save_playbook_rejects_non_string_commands(tmp_path, monkeypatch) -> None:
    """Executable phase fields must be plain strings."""
    from modules import llm_yaml_repair

    monkeypatch.chdir(tmp_path)
    bad = {"phases": [{"name": "x", "command": {"inject": True}}]}
    with pytest.raises(ValueError):
        llm_yaml_repair.save_playbook(bad, "bad_shape")


def test_save_playbook_accepts_valid_shape(tmp_path, monkeypatch) -> None:
    """A well-formed playbook persists under playbooks/."""
    from modules import llm_yaml_repair

    monkeypatch.chdir(tmp_path)
    path = llm_yaml_repair.save_playbook(
        {"apt_name": "T", "phases": [{"name": "recon", "command": "nmap -sV 10.0.0.5"}]},
        "valid_playbook",
    )
    assert str(path) == "playbooks/valid_playbook.yaml"
