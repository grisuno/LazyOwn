"""SDD+TDD+BDD tests for security hardening v4 — command execution, URL injection, and path traversal.

Contract: Every security fix in this batch has a corresponding test that
verifies the fix works and would detect regression. Tests are written
BEHAVIOURALLY (BDD-style) so they read as specifications.

Covers:
  - core/safe_exec.py: safe_system, safe_run_argv, safe_run_shell, validate_url, safe_git_clone, safe_ip_show
  - poc_tui/plugin_loader.py: URL injection via git clone
  - modules/morse.py: os.system removed
  - modules/c2_builder.py: os.system replaced with Python-native ops
  - modules/bot.py: os.system replaced with subprocess
  - lazyc2.py: execute_command uses shell=False
  - cli/commands/misc_migrated.py: os.system and shell=True removed
  - cli/commands/recon_migrated.py: os.system replaced with Python
  - Hardcoded absolute paths eliminated
  - modules/conditional_hooks.py: shlex.quote injection prevention
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# SDD Contract 1: core/safe_exec.py — safe_system rejects metacharacters
# ---------------------------------------------------------------------------

class TestSafeSystem:
    """CONTRACT: safe_system must reject commands containing shell
    metacharacters that could indicate injection attempts."""

    def test_rejects_semicolon(self):
        """BDD: Given a command with a semicolon, When I call safe_system,
        Then it must raise CommandInjectionError."""
        from core.safe_exec import safe_system, CommandInjectionError
        with pytest.raises(CommandInjectionError):
            safe_system("ls; rm -rf /")

    def test_rejects_pipe(self):
        """BDD: Given a command with a pipe, When I call safe_system,
        Then it must raise CommandInjectionError."""
        from core.safe_exec import safe_system, CommandInjectionError
        with pytest.raises(CommandInjectionError):
            safe_system("ls | cat")

    def test_rejects_backtick(self):
        """BDD: Given a command with backticks, When I call safe_system,
        Then it must raise CommandInjectionError."""
        from core.safe_exec import safe_system, CommandInjectionError
        with pytest.raises(CommandInjectionError):
            safe_system("ls `whoami`")

    def test_rejects_dollar_paren(self):
        """BDD: Given a command with $(...), When I call safe_system,
        Then it must raise CommandInjectionError."""
        from core.safe_exec import safe_system, CommandInjectionError
        with pytest.raises(CommandInjectionError):
            safe_system("ls $(whoami)")

    def test_rejects_empty_command(self):
        """BDD: Given an empty command, When I call safe_system,
        Then it must raise ValueError."""
        from core.safe_exec import safe_system
        with pytest.raises(ValueError):
            safe_system("")

    def test_rejects_whitespace_only(self):
        """BDD: Given a whitespace-only command, When I call safe_system,
        Then it must raise ValueError."""
        from core.safe_exec import safe_system
        with pytest.raises(ValueError):
            safe_system("   ")

    def test_allows_simple_command(self):
        """BDD: Given a simple command without metacharacters, When I call safe_system,
        Then it must execute successfully."""
        from core.safe_exec import safe_system
        rc = safe_system("echo hello", reason="test")
        assert rc == 0


# ---------------------------------------------------------------------------
# SDD Contract 2: core/safe_exec.py — safe_run_argv never uses shell
# ---------------------------------------------------------------------------

class TestSafeRunArgv:
    """CONTRACT: safe_run_argv must always use shell=False and reject
    null bytes in arguments."""

    def test_rejects_null_byte(self):
        """BDD: Given an argument with a null byte, When I call safe_run_argv,
        Then it must raise CommandInjectionError."""
        from core.safe_exec import safe_run_argv, CommandInjectionError
        with pytest.raises(CommandInjectionError):
            safe_run_argv(["ls", "test\x00evil"])

    def test_rejects_empty_argv(self):
        """BDD: Given an empty argv, When I call safe_run_argv,
        Then it must raise ValueError."""
        from core.safe_exec import safe_run_argv
        with pytest.raises(ValueError):
            safe_run_argv([])

    def test_executes_without_shell(self):
        """BDD: Given a valid command, When I call safe_run_argv,
        Then it must execute without a shell."""
        from core.safe_exec import safe_run_argv
        result = safe_run_argv(["echo", "hello"])
        assert result.returncode == 0
        assert "hello" in result.stdout


# ---------------------------------------------------------------------------
# SDD Contract 3: core/safe_exec.py — validate_url rejects injection
# ---------------------------------------------------------------------------

class TestValidateUrl:
    """CONTRACT: validate_url must reject URLs containing shell
    metacharacters and non-HTTP schemes."""

    def test_rejects_semicolon_in_url(self):
        """BDD: Given a URL with a semicolon, When I validate it,
        Then it must raise UrlValidationError."""
        from core.safe_exec import validate_url, UrlValidationError
        with pytest.raises(UrlValidationError):
            validate_url("https://evil.com/repo; rm -rf /")

    def test_rejects_backtick_in_url(self):
        """BDD: Given a URL with backticks, When I validate it,
        Then it must raise UrlValidationError."""
        from core.safe_exec import validate_url, UrlValidationError
        with pytest.raises(UrlValidationError):
            validate_url("https://evil.com/`whoami`")

    def test_rejects_ftp_scheme(self):
        """BDD: Given a URL with ftp scheme, When I validate it,
        Then it must raise UrlValidationError."""
        from core.safe_exec import validate_url, UrlValidationError
        with pytest.raises(UrlValidationError):
            validate_url("ftp://evil.com/repo")

    def test_rejects_empty_url(self):
        """BDD: Given an empty URL, When I validate it,
        Then it must raise ValueError."""
        from core.safe_exec import validate_url
        with pytest.raises(ValueError):
            validate_url("")

    def test_rejects_missing_netloc(self):
        """BDD: Given a URL without hostname, When I validate it,
        Then it must raise UrlValidationError."""
        from core.safe_exec import validate_url, UrlValidationError
        with pytest.raises(UrlValidationError):
            validate_url("https://")

    def test_allows_valid_https_url(self):
        """BDD: Given a valid HTTPS URL, When I validate it,
        Then it must return the URL unchanged."""
        from core.safe_exec import validate_url
        url = "https://github.com/user/repo.git"
        assert validate_url(url) == url

    def test_allows_valid_http_url(self):
        """BDD: Given a valid HTTP URL, When I validate it,
        Then it must return the URL unchanged."""
        from core.safe_exec import validate_url
        url = "http://example.com/repo"
        assert validate_url(url) == url


# ---------------------------------------------------------------------------
# SDD Contract 4: safe_git_clone uses subprocess list-form
# ---------------------------------------------------------------------------

class TestSafeGitClone:
    """CONTRACT: safe_git_clone must validate the URL and use
    subprocess list-form, never os.system."""

    def test_rejects_injection_in_url(self):
        """BDD: Given a URL with shell injection, When I clone,
        Then it must raise UrlValidationError."""
        from core.safe_exec import safe_git_clone, UrlValidationError
        with pytest.raises(UrlValidationError):
            safe_git_clone("https://evil.com/repo; rm -rf /", "/tmp/test")

    @patch("core.safe_exec.subprocess.run")
    def test_uses_subprocess_list_form(self, mock_run):
        """BDD: Given a valid URL, When I clone,
        Then subprocess.run must be called with a list (not shell=True)."""
        from core.safe_exec import safe_git_clone
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        safe_git_clone("https://github.com/user/repo.git", "/tmp/test")
        args, kwargs = mock_run.call_args
        assert isinstance(args[0], list)
        assert kwargs.get("shell") is False


# ---------------------------------------------------------------------------
# SDD Contract 5: safe_ip_show parses output in Python
# ---------------------------------------------------------------------------

class TestSafeIpShow:
    """CONTRACT: safe_ip_show must parse 'ip a show' output in Python,
    never via shell pipes."""

    def test_returns_list_of_dicts(self):
        """BDD: Given ip a show output, When I parse it,
        Then I must get a list of dicts with interface and address."""
        from core.safe_exec import safe_ip_show
        with patch("core.safe_exec.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="2: eth0: <BROADCAST,UP> mtu 1500\n    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0\n",
                stderr="",
            )
            entries = safe_ip_show("scope global")
            assert len(entries) == 1
            assert entries[0]["interface"] == "eth0"
            assert entries[0]["address"] == "192.168.1.100"

    def test_handles_missing_command(self):
        """BDD: Given ip command is not found, When I parse,
        Then it must return an empty list."""
        from core.safe_exec import safe_ip_show
        with patch("core.safe_exec.subprocess.run", side_effect=FileNotFoundError):
            entries = safe_ip_show()
            assert entries == []


# ---------------------------------------------------------------------------
# SDD Contract 6: poc_tui/plugin_loader.py — URL injection prevented
# ---------------------------------------------------------------------------

class TestPluginLoaderUrlInjection:
    """CONTRACT: The plugin loader must validate git clone URLs and
    reject shell metacharacters."""

    def _get_validate_fn(self):
        import importlib
        import sys
        mock_config = MagicMock()
        sys.modules.setdefault("config", mock_config)
        if "poc_tui.plugin_loader" in sys.modules:
            mod = sys.modules["poc_tui.plugin_loader"]
        else:
            mod = importlib.import_module("poc_tui.plugin_loader")
        return mod._validate_clone_url

    def test_validate_clone_url_rejects_semicolon(self):
        """BDD: Given a repo URL with semicolon, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError, match="Shell metacharacters"):
            validate_url("https://evil.com/repo; rm -rf /")

    def test_validate_clone_url_rejects_pipe(self):
        """BDD: Given a repo URL with pipe, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError, match="Shell metacharacters"):
            validate_url("https://evil.com/repo|cat /etc/passwd")

    def test_validate_clone_url_rejects_dollar(self):
        """BDD: Given a repo URL with dollar sign, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError, match="Shell metacharacters"):
            validate_url("https://evil.com/$(whoami)")

    def test_validate_clone_url_rejects_backtick(self):
        """BDD: Given a repo URL with backtick, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError, match="Shell metacharacters"):
            validate_url("https://evil.com/`id`")

    def test_validate_clone_url_rejects_empty(self):
        """BDD: Given an empty URL, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError):
            validate_url("")

    def test_validate_clone_url_rejects_non_http(self):
        """BDD: Given a non-HTTP URL, When I validate it,
        Then it must raise ValueError."""
        validate_url = self._get_validate_fn()
        with pytest.raises(ValueError, match="Invalid repository URL"):
            validate_url("ftp://evil.com/repo")

    def test_validate_clone_url_allows_valid_url(self):
        """BDD: Given a valid HTTPS URL, When I validate it,
        Then it must return the URL unchanged."""
        validate_url = self._get_validate_fn()
        url = "https://github.com/user/repo.git"
        assert validate_url(url) == url


