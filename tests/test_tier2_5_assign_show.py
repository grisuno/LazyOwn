"""Tier 2.5 assign + show tests.

Covers the small but operator-visible behaviours added in Tier 2.5:

- :func:`cli.assign.apply_assign` validates, mutates and persists.
- :func:`cli.show.format_payload` renders deterministic output.
- ``lazyown.py`` wires both helpers into ``do_assign`` / ``do_show`` and
  adds ``complete_assign`` + an aliases refresh after every payload write.

The shell-side checks are static (regex over the source) so the tests do
not have to boot ``LazyOwnShell`` or import ``utils`` (which reads
``sys.argv`` at module load time).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


class TestApplyAssign:
    def test_returns_true_when_key_exists(self):
        from cli.assign import apply_assign

        params = {"rhost": "1.1.1.1"}
        assert apply_assign(params, "rhost", "2.2.2.2") is True
        assert params["rhost"] == "2.2.2.2"

    def test_returns_false_when_key_missing(self):
        from cli.assign import apply_assign

        params = {"rhost": "1.1.1.1"}
        assert apply_assign(params, "unknown_key", "x") is False
        assert "unknown_key" not in params

    def test_does_not_invoke_save_on_failure(self):
        from cli.assign import apply_assign

        calls = []
        params = {"rhost": "1.1.1.1"}
        apply_assign(params, "missing", "x", save=lambda p: calls.append(dict(p)))
        assert calls == []

    def test_invokes_save_on_success(self):
        from cli.assign import apply_assign

        calls = []
        params = {"rhost": "1.1.1.1"}
        apply_assign(params, "rhost", "9.9.9.9", save=lambda p: calls.append(dict(p)))
        assert len(calls) == 1
        assert calls[0]["rhost"] == "9.9.9.9"

    def test_save_receives_mutated_dict(self):
        from cli.assign import apply_assign

        snapshots = []
        params = {"rhost": "1.1.1.1", "lhost": "127.0.0.1"}

        def saver(p):
            snapshots.append(dict(p))

        apply_assign(params, "rhost", "8.8.8.8", save=saver)
        assert snapshots[0] == {"rhost": "8.8.8.8", "lhost": "127.0.0.1"}

    def test_save_optional(self):
        from cli.assign import apply_assign

        params = {"rhost": "1.1.1.1"}
        assert apply_assign(params, "rhost", "x") is True
        assert params["rhost"] == "x"

    def test_persists_to_disk_via_save_payload(self, tmp_path):
        """End-to-end with the real ``core.config.save_payload``."""
        from cli.assign import apply_assign
        from core.config import save_payload

        target = tmp_path / "payload.json"
        params = {"rhost": "1.1.1.1", "lhost": "127.0.0.1"}

        ok = apply_assign(
            params,
            "rhost",
            "10.10.10.10",
            save=lambda p: save_payload(p, target),
        )
        assert ok is True
        on_disk = json.loads(target.read_text(encoding="utf-8"))
        assert on_disk["rhost"] == "10.10.10.10"
        assert on_disk["lhost"] == "127.0.0.1"


class TestFormatPayload:
    def test_empty_payload_returns_empty_string(self):
        from cli.show import format_payload

        assert format_payload({}) == ""

    def test_renders_keys_sorted(self):
        from cli.show import format_payload

        rendered = format_payload({"b": "2", "a": "1", "c": "3"})
        lines = rendered.splitlines()
        assert lines[0].startswith("a")
        assert lines[1].startswith("b")
        assert lines[2].startswith("c")

    def test_aligns_column_to_widest_key(self):
        from cli.show import format_payload

        rendered = format_payload({"a": "1", "long_key": "2"})
        lines = rendered.splitlines()
        width = len("long_key")
        for line in lines:
            assert line[width : width + 2] == "  "
            assert line[width + 2 :].strip() != ""

    def test_none_values_render_as_empty(self):
        from cli.show import format_payload

        rendered = format_payload({"foo": None})
        assert rendered.endswith("  ")

    def test_keys_whitelist_filters_output(self):
        from cli.show import format_payload

        rendered = format_payload({"a": "1", "b": "2", "c": "3"}, keys=["a", "c"])
        keys_seen = [line.split("  ")[0].strip() for line in rendered.splitlines()]
        assert keys_seen == ["a", "c"]

    def test_missing_whitelist_keys_render_as_empty(self):
        from cli.show import format_payload

        rendered = format_payload({"a": "1"}, keys=["a", "missing"])
        lines = {line.split("  ")[0].strip(): line for line in rendered.splitlines()}
        assert lines["missing"].endswith("  ")

    def test_int_value_rendered_as_string(self):
        from cli.show import format_payload

        rendered = format_payload({"port": 4444})
        assert "4444" in rendered

    def test_no_ansi_codes(self):
        from cli.show import format_payload

        rendered = format_payload({"a": "1", "b": "2"})
        assert "\x1b" not in rendered


class TestLazyOwnAssignWiring:
    @pytest.fixture(scope="class")
    def src(self) -> str:
        return LAZYOWN_PATH.read_text(encoding="utf-8")

    def test_imports_apply_assign(self, src):
        assert "from cli.assign import apply_assign" in src

    def test_imports_save_payload_from_core(self, src):
        assert "from core.config import save_payload" in src

    def test_imports_format_payload(self, src):
        assert "from cli.show import format_payload" in src

    def test_do_assign_calls_apply_assign(self, src):
        body = self._extract_method_body(src, "do_assign")
        assert "_apply_assign(" in body
        assert "save=_save_payload" in body

    def test_do_assign_refreshes_aliases(self, src):
        body = self._extract_method_body(src, "do_assign")
        assert "self.aliases.update(" in body
        assert "_load_aliases(self.params)" in body

    def test_do_assign_no_longer_directly_mutates_params(self, src):
        body = self._extract_method_body(src, "do_assign")
        assert "self.params[param] = value" not in body, (
            "do_assign should delegate mutation to apply_assign, not assign self.params directly"
        )

    def test_complete_assign_defined(self, src):
        assert re.search(r"^\s*def complete_assign\(", src, re.MULTILINE)

    def test_complete_assign_reads_self_params(self, src):
        body = self._extract_method_body(src, "complete_assign")
        assert "self.params" in body, "completion must be data-driven from self.params"

    def test_do_show_uses_format_payload(self, src):
        body = self._extract_method_body(src, "do_show")
        assert "_format_payload(self.params)" in body

    def test_do_payload_refreshes_aliases(self, src):
        body = self._extract_method_body(src, "do_payload")
        assert "self.aliases.update(" in body
        assert "_load_aliases(self.params)" in body

    @staticmethod
    def _extract_method_body(src: str, name: str) -> str:
        pattern = re.compile(
            rf"^(\s*)def {re.escape(name)}\(.*?\):\n(.*?)(?=^\1(?:def |@cmd2|@with_)|^class )",
            re.MULTILINE | re.DOTALL,
        )
        match = pattern.search(src)
        if match is None:
            return ""
        return match.group(2)


class TestCompleteAssignBehaviour:
    """Smoke-test the matching logic in isolation, without booting cmd2."""

    def test_returns_keys_starting_with_text(self):
        params = {"rhost": "x", "rport": "y", "lhost": "z"}
        text = "r"
        line = "assign r"
        endidx = len(line)
        # Mirror the production logic.
        import shlex

        try:
            tokens = shlex.split(line[:endidx]) if line else []
        except ValueError:
            tokens = line[:endidx].split()
        index = len(tokens) - (0 if line[:endidx].endswith(" ") else 1)
        assert index == 1
        matches = sorted(k for k in params if k.startswith(text))
        assert matches == ["rhost", "rport"]

    def test_no_completion_for_value_position(self):
        line = "assign rhost "
        endidx = len(line)
        import shlex

        tokens = shlex.split(line[:endidx]) if line else []
        index = len(tokens) - (0 if line[:endidx].endswith(" ") else 1)
        assert index == 2
