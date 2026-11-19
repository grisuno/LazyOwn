"""Post-tool signal is observational, not enforcement (bug 2.3).

The loop step used ``intercept.observe_post_tool`` whose crude regex matched
bare ``timeout``/``no such``, so a benign ``timeout 10 nc`` echo logged a false
``error`` and the label read like an enforcement block. The step now classifies
with the calibrated ``outcome_attribution.classify`` and emits a non-enforcing
``post-signal`` kind that never changes the step's return status.
"""

from __future__ import annotations

import inspect

import modules.intercept as intercept
import modules.lazy_loop as loop
import modules.outcome_attribution as attribution


def test_classify_ignores_benign_timeout_echo():
    """A command that merely echoes ``timeout``/``no such`` is not an error.

    The old classifier flagged it; the calibrated one does not, which is the
    whole point of the swap.
    """
    benign = "timeout 10 nc 10.0.0.1 4444; ls: no such option here"
    assert attribution.classify(benign) == "ok"
    assert intercept.observe_post_tool(benign) == "error"


def test_classify_still_flags_real_block_and_error():
    """Genuine WAF blocks and transport errors are still caught."""
    assert attribution.classify("HTTP/1.1 403 Forbidden\nrequest blocked") == "blocked"
    assert attribution.classify("bash: foo: command not found") == "error"
    assert attribution.classify("HTTP/1.1 200 OK\nserver: cloudflare") == "ok"


def test_guard_step_uses_calibrated_classifier_and_post_signal():
    """The loop step wires the calibrated classifier and a non-enforcing kind."""
    src = inspect.getsource(loop.Worker._guard_step)
    assert "from modules.outcome_attribution import classify" in src
    assert "observe_post_tool" not in src
    assert '"post-signal"' in src
    assert "not enforced" in src


def test_post_signal_block_does_not_short_circuit_return():
    """The post-signal branch emits only; the ok-return path stays below it.

    A block signal must not become a loop enforcement decision: the method's
    terminal success return (``"ok"``) is reached after the post-signal emit.
    """
    src = inspect.getsource(loop.Worker._guard_step)
    signal_at = src.index('"post-signal"')
    ok_return_at = src.rindex('return output, "ok", ""')
    assert ok_return_at > signal_at
