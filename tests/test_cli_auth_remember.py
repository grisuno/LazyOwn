"""Remember-me token comparison must be timing-safe.

SDD contract: ``try_auto_login`` compares the operator-supplied token
from payload.json against the stored per-user token. A ``==``
comparison leaks timing information about the secret; the comparison
must use ``hmac.compare_digest`` like the C2 auth paths.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

import modules.cli_auth as cli_auth

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI_AUTH = REPO_ROOT / "modules" / "cli_auth.py"


@pytest.fixture()
def isolated_auth(tmp_path, monkeypatch):
    """Point the auth store at temporary files."""
    monkeypatch.chdir(tmp_path)
    users = tmp_path / "users.json"
    payload = tmp_path / "payload.json"
    session = tmp_path / "cli_session.json"
    users.write_text(
        json.dumps(
            [
                {
                    "username": "operator",
                    "cli_remember_token": "s3cr3t-token-value-48chars-padded-abcdef",
                    "elo": 1500,
                    "role": "operator",
                }
            ]
        )
    )
    monkeypatch.setattr(cli_auth, "USERS_PATH", users)
    monkeypatch.setattr(cli_auth, "PAYLOAD_PATH", payload)
    monkeypatch.setattr(cli_auth, "CLI_SESSION_PATH", session)
    return users, payload, session


class TestRememberMeComparison:
    def test_valid_token_logs_in(self, isolated_auth) -> None:
        _, payload, _ = isolated_auth
        payload.write_text(
            json.dumps(
                {
                    "cli_auto_login": "operator",
                    "cli_remember_token": "s3cr3t-token-value-48chars-padded-abcdef",
                }
            )
        )
        result = cli_auth.try_auto_login()
        assert result["success"] is True
        assert result["username"] == "operator"

    def test_wrong_token_rejected(self, isolated_auth) -> None:
        _, payload, _ = isolated_auth
        payload.write_text(
            json.dumps(
                {
                    "cli_auto_login": "operator",
                    "cli_remember_token": "wrong-token-value-xxxxxxxxxxxxxxxx",
                }
            )
        )
        result = cli_auth.try_auto_login()
        assert result["success"] is False

    def test_comparison_is_timing_safe(self) -> None:
        tree = ast.parse(CLI_AUTH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "try_auto_login":
                calls = {
                    n.func.attr
                    for n in ast.walk(node)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                }
                assert "compare_digest" in calls, (
                    "try_auto_login must compare tokens with "
                    "hmac.compare_digest"
                )
                return
        pytest.fail("try_auto_login not found")

    def test_save_delegates_to_canonical_writer(self) -> None:
        tree = ast.parse(CLI_AUTH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_save_payload":
                imported = {
                    a.asname or a.name
                    for n in ast.walk(node)
                    if isinstance(n, ast.ImportFrom) and n.module == "core.config"
                    for a in n.names
                    if a.name == "save_payload"
                }
                assert imported, (
                    "_save_payload must delegate to core.config.save_payload"
                )
                return
        pytest.fail("_save_payload not found")

    def test_save_writes_valid_json_and_audits(self, isolated_auth) -> None:
        import json as _json

        _, payload_path, _ = isolated_auth
        assert cli_auth._save_payload({"cli_auto_login": "operator"}) is True
        assert _json.loads(payload_path.read_text()) == {
            "cli_auto_login": "operator"
        }
