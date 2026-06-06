"""Tests for cli/command_chain.py.

The chain module is decomposed into single-responsibility collaborators so
each level of behaviour is covered in isolation, plus a small set of
facade-level tests that exercise the composition wired in CommandChain.

Tests follow the same conventions as ``tests/test_reactive_hints.py`` and
``tests/test_exploration_engine.py`` — fakes are injected via constructor
arguments, no monkeypatching of module globals.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.command_chain import (  # noqa: E402
    SOURCE_ADDON,
    SOURCE_PHASE,
    SOURCE_STATIC,
    SOURCE_TOOL,
    ChainConfig,
    CommandChain,
    DynamicNextResolver,
    NextStep,
    PrerequisiteRegistry,
    ServiceNextResolver,
    StaticNextRegistry,
    _normalise,
)
from cli.exploration import AddonEntry, DiscoveredService, ToolEntry  # noqa: E402


def _svc(service: str, port: int = 80, host: str = "10.0.0.1", proto: str = "tcp") -> DiscoveredService:
    return DiscoveredService(host=host, port=port, proto=proto, service=service)


class _FakeEngine:
    """Minimal ExplorationEngine double — only the methods the chain uses."""

    def __init__(
        self,
        services: list[DiscoveredService] | None = None,
        addons: list[AddonEntry] | None = None,
        tools: list[ToolEntry] | None = None,
        history: set[str] | None = None,
    ) -> None:
        self._services = services or []
        self._addons = addons or []
        self._tools = tools or []
        self._history = history or set()

    def services(self, target: str | None = None) -> list[DiscoveredService]:
        return list(self._services)

    def unexplored_addons(self, target: str | None = None) -> list[AddonEntry]:
        return list(self._addons)

    def unexplored_tools(self, target: str | None = None) -> list[ToolEntry]:
        return list(self._tools)

    def history(self) -> set[str]:
        return set(self._history)


def test_normalise_strips_do_prefix_and_extra_tokens() -> None:
    assert _normalise("do_lazynmap") == "lazynmap"
    assert _normalise("lazynmap -sV") == "lazynmap"
    assert _normalise("") == ""
    assert _normalise("   ping   ") == "ping"


def test_prerequisites_known_and_unknown() -> None:
    reg = PrerequisiteRegistry()
    assert reg.prerequisites("lazynmap") == ["ping"]
    assert reg.prerequisites("do_evil-winrm") == ["secretsdump"]
    assert reg.prerequisites("nope") == []
    assert reg.prerequisites("ping") == []


def test_missing_prerequisites_skips_already_run() -> None:
    reg = PrerequisiteRegistry()
    assert reg.missing("lazynmap", history=["ping"]) == []
    assert reg.missing("lazynmap", history=[]) == ["ping"]
    assert reg.missing("evil-winrm", history=["secretsdump"]) == []


def test_static_next_registry_uses_killchain_table() -> None:
    reg = StaticNextRegistry()
    nxt = reg.next_for("lazynmap")
    assert "gobuster" in nxt and "enum4linux" in nxt
    assert reg.next_for("do_lazynmap") == nxt
    assert reg.next_for("nope") == []


def test_static_next_registry_phase_priority_fallback() -> None:
    reg = StaticNextRegistry()
    assert "linpeas" in reg.phase_priority("privesc")
    assert reg.phase_priority("") == reg.phase_priority("recon")
    assert reg.phase_priority("bogus") == reg.phase_priority("recon")


def test_service_next_resolver_maps_known_services_only() -> None:
    resolver = ServiceNextResolver()
    out = resolver.followups([_svc("http", 80), _svc("smb", 445, proto="tcp")])
    verbs = [v for v, _r in out]
    assert "gobuster" in verbs
    assert "enum4linux" in verbs
    for _verb, reason in out:
        assert "open " in reason


def test_service_next_resolver_dedupes_repeated_services() -> None:
    resolver = ServiceNextResolver()
    out = resolver.followups([_svc("http", 80), _svc("http", 8080)])
    verbs = [v for v, _r in out]
    assert verbs == sorted(set(verbs), key=verbs.index)


def test_dynamic_next_resolver_orders_static_before_dynamic() -> None:
    engine = _FakeEngine(services=[_svc("smb", 445)], history=set())
    resolver = DynamicNextResolver(exploration_engine=engine)
    steps = resolver.resolve("lazynmap", phase="enum", limit=10)
    names = [s.name for s in steps]
    static_idx = names.index("gobuster") if "gobuster" in names else -1
    service_idx = names.index("enum4linux") if "enum4linux" in names else -1
    assert static_idx != -1 and service_idx != -1
    assert static_idx < service_idx


def test_dynamic_next_resolver_filters_history() -> None:
    engine = _FakeEngine(
        services=[_svc("smb", 445)], history={"enum4linux", "gobuster"}
    )
    resolver = DynamicNextResolver(exploration_engine=engine)
    steps = resolver.resolve("lazynmap", limit=10)
    assert all(s.name not in {"enum4linux", "gobuster"} for s in steps)


def test_dynamic_next_resolver_includes_unexplored_addons_and_tools() -> None:
    addon = AddonEntry(
        name="my_addon", description="", category="14",
        addon_os="linux", trigger=("http",), repo_url="", enabled=True,
        source_path="lazyaddons/my_addon.yaml",
    )
    tool = ToolEntry(
        name="my_tool", description="", category="",
        tool_os="any", trigger=("http",), active=True,
        source_path="tools/my_tool.tool",
    )
    engine = _FakeEngine(
        services=[_svc("http", 80)], addons=[addon], tools=[tool], history=set()
    )
    resolver = DynamicNextResolver(exploration_engine=engine)
    steps = resolver.resolve("lazynmap", limit=20)
    sources = {s.source for s in steps}
    names = {s.name for s in steps}
    assert SOURCE_ADDON in sources and "my_addon" in names
    assert SOURCE_TOOL in sources and "my_tool" in names


def test_dynamic_next_resolver_phase_fallback_when_no_signal() -> None:
    engine = _FakeEngine(services=[], addons=[], tools=[], history=set())
    resolver = DynamicNextResolver(exploration_engine=engine)
    steps = resolver.resolve("unknown_verb", phase="privesc", limit=5)
    assert steps, "expected phase fallback to populate steps"
    assert all(s.source == SOURCE_PHASE for s in steps)


def test_dynamic_next_resolver_respects_limit() -> None:
    engine = _FakeEngine(services=[_svc("http", 80)], history=set())
    resolver = DynamicNextResolver(exploration_engine=engine)
    steps = resolver.resolve("lazynmap", limit=2)
    assert len(steps) == 2


def test_chain_facade_returns_serialisable_view() -> None:
    engine = _FakeEngine(services=[_svc("smb", 445)], history=set())
    chain = CommandChain(
        next_resolver=DynamicNextResolver(exploration_engine=engine)
    )
    view = chain.chain("lazynmap", phase="enum")
    assert view["command"] == "lazynmap"
    assert view["prev"] == ["ping"]
    assert isinstance(view["next"], list)
    for step in view["next"]:
        assert set(step) == {"name", "source", "reason"}


def test_chain_missing_prerequisites_when_history_empty() -> None:
    chain = CommandChain()
    assert chain.missing_prerequisites("lazynmap", history=[]) == ["ping"]
    assert chain.missing_prerequisites("lazynmap", history=["ping"]) == []


def test_next_step_to_dict_round_trip() -> None:
    step = NextStep(name="ping", source=SOURCE_STATIC, reason="seed")
    assert step.to_dict() == {"name": "ping", "source": SOURCE_STATIC, "reason": "seed"}


def test_chain_config_defaults_are_isolated_per_instance() -> None:
    a = ChainConfig()
    b = ChainConfig()
    assert a.prerequisites is not b.prerequisites
    assert a.service_followups is not b.service_followups


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
