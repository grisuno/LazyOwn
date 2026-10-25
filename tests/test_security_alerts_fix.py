"""Regression tests for CodeQL alerts #941-#972 (SSRF, TLS, clear-text, ReDoS, paths).

BDD contracts:
- GIVEN attacker-controlled proxy/HTTP input, WHEN validated, THEN metadata
  targets are denied, private targets follow operator policy, and upstream
  connections dial validated IPs (no DNS-rebinding TOCTOU).
- GIVEN lab self-signed TLS, WHEN connecting, THEN verification stays on by
  default and unverified fallback needs explicit operator opt-in.
- GIVEN secrets (reverse-shell password, loot, traces), WHEN persisted,
  THEN at rest they are sealed (AES-256-GCM) or scrubbed, with owner-only
  file modes and minimal plaintext lifetime.
- GIVEN uncontrolled path/regex input, WHEN handled, THEN validation is
  linear-time (no ReDoS), traversal is blocked, and symlinks cannot escape.

TDD: these tests are the red phase for the fix. SDD: each family maps to
one contract in core/hardening.py. BDD: scenario names below.
"""

from __future__ import annotations

import json
import os
import time


def test_ssrf_metadata_hosts_denied():
    """BDD: cloud metadata hosts are denied even with private allowed."""
    from modules.lazy_proxy import _validate_proxy_target

    os.environ.pop("LAZY_PROXY_ALLOW_PRIVATE", None)
    for host in ("169.254.169.254", "100.100.100.200", "metadata.google.internal", "instance-data"):
        try:
            _validate_proxy_target(host, 80, "http")
        except ValueError:
            continue
        raise AssertionError(f"metadata host {host!r} was not denied")


def test_ssrf_dns_rebinding_to_metadata_denied(monkeypatch):
    """BDD: DNS resolving to metadata IP is denied (rebinding guard)."""
    import modules.lazy_proxy as proxy

    monkeypatch.setattr(proxy, "_resolved_ips", lambda host: ["169.254.169.254"])
    try:
        proxy._validate_proxy_target("evil.example.com", 80, "http")
    except ValueError:
        return
    raise AssertionError("DNS-rebinding to metadata IP was not denied")


def test_ssrf_private_policy_flag(monkeypatch):
    """BDD: LAZY_PROXY_ALLOW_PRIVATE=0 denies resolved private addresses."""
    import modules.lazy_proxy as proxy

    monkeypatch.setenv("LAZY_PROXY_ALLOW_PRIVATE", "0")
    monkeypatch.setattr(proxy, "_resolved_ips", lambda host: ["192.168.1.10"])
    try:
        proxy._validate_proxy_target("lab.example.com", 80, "http")
    except ValueError:
        return
    raise AssertionError("private address was not denied with flag off")


def test_ssrf_upstream_path_rejected():
    """BDD: absolute URLs, CRLF and NUL paths never reach upstream."""
    from core.hardening import validate_upstream_path

    for bad in ("http://evil/x", "/a\r\nInjected: 1", "/a\x00b", "", "x" * 9000, "no-leading-slash"):
        assert validate_upstream_path(bad) is False, f"path {bad[:20]!r} accepted"


def test_ssrf_pinned_connection_dials_validated_ip(monkeypatch):
    """BDD: relay dials the validated IP, preserving SNI/host header."""
    import modules.lazy_proxy as proxy

    monkeypatch.setattr(proxy, "_resolved_ips", lambda host: ["93.184.216.34"])
    validated, ips = proxy.resolve_validated_target("example.com", 80, "http")
    assert validated == "example.com"
    assert ips == ["93.184.216.34"]
    dialed: dict = {}

    class FakeSock:
        def close(self):
            return None

    def fake_create_connection(address, timeout=None):
        dialed["address"] = address
        return FakeSock()

    monkeypatch.setattr(proxy.socket, "create_connection", fake_create_connection)
    sock = proxy.connect_pinned(validated, ips, 80, "http", timeout=1.0)
    assert dialed["address"][0] == "93.184.216.34"
    sock.close()


def test_tls_default_context_verifies():
    """BDD: default upstream TLS verifies with TLS 1.2 floor."""
    import ssl

    from core.hardening import tls_secure_context

    context = tls_secure_context()
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True
    assert context.minimum_version == ssl.TLSVersion.TLSv1_2


