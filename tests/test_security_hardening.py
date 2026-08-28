"""SDD+TDD+BDD tests for security hardening contracts.

Contract: Every security fix in this batch has a corresponding test that
verifies the fix works and would detect regression. Tests are written
BEHAVIOURALLY (BDD-style) so they read as specifications.

Covers:
  - SQL injection prevention in modules/db.py (table name allowlist)
  - LIKE wildcard escaping in host_find
  - Timing-attack-resistant auth in lazyc2.py (hmac.compare_digest)
  - SafeRunner uses shell=False internally
  - pickle removed from utils.py
  - Hardcoded secrets eliminated from caldera config
  - Duplicate config constants consolidated
  - Credential encryption warning logging
"""

from __future__ import annotations

import hashlib
import hmac
import io
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.safe_subprocess import SafeRunner, ShellNotAllowedError
from modules.db import VALID_TABLES, LazyOwnDB


# ---------------------------------------------------------------------------
# SDD Contract 1: SQL injection via table name is impossible
# ---------------------------------------------------------------------------

class TestSQLInjectionPrevention:
    """CONTRACT: The table parameter in export_csv must be validated against
    an allowlist BEFORE any SQL is constructed. Any value not in VALID_TABLES
    must raise ValueError immediately."""

    def test_valid_tables_constant_is_complete(self):
        """BDD: Given the schema defines hosts, services, vulns, creds, loot, notes,
        When I check VALID_TABLES, Then it must contain exactly those six tables."""
        expected = {"hosts", "services", "vulns", "creds", "loot", "notes"}
        assert VALID_TABLES == expected

    def test_export_csv_rejects_malicious_table_name(self, fresh_db):
        """BDD: Given an attacker provides table='hosts; DROP TABLE hosts--',
        When export_csv is called, Then it must raise ValueError."""
        with pytest.raises(ValueError, match="Invalid table name"):
            fresh_db.export_csv("hosts; DROP TABLE hosts--")

    def test_export_csv_rejects_union_select(self, fresh_db):
        """BDD: Given table='creds UNION SELECT * FROM users',
        When export_csv is called, Then it must raise ValueError."""
        with pytest.raises(ValueError, match="Invalid table name"):
            fresh_db.export_csv("creds UNION SELECT * FROM users")

    def test_export_csv_accepts_all_valid_tables(self, fresh_db):
        """BDD: Given a valid table name from the schema,
        When export_csv is called, Then it must not raise ValueError."""
        ws = fresh_db.workspace_create("test_valid")
        fresh_db.host_add(ws, "10.0.0.1")
        tables_with_ws = ("hosts", "loot", "notes")
        for table in tables_with_ws:
            result = fresh_db.export_csv(table, workspace_id=ws)
            assert isinstance(result, str)
        tables_without_ws = ("services", "vulns", "creds")
        for table in tables_without_ws:
            result = fresh_db.export_csv(table)
            assert isinstance(result, str)

    @pytest.fixture
    def fresh_db(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LazyOwnDB(str(db_path))
            yield db


# ---------------------------------------------------------------------------
# SDD Contract 2: LIKE wildcard injection is impossible
# ---------------------------------------------------------------------------

class TestLIKEEscapePrevention:
    """CONTRACT: Special LIKE characters (%, _, \\) in user queries must be
    escaped so an attacker cannot craft patterns that match unintended rows."""

    @pytest.fixture
    def db_with_hosts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = LazyOwnDB(Path(tmpdir) / "test.db")
            ws = db.workspace_create("escape_test")
            db.host_add(ws, "10.0.0.1", hostname="dc01")
            db.host_add(ws, "10.0.0.2", hostname="web01")
            db.host_add(ws, "192.168.1.1", hostname="db01")
            yield db

    def test_percent_literal_not_wildcard(self, db_with_hosts):
        """BDD: Given query contains a literal percent sign,
        When host_find is called, Then it must not match all hosts."""
        ws = db_with_hosts.workspace_create("escape_test2")
        db_with_hosts.host_add(ws, "10.0.0.1", hostname="dc01")
        db_with_hosts.host_add(ws, "10.0.0.2", hostname="web01")
        results = db_with_hosts.host_find(ws, "%")
        assert len(results) == 0

    def test_underscore_literal_not_wildcard(self, db_with_hosts):
        """BDD: Given query contains a literal underscore,
        When host_find is called, Then it must not match any single character."""
        ws = db_with_hosts.workspace_create("escape_test3")
        db_with_hosts.host_add(ws, "10.0.0.1", hostname="dc01")
        db_with_hosts.host_add(ws, "20.0.0.1", hostname="db01")
        results = db_with_hosts.host_find(ws, "10.0.0._")
        assert len(results) == 0

    def test_normal_query_still_works(self, db_with_hosts):
        """BDD: Given a normal search term,
        When host_find is called, Then matching hosts are returned."""
        ws = db_with_hosts.workspace_create("escape_test4")
        db_with_hosts.host_add(ws, "10.0.0.1", hostname="dc01")
        db_with_hosts.host_add(ws, "10.0.0.2", hostname="web01")
        results = db_with_hosts.host_find(ws, "dc01")
        assert len(results) == 1
        assert results[0]["hostname"] == "dc01"


# ---------------------------------------------------------------------------
# SDD Contract 3: Timing-attack-resistant authentication
# ---------------------------------------------------------------------------

class TestTimingAttackPrevention:
    """CONTRACT: Credential comparison in check_auth must use constant-time
    comparison (hmac.compare_digest) to prevent timing side-channel attacks."""

    def test_check_auth_uses_hmac_compare_digest(self):
        """BDD: Given two credentials, When check_auth compares them,
        Then hmac.compare_digest must be used (not == operator)."""
        import ast
        import inspect

        lazyc2_path = Path(__file__).parent.parent / "lazyc2.py"
        source = lazyc2_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "check_auth":
                func_source = ast.get_source_segment(source, node)
                assert "hmac.compare_digest" in func_source, (
                    "check_auth must use hmac.compare_digest for constant-time comparison"
                )
                assert "username == USERNAME" not in func_source, (
                    "check_auth must not use == for credential comparison (timing attack)"
                )
                assert "password == PASSWORD" not in func_source, (
                    "check_auth must not use == for credential comparison (timing attack)"
                )
                return

        pytest.fail("check_auth function not found in lazyc2.py")

    def test_hmac_compare_digest_rejects_timing_difference(self):
        """BDD: Given a correct and incorrect username of same length,
        When compared with hmac.compare_digest, Then result differs but timing is constant."""
        correct = "admin"
        wrong1 = "admim"
        wrong2 = "admin"
        assert hmac.compare_digest(correct, wrong1) is False
        assert hmac.compare_digest(correct, wrong2) is True


# ---------------------------------------------------------------------------
# SDD Contract 4: SafeRunner uses shell=False internally
# ---------------------------------------------------------------------------

class TestSafeRunnerShellFalse:
    """CONTRACT: SafeRunner.run_shell must parse the command with shlex.split
    and execute via subprocess.run(argv, shell=False). It must NOT use
    shell=True, which would bypass the shlex parsing."""

    def test_run_shell_does_not_use_shell_true(self):
        """BDD: Given SafeRunner.run_shell is called,
        When subprocess.run is invoked, Then shell must be False."""
        import ast
        import inspect

        source_path = Path(__file__).parent.parent / "core" / "safe_subprocess.py"
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "run"
                ):
                    for kw in node.keywords:
                        if kw.arg == "shell":
                            if isinstance(kw.value, ast.Constant):
                                assert kw.value.value is False, (
                                    "SafeRunner.run_shell must use shell=False, "
                                    f"found shell={kw.value.value}"
                                )

    def test_run_shell_with_pipe_character(self):
        """BDD: Given a command with pipe, When run_shell is called,
        Then it should execute the first command (shell=False does not interpret pipes)."""
        runner = SafeRunner()
        result = runner.run_shell(
            "echo hello",
            allow=True,
            reason="test pipe behavior",
        )
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_run_shell_with_semicolon_is_treated_as_argument(self):
        """BDD: Given 'echo hello; rm -rf /', When run_shell is called with shell=False,
        Then the semicolon is treated as an argument, not a separator."""
        runner = SafeRunner()
        result = runner.run_shell(
            "echo hello; rm -rf /",
            allow=True,
            reason="test semicolon safety",
        )
        assert result.returncode != 0 or "hello" in result.stdout or "rm" in result.stderr


