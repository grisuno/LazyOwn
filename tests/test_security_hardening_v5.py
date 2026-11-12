"""Security hardening v5: operator credential and channel contracts.

Covers the fixes for the follow-up review of the CVE-2026-68502 tree:
``/api/data`` must not leak live operator credentials, the web terminal
input handler must not touch the shell's unwritable ``stdin``, MFA-less
admin accounts must be loudly flagged at boot, health/metrics must gate
their detail, CLI-to-C2 HTTPS calls must not ship ``verify=False``, and
operator-supplied payload parameters must be shell-quoted.
"""

from __future__ import annotations

import ast
import os
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYC2_SRC = (REPO_ROOT / "lazyc2.py").read_text(encoding="utf-8")
LAZYOWN_SRC = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")
LAZYC2_TREE = ast.parse(LAZYC2_SRC)
LAZYOWN_TREE = ast.parse(LAZYOWN_SRC)


def _find(tree: ast.Module, name: str, kind=ast.FunctionDef):
    return next(
        node
        for node in ast.walk(tree)
        if isinstance(node, kind) and node.name == name
    )


def _route_decorators(tree: ast.Module) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        path = None
        decorators = set()
        for dec in node.decorator_list:
            if (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Attribute)
                and dec.func.attr == "route"
                and isinstance(dec.func.value, ast.Name)
                and dec.func.value.id == "app"
                and dec.args
                and isinstance(dec.args[0], ast.Constant)
            ):
                path = dec.args[0].value
            else:
                decorators.add(getattr(dec, "attr", getattr(dec, "id", "")))
        if path is not None:
            result[path] = decorators
    return result


class TestNoOperatorCredentialLeak:
    def test_api_data_inner_omits_username_password(self) -> None:
        inner = _find(LAZYC2_TREE, "_api_data_inner")
        assert not _has_jsonify_key(inner, "username"), "/api/data still emits the operator username"
        assert not _has_jsonify_key(inner, "password"), "/api/data still emits the operator password"

    def test_index_route_does_not_render_credentials(self) -> None:
        index = _find(LAZYC2_TREE, "index")
        for kw in ast.walk(index):
            if isinstance(kw, ast.keyword) and kw.arg in ("username", "password"):
                assert not (
                    isinstance(kw.value, ast.Name) and kw.value.id in ("USERNAME", "PASSWORD")
                ), f"index route still renders live operator {kw.arg}"

    def test_templates_do_not_embed_operator_password(self) -> None:
        for template in (REPO_ROOT / "templates").glob("*.html"):
            text = template.read_text(encoding="utf-8", errors="replace")
            assert "{{ password }}" not in text, f"{template.name} embeds operator password"
            assert "btoa(`${username}:${password}`)" not in text, (
                f"{template.name} builds Basic auth from embedded credentials"
            )


def _has_jsonify_key(func: ast.FunctionDef, key: str) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and k.value == key:
                    return True
    return False


class TestWebTerminalInputHandler:
    def test_handle_input_never_writes_shell_stdin(self) -> None:
        handler = _find(LAZYC2_TREE, "handle_input")
        src = ast.dump(handler)
        assert "stdin.write" not in src, "handle_input still writes to the shell's unwritable stdin"
        assert "stdin.seek" not in src

    def test_handle_input_keeps_one_cmd_and_guards(self) -> None:
        handler = _find(LAZYC2_TREE, "handle_input")
        src = ast.dump(handler)
        assert "one_cmd" in src
        assert "login_required" in {ast.dump(d) for d in handler.decorator_list} or any(
            "login_required" in ast.dump(d) for d in handler.decorator_list
        )


class TestAdminMfaWarning:
    def test_warn_admins_without_mfa_exists_and_runs_at_boot(self) -> None:
        warn = _find(LAZYC2_TREE, "_warn_admins_without_mfa")
        assert warn is not None
        assert "mfa_enabled" in ast.dump(warn)
        assert "_warn_admins_without_mfa()" in LAZYC2_SRC

    def test_boot_block_calls_both_bootstrap_and_warning(self) -> None:
        for node in ast.walk(LAZYC2_TREE):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == "_RUN_MAIN":
                calls = {
                    n.func.id
                    for n in ast.walk(node)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                }
                assert "_bootstrap_initial_admin" in calls
                assert "_warn_admins_without_mfa" in calls
                return
        raise AssertionError("no _RUN_MAIN boot block found")


