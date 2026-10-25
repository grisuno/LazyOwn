"""Malleable C2 agent: template safety, key ownership, record reading."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules import c2_agent as agent  # noqa: E402


def test_client_id_derivation() -> None:
    """Targets map to stable file-safe ids; hostile input is rejected."""
    assert agent.client_id_for("172.17.0.2") == "msf-172-17-0-2"
    assert agent.validate_client_id("msf-172-17-0-2") == "msf-172-17-0-2"
    for bad in ["", "../x", "a b", "x" * 65, ";evil"]:
        try:
            agent.validate_client_id(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted hostile id: {bad!r}")


def test_template_renders_without_tokens() -> None:
    """Rendered agents carry config, never raw placeholders."""
    text = agent.build_agent("http://192.168.1.120:8080", "msf-172-17-0-2", "ab" * 32, rat_key="cd" * 32, route="/gmail/v1/users/")
    assert "{C2}" not in text and "{KEY}" not in text and "{ID}" not in text
    assert "http://192.168.1.120:8080" in text and "msf-172-17-0-2" in text
    assert "ab" * 32 in text


def test_template_rejects_bad_inputs() -> None:
    """Short keys, bad URLs, and hostile ids never render."""
    for kwargs in (
        {"c2_url": "http://x/", "client_id": "a", "aes_hex": "zz"},
        {"c2_url": "ftp://x/", "client_id": "a", "aes_hex": "ab" * 32},
        {"c2_url": "http://x/", "client_id": "../x", "aes_hex": "ab" * 32},
    ):
        try:
            agent.build_agent(**kwargs)
        except ValueError:
            continue
        raise AssertionError(f"rendered bad input: {kwargs}")


def test_template_is_py25_safe() -> None:
    """The agent must avoid constructs missing from Python 2.5 stdlib."""
    text = agent.build_agent("http://127.0.0.1:8080", "lab-1", "ab" * 32, rat_key="cd" * 32)
    assert "timeout=" not in text, "py2.5 urllib/httplib lack timeout kwargs"
    assert " except " in text and ", e:" in text
    assert " as e" not in text.replace("has ", ""), "py2.5 lacks 'except as'"
    assert "import json" not in text, "py2.5 has no json module"


def test_template_drops_inherited_fds() -> None:
    """Agents born in backdoor shells must not hold the listen socket."""
    text = agent.build_agent("http://127.0.0.1:8080", "lab-1", "ab" * 32, rat_key="cd" * 32)
    assert "closerange" not in text, "os.closerange is missing on python2.5"
    assert "range(3, 256)" in text and "os.close(_fd)" in text
    assert '"""' not in text, "triple quotes would terminate the module template string"


def test_key_never_generated_silently(tmp_path: Path, monkeypatch) -> None:
    """No key file and no snapshot means a loud failure, not a new key."""
    monkeypatch.setattr(agent, "_SESSIONS_DIR", tmp_path)
    try:
        agent._ensure_key()
    except RuntimeError as exc:
        assert "Start the server first" in str(exc)
        return
    raise AssertionError("silently generated a key")


def test_key_snapshot_roundtrip(tmp_path: Path, monkeypatch) -> None:
    """A pinned key file is snapshotted and reused byte-identically."""
    monkeypatch.setattr(agent, "_SESSIONS_DIR", tmp_path)
    raw = bytes(range(32))
    (tmp_path / "key.aes").write_bytes(raw)
    first = agent._ensure_key()
    assert first == raw.hex()
    assert json.loads((tmp_path / "c2_lab.json").read_text())["aes_hex"] == raw.hex()
    (tmp_path / "key.aes").unlink()
    assert agent._ensure_key() == raw.hex()


def test_read_records_newest_last(tmp_path: Path, monkeypatch) -> None:
    """Record reading parses JSONL and caps to the tail."""
    monkeypatch.setattr(agent, "_SESSIONS_DIR", tmp_path)
    path = tmp_path / "msf-9-9-9-9.records.jsonl"
    path.write_text(
        "\n".join(json.dumps({"command": f"cmd{i}", "output": f"out{i}"}) for i in range(5)) + "\n",
        encoding="utf-8",
    )
    rows = agent.read_records("msf-9-9-9-9", limit=2)
    assert [r["command"] for r in rows] == ["cmd3", "cmd4"]
    assert agent.read_records("nobody") == []


def test_c2_addon_contract() -> None:
    """The session commands exist as routable shell verbs."""

    found = set()
    for path in (_ROOT / "cli" / "commands").glob("c2_session.py"):
        text = path.read_text()
        for name in ("do_c2_server", "do_c2_deploy", "do_c2_exec", "do_c2_loot"):
            if f"def {name}" in text:
                found.add(name)
    assert found == {"do_c2_server", "do_c2_deploy", "do_c2_exec", "do_c2_loot"}
    assert re.search(r"isatty", (_ROOT / "lazyown.py").read_text()), "loop-safe input guards required"