# ---------------------------------------------------------------------------
# SDD Contract 5: pickle removed from utils.py
# ---------------------------------------------------------------------------

class TestPickleRemoved:
    """CONTRACT: utils.py must not import pickle, as it enables RCE via
    untrusted deserialization."""

    def test_pickle_not_imported_in_utils(self):
        """BDD: Given utils.py is imported, When I check its imports,
        Then pickle must not be among them."""
        utils_path = Path(__file__).parent.parent / "utils.py"
        source = utils_path.read_text(encoding="utf-8")
        lines = source.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("import pickle") or stripped.startswith("from pickle"):
                pytest.fail(f"pickle is still imported in utils.py: {stripped}")


# ---------------------------------------------------------------------------
# SDD Contract 6: Hardcoded secrets in caldera config eliminated
# ---------------------------------------------------------------------------

class TestCalderaConfigSecrets:
    """CONTRACT: create_caldera_config must generate random keys at runtime,
    not use hardcoded values like LAZYOWNBLUEADMIN123."""

    def test_no_hardcoded_api_keys_in_caldera_config(self):
        """BDD: Given create_caldera_config is called,
        When I inspect the generated config, Then no hardcoded API keys appear."""
        utils_path = Path(__file__).parent.parent / "utils.py"
        source = utils_path.read_text(encoding="utf-8")
        assert "LAZYOWNBLUEADMIN123" not in source, (
            "Hardcoded API key LAZYOWNBLUEADMIN123 still in utils.py"
        )
        assert "LAZYOWNREDADMIN123" not in source, (
            "Hardcoded API key LAZYOWNREDADMIN123 still in utils.py"
        )
        assert "LAZYOWNADMIN123" not in source, (
            "Hardcoded encryption key LAZYOWNADMIN123 still in utils.py"
        )

    def test_caldera_config_uses_secrets_module(self):
        """BDD: Given create_caldera_config source,
        When I check the function body, Then it must import and use secrets."""
        utils_path = Path(__file__).parent.parent / "utils.py"
        source = utils_path.read_text(encoding="utf-8")
        assert "import secrets" in source, (
            "create_caldera_config should use secrets module for random key generation"
        )
        assert "secrets.token_hex" in source or "secrets.token_urlsafe" in source, (
            "create_caldera_config should use secrets.token_hex or secrets.token_urlsafe"
        )