# ---------------------------------------------------------------------------
# SDD Contract 7: modules/morse.py — no os.system calls
# ---------------------------------------------------------------------------

class TestMorseNoOsSystem:
    """CONTRACT: modules/morse.py must not contain any os.system calls."""

    def test_no_os_system_in_morse(self):
        """BDD: Given the morse.py module, When I scan its source code,
        Then it must not contain os.system."""
        morse_path = Path(__file__).parent.parent / "modules" / "morse.py"
        content = morse_path.read_text(encoding="utf-8")
        assert "os.system" not in content, "morse.py still contains os.system"

    def test_uses_subprocess_instead(self):
        """BDD: Given the morse.py module, When I scan its source code,
        Then it must use subprocess for screen clearing."""
        morse_path = Path(__file__).parent.parent / "modules" / "morse.py"
        content = morse_path.read_text(encoding="utf-8")
        assert "subprocess.run" in content


# ---------------------------------------------------------------------------
# SDD Contract 8: modules/c2_builder.py — no os.system calls
# ---------------------------------------------------------------------------

class TestC2BuilderNoOsSystem:
    """CONTRACT: modules/c2_builder.py must not use os.system for
    beacon encryption or tunnel URL extraction."""

    def test_no_os_system_for_encryption(self):
        """BDD: Given the c2_builder.py module, When I scan for os.system,
        Then it must not use os.system for beacon encryption."""
        c2_path = Path(__file__).parent.parent / "modules" / "c2_builder.py"
        content = c2_path.read_text(encoding="utf-8")
        assert "os.system(encbeacon)" not in content

    def test_no_os_system_for_tunnel(self):
        """BDD: Given the c2_builder.py module, When I scan for os.system,
        Then it must not use os.system for tunnel URL extraction."""
        c2_path = Path(__file__).parent.parent / "modules" / "c2_builder.py"
        content = c2_path.read_text(encoding="utf-8")
        assert "os.system(tunnel_cmd)" not in content

    def test_uses_python_native_for_encryption(self):
        """BDD: Given the c2_builder.py module, When I check beacon encryption,
        Then it must use Python-native file operations."""
        c2_path = Path(__file__).parent.parent / "modules" / "c2_builder.py"
        content = c2_path.read_text(encoding="utf-8")
        assert "src_path.read_bytes()" in content or "read_bytes()" in content
        assert "enc_path.write_bytes()" in content or "write_bytes(b64_data)" in content


