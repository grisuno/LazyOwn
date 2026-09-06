"""API-key resolution contract tests.

Covers the two defects that broke ``vulnbot_groq``:

- ``self.params["api_key"]`` was hardcoded to ``None`` in ``lazyown.py``
  instead of reading the config-derived ``api_key`` class attribute, so every
  startup-level gate (``recon``, ``lazyown`` chain, AI bootstrap) saw no key.
- ``replace_command_placeholders`` only handled ``{key}`` while addons emit
  ``{{key}}`` (documented in ``modules/yaml_generator.py``), so
  ``GROQ_API_KEY="{{ api_key }}"`` was never substituted.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"


class TestApiKeyWiredIntoParams:
    def test_params_api_key_is_not_hardcoded_none(self):
        src = LAZYOWN_PATH.read_text(encoding="utf-8")
        assert '"api_key": None' not in src, (
            "self.params must bind api_key from the config class attribute, "
            "not a hardcoded None"
        )

    def test_params_api_key_binds_config_attr(self):
        src = LAZYOWN_PATH.read_text(encoding="utf-8")
        assert '"api_key": api_key,' in src, (
            "self.params must reference the api_key class attribute "
            "populated from Config(load_payload())"
        )

    def test_class_attribute_api_key_reads_payload(self):
        src = LAZYOWN_PATH.read_text(encoding="utf-8")
        assert "api_key = config.api_key" in src


class TestReplaceCommandPlaceholders:
    def test_double_brace_substitution(self):
        from utils import replace_command_placeholders

        command = 'export GROQ_API_KEY="{{ api_key }}" && run'
        out = replace_command_placeholders(command, {"api_key": "gsk_real"})
        assert out == 'export GROQ_API_KEY="gsk_real" && run'

    def test_single_brace_substitution(self):
        from utils import replace_command_placeholders

        out = replace_command_placeholders(
            "--file ../sessions/vulns_{rhost}.nmap",
            {"rhost": "10.10.11.5"},
        )
        assert out == "--file ../sessions/vulns_10.10.11.5.nmap"

    def test_mixed_braces_in_one_command(self):
        from utils import replace_command_placeholders

        command = 'x -t {{ domain }} -u {rhost}'
        out = replace_command_placeholders(
            command, {"domain": "a.io", "rhost": "1.1.1.1"}
        )
        assert out == "x -t a.io -u 1.1.1.1"

    def test_missing_key_left_intact(self):
        from utils import replace_command_placeholders

        command = "run --x {{ missing }}"
        out = replace_command_placeholders(command, {})
        assert out == "run --x {{ missing }}"
