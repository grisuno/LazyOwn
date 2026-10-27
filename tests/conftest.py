"""Global pytest isolation hooks.

Resets module-level singleton state that otherwise leaks between tests and
causes order-dependent failures (the world-model singleton cached by
``modules.world_model.get_world_model``). Each test starts from a clean
singleton so a test can never observe engagement state written by an
earlier test.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolated_llm_health(tmp_path, monkeypatch):
    """Isolate the persisted LLM breaker and its shared registry per test.

    ``llm_pool`` is importable both as ``modules.llm_pool`` and as a
    top-level ``llm_pool`` (tests that add ``modules/`` to ``sys.path``);
    both module objects must point at the isolated path or breaker state
    leaks between tests through the real ``sessions/lazy`` file.
    """
    import importlib
    import sys
    from pathlib import Path as _Path

    modules_dir = str(_Path(__file__).resolve().parent.parent / "modules")
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)

    def _isolated_path():
        return tmp_path / "llm_health.json"

    for module_name in ("modules.llm_pool", "llm_pool"):
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        monkeypatch.setattr(module, "_health_path", _isolated_path, raising=False)
        if hasattr(module, "_SHARED_HEALTH"):
            monkeypatch.setattr(module, "_SHARED_HEALTH", None)


@pytest.fixture(autouse=True)
def _fast_llm_connect_backoff(monkeypatch):
    """Keep the pool's connect-retry backoff out of test wall-clock.

    The retry itself is exercised by unit tests that stub ``sleep``;
    everywhere else the offline backend fails fast, so the real backoff
    would only add seconds per pool call across the suite.
    """
    try:
        import modules.lazy_loop as loop_module

        monkeypatch.setattr(loop_module, "LLM_CONNECT_BACKOFF_SEC", 0.0)
    except Exception:
        return


@pytest.fixture(autouse=True)
def _reset_world_model_singleton() -> None:
    """Drop the cached WorldModel before and after every test."""
    import modules.world_model as wm

    wm._default_wm = None
    yield
    wm._default_wm = None


@pytest.fixture(autouse=True)
def _reset_guard_harness() -> None:
    """Give every test a fresh capacity ledger in the shared harness.

    The global harness is process-wide and its capacity envelope
    accumulates units across a long session; without a per-test reset a
    suite-wide run saturates the mission tier and unrelated guarded
    calls are refused (order-dependent failures).
    """
    try:
        from modules.guardrails.harness import reset_global_harness
    except Exception:
        yield
        return
    reset_global_harness()
    yield
    reset_global_harness()


@pytest.fixture(autouse=True)
def _offline_llm_for_loop_tests(request, monkeypatch):
    """Loop/lazy unit tests never reach live LLM backends.

    The loop's planner and goal decomposer call the configured chain;
    without this pin the suite would depend on whatever local ollama or
    gateway happens to answer, making tests slow and nondeterministic.
    Tests exercising the pool patch ``llm_factory.complete`` themselves.
    """
    raw = getattr(getattr(request.node, "module", None), "__name__", "") or ""
    name = raw.rsplit(".", 1)[-1]
    if not name.startswith(("test_loop", "test_lazy")):
        return
    try:
        import modules.llm_factory as factory
    except Exception:
        return

    def _offline(model, prompt, max_tokens=800):
        raise RuntimeError("llm backends disabled in unit tests")

    monkeypatch.setattr(factory, "complete", _offline)

    class _HealthyRegistry:
        """Health stub keeping every member available for the test."""

        def healthy(self, name: str) -> bool:
            return True

        def report_failure(self, name: str, reason: str = "") -> None:
            return None

        def report_success(self, name: str) -> None:
            return None

    try:
        import modules.llm_pool as pool_module

        monkeypatch.setattr(pool_module, "shared_registry", lambda: _HealthyRegistry())
    except Exception:
        pass

    try:
        import modules.lazy_loop as loop_module

        monkeypatch.setattr(loop_module, "COLD_BACKGROUND_ENABLED", False)
        monkeypatch.setattr(loop_module, "REPORTER_BACKGROUND_ENABLED", False)
    except Exception:
        pass

    try:
        import modules.lazy_agent as agent_module

        monkeypatch.setattr(agent_module, "resolve_agentic_model", lambda exclude=None: None)
    except Exception:
        pass

    try:
        import modules.loop_ai_bridge as bridge_module

        monkeypatch.setattr(bridge_module, "_stage", lambda name, default=True: False)
        monkeypatch.setattr(bridge_module, "_SINGLETONS", {})
    except Exception:
        pass

    try:
        import tempfile
        from pathlib import Path as _Path

        import modules.lazy_bridge as bridge

        sandbox = _Path(tempfile.mkdtemp(prefix="lazy-bridge-test-"))
        monkeypatch.setattr(bridge, "SESSIONS_DIR", sandbox)
        monkeypatch.setattr(bridge, "LAZY_DIR", sandbox)
    except Exception:
        pass
