"""Contract tests for modules/loop/control_plane.py.

Pins the per-step operator control gate extracted from the daemon
``_run_objective`` coroutine: focus loss and pause handling, with the
fail-open "continue" guarantee on any control error.
"""

import asyncio

from modules.loop.control_plane import precheck_control


class _FakeControl:
    """Minimal operator control handle for the precheck gate."""

    def __init__(self, in_focus=True, paused=False, focus_targets=None, raise_on=None):
        self._in_focus = in_focus
        self._paused = paused
        self._focus_targets = focus_targets or []
        self._raise_on = raise_on

    def target_in_focus(self, _target):
        if self._raise_on == "focus":
            raise RuntimeError("control file corrupt")
        return self._in_focus

    def is_paused(self):
        return self._paused

    def load(self):
        return type("S", (), {"focus_targets": self._focus_targets})()


def _run(control, emit, **kwargs):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(
            precheck_control(
                control,
                "10.0.0.5",
                "obj1",
                1,
                emit=emit,
                loop=loop,
                wait_until_unpaused=kwargs.get("wait_until_unpaused"),
                poll_interval=0.0,
                max_wait=10.0,
            )
        )
    finally:
        loop.close()


def _collect():
    events = []
    return events, (lambda name, payload: events.append((name, payload)))


def test_no_control_continues():
    events, emit = _collect()
    assert _run(None, emit) is False
    assert events == []


def test_out_of_focus_stops():
    events, emit = _collect()
    control = _FakeControl(in_focus=False, focus_targets=["10.0.0.9"])
    assert _run(control, emit) is True
    assert events[0][0] == "TARGET_OUT_OF_FOCUS"
    assert events[0][1]["focus"] == ["10.0.0.9"]


def test_in_focus_not_paused_continues():
    events, emit = _collect()
    control = _FakeControl(in_focus=True, paused=False)
    assert _run(control, emit, wait_until_unpaused=lambda *a, **k: True) is False
    assert events == []


def test_paused_then_resumed_continues():
    events, emit = _collect()
    control = _FakeControl(in_focus=True, paused=True)
    assert _run(control, emit, wait_until_unpaused=lambda *a, **k: True) is False
    names = [e[0] for e in events]
    assert names == ["DAEMON_PAUSED", "DAEMON_RESUMED"]


def test_paused_beyond_ceiling_stops():
    events, emit = _collect()
    control = _FakeControl(in_focus=True, paused=True)
    assert _run(control, emit, wait_until_unpaused=lambda *a, **k: False) is True
    names = [e[0] for e in events]
    assert names == ["DAEMON_PAUSED", "DAEMON_PAUSE_TIMEOUT"]


def test_paused_without_waiter_skips_pause():
    events, emit = _collect()
    control = _FakeControl(in_focus=True, paused=True)
    assert _run(control, emit, wait_until_unpaused=None) is False
    assert events == []


def test_control_error_fails_open():
    events, emit = _collect()
    control = _FakeControl(raise_on="focus")
    assert _run(control, emit) is False