def test_tls_lab_fallback_needs_opt_in(monkeypatch):
    """BDD: self-signed lab fallback is fail-closed without opt-in."""
    import modules.lazy_proxy as proxy

    monkeypatch.delenv("LAZY_PROXY_ALLOW_SELF_SIGNED_LAB", raising=False)
    assert proxy.tls_lab_unverified_allowed("127.0.0.1") is False
    monkeypatch.setenv("LAZY_PROXY_ALLOW_SELF_SIGNED_LAB", "1")
    assert proxy.tls_lab_unverified_allowed("127.0.0.1") is True
    monkeypatch.delenv("LAZY_PROXY_ALLOW_SELF_SIGNED_LAB", raising=False)
    assert proxy.tls_lab_unverified_allowed("93.184.216.34") is False


def test_reverse_shell_password_sealed_roundtrip(tmp_path):
    """BDD: reverse-shell fallback persists sealed, owner-only, round-trips."""
    import pathlib

    from core.hardening import store_secret_owner_only
    from core.reverse_shell_secret import (
        generate_reverse_shell_password,
        load_reverse_shell_password,
        seal_reverse_shell_password,
    )

    password = generate_reverse_shell_password()
    assert len(password) >= 32
    secret_path = tmp_path / "sessions" / ".reverse_shell_password"
    store_secret_owner_only(str(secret_path), seal_reverse_shell_password(password) + "\n")
    assert secret_path.exists()
    mode = oct(secret_path.stat().st_mode & 0o777)
    assert mode == "0o600", f"expected 0600, got {mode}"
    raw = secret_path.read_text()
    assert password not in raw, "password stored in clear text"
    assert load_reverse_shell_password(secret_path) == password
    source = pathlib.Path("lazyc2.py").read_text()
    assert "core.reverse_shell_secret" in source
    assert "seal_reverse_shell_password" in source
    assert "REVERSE_SHELL_SECRET_FILENAME" in source


def test_loot_secret_sealed_roundtrip():
    """BDD: dominance loot seals secrets and unseals for operator reuse."""
    from modules.domain_dominance import DomainDominance

    engine = DomainDominance.__new__(DomainDominance)
    sealed = engine._seal_loot_secret("Sup3rSecret!")
    assert sealed != "Sup3rSecret!"
    assert engine._unseal_loot_secret(sealed) == "Sup3rSecret!"
    assert engine._unseal_loot_secret("") == ""


def test_activity_and_trace_scrubbed(tmp_path):
    """BDD: activity/trace stores never persist clear-text credentials."""
    from modules.lazy_loop import ActivityLog, scrub_secrets

    nasty = "export GROQ_API_KEY=sk-live-12345678 and password=Sup3rSecret and bearer abcdefgh1234"
    cleaned = scrub_secrets(nasty)
    assert "sk-live-12345678" not in cleaned
    assert "Sup3rSecret" not in cleaned
    import modules.lazy_loop as loop

    monkeypatch_store = tmp_path / "store"
    monkeypatch_store.mkdir()
    orig = loop.STORE_DIR
    loop.STORE_DIR = monkeypatch_store
    try:
        log = ActivityLog("task-test")
        record = log.emit("worker", "note", nasty)
        assert "Sup3rSecret" not in json.dumps(record)
        stored = log._path.read_text()
        assert "Sup3rSecret" not in stored
        assert "sk-live-12345678" not in stored
        mode = oct(log._path.stat().st_mode & 0o777)
        assert mode == "0o600", f"expected 0600, got {mode}"
    finally:
        loop.STORE_DIR = orig


def test_trace_redaction_helper():
    """BDD: MCP worker-trace redaction removes credential patterns."""
    from core.hardening import redact_text

    nasty = "SMBPass Sup3rSecret password=abc123 bearer token12345678"
    cleaned = redact_text(nasty)
    assert "Sup3rSecret" not in cleaned
    assert "abc123" not in cleaned


