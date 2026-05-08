"""``core`` package and ``utils`` re-export tests.

Validate the ``core/`` package layout and confirm ``utils.py`` continues to
re-export every public name so the CLI commands and the C2 routes that import
from ``utils`` keep working.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
UTILS_PATH = REPO_ROOT / "utils.py"


def _run_in_subprocess(snippet: str) -> str:
    """Execute ``snippet`` in a clean subprocess so utils.py argv parsing does not fire."""
    result = subprocess.run(
        [sys.executable, "-c", snippet],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=30,
    )
    if result.returncode != 0:
        pytest.fail(f"subprocess failed:\nstderr: {result.stderr}\nstdout: {result.stdout}")
    return result.stdout.strip()


class TestCorePackageStructure:
    """Each ``core`` module must exist and parse cleanly."""

    @pytest.mark.parametrize(
        "module",
        ["__init__.py", "console.py", "config.py", "crypto.py", "validators.py", "protocols.py"],
    )
    def test_module_exists_and_parses(self, module):
        path = CORE_DIR / module
        assert path.exists(), f"missing core module: {module}"
        ast.parse(path.read_text(encoding="utf-8"))


class TestCoreConsole:
    """ANSI constants and print helpers."""

    def test_ansi_constants_have_escape_prefix(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.console import GREEN, RED, RESET, WHITE, YELLOW

        for c in (RESET, RED, GREEN, YELLOW, WHITE):
            assert c.startswith("\033["), f"not an ANSI escape: {c!r}"

    def test_print_msg_writes_green_payload(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.console import print_msg

        print_msg("hello")
        out = capsys.readouterr().out
        assert "hello" in out
        assert "\033[32m" in out

    def test_print_error_writes_red_payload(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.console import print_error

        print_error("boom")
        out = capsys.readouterr().out
        assert "boom" in out
        assert "\033[31m" in out

    def test_print_warn_writes_warn_glyph(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.console import print_warn

        print_warn("careful")
        out = capsys.readouterr().out
        assert "careful" in out
        assert "[⚠]" in out

    def test_surrogate_chars_are_stripped(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.console import print_msg

        print_msg("hi\udce2 there")
        out = capsys.readouterr().out
        assert "\udce2" not in out
        assert "hi" in out and "there" in out


class TestCoreConfig:
    """Config wrapper, load_payload, save_payload."""

    def test_config_attribute_and_item_access(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lport": 9999})
        assert cfg.rhost == "10.0.0.1"
        assert cfg["lport"] == 9999

    def test_config_missing_key_returns_none(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.config import Config

        assert Config({})["anything"] is None

    def test_load_payload_reads_real_file(self, tmp_path, monkeypatch):
        sys.path.insert(0, str(REPO_ROOT))
        from core.config import load_payload, save_payload

        target = tmp_path / "payload.json"
        save_payload({"rhost": "127.0.0.1", "lport": 5555}, target)
        loaded = load_payload(target)
        assert loaded == {"rhost": "127.0.0.1", "lport": 5555}

    def test_save_payload_is_atomic(self, tmp_path):
        sys.path.insert(0, str(REPO_ROOT))
        from core.config import save_payload

        target = tmp_path / "payload.json"
        save_payload({"k": "v"}, target)
        assert target.exists()
        assert json.loads(target.read_text(encoding="utf-8")) == {"k": "v"}
        for sibling in tmp_path.iterdir():
            assert not sibling.name.endswith(".tmp"), f"leftover tmp file: {sibling}"

    def test_save_payload_creates_parent_dirs(self, tmp_path):
        sys.path.insert(0, str(REPO_ROOT))
        from core.config import save_payload

        target = tmp_path / "nested" / "path" / "payload.json"
        save_payload({"a": 1}, target)
        assert target.exists()


class TestCoreCrypto:
    """xor_encrypt_decrypt is symmetric and matches legacy behavior."""

    def test_roundtrip(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.crypto import xor_encrypt_decrypt

        for plaintext in (b"", b"a", b"Hello, World!", bytes(range(256))):
            encrypted = xor_encrypt_decrypt(plaintext, "secret-key")
            decrypted = xor_encrypt_decrypt(bytes(encrypted), "secret-key")
            assert bytes(decrypted) == plaintext

    def test_returns_bytearray(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.crypto import xor_encrypt_decrypt

        result = xor_encrypt_decrypt(b"abc", "k")
        assert isinstance(result, bytearray)

    def test_empty_key_raises(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.crypto import xor_encrypt_decrypt

        with pytest.raises(ValueError):
            xor_encrypt_decrypt(b"abc", "")

    def test_matches_legacy_known_vector(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.crypto import xor_encrypt_decrypt

        expected = bytearray([ord("a") ^ ord("k"), ord("b") ^ ord("k"), ord("c") ^ ord("k")])
        assert xor_encrypt_decrypt(b"abc", "k") == expected


class TestCoreValidators:
    """Validators short-circuit cleanly without raising."""

    def test_check_rhost_truthy(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_rhost

        assert check_rhost("10.0.0.1") is True

    def test_check_rhost_empty_returns_false(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_rhost

        assert check_rhost("") is False
        assert "rhost must be set" in capsys.readouterr().out

    def test_check_lhost_empty(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_lhost

        assert check_lhost(None) is False
        assert "lhost must be set" in capsys.readouterr().out

    def test_check_lport_zero_falsy(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_lport

        assert check_lport(0) is False

    def test_check_port_valid_range(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_port

        assert check_port(1) is True
        assert check_port(65535) is True
        assert check_port("8080") is True

    def test_check_port_invalid(self, capsys):
        sys.path.insert(0, str(REPO_ROOT))
        from core.validators import check_port

        assert check_port(0) is False
        assert check_port(70000) is False
        assert check_port("abc") is False


class TestCoreProtocols:
    """Protocols are runtime-checkable structural types."""

    def test_protocols_importable(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.protocols import BridgeCatalog, LLMBackend, MemoryStore, OutcomeEvaluator, Selector

        for proto in (Selector, LLMBackend, MemoryStore, BridgeCatalog, OutcomeEvaluator):
            assert hasattr(proto, "_is_protocol")

    def test_selector_protocol_accepts_conforming_object(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.protocols import Selector

        class Dummy:
            name = "dummy"

            def suggest(self, target, phase, context=None):
                return None

        assert isinstance(Dummy(), Selector)

    def test_llm_backend_protocol_rejects_nonconforming(self):
        sys.path.insert(0, str(REPO_ROOT))
        from core.protocols import LLMBackend

        class Bogus:
            pass

        assert not isinstance(Bogus(), LLMBackend)


class TestUtilsBackwardsCompat:
    """utils.py must still expose every public symbol the ``core`` package owns."""

    @pytest.mark.parametrize(
        "name",
        [
            "Config",
            "load_payload",
            "save_payload",
            "RESET",
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "MAGENTA",
            "CYAN",
            "WHITE",
            "BG_RED",
            "BG_GREEN",
            "BRIGHT_GREEN",
            "COLOR_256",
            "TRUE_COLOR",
            "SURROGATE_CHARS",
            "TRANSLATION_TABLE",
            "print_msg",
            "print_warn",
            "print_error",
            "print_succ",
            "xor_encrypt_decrypt",
            "check_rhost",
            "check_lhost",
            "check_lport",
            "check_port",
        ],
    )
    def test_symbol_is_re_exported(self, name):
        out = _run_in_subprocess(
            f"import sys; sys.argv=['utils_compat']; import utils; print(hasattr(utils, {name!r}))"
        )
        assert out == "True", f"utils.{name} missing — broken core re-export"

    def test_utils_no_inline_config_class(self):
        """utils.py must not redefine Config — it must come from core."""
        tree = ast.parse(UTILS_PATH.read_text(encoding="utf-8"))
        configs = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "Config"]
        assert configs == [], f"Config still inline in utils.py at {[c.lineno for c in configs]}"

    def test_utils_no_inline_load_payload(self):
        """utils.py must not redefine load_payload — it must come from core."""
        tree = ast.parse(UTILS_PATH.read_text(encoding="utf-8"))
        defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "load_payload"]
        assert defs == [], f"load_payload still inline in utils.py at {[d.lineno for d in defs]}"

    def test_utils_no_inline_xor(self):
        tree = ast.parse(UTILS_PATH.read_text(encoding="utf-8"))
        defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "xor_encrypt_decrypt"]
        assert defs == []

    def test_utils_no_inline_validators(self):
        tree = ast.parse(UTILS_PATH.read_text(encoding="utf-8"))
        defs = [
            n.name
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name in {"check_rhost", "check_lhost", "check_lport"}
        ]
        assert defs == [], f"validators still inline in utils.py: {defs}"

    def test_utils_no_inline_print_helpers(self):
        tree = ast.parse(UTILS_PATH.read_text(encoding="utf-8"))
        defs = [
            n.name
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name in {"print_msg", "print_warn", "print_error"}
        ]
        assert defs == [], f"print helpers still inline in utils.py: {defs}"

    def test_utils_imports_from_core(self):
        text = UTILS_PATH.read_text(encoding="utf-8")
        for required in (
            "from core.config import",
            "from core.console import",
            "from core.crypto import",
            "from core.validators import",
        ):
            assert required in text, f"utils.py missing import: {required}"


class TestUtilsParsesAndRunsAfterRefactor:
    """utils.py must still parse and import without exploding."""

    def test_parses(self):
        ast.parse(UTILS_PATH.read_text(encoding="utf-8"))

    def test_imports_in_clean_subprocess(self):
        out = _run_in_subprocess("import sys; sys.argv=['x']; import utils; print('OK')")
        assert out == "OK"

    def test_load_payload_via_utils_returns_payload(self):
        out = _run_in_subprocess(
            "import sys; sys.argv=['x']; from utils import load_payload; p = load_payload(); print('rhost' in p)"
        )
        assert out == "True"
