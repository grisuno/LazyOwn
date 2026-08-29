"""Tests for cli/command_form.py.

Exercises field selection, default propagation from payload, command
assembly and the runner override.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.command_form import (  # noqa: E402
    CommandFormConfig,
    CommandFormState,
    build_state,
    launch_form,
)


def _index() -> dict:
    return {
        "commands": [
            {"name": "do_lazynmap", "summary": "nmap orchestration"},
            {"name": "do_ffuf", "summary": "web fuzzer"},
        ],
    }


def test_fields_default_set_when_command_unknown() -> None:
    """Commands without a per-command field set fall back to the default."""
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_unknown_verb",
        index=_index(),
        payload={},
    )
    fields = state.fields()
    assert tuple(field.identifier for field in fields) == ("target", "attacker", "port")


def test_fields_specific_set_for_known_command() -> None:
    """Per-command sets win over the default."""
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload={},
    )
    identifiers = [field.identifier for field in state.fields()]
    assert "target" in identifiers
    assert "device" in identifiers


def test_initial_values_come_from_payload() -> None:
    """Fields are pre-populated from the matching payload key."""
    payload = {"rhost": "10.0.0.5", "rport": 8443}
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload=payload,
    )
    assert state.values["target"] == "10.0.0.5"
    assert state.values["port"] == "8443"


def test_overrides_lists_diverging_field_payload_pairs() -> None:
    """Diverging values are surfaced as ``(payload_key, value)`` tuples."""
    payload = {"rhost": "10.0.0.1"}
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload=payload,
    )
    state.set_value("target", "10.0.0.99")
    overrides = state.overrides()
    assert ("rhost", "10.0.0.99") in overrides


def test_overrides_empty_when_values_match_payload() -> None:
    """Untouched fields produce no overrides."""
    payload = {"rhost": "10.0.0.1"}
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload=payload,
    )
    assert state.overrides() == []


def test_verb_line_returns_just_verb_without_extras() -> None:
    """``verb_line`` strips ``do_`` and appends extra args when present."""
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload={},
    )
    assert state.verb_line() == "lazynmap"
    state.set_extra_args("-T4 --top-ports 1000")
    assert state.verb_line() == "lazynmap -T4 --top-ports 1000"


def test_build_command_preview_renders_annotations_and_verb() -> None:
    """The preview string keeps overrides + verb on a single readable line."""
    payload = {"rhost": "10.0.0.1"}
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_lazynmap",
        index=_index(),
        payload=payload,
    )
    state.set_value("target", "10.0.0.99")
    preview = state.build_command()
    assert "rhost=10.0.0.99" in preview
    assert "lazynmap" in preview


def test_is_valid_true_when_command_known() -> None:
    """A name present in the index is reported as valid."""
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="lazynmap",
        index=_index(),
        payload={},
    )
    assert state.is_valid() is True
    assert state.summary() == "nmap orchestration"


def test_is_valid_false_for_unknown_command() -> None:
    """An unknown verb is reported as invalid."""
    state = CommandFormState(
        config=CommandFormConfig(),
        command_name="do_bogus",
        index=_index(),
        payload={},
    )
    assert state.is_valid() is False


def test_launch_form_runner_returns_state() -> None:
    """The runner override lets tests bypass Textual and inspect overrides."""
    payload = {"rhost": "10.0.0.1"}

    def runner(context):
        state = context["state"]
        state.set_value("target", "10.0.0.7")
        return state

    result = launch_form("lazynmap", payload=payload, runner=runner)
    assert result is not None
    assert ("rhost", "10.0.0.7") in result.overrides()
    assert result.verb_line() == "lazynmap"


def test_build_state_loads_from_default_index(monkeypatch) -> None:
    """The factory wires through ``cli.palette.load_index`` when no override given."""
    monkeypatch.setattr("cli.command_form._load_index", lambda: _index())
    state = build_state("lazynmap")
    assert state.summary() == "nmap orchestration"
