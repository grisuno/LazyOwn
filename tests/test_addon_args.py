"""Contract tests for the addon runtime argument namespace.

Pins :mod:`core.addon_args` — the single ``execute_command`` rendering
contract: ``--argN`` extraction, token-drop semantics for unresolved
``{argN}``, quoting, and exact backward compatibility of the classic
``{key}`` / ``{{key}}`` placeholder substitution.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import cmd2
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.addon_args import extract_cli_args, render_command  # noqa: E402


class TestExtractCliArgs:
    def test_mixed_forms_last_wins(self):
        rest, args = extract_cli_args(["run", "x", "--arg1", "v1", "--arg2=v2", "--arg1", "v3"])
        assert rest == ["run", "x"]
        assert args == {"arg1": "v3", "arg2": "v2"}

    def test_double_dash_stops_extraction(self):
        rest, args = extract_cli_args(["--arg1", "v", "--", "--arg2", "w"])
        assert rest == ["--", "--arg2", "w"]
        assert args == {"arg1": "v"}

    def test_valueless_flag_at_end(self):
        rest, args = extract_cli_args(["tool", "--arg7"])
        assert rest == ["tool"]
        assert args == {"arg7": ""}

    def test_unknown_flag_shape_passes_through(self):
        rest, args = extract_cli_args(["tool", "--word-list", "x", "--1bad", "y"])
        assert rest == ["tool", "--word-list", "x", "--1bad", "y"]
        assert args == {}


class TestRenderCommand:
    CTX = {"url": "http://10.0.0.5"}
    TPL = "ffuf -u {url}/FUZZ -w {arg1} -mc {arg2} {arg3}"

    def test_all_args_render(self):
        out = render_command(self.TPL, self.CTX, {"arg1": "words.txt", "arg2": "200,301", "arg3": "-t 50"})
        assert out == "ffuf -u http://10.0.0.5/FUZZ -w words.txt -mc 200,301 '-t 50'"

    def test_token_drop_dangling_flag_goes_too(self):
        out = render_command(self.TPL, self.CTX, {"arg1": "words.txt"})
        assert out == "ffuf -u http://10.0.0.5/FUZZ -w words.txt"

    def test_token_drop_all_args(self):
        out = render_command(self.TPL, self.CTX, {})
        assert out == "ffuf -u http://10.0.0.5/FUZZ"

    def test_no_format_collateral(self):
        assert render_command("awk '{print $1}' {arg1}", {}, {}) == "awk '{print $1}'"
        assert render_command("awk '{print $1}'", {}, {}) == "awk '{print $1}'"

    def test_injection_blocked_by_quote(self):
        assert render_command("echo {arg1}", {}, {"arg1": "; rm -rf /"}) == "echo '; rm -rf /'"

    def test_control_chars_rejected(self):
        with pytest.raises(ValueError):
            render_command("echo {arg1}", {}, {"arg1": "a\x00b"})

    def test_explicit_empty_arg_renders_quoted_empty(self):
        assert render_command("tool {arg1}", {}, {"arg1": ""}) == "tool ''"

    def test_yaml_defaults_lower_precedence_than_cli(self):
        out = render_command("tool {arg1}", {}, {"arg1": "cli"}, {"arg1": "default"})
        assert out == "tool cli"
        out = render_command("tool {arg1}", {}, {}, {"arg1": "default"})
        assert out == "tool default"

    def test_spaced_arg_placeholder_canonicalised(self):
        out = render_command("tool { arg1 }", {}, {"arg1": "v"})
        assert out == "tool v"


class TestClassicCompatibility:
    def test_double_brace_resolves(self):
        assert render_command("{{rhost}}", {"rhost": "1.2.3.4"}) == "1.2.3.4"

    def test_double_brace_spaced_resolves(self):
        assert render_command("{{ api_key }}", {"api_key": "gsk_real"}) == "gsk_real"

    def test_mixed_braces(self):
        out = render_command("x -t {{ domain }} -u {rhost}", {"domain": "a.io", "rhost": "1.1.1.1"})
        assert out == "x -t a.io -u 1.1.1.1"

    def test_single_brace_spaced_resolves(self):
        assert render_command("{ rhost }", {"rhost": "1.2.3.4"}) == "1.2.3.4"

    def test_unknown_key_left_verbatim_with_spacing(self):
        assert render_command("tool {missing_key}", {}) == "tool {missing_key}"
        assert render_command("run --x {{ missing }}", {}) == "run --x {{ missing }}"

    def test_placeholder_glued_to_punctuation(self):
        assert render_command("tool {rhost};", {"rhost": "1.2.3.4"}) == "tool 1.2.3.4;"

    def test_classic_values_not_quoted(self):
        assert render_command("tool -p '{pass}'", {"pass": "P@ss"}) == "tool -p 'P@ss'"


class TestUtilsDelegate:
    def test_replace_command_placeholders_delegates(self):
        from utils import replace_command_placeholders

        assert replace_command_placeholders('export K="{{ api_key }}" && run', {"api_key": "gsk_real"}) == (
            'export K="gsk_real" && run'
        )
        assert replace_command_placeholders("x -t {{ domain }} -u {rhost}", {"domain": "a.io", "rhost": "1.1.1.1"}) == (
            "x -t a.io -u 1.1.1.1"
        )
        assert replace_command_placeholders("run --x {{ missing }}", {}) == "run --x {{ missing }}"


class TestCreatorAllowlist:
    def test_arg_placeholders_accepted_without_declaration(self):
        from lazyc2.addon_creator import AddonDraft, AddonValidator

        draft = AddonDraft(name="probe", description="d", author="a", version="1.0")
        draft.execute_command = "ffuf -w {arg1} -u {rhost}"
        issues = [i for i in AddonValidator(draft).validate() if "arg1" in str(i)]
        assert issues == []

    def test_undeclared_placeholder_still_rejected(self):
        from lazyc2.addon_creator import AddonDraft, AddonValidator

        draft = AddonDraft(name="probe", description="d", author="a", version="1.0")
        draft.execute_command = "ffuf -w {totally_unknown_knob} -u {rhost}"
        issues = [i for i in AddonValidator(draft).validate() if "totally_unknown_knob" in str(i)]
        assert issues, "undeclared non-argN placeholder must still be rejected"


class TestHeadlessAddonPath:
    def test_lazy_addon_run_renders_arg_namespace(self, tmp_path, monkeypatch):
        from cli.commands.lazyops import LazyCommandSet

        monkeypatch.chdir(tmp_path)
        addon_dir = tmp_path / "lazyaddons"
        addon_dir.mkdir()
        (addon_dir / "echo_args.yaml").write_text(
            "name: echo_args\n"
            "description: test fixture\n"
            "author: tester\n"
            "version: '1.0'\n"
            "enabled: true\n"
            "os: linux\n"
            "tool:\n"
            "  name: echo_args\n"
            "  execute_command: echo {rhost} {arg1} {arg2}\n"
            "category: 12. Miscellaneous\n",
            encoding="utf-8",
        )

        cmdset = LazyCommandSet.__new__(LazyCommandSet)
        shell = cmd2.Cmd(allow_cli_args=False)
        shell.params = {"rhost": "10.10.10.1"}
        cmdset._resolve_shell = lambda: shell

        captured = {}

        def fake_run(command, **kwargs):
            captured["command"] = command
            return "ok"

        with patch("core.process.run_command", side_effect=fake_run):
            cmdset.do_lazy_addon("run echo_args --arg1 hello --arg2 'two words'")

        assert captured["command"] == "echo 10.10.10.1 hello 'two words'", captured