class TestHealthMetricsGating:
    def test_health_and_metrics_stay_decorator_free(self) -> None:
        routes = _route_decorators(LAZYC2_TREE)
        for path in ("/health", "/metrics"):
            assert not (routes.get(path, set()) & {"requires_auth", "login_required", "requires_auth_or_session"})

    def test_metrics_gates_remote_callers(self) -> None:
        metrics = _find(LAZYC2_TREE, "metrics_exposition")
        src = ast.dump(metrics)
        assert "_is_local_request" in src
        assert "compare_digest" in src
        assert "c2_metrics_token" in LAZYC2_SRC

    def test_health_hides_detail_from_remote_callers(self) -> None:
        health = _find(LAZYC2_TREE, "health_check")
        assert "_is_local_request" in ast.dump(health)

    def test_is_local_request_exists(self) -> None:
        _find(LAZYC2_TREE, "_is_local_request")


class TestC2TlsVerification:
    def test_no_verify_false_in_operator_channels(self) -> None:
        for name, tree in (("lazyc2.py", LAZYC2_TREE), ("lazyown.py", LAZYOWN_TREE)):
            for node in ast.walk(tree):
                if isinstance(node, ast.keyword) and node.arg == "verify":
                    assert not (
                        isinstance(node.value, ast.Constant) and node.value.value is False
                    ), f"{name}: request issued with verify=False"

    def test_resolve_c2_tls_verify_pins_local_cert(self, tmp_path, monkeypatch) -> None:
        fn, payload_ref = _resolve_c2_tls_verify_fn()
        fake = types.SimpleNamespace()
        fake.__dict__["params"] = {}
        payload_ref["c2_tls_verify"] = "auto"
        monkeypatch.chdir(tmp_path)
        (tmp_path / "cert.pem").write_text("-----BEGIN CERTIFICATE-----\n")
        assert fn(fake) == str(tmp_path / "cert.pem")

    def test_resolve_c2_tls_verify_auto_falls_back_openly(self, tmp_path, monkeypatch) -> None:
        fn, payload_ref = _resolve_c2_tls_verify_fn()
        fake = types.SimpleNamespace()
        fake.__dict__["params"] = {}
        payload_ref["c2_tls_verify"] = "auto"
        monkeypatch.chdir(tmp_path)
        assert fn(fake) is False

    def test_resolve_c2_tls_verify_runtime_override_false(self, tmp_path, monkeypatch) -> None:
        fn, payload_ref = _resolve_c2_tls_verify_fn()
        fake = types.SimpleNamespace()
        fake.__dict__["params"] = {"c2_tls_verify": False}
        payload_ref["c2_tls_verify"] = True
        monkeypatch.chdir(tmp_path)
        assert fn(fake) is False

    def test_resolve_c2_tls_verify_payload_true_uses_system_store(self, tmp_path, monkeypatch) -> None:
        fn, payload_ref = _resolve_c2_tls_verify_fn()
        fake = types.SimpleNamespace()
        fake.__dict__["params"] = {}
        payload_ref["c2_tls_verify"] = True
        monkeypatch.chdir(tmp_path)
        assert fn(fake) is True

    def test_resolve_c2_tls_verify_payload_path(self, tmp_path, monkeypatch) -> None:
        fn, payload_ref = _resolve_c2_tls_verify_fn()
        fake = types.SimpleNamespace()
        fake.__dict__["params"] = {}
        ca_file = tmp_path / "custom_ca.pem"
        ca_file.write_text("-----BEGIN CERTIFICATE-----\n")
        payload_ref["c2_tls_verify"] = str(ca_file)
        monkeypatch.chdir(tmp_path)
        assert fn(fake) == str(ca_file)


def _resolve_c2_tls_verify_fn():
    """Exec the helper with a controllable ``load_payload`` mock.

    Returns:
        Tuple of (the function, a dict standing in for payload.json).
    """
    node = _find(LAZYOWN_TREE, "_resolve_c2_tls_verify")
    payload_ref: dict = {}
    namespace: dict = {
        "os": os,
        "print_warn": lambda *_: None,
        "load_payload": lambda: dict(payload_ref),
    }
    exec(
        compile(ast.Module(body=[node], type_ignores=[]), "<verify>", "exec"),
        namespace,
    )
    return namespace["_resolve_c2_tls_verify"], payload_ref


class TestPathHijackingQuoting:
    def test_binary_name_is_shell_quoted(self) -> None:
        fn = _find(LAZYOWN_TREE, "run_lazypathhijacking")
        quoted = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "quote"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "shlex"
            for node in ast.walk(fn)
        )
        assert quoted, "binary_name interpolated unquoted into shell commands"