def test_credentials_file_sync_writes_live_creds(tmp_path: Path) -> None:
    """c2_server start publishes live creds where the shell looks for them."""
    from modules import c2_agent as _agent

    target = tmp_path / ".c2_credentials.txt"
    monkeypatch_target = _agent._CREDENTIALS_FILE
    try:
        _agent._CREDENTIALS_FILE = target
        _agent._sync_credentials_file("labop", "s3cret!")
        content = target.read_text(encoding="utf-8")
        assert "USERNAME=labop" in content and "PASSWORD=s3cret!" in content
    finally:
        _agent._CREDENTIALS_FILE = monkeypatch_target
    import os as _os
    import stat as _stat

    assert _stat.S_IMODE(_os.stat(target).st_mode) == 0o600


def test_shell_sync_runs_after_params_exist() -> None:
    """Guard the historical bug: _sync before self.params was dead code."""
    import inspect as _inspect

    import lazyown as _lazyown

    source, start = _inspect.getsourcelines(_lazyown.LazyOwnShell.__init__)
    params_line = next(i for i, ln in enumerate(source) if "self.params = {" in ln)
    sync_line = next(i for i, ln in enumerate(source) if "_sync_c2_credentials()" in ln)
    assert sync_line > params_line, "sync must run after self.params exists"


def test_shell_sync_adopts_file_creds(tmp_path: Path, monkeypatch) -> None:
    """Shell adopts .c2_credentials.txt creds into auth + params + payload."""
    import lazyown as _lazyown

    creds = tmp_path / ".c2_credentials.txt"
    creds.write_text("USERNAME=labop\nPASSWORD=s3cret!\n", encoding="utf-8")
    saved: dict = {}

    class _Stub:
        path = str(tmp_path)
        params = {"c2_user": "admin", "c2_pass": "old"}

        def __init__(self) -> None:
            self.c2_auth = ("admin", "old")

    monkeypatch.setattr(_lazyown, "load_payload", lambda: saved)
    monkeypatch.setattr("core.config.save_payload", lambda p, path=None: saved.update(p))
    stub = _Stub()
    saved.update({"rhost": "1.2.3.4", "lhost": "5.6.7.8"})
    _lazyown.LazyOwnShell._sync_c2_credentials(stub)
    assert stub.c2_auth == ("labop", "s3cret!")
    assert saved.get("c2_user") == "labop"


def test_sync_refuses_keyless_payload(tmp_path: Path, monkeypatch) -> None:
    """_sync never persists when the loaded payload lacks core keys."""
    import lazyown as _lazyown

    creds = tmp_path / ".c2_credentials.txt"
    creds.write_text("USERNAME=labop\nPASSWORD=s3cret!\n", encoding="utf-8")

    class _Stub:
        path = str(tmp_path)
        params = {"c2_user": "admin", "c2_pass": "old"}

        def __init__(self) -> None:
            self.c2_auth = ("admin", "old")

    monkeypatch.setattr(_lazyown, "load_payload", lambda: {"c2_user": "x"})
    saved: list = []
    monkeypatch.setattr("core.config.save_payload", lambda p, path=None: saved.append(dict(p)))
    stub = _Stub()
    _lazyown.LazyOwnShell._sync_c2_credentials(stub)
    assert saved == [], "must not persist a key-less payload"


def test_c2_session_commands_are_non_interactive() -> None:
    """Loop-safety invariant: session commands never block on input()."""
    import ast as _ast

    tree = _ast.parse((_ROOT / "cli" / "commands" / "c2_session.py").read_text(encoding="utf-8"))
    for node in _ast.walk(tree):
        if isinstance(node, _ast.FunctionDef) and node.name.startswith("do_c2_"):
            src = _ast.get_source_segment(
                (_ROOT / "cli" / "commands" / "c2_session.py").read_text(encoding="utf-8"), node
            ) or ""
            assert "input(" not in src, f"{node.name} must never prompt"


def test_c2_reboot_registered() -> None:
    """c2_reboot exists with operator-facing usage docs."""
    import ast as _ast

    tree = _ast.parse((_ROOT / "cli" / "commands" / "c2_session.py").read_text(encoding="utf-8"))
    names = {n.name for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)}
    assert "do_c2_reboot" in names


def test_fresh_lab_creds_rotate_and_shape() -> None:
    """Rotated lab creds are unique per call and shell-safe."""
    import sys as _sys

    _sys.path.insert(0, str(_ROOT / "cli" / "commands"))
    import importlib as _importlib

    _mod = _importlib.import_module("c2_session")
    first = _mod._fresh_lab_creds()
    second = _mod._fresh_lab_creds()
    assert first != second
    for user, password in (first, second):
        assert len(user) == 12 and set(user) <= set("abcdefghijklmnopqrstuvwxyz0123456789")
        assert len(password) == 20
        assert not (set(password) & set(";|&$()`{}!><*?~#\\'\"\n\r \t:"))
