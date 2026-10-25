"""pi loop-leg contract tests.

The ``pi:`` model spec routes loop-mode completions through the local pi
coding-agent CLI (``local-qwen`` provider on the llama.cpp Qwen server).
Like the ``toposwarm:`` leg, ``pi:`` is a completion prefix only — it is
deliberately NOT a registered factory backend, so the backend contract
in ``test_llm_contract.py`` stays untouched. Dead legs raise
``RuntimeError`` so ``LlmPool.complete`` fails over to the next member.
"""

from __future__ import annotations

import subprocess

import pytest

from modules import llm_factory


class _Proc:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _patch_run(monkeypatch: pytest.MonkeyPatch, proc: _Proc, **kwargs) -> dict:
    """Patch which/run; return the captured call kwargs."""
    monkeypatch.setattr(llm_factory.shutil, "which", lambda name: "/usr/bin/pi")
    seen: dict = {}

    def _fake_run(cmd, **call_kwargs):
        seen["cmd"] = cmd
        seen.update(call_kwargs)
        exc = kwargs.get("raise_exc")
        if exc is not None:
            raise exc
        return proc

    monkeypatch.setattr(llm_factory.subprocess, "run", _fake_run)
    return seen


def test_pi_missing_binary_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """No pi CLI in PATH raises for pool failover."""
    monkeypatch.setattr(llm_factory.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="not in PATH"):
        llm_factory.complete("pi:local-model", "hi")


def test_pi_success_returns_text(monkeypatch: pytest.MonkeyPatch) -> None:
    """Happy path returns stripped stdout via list-form argv, shell=False."""
    seen = _patch_run(monkeypatch, _Proc(stdout="  hello world\n"))
    assert llm_factory.complete("pi:local-model", "hi") == "hello world"
    assert seen["cmd"][:4] == ["/usr/bin/pi", "--model", "local-qwen/local-model", "--print"]
    assert seen["cmd"][4] == "hi"
    assert seen["shell"] is False


def test_pi_model_passthrough(monkeypatch: pytest.MonkeyPatch) -> None:
    """Spec model id selects the pi provider model."""
    seen = _patch_run(monkeypatch, _Proc(stdout="ok"))
    llm_factory.complete("pi:other-id", "hi")
    assert seen["cmd"][2] == "local-qwen/other-id"


def test_pi_default_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """Bare pi: prefix uses the local-model default."""
    seen = _patch_run(monkeypatch, _Proc(stdout="ok"))
    llm_factory.complete("pi:", "hi")
    assert seen["cmd"][2] == "local-qwen/local-model"


def test_pi_prefix_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    """PI: resolves like pi:."""
    seen = _patch_run(monkeypatch, _Proc(stdout="ok"))
    assert llm_factory.complete("PI:local-model", "hi") == "ok"
    assert seen["cmd"][2] == "local-qwen/local-model"


def test_pi_nonzero_exit_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-zero CLI exit raises for pool failover."""
    _patch_run(monkeypatch, _Proc(returncode=1, stderr="boom"))
    with pytest.raises(RuntimeError, match="failed"):
        llm_factory.complete("pi:local-model", "hi")


def test_pi_empty_reply_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Empty stdout raises so the pool moves to the next leg."""
    _patch_run(monkeypatch, _Proc(stdout="   \n"))
    with pytest.raises(RuntimeError, match="empty"):
        llm_factory.complete("pi:local-model", "hi")


def test_pi_timeout_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Expired subprocess timeout raises for pool failover."""
    _patch_run(
        monkeypatch,
        _Proc(),
        raise_exc=subprocess.TimeoutExpired(cmd="pi", timeout=1),
    )
    with pytest.raises(RuntimeError, match="timed out"):
        llm_factory.complete("pi:local-model", "hi")


def test_pi_empty_prompt_short_circuits(monkeypatch: pytest.MonkeyPatch) -> None:
    """Empty prompt never shells out."""
    called = []
    monkeypatch.setattr(llm_factory.shutil, "which", lambda name: called.append(name) or "/usr/bin/pi")
    assert llm_factory.complete("pi:local-model", "   ") == ""
    assert called == []


def test_pi_stream_falls_back_to_complete(monkeypatch: pytest.MonkeyPatch) -> None:
    """stream_complete has no pi streamer; it must answer via complete()."""
    seen = _patch_run(monkeypatch, _Proc(stdout="streamed-ok"))
    assert llm_factory.stream_complete("pi:local-model", "hi") == "streamed-ok"
    assert seen["cmd"][2] == "local-qwen/local-model"


def test_pi_pool_member_resolves(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """The loop pool drives the pi leg through the factory spec."""
    from modules.lazy_loop import LlmPool

    monkeypatch.setattr(
        llm_factory,
        "_pi_complete",
        lambda model, prompt, max_tokens=800: "pi-says-hi",
    )
    pool = LlmPool.__new__(LlmPool)
    pool._health = None
    pool._path = tmp_path / "llm_pool.json"
    pool._usage = tmp_path / "llm_usage.json"
    members = [{"name": "pi-qwen", "model": "pi:local-model", "priority": 6}]
    assert pool.complete("hi", members=members) == "pi-says-hi"