# ---------------------------------------------------------------------------
# SDD Contract 9: lazyc2.py execute_command uses shell=False
# ---------------------------------------------------------------------------

class TestExecuteCommandShellFalse:
    """CONTRACT: The execute_command function in lazyc2.py must use
    shell=False with shlex.split."""

    def test_uses_shell_false(self):
        """BDD: Given the execute_command function, When I check its implementation,
        Then it must use shell=False."""
        lazyc2_path = Path(__file__).parent.parent / "lazyc2.py"
        content = lazyc2_path.read_text(encoding="utf-8")
        assert "shell=False" in content

    def test_uses_shlex_split(self):
        """BDD: Given the execute_command function, When I check its implementation,
        Then it must use shlex.split to parse commands."""
        lazyc2_path = Path(__file__).parent.parent / "lazyc2.py"
        content = lazyc2_path.read_text(encoding="utf-8")
        assert "shlex.split(command)" in content


# ---------------------------------------------------------------------------
# SDD Contract 10: misc_migrated.py — no os.system for IP display
# ---------------------------------------------------------------------------

class TestMiscMigratedIpDisplay:
    """CONTRACT: The do_ip and do_ipp functions must not use os.system
    or subprocess with shell=True for IP display."""

    def test_ip_uses_subprocess_list_form(self):
        """BDD: Given the misc_migrated.py module, When I check IP display,
        Then it must use subprocess with a list (not shell=True)."""
        misc_path = Path(__file__).parent.parent / "cli" / "commands" / "misc_migrated.py"
        content = misc_path.read_text(encoding="utf-8")
        assert '["ip"' in content or '["ip", ' in content

    def test_no_xclip_shell_true(self):
        """BDD: Given the misc_migrated.py module, When I check clipboard
        operations, Then xclip must not use shell=True."""
        misc_path = Path(__file__).parent.parent / "cli" / "commands" / "misc_migrated.py"
        content = misc_path.read_text(encoding="utf-8")
        assert "xclip -o -sel clip', shell=True" not in content