def test_path_helpers_block_traversal(tmp_path):
    """BDD: traversal, absolute, NUL and symlink escapes are blocked."""
    from core.hardening import is_safe_dir_path, is_safe_yaml_name, safe_join_under

    base = tmp_path / "atomics"
    base.mkdir()
    assert is_safe_dir_path("T1110/brute") is True
    for bad in ("../etc", "/abs", "a\\b", "a\x00b", "", "x" * 300, ".", "..", "a/../b"):
        assert is_safe_dir_path(bad) is False, f"dir {bad!r} accepted"
    assert is_safe_yaml_name("T1110.yaml") is True
    for bad in (".hidden.yaml", "a/b.yaml", "T 1110.yaml", "x" * 300, "noext", "a\x00.yaml"):
        assert is_safe_yaml_name(bad) is False, f"yaml {bad!r} accepted"
    outside = tmp_path / "outside.txt"
    outside.write_text("x")
    try:
        safe_join_under(str(base), "../outside.txt")
    except Exception:
        pass
    else:
        raise AssertionError("traversal escape was not blocked")
    link = base / "link"
    try:
        link.symlink_to(outside)
    except OSError:
        pass
    else:
        try:
            safe_join_under(str(base), "link")
        except Exception:
            pass
        else:
            raise AssertionError("symlink escape was not blocked")


def test_path_validators_linear_time():
    """BDD: crafted long inputs validate in linear time (no ReDoS)."""
    from core.hardening import is_safe_dir_path, is_safe_yaml_name

    evil_dir = "a!" + "a" * 10000 + "!"
    evil_yaml = "a" * 10000 + ".yaml"
    start = time.time()
    assert is_safe_dir_path(evil_dir) is False
    assert is_safe_yaml_name(evil_yaml) is False
    assert is_safe_yaml_name("T1110.yaml") is True
    assert time.time() - start < 1.0


def test_emoji_detector_without_broad_ranges():
    """BDD: emoji flagged, plain text clean, no broad regex ranges in source."""
    import pathlib

    from skills.claude_md_orchestrator.validators import check_no_emoji

    assert check_no_emoji("plain text", "p") == []
    assert len(check_no_emoji("hello \U0001f600", "p")) == 1
    source = pathlib.Path("skills/claude_md_orchestrator/validators.py").read_text()
    for broad in ("\u2600-\u26ff", "\u2700-\u27bf", "\u2b00-\u2bff"):
        assert broad not in source, f"broad range {broad!r} still present"


def test_safe_open_under_rejects_symlink(tmp_path):
    """BDD: symlink escapes are rejected at open time (O_NOFOLLOW)."""
    import pytest

    from core.hardening import safe_open_under

    base = tmp_path / "root"
    base.mkdir()
    (base / "real.txt").write_text("ok")
    with safe_open_under(str(base), "real.txt", "r", encoding="utf-8") as handle:
        assert handle.read() == "ok"
    outside = tmp_path / "outside.txt"
    outside.write_text("secret")
    link = base / "evil.txt"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises((OSError, Exception)):
        safe_open_under(str(base), "evil.txt", "r", encoding="utf-8")


def _response_calls_with_raw_exception(tree: "ast.AST") -> list[str]:
    """Return response-call locations leaking a raw exception object.

    A response call is ``jsonify(...)``, ``render_template(...)`` or
    ``flash(...)``. Using ``type(exc).__name__`` inside is allowed; any
    other reference to an exception variable is a leak.
    """
    import ast as _ast

    leaks: list[str] = []
    for node in _ast.walk(tree):
        if not isinstance(node, _ast.Call):
            continue
        func = node.func
        name = ""
        if isinstance(func, _ast.Name):
            name = func.id
        elif isinstance(func, _ast.Attribute):
            name = func.attr
        if name not in ("jsonify", "render_template", "flash"):
            continue
        for arg in list(node.args) + [kw.value for kw in node.keywords]:
            for child in _ast.walk(arg):
                if isinstance(child, _ast.Name) and child.id in ("exc", "e", "_exc", "_e"):
                    leaks.append(f"{name} leaks '{child.id}' at line {getattr(node, 'lineno', '?')}")
    return leaks


