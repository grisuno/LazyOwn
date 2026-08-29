"""SDD+TDD+BDD tests for security hardening batch v2.

Contract: Every security fix in this batch has a corresponding test that
verifies the fix works and would detect regression. Tests are written
BEHAVIOURALLY (BDD-style) so they read as specifications.

Covers:
  - P0: Command injection prevention in cli/commands/ai.py
  - P0: Credential injection prevention in cli/commands/postexp_migrated.py
  - P1: DNS command allowlist enforcement in lazyc2.py
  - P1: Safe shell execution in cli/commands/misc_migrated.py
  - P1: Credential encryption at rest in modules/phishing_orchestrator.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent


def _read(relpath: str) -> str:
    return (_ROOT / relpath).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# SDD Contract 1: AI commands must not pass secrets through shell strings
# ---------------------------------------------------------------------------

class TestAICommandInjectionPrevention:
    """CONTRACT: The do_ask and do_groq methods must NEVER pass api_key or
    user prompts through os.system() or shell string interpolation.
    They must use subprocess.run() with list-form arguments and pass
    the API key via environment variable only."""

    SOURCE = _read("cli/commands/ai.py")

    def test_no_os_system_in_ai_module(self):
        """BDD: Given the ai module source is loaded,
        When I scan for os.system calls,
        Then none must exist."""
        assert "os.system(" not in self.SOURCE

    def test_uses_subprocess_run(self):
        """BDD: Given the ai module source is loaded,
        When I check for subprocess usage,
        Then subprocess.run must be present."""
        assert "subprocess.run" in self.SOURCE

    def test_api_key_passed_via_env_dict(self):
        """BDD: Given the api_key contains shell metacharacters,
        When do_ask or do_groq execute,
        Then the api_key must only appear in an env dict, never in a command string."""
        assert 'env[GROQ_API_KEY_ENV] = api_key' in self.SOURCE

    def test_no_fstring_with_api_key_in_command(self):
        """BDD: Given the source is scanned for f-string command construction,
        When api_key appears in an f-string targeting subprocess,
        Then it must be in the env parameter only."""
        fstring_lines = [
            line for line in self.SOURCE.split("\n")
            if "f\"" in line or "f'" in line
        ]
        for line in fstring_lines:
            if "api_key" in line and ("sshpass" in line or "scp" in line or "&&" in line):
                pytest.fail(f"api_key in shell f-string: {line.strip()}")

    def test_do_ask_uses_sys_executable(self):
        """BDD: Given do_ask spawns a Python subprocess,
        When it constructs the command,
        Then it must use sys.executable, not hardcoded 'python3'."""
        assert "sys.executable" in self.SOURCE


# ---------------------------------------------------------------------------
# SDD Contract 2: SSH credentials must never appear in shell command strings
# ---------------------------------------------------------------------------

class TestSSHCredentialInjectionPrevention:
    """CONTRACT: The postexp_migrated module must NEVER pass passwords
    through shell command strings via sshpass -p '{password}'.
    Passwords must be passed via SSHPASS environment variable with -e flag."""

    SOURCE = _read("cli/commands/postexp_migrated.py")

    def test_no_sshpass_minus_p_in_code(self):
        """BDD: Given the postexp module source is loaded,
        When I scan for sshpass -p in actual code (not docstrings),
        Then it must not appear."""
        lines = self.SOURCE.split("\n")
        in_docstring = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if "sshpass -p" in line and "sshpass -e" not in line:
                pytest.fail(f"sshpass -p found in code: {line.strip()}")

    def test_sshpass_uses_e_flag(self):
        """BDD: Given sshpass is invoked,
        When the command is constructed,
        Then it must use the -e flag for environment-based password."""
        assert "sshpass\", \"-e\"" in self.SOURCE or "sshpass', '-e'" in self.SOURCE

    def test_ssppass_env_var_used(self):
        """BDD: Given sshpass is invoked,
        When the password is passed,
        Then it must be via SSHPASS environment variable."""
        assert "SSHPASS" in self.SOURCE

    def test_sshpass_in_list_form(self):
        """BDD: Given sshpass is invoked,
        When subprocess.run is called,
        Then it must use list-form arguments."""
        assert '["sshpass"' in self.SOURCE or "['sshpass'" in self.SOURCE

    def test_password_not_in_fstring_command(self):
        """BDD: Given a password contains shell metacharacters,
        When the SCP command is constructed,
        Then the password must not appear in any f-string in code."""
        lines = self.SOURCE.split("\n")
        in_docstring = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if ("f\"sshpass" in line or "f'sshpass" in line):
                pytest.fail(f"sshpass in f-string: {line.strip()}")


# ---------------------------------------------------------------------------
# SDD Contract 3: DNS commands must be validated against an allowlist
# ---------------------------------------------------------------------------

class TestDNSCommandAllowlist:
    """CONTRACT: The DNS C2 resolver must validate decoded commands against
    a strict allowlist before processing. Unknown commands must be rejected."""

    SOURCE = _read("lazyc2.py")

    def test_allowlist_exists_as_frozenset(self):
        """BDD: Given the lazyc2 module source is loaded,
        When I check for the DNS command allowlist,
        Then _DNS_COMMAND_ALLOWLIST must be defined as a frozenset."""
        assert "_DNS_COMMAND_ALLOWLIST = frozenset({" in self.SOURCE

    def test_max_length_constant_exists(self):
        """BDD: Given the DNS resolver processes commands,
        When a command is decoded,
        Then _DNS_MAX_DECODED_LENGTH must be defined."""
        assert "_DNS_MAX_DECODED_LENGTH" in self.SOURCE

    def test_allowlist_is_finite_and_reasonable(self):
        """BDD: Given the allowlist is defined,
        When I inspect its size,
        Then it must contain fewer than 20 entries (principle of least privilege)."""
        match = re.search(
            r"_DNS_COMMAND_ALLOWLIST = frozenset\(\{(.*?)\}\)",
            self.SOURCE, re.DOTALL,
        )
        assert match, "_DNS_COMMAND_ALLOWLIST frozenset not found"
        entries = [e.strip().strip('"').strip("'") for e in match.group(1).split(",") if e.strip()]
        assert len(entries) < 20, f"Allowlist too large: {len(entries)} entries"

    def test_dns_handler_checks_allowlist(self):
        """BDD: Given a DNS query is decoded,
        When the command starts with 'exec:',
        Then the handler must check if the command is in _DNS_COMMAND_ALLOWLIST."""
        assert "not in _DNS_COMMAND_ALLOWLIST" in self.SOURCE

    def test_dns_handler_checks_length(self):
        """BDD: Given a DNS query decodes to a very long string,
        When the handler processes it,
        Then it must check len(command) against _DNS_MAX_DECODED_LENGTH."""
        assert "len(command) > _DNS_MAX_DECODED_LENGTH" in self.SOURCE

    def test_dangerous_command_not_in_allowlist(self):
        """BDD: Given the allowlist is defined,
        When I check for dangerous commands,
        Then destructive commands must not be in the allowlist."""
        match = re.search(
            r"_DNS_COMMAND_ALLOWLIST = frozenset\(\{(.*?)\}\)",
            self.SOURCE, re.DOTALL,
        )
        assert match
        dangerous = {"rm", "curl", "wget", "dd", "mkfs", "shutdown", "reboot", "halt", "nc", "ncat"}
        entries = {e.strip().strip('"').strip("'") for e in match.group(1).split(",") if e.strip()}
        assert dangerous.isdisjoint(entries), f"Dangerous commands in allowlist: {dangerous & entries}"


# ---------------------------------------------------------------------------
# SDD Contract 4: Shell execution must capture output safely
# ---------------------------------------------------------------------------

class TestSafeShellExecution:
    """CONTRACT: The do_sys command must use subprocess.run with output
    capture instead of os.system() which discards output and provides
    no exit code handling."""

    SOURCE = _read("cli/commands/misc_migrated.py")

    def test_do_sys_uses_subprocess(self):
        """BDD: Given the misc_migrated source is loaded,
        When I locate the do_sys method,
        Then it must use subprocess.run, not os.system."""
        lines = self.SOURCE.split("\n")
        in_do_sys = False
        do_sys_lines = []
        for line in lines:
            if "def do_sys" in line:
                in_do_sys = True
            elif in_do_sys and line.strip().startswith("def "):
                break
            elif in_do_sys:
                do_sys_lines.append(line)
        do_sys_block = "\n".join(do_sys_lines)
        assert "subprocess.run" in do_sys_block
        assert "os.system" not in do_sys_block

    def test_do_sys_captures_output(self):
        """BDD: Given a command is executed via 'sys',
        When the command produces stdout/stderr,
        Then the output must be captured."""
        lines = self.SOURCE.split("\n")
        in_do_sys = False
        do_sys_lines = []
        for line in lines:
            if "def do_sys" in line:
                in_do_sys = True
            elif in_do_sys and line.strip().startswith("def "):
                break
            elif in_do_sys:
                do_sys_lines.append(line)
        do_sys_block = "\n".join(do_sys_lines)
        assert "capture_output=True" in do_sys_block

    def test_no_os_system_in_misc_module_code(self):
        """BDD: Given the misc_migrated module source,
        When I scan for os.system in actual code (not docstrings),
        Then it must not appear in any command execution method."""
        lines = self.SOURCE.split("\n")
        in_docstring = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if "os.system(" in line and "def do_" in "".join(lines[max(0, i - 20):i]):
                pytest.fail(f"os.system in command method at line {i + 1}: {line.strip()}")


# ---------------------------------------------------------------------------
# SDD Contract 5: Phishing credentials must be encrypted at rest
# ---------------------------------------------------------------------------

class TestCredentialEncryptionAtRest:
    """CONTRACT: Harvested phishing credentials must be encrypted before
    writing to disk. Passwords must never appear in plaintext in JSON
    or log files."""

    SOURCE = _read("modules/phishing_orchestrator.py")

    def test_encrypt_function_exists(self):
        """BDD: Given the phishing orchestrator source is loaded,
        When I check for credential encryption,
        Then _encrypt_credential function must be defined."""
        assert "def _encrypt_credential(" in self.SOURCE

    def test_decrypt_function_exists(self):
        """BDD: Given encrypted credentials exist on disk,
        When the operator needs to read them,
        Then _decrypt_credential must be defined."""
        assert "def _decrypt_credential(" in self.SOURCE

    def test_hash_function_exists(self):
        """BDD: Given credentials are logged,
        When writing to the audit log,
        Then _hash_credential_for_log must be defined."""
        assert "def _hash_credential_for_log(" in self.SOURCE

    def test_record_credentials_encrypts_password(self):
        """BDD: Given record_credentials is called,
        When the password is written to JSON,
        Then _encrypt_credential must be called on the password."""
        assert "_encrypt_credential(password)" in self.SOURCE

    def test_log_uses_hash_not_plaintext(self):
        """BDD: Given the audit log is written,
        When the password field is recorded,
        Then _hash_credential_for_log must be used, not plaintext."""
        assert "_hash_credential_for_log(password)" in self.SOURCE

    def test_uses_aes_encryption(self):
        """BDD: Given credentials are encrypted,
        When the encryption is performed,
        Then AES-256-GCM must be used (via core.crypto)."""
        assert "AESencrypt" in self.SOURCE

    def test_imports_base64_for_encoding(self):
        """BDD: Given encrypted bytes need to be stored as text,
        When the encryption is performed,
        Then base64 encoding must be used."""
        assert "import base64" in self.SOURCE

    def test_credential_key_derivation(self):
        """BDD: Given encryption requires a key,
        When the key is derived,
        Then _derive_credential_key must be defined."""
        assert "def _derive_credential_key(" in self.SOURCE


# ---------------------------------------------------------------------------
# SDD Contract 6: No os.system in security-critical paths
# ---------------------------------------------------------------------------

class TestNoOsSystemInCriticalPaths:
    """CONTRACT: Security-critical modules must not use os.system() which
    provides no output capture, no exit code control, and is vulnerable
    to shell injection."""

    def test_ai_module_no_os_system(self):
        """BDD: Given the AI command module source,
        When I scan for os.system calls,
        Then none must exist."""
        source = _read("cli/commands/ai.py")
        assert "os.system(" not in source

    def test_postexp_no_sshpass_in_fstring_code(self):
        """BDD: Given the post-exploitation module source,
        When I scan for sshpass in f-strings in code,
        Then none must exist."""
        source = _read("cli/commands/postexp_migrated.py")
        lines = source.split("\n")
        in_docstring = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if "f\"sshpass" in line or "f'sshpass" in line:
                pytest.fail(f"sshpass in f-string: {line.strip()}")

    def test_dns_resolver_has_allowlist_guard(self):
        """BDD: Given the DNS resolver source,
        When I scan for the exec: handler,
        Then it must contain an allowlist check."""
        source = _read("lazyc2.py")
        assert "not in _DNS_COMMAND_ALLOWLIST" in source

    def test_misc_sys_no_os_system(self):
        """BDD: Given the misc_migrated module source,
        When I locate the do_sys method,
        Then os.system must not be used."""
        source = _read("cli/commands/misc_migrated.py")
        lines = source.split("\n")
        in_do_sys = False
        for line in lines:
            if "def do_sys" in line:
                in_do_sys = True
            elif in_do_sys and line.strip().startswith("def "):
                break
            elif in_do_sys and "os.system" in line:
                pytest.fail("do_sys must not use os.system")