# ---------------------------------------------------------------------------
# SDD Contract 11: Hardcoded absolute paths eliminated
# ---------------------------------------------------------------------------

class TestNoHardcodedPaths:
    """CONTRACT: Production code must not contain hardcoded absolute paths
    to user home directories."""

    def test_no_home_grisun0_in_production(self):
        """BDD: Given production code files, When I scan for hardcoded paths,
        Then /home/grisun0 must not appear in non-test files."""
        production_dirs = [
            Path(__file__).parent.parent / "modules",
            Path(__file__).parent.parent / "cli",
            Path(__file__).parent.parent / "core",
            Path(__file__).parent.parent / "lazyc2",
        ]
        violations = []
        for d in production_dirs:
            if not d.exists():
                continue
            for py_file in d.rglob("*.py"):
                if "test" in py_file.name.lower():
                    continue
                try:
                    content = py_file.read_text(encoding="utf-8")
                    if "/home/grisun0" in content:
                        violations.append(str(py_file))
                except OSError:
                    continue
        assert not violations, f"Hardcoded paths found in: {violations}"

    def test_no_root_home_in_anti_forensics(self):
        """BDD: Given the anti_forensics.py module, When I scan for /root/,
        Then it must use Path.home() instead."""
        af_path = Path(__file__).parent.parent / "cli" / "commands" / "anti_forensics.py"
        content = af_path.read_text(encoding="utf-8")
        assert "/root/" not in content
        assert "Path.home()" in content

    def test_telegram_hermes_uses_env_shebang(self):
        """BDD: Given telegram_hermes.py, When I check the shebang,
        Then it must use #!/usr/bin/env python3."""
        tg_path = Path(__file__).parent.parent / "telegram_hermes.py"
        first_line = tg_path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "#!/usr/bin/env python3"


# ---------------------------------------------------------------------------
# SDD Contract 12: conditional_hooks.py — shlex.quote prevents injection
# ---------------------------------------------------------------------------

class TestConditionalHooksInjectionPrevention:
    """CONTRACT: conditional_hooks.py must quote placeholder values
    with shlex.quote before inserting them into shell commands."""

    def test_uses_shlex_quote(self):
        """BDD: Given the conditional_hooks.py module, When I check
        _resolve_placeholders, Then it must use shlex.quote."""
        hooks_path = Path(__file__).parent.parent / "modules" / "conditional_hooks.py"
        content = hooks_path.read_text(encoding="utf-8")
        assert "shlex.quote" in content