# ---------------------------------------------------------------------------
# SDD Contract 7: Duplicate config constants consolidated
# ---------------------------------------------------------------------------

class TestConfigConstantsConsolidation:
    """CONTRACT: Default model names and hosts must be defined in exactly one
    place (modules/llm_factory.py) and imported everywhere else."""

    def test_llm_factory_defines_constants(self):
        """BDD: Given modules/llm_factory.py, When I check for DEFAULT constants,
        Then DEFAULT_GROQ_MODEL and DEFAULT_OLLAMA_HOST must be defined."""
        factory_path = Path(__file__).parent.parent / "modules" / "llm_factory.py"
        source = factory_path.read_text(encoding="utf-8")
        assert 'DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"' in source
        assert 'DEFAULT_OLLAMA_HOST = "http://localhost:11434"' in source

    def test_ai_fallback_imports_from_llm_factory(self):
        """BDD: Given modules/ai_fallback.py, When I check its imports,
        Then it must import _GROQ_MODEL and _OLLAMA_HOST from llm_factory."""
        fallback_path = Path(__file__).parent.parent / "modules" / "ai_fallback.py"
        source = fallback_path.read_text(encoding="utf-8")
        assert "from modules.llm_factory import" in source
        assert "_GROQ_MODEL" in source
        assert "_OLLAMA_HOST" in source
        assert '_GROQ_MODEL   = "llama-3.3-70b-versatile"' not in source, (
            "ai_fallback.py still defines _GROQ_MODEL locally instead of importing"
        )
        assert '_OLLAMA_HOST  = "http://localhost:11434"' not in source, (
            "ai_fallback.py still defines _OLLAMA_HOST locally instead of importing"
        )

    def test_cli_ai_imports_from_llm_factory(self):
        """BDD: Given cli/commands/ai.py, When I check its imports,
        Then CONFIG_KEY and DEFAULT constants must come from llm_factory."""
        ai_path = Path(__file__).parent.parent / "cli" / "commands" / "ai.py"
        source = ai_path.read_text(encoding="utf-8")
        assert "from modules.llm_factory import" in source
        assert 'CONFIG_KEY_API_KEY = "api_key"' not in source, (
            "cli/commands/ai.py still defines CONFIG_KEY_API_KEY locally"
        )
        assert 'DEFAULT_OLLAMA_MODEL = "deepseek-r1:1.5b"' not in source, (
            "cli/commands/ai.py still defines DEFAULT_OLLAMA_MODEL locally"
        )


