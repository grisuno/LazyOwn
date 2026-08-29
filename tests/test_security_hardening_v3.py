"""Security hardening tests — SDD+TDD+BDD for all boy-scout fixes.

Contract: every fix from the security audit must have a test that:
1. Validates the vulnerable pattern is eliminated (red-green).
2. Confirms the safe alternative behaves correctly.
3. Covers edge cases (empty input, special chars, traversal attempts).

Run: pytest tests/test_security_hardening_v3.py -v
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


class TestSafeSubprocessRun:
    """BDD: GIVEN a command to run, WHEN using safe_subprocess_run,
    THEN it must never invoke a shell and must reject null bytes."""

    def test_rejects_empty_argv(self):
        from core.hardening import safe_subprocess_run
        with pytest.raises(ValueError):
            safe_subprocess_run([])

    def test_rejects_null_bytes(self):
        from core.hardening import safe_subprocess_run, SecurityViolation
        with pytest.raises(SecurityViolation, match="Null byte"):
            safe_subprocess_run(["echo", "hello\x00world"])

    def test_runs_command_without_shell(self):
        from core.hardening import safe_subprocess_run
        result = safe_subprocess_run(["echo", "hello"])
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_captures_stderr(self):
        from core.hardening import safe_subprocess_run
        result = safe_subprocess_run(["ls", "/nonexistent_path_xyz"])
        assert result.returncode != 0
        assert len(result.stderr) > 0

    def test_shell_false_enforced(self):
        from core.hardening import safe_subprocess_run
        import unittest.mock as mock
        with mock.patch("core.hardening.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            safe_subprocess_run(["echo", "test"], reason="unit test")
            call_kwargs = m.call_args[1]
            assert call_kwargs.get("shell") is False

    def test_returns_completed_process_fields(self):
        from core.hardening import safe_subprocess_run
        result = safe_subprocess_run(["echo", "test"])
        assert hasattr(result, "returncode")
        assert hasattr(result, "stdout")
        assert hasattr(result, "stderr")
        assert isinstance(result.returncode, int)

    def test_timeout_passed_through(self):
        from core.hardening import safe_subprocess_run
        import unittest.mock as mock
        with mock.patch("core.hardening.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            safe_subprocess_run(["echo", "x"], timeout=42)
            call_kwargs = m.call_args[1]
            assert call_kwargs["timeout"] == 42

    def test_capture_output_default_true(self):
        from core.hardening import safe_subprocess_run
        import unittest.mock as mock
        with mock.patch("core.hardening.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            safe_subprocess_run(["echo", "x"])
            call_kwargs = m.call_args[1]
            assert call_kwargs["capture_output"] is True

    def test_check_false(self):
        from core.hardening import safe_subprocess_run
        import unittest.mock as mock
        with mock.patch("core.hardening.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            safe_subprocess_run(["echo", "x"])
            call_kwargs = m.call_args[1]
            assert call_kwargs["check"] is False

    def test_text_mode_enabled(self):
        from core.hardening import safe_subprocess_run
        import unittest.mock as mock
        with mock.patch("core.hardening.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            safe_subprocess_run(["echo", "x"])
            call_kwargs = m.call_args[1]
            assert call_kwargs["text"] is True


class TestSafeClipboardCopy:
    """BDD: GIVEN content to copy, WHEN using safe_clipboard_copy,
    THEN it uses subprocess list-form and rejects oversized content."""

    def test_rejects_oversized_content(self):
        from core.hardening import safe_clipboard_copy, SecurityViolation
        with pytest.raises(SecurityViolation, match="exceeds"):
            safe_clipboard_copy("x" * 100000)

    def test_returns_false_without_clipboard_tool(self):
        from core.hardening import safe_clipboard_copy
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = safe_clipboard_copy("test content")
            assert result is False


class TestBuildSshpassCommand:
    """BDD: GIVEN ssh credentials, WHEN building sshpass command,
    THEN it must use -e flag and never expose password."""

    def test_uses_e_flag_not_p(self):
        from core.hardening import build_sshpass_command
        cmd = build_sshpass_command("secretpass", ["ssh", "user@host"])
        assert cmd[0] == "sshpass"
        assert cmd[1] == "-e"
        assert "secretpass" not in " ".join(cmd)

    def test_rejects_oversized_password(self):
        from core.hardening import build_sshpass_command, SecurityViolation
        with pytest.raises(SecurityViolation, match="exceeds maximum"):
            build_sshpass_command("x" * 300, ["ssh", "user@host"])

    def test_rejects_null_bytes_in_password(self):
        from core.hardening import build_sshpass_command, SecurityViolation
        with pytest.raises(SecurityViolation, match="Null byte"):
            build_sshpass_command("pass\x00word", ["ssh", "user@host"])


class TestSetSshpassEnv:
    """BDD: GIVEN a password, WHEN setting sshpass env,
    THEN SSHPASS is set and null bytes are rejected."""

    def test_sets_ssplash_env(self):
        from core.hardening import set_sshpass_env
        env = set_sshpass_env("testpass")
        assert env.get("SSHPASS") == "testpass"

    def test_preserves_existing_env(self):
        from core.hardening import set_sshpass_env
        env = set_sshpass_env("testpass")
        assert "PATH" in env

    def test_rejects_null_bytes(self):
        from core.hardening import set_sshpass_env, SecurityViolation
        with pytest.raises(SecurityViolation, match="Null byte"):
            set_sshpass_env("pass\x00word")


class TestEscapeHtmlContent:
    """BDD: GIVEN user-controlled data, WHEN escaping for HTML,
    THEN special characters are properly escaped."""

    def test_escapes_script_tags(self):
        from core.hardening import escape_html_content
        result = escape_html_content('<script>alert("xss")</script>')
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_escapes_quotes(self):
        from core.hardening import escape_html_content
        result = escape_html_content('value" onclick="alert(1)')
        assert "&quot;" in result
        assert "onclick" in result

    def test_preserves_safe_content(self):
        from core.hardening import escape_html_content
        result = escape_html_content("hello world 123")
        assert result == "hello world 123"

    def test_handles_empty_string(self):
        from core.hardening import escape_html_content
        result = escape_html_content("")
        assert result == ""


class TestSafePathJoin:
    """BDD: GIVEN a base dir and user path, WHEN joining safely,
    THEN path traversal is blocked."""

    def test_allows_safe_paths(self, tmp_path):
        from core.hardening import safe_path_join
        result = safe_path_join(str(tmp_path), "subdir/file.txt")
        assert result.startswith(str(tmp_path))

    def test_blocks_traversal(self, tmp_path):
        from core.hardening import safe_path_join, SecurityViolation
        with pytest.raises(SecurityViolation, match="Path traversal"):
            safe_path_join(str(tmp_path), "../../../etc/passwd")

    def test_blocks_symlink_escape(self, tmp_path):
        from core.hardening import safe_path_join, SecurityViolation
        symlink = tmp_path / "escape_link"
        symlink.symlink_to("/etc")
        with pytest.raises(SecurityViolation, match="Path traversal"):
            safe_path_join(str(tmp_path), "escape_link/passwd")

    def test_rejects_empty_path(self, tmp_path):
        from core.hardening import safe_path_join
        with pytest.raises(ValueError):
            safe_path_join(str(tmp_path), "")


class TestValidateNetworkCidr:
    """BDD: GIVEN a network CIDR, WHEN validating,
    THEN only valid notation is accepted."""

    def test_accepts_valid_cidr(self):
        from core.hardening import validate_network_cidr
        assert validate_network_cidr("192.168.1.0/24") is True
        assert validate_network_cidr("10.0.0.0/8") is True

    def test_rejects_invalid_cidr(self):
        from core.hardening import validate_network_cidr
        assert validate_network_cidr("not_a_cidr") is False
        assert validate_network_cidr("999.999.999.999/24") is False

    def test_rejects_empty(self):
        from core.hardening import validate_network_cidr
        assert validate_network_cidr("") is False


class TestValidatePortSpec:
    """BDD: GIVEN a port specification, WHEN validating,
    THEN only valid formats are accepted."""

    def test_accepts_valid_ports(self):
        from core.hardening import validate_port_spec
        assert validate_port_spec("22") is True
        assert validate_port_spec("22,80,443") is True
        assert validate_port_spec("1-1024") is True

    def test_rejects_invalid_ports(self):
        from core.hardening import validate_port_spec
        assert validate_port_spec("abc") is False
        assert validate_port_spec("") is False


class TestValidateHost:
    """BDD: GIVEN a hostname or IP, WHEN validating,
    THEN only valid formats are accepted."""

    def test_accepts_valid_ip(self):
        from core.hardening import validate_host
        assert validate_host("192.168.1.1") is True

    def test_accepts_valid_hostname(self):
        from core.hardening import validate_host
        assert validate_host("example.com") is True

    def test_rejects_invalid(self):
        from core.hardening import validate_host
        assert validate_host("") is False
        assert validate_host("a" * 300) is False


class TestRequireEncryptionKey:
    """BDD: WHEN requiring an encryption key,
    THEN it must never fall back to a static default."""

    def test_raises_without_key(self):
        from core.hardening import require_encryption_key, SecurityViolation
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(SecurityViolation, match="Encryption key required"):
                require_encryption_key()

    def test_reads_from_env(self):
        from core.hardening import require_encryption_key
        with patch.dict(os.environ, {"TEST_KEY": "my-secret"}):
            result = require_encryption_key(env_key="TEST_KEY")
            assert result == "my-secret"

    def test_reads_from_file(self, tmp_path):
        from core.hardening import require_encryption_key
        key_file = tmp_path / ".secret_key"
        key_file.write_text("file-secret")
        result = require_encryption_key(env_key="NONEXISTENT", secret_file=key_file)
        assert result == "file-secret"


class TestSanitizeFilename:
    """BDD: GIVEN a filename, WHEN sanitizing,
    THEN dangerous characters are removed."""

    def test_removes_dangerous_chars(self):
        from core.hardening import sanitize_filename
        result = sanitize_filename("file; rm -rf / .txt")
        assert ";" not in result
        assert "rm" in result

    def test_handles_empty(self):
        from core.hardening import sanitize_filename
        result = sanitize_filename("")
        assert result == "unnamed"

    def test_truncates_long_names(self):
        from core.hardening import sanitize_filename
        result = sanitize_filename("a" * 300 + ".txt", max_length=255)
        assert len(result) <= 255


class TestPhishingOrchestratorKey:
    """BDD: GIVEN the phishing orchestrator,
    THEN it must require a proper encryption key."""

    def test_raises_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            from modules.phishing_orchestrator import _derive_credential_key
            from unittest.mock import patch as mock_patch
            from pathlib import Path
            with mock_patch.object(Path, "exists", return_value=False):
                with pytest.raises(RuntimeError, match="not configured"):
                    _derive_credential_key()

    def test_works_with_env_key(self):
        with patch.dict(os.environ, {"LAZYOWN_SECRET_KEY": "test-key-123"}):
            from modules.phishing_orchestrator import _derive_credential_key
            key = _derive_credential_key()
            assert len(key) > 0


class TestIcmpServerCommandExecution:
    """BDD: GIVEN a command for the ICMP server,
    THEN it must not use shell=True."""

    def test_execute_command_uses_list_form(self):
        with patch("modules.icmp_server.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess([], 0, stdout="ok", stderr="")
            from modules.icmp_server import execute_command
            execute_command("echo hello")
            args = mock_run.call_args
            assert args[1].get("shell") is False or (args[0] and isinstance(args[0][0], list))

    def test_handles_empty_command(self):
        from modules.icmp_server import execute_command
        result = execute_command("")
        assert "Empty command" in result

    def test_handles_invalid_command(self):
        from modules.icmp_server import execute_command
        result = execute_command("nonexistent_command_xyz_12345")
        assert len(result) > 0


class TestResourceScriptEngine:
    """BDD: GIVEN a resource script command,
    THEN it must not use shell=True."""

    def test_run_command_uses_list_form(self):
        from modules.resource_script import ScriptContext, ResourceScriptEngine
        executed = []
        ctx = ScriptContext(on_command=lambda cmd: executed.append(cmd))
        engine = ResourceScriptEngine(ctx)
        engine.ctx.run_command("echo test")
        assert len(executed) == 1
        assert "echo" in executed[0]


class TestPivotingCommands:
    """BDD: GIVEN pivoting operations,
    THEN shell=True must be eliminated from pivoting code."""

    def test_pivoting_module_has_no_shell_true(self):
        import ast
        base = Path(__file__).resolve().parent.parent
        target = base / "cli/commands/pivoting.py"
        if not target.exists():
            target = Path("/home/grisun0/LazyOwn/cli/commands/pivoting.py")
        with open(target) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    pytest.fail(f"shell=True found at line {node.lineno}")


class TestAntiForensicsCommands:
    """BDD: GIVEN anti-forensics operations,
    THEN shell=True must be eliminated from anti_forensics code."""

    def test_anti_forensics_has_no_shell_true(self):
        import ast
        base = Path(__file__).resolve().parent.parent
        target = base / "cli/commands/anti_forensics.py"
        if not target.exists():
            target = Path("/home/grisun0/LazyOwn/cli/commands/anti_forensics.py")
        with open(target) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    pytest.fail(f"shell=True found at line {node.lineno}")