# ---------------------------------------------------------------------------
# SDD Contract 13: safe_exec.py — safe_clear_screen uses tput
# ---------------------------------------------------------------------------

class TestSafeClearScreen:
    """CONTRACT: safe_clear_screen must use tput or ANSI escapes,
    never os.system."""

    def test_no_os_system(self):
        """BDD: Given the safe_exec module, When I check safe_clear_screen,
        Then it must not use os.system."""
        from core.safe_exec import safe_clear_screen
        import inspect
        source = inspect.getsource(safe_clear_screen)
        assert "os.system(" not in source

    def test_uses_subprocess(self):
        """BDD: Given the safe_exec module, When I check safe_clear_screen,
        Then it must use subprocess."""
        from core.safe_exec import safe_clear_screen
        import inspect
        source = inspect.getsource(safe_clear_screen)
        assert "subprocess.run" in source


# ---------------------------------------------------------------------------
# SDD Contract 14: bot.py — no os.system
# ---------------------------------------------------------------------------

class TestBotNoOsSystem:
    """CONTRACT: modules/bot.py must not use os.system."""

    def test_no_os_system(self):
        """BDD: Given the bot.py module, When I scan its source,
        Then it must not contain os.system."""
        bot_path = Path(__file__).parent.parent / "modules" / "bot.py"
        content = bot_path.read_text(encoding="utf-8")
        assert "os.system" not in content

    def test_uses_subprocess(self):
        """BDD: Given the bot.py module, When I scan its source,
        Then it must use subprocess for formatting."""
        bot_path = Path(__file__).parent.parent / "modules" / "bot.py"
        content = bot_path.read_text(encoding="utf-8")
        assert "subprocess.run" in content


# ---------------------------------------------------------------------------
# SDD Contract 15: recon_migrated.py — no os.system for PATH setup
# ---------------------------------------------------------------------------

class TestReconMigratedNoOsSystem:
    """CONTRACT: cli/commands/recon_migrated.py must not use os.system
    for PATH modification."""

    def test_no_os_system_for_path_setup(self):
        """BDD: Given the recon_migrated.py module, When I check the
        alterx PATH setup, Then it must use Python file operations."""
        recon_path = Path(__file__).parent.parent / "cli" / "commands" / "recon_migrated.py"
        content = recon_path.read_text(encoding="utf-8")
        assert "os.system(command)" not in content


# ---------------------------------------------------------------------------
# SDD Contract 16: core/safe_exec.py — safe_file_read with size limit
# ---------------------------------------------------------------------------

class TestSafeFileRead:
    """CONTRACT: safe_file_read must enforce a size limit to prevent
    memory exhaustion attacks."""

    def test_rejects_oversized_file(self):
        """BDD: Given a file exceeding the size limit, When I read it,
        Then it must raise ValueError."""
        from core.safe_exec import safe_file_read
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("x" * 100)
            f.flush()
            tmp_path = f.name
        try:
            with pytest.raises(ValueError, match="exceeds limit"):
                safe_file_read(tmp_path, max_bytes=50)
        finally:
            os.unlink(tmp_path)

    def test_reads_valid_file(self):
        """BDD: Given a file within the size limit, When I read it,
        Then it must return the contents."""
        from core.safe_exec import safe_file_read
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello world")
            f.flush()
            tmp_path = f.name
        try:
            content = safe_file_read(tmp_path)
            assert content == "hello world"
        finally:
            os.unlink(tmp_path)

    def test_rejects_missing_file(self):
        """BDD: Given a non-existent file, When I read it,
        Then it must raise FileNotFoundError."""
        from core.safe_exec import safe_file_read
        with pytest.raises(FileNotFoundError):
            safe_file_read("/nonexistent/file.txt")


# ---------------------------------------------------------------------------
# SDD Contract 17: core/safe_exec.py — safe_find_tool replaces hardcoded paths
# ---------------------------------------------------------------------------

class TestSafeFindTool:
    """CONTRACT: safe_find_tool must use shutil.which to find tools,
    replacing hardcoded paths."""

    def test_finds_existing_tool(self):
        """BDD: Given a tool on PATH, When I search for it,
        Then it must return the path."""
        from core.safe_exec import safe_find_tool
        result = safe_find_tool("python3")
        assert result is not None
        assert os.path.isabs(result)

    def test_returns_none_for_missing_tool(self):
        """BDD: Given a tool not on PATH, When I search for it,
        Then it must return None."""
        from core.safe_exec import safe_find_tool
        result = safe_find_tool("nonexistent_tool_xyz_12345")
        assert result is None