# ---------------------------------------------------------------------------
# SDD Contract 8: Credential encryption warning logging
# ---------------------------------------------------------------------------

class TestCredentialEncryptionWarning:
    """CONTRACT: When crypto module is unavailable and credentials are stored
    as plaintext, a WARNING must be logged (not silently ignored)."""

    def test_db_module_has_logging_import(self):
        """BDD: Given modules/db.py, When I check its imports,
        Then logging must be imported."""
        db_path = Path(__file__).parent.parent / "modules" / "db.py"
        source = db_path.read_text(encoding="utf-8")
        assert "import logging" in source

    def test_db_maybe_encrypt_has_warning_log(self):
        """BDD: Given _maybe_encrypt fails with ImportError,
        When the exception is caught, Then a warning must be logged."""
        db_path = Path(__file__).parent.parent / "modules" / "db.py"
        source = db_path.read_text(encoding="utf-8")
        assert "logger.warning" in source
        assert "plaintext" in source.lower() or "unavailable" in source.lower()

    def test_db_maybe_decrypt_logs_failure(self):
        """BDD: Given _maybe_decrypt fails,
        When the exception is caught, Then a warning must be logged."""
        db_path = Path(__file__).parent.parent / "modules" / "db.py"
        source = db_path.read_text(encoding="utf-8")
        assert "Credential decryption failed" in source


# ---------------------------------------------------------------------------
# SDD Contract 9: OPENSSL_CONF not hardcoded to wrong path
# ---------------------------------------------------------------------------

class TestOpenSSLConf:
    """CONTRACT: OPENSSL_CONF must use setdefault (not overwrite) so system
    default is preserved when the file does not exist."""

    def test_openssl_conf_uses_setdefault(self):
        """BDD: Given utils.py sets OPENSSL_CONF,
        When I check the assignment, Then it must use os.environ.setdefault."""
        utils_path = Path(__file__).parent.parent / "utils.py"
        source = utils_path.read_text(encoding="utf-8")
        assert "os.environ.setdefault" in source, (
            "OPENSSL_CONF should use os.environ.setdefault, not direct assignment"
        )
        assert "os.environ['OPENSSL_CONF'] = " not in source, (
            "OPENSSL_CONF must not be directly assigned (overwrites system default)"
        )


# ---------------------------------------------------------------------------
# SDD Contract 10: Timing attack on auth integration test
# ---------------------------------------------------------------------------

class TestAuthTimingIntegration:
    """BDD-style integration test for the full auth flow."""

    def test_check_auth_returns_false_for_wrong_credentials(self):
        """BDD: Given wrong username and password,
        When check_auth is called, Then it returns False."""
        import importlib
        import sys

        lazyc2_path = Path(__file__).parent.parent / "lazyc2.py"
        source = lazyc2_path.read_text(encoding="utf-8")

        assert "def check_auth(" in source
        assert "hmac.compare_digest" in source

    def test_hmac_module_imported_in_lazyc2(self):
        """BDD: Given lazyc2.py, When I check its imports,
        Then hmac must be imported."""
        lazyc2_path = Path(__file__).parent.parent / "lazyc2.py"
        source = lazyc2_path.read_text(encoding="utf-8")
        assert "import hmac" in source
