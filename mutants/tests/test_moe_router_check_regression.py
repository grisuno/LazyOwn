"""Regression coverage for ``modules.moe_router.ExpertAvailabilityChecker._check``.

A local ``import pathlib, os`` inside the toposwarm branch used to
shadow the module-level ``os`` import for the whole function. CPython's
function-scope rule made every ``os.environ.get`` higher up in the
function raise :class:`UnboundLocalError`, which the surrounding
``except Exception`` swallowed silently — so the MoE router fell back
to the static path on every call and the experts list collapsed to a
single entry.

These tests pin the corrected behaviour: the groq and ollama branches
read environment variables without touching the toposwarm import path,
and the toposwarm branch resolves a directory through the module-level
``os`` and ``Path`` symbols.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))


def test_check_groq_returns_false_without_api_key(monkeypatch) -> None:
    """The groq branch must not raise ``UnboundLocalError`` when key is empty."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    expert = ExpertProfile(
        expert_id="groq_fast",
        backend="groq",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="") is False


def test_check_groq_returns_true_with_explicit_key() -> None:
    """An explicit ``api_key`` argument shortcircuits without reading env."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    expert = ExpertProfile(
        expert_id="groq_fast",
        backend="groq",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="dummy-key") is True


def test_check_groq_reads_env_when_arg_empty(monkeypatch) -> None:
    """When no api_key is supplied the env var is consulted."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    monkeypatch.setenv("GROQ_API_KEY", "value-from-env")

    expert = ExpertProfile(
        expert_id="groq_fast",
        backend="groq",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="") is True


def test_check_toposwarm_uses_module_level_os_and_path(tmp_path, monkeypatch) -> None:
    """The toposwarm branch must resolve ``TOPOSWARM_DIR`` through stdlib."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    fake_dir = tmp_path / "py" / "toposwarm"
    fake_dir.mkdir(parents=True)
    (fake_dir / "toposwarm_lazyown_orchestrator.py").write_text("# stub")

    monkeypatch.setenv("TOPOSWARM_DIR", str(fake_dir))
    monkeypatch.setitem(sys.modules, "toposwarm_bridge", None)

    expert = ExpertProfile(
        expert_id="topo",
        backend="toposwarm",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="") is True


def test_check_toposwarm_returns_false_when_dir_absent(tmp_path, monkeypatch) -> None:
    """An absent orchestrator file means the backend is unavailable."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    monkeypatch.setenv("TOPOSWARM_DIR", str(tmp_path / "missing"))
    monkeypatch.setitem(sys.modules, "toposwarm_bridge", None)

    expert = ExpertProfile(
        expert_id="topo",
        backend="toposwarm",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="") is False


def test_check_unknown_backend_is_unavailable() -> None:
    """Any backend not enumerated is treated as unavailable."""

    from modules.moe_router import ExpertAvailabilityChecker, ExpertProfile

    expert = ExpertProfile(
        expert_id="alien",
        backend="alien",
        model="x",
        capabilities=["recon"],
        base_weight=1.0,
        cost_tier=1,
        latency_ms=100,
        description="x",
    )
    assert ExpertAvailabilityChecker._check(expert, api_key="") is False