def test_c2_responses_never_carry_raw_exceptions():
    """BDD: HTTP responses carry generic errors, never exception text."""
    import ast as _ast
    import pathlib

    candidates = ["lazyc2.py"] + sorted(str(path) for path in pathlib.Path("lazyc2/blueprints").glob("*.py"))
    for candidate in candidates:
        tree = _ast.parse(pathlib.Path(candidate).read_text())
        pruned = []
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Call):
                func = node.func
                callee = func.id if isinstance(func, _ast.Name) else getattr(func, "attr", "")
                if callee in ("jsonify", "render_template", "flash"):
                    pruned.append(node)
        for call in pruned:
            for arg in list(call.args) + [kw.value for kw in call.keywords]:
                for child in _ast.walk(arg):
                    if not (isinstance(child, _ast.Name) and child.id in ("exc", "e", "_exc", "_e")):
                        continue
                    parent_is_type_name = False
                    for parent in _ast.walk(arg):
                        if (
                            isinstance(parent, _ast.Call)
                            and isinstance(parent.func, _ast.Name)
                            and parent.func.id == "type"
                            and child in _ast.walk(parent)
                        ):
                            parent_is_type_name = True
                    assert parent_is_type_name, f"{candidate}:{call.lineno} leaks raw exception"
    assert _response_calls_with_raw_exception(_ast.parse("x = 1")) == []


def test_get_output_logs_type_only():
    """BDD: shell output (credential-bearing) never reaches server logs."""
    import ast as _ast
    import pathlib

    tree = _ast.parse(pathlib.Path("lazyc2.py").read_text())
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and node.name == "get_output":
            for child in _ast.walk(node):
                if isinstance(child, _ast.Call):
                    func = child.func
                    callee = func.id if isinstance(func, _ast.Name) else getattr(func, "attr", "")
                    if callee in ("error", "exception", "warning", "info", "debug"):
                        for arg in list(child.args) + [kw.value for kw in child.keywords]:
                            if isinstance(arg, _ast.JoinedStr):
                                for part in arg.values:
                                    if isinstance(part, _ast.FormattedValue) and isinstance(part.value, _ast.Name):
                                        assert part.value.id != "output", "raw shell output flows into logs"
            return
    raise AssertionError("get_output not found in lazyc2.py")


def test_graph_nodes_scrubbed_before_persist(tmp_path):
    """BDD: graph node text is scrubbed so stores never hold secrets."""
    import json as _json

    import modules.lazy_loop as loop

    store = tmp_path / "graph_store"
    store.mkdir()
    orig = loop.STORE_DIR
    loop.STORE_DIR = store
    try:
        graph = loop.ExplorationGraph("task-secret")
        node = graph.add_node("finding", "admin password=Sup3rSecret leak")
        assert "Sup3rSecret" not in node.text
        persisted = _json.loads(graph._path.read_text())
        assert "Sup3rSecret" not in _json.dumps(persisted)
        assert graph.finding_signature("admin password=Sup3rSecret leak")
        assert graph.edit_goal if hasattr(graph, "edit_goal") else True
    finally:
        loop.STORE_DIR = orig


def test_goal_edit_scrubs_text(tmp_path):
    """BDD: direct goal edits cannot smuggle secrets into the store."""
    import json as _json

    import modules.lazy_loop as loop

    store = tmp_path / "goal_store"
    store.mkdir()
    orig = loop.STORE_DIR
    loop.STORE_DIR = store
    try:
        graph = loop.ExplorationGraph("task-goal")
        node = graph.add_node("goal", "initial goal")
        engine = loop.LazyLoopEngine.__new__(loop.LazyLoopEngine)
        assert engine.edit_goal("task-goal", node.node_id, "escalate with password=Sup3rSecret") is True
        reloaded = loop.ExplorationGraph("task-goal")
        assert "Sup3rSecret" not in reloaded.get(node.node_id).text
        assert "Sup3rSecret" not in graph._path.read_text()
    finally:
        loop.STORE_DIR = orig


def test_secret_store_owner_only(tmp_path):
    """BDD: secret files are created owner-only with no clear-text leakage."""
    from core.hardening import store_secret_owner_only

    target = tmp_path / "sub" / "secret.txt"
    store_secret_owner_only(str(target), "s3cret-value")
    assert target.read_text() == "s3cret-value"
    assert oct(target.stat().st_mode & 0o777) == "0o600"
