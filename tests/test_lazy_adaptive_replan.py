"""Adaptive replanner wiring through the ChainRunner (apt_chain --adaptive).

Every scenario states Given, When, Then.
"""

from __future__ import annotations

import cli.apt_chain_support as support
from cli.apt_chain_support import build_adaptive_replanner, compose_replanners, parse_chain_args
from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunner


def _chain(steps: list[ChainStep]) -> Chain:
    """Build a one-target chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps)


def _fail_locked_out(command: str) -> str:
    """Executor replies that behave as a permission wall."""
    del command
    return "SMB SessionError: STATUS_ACCESS_DENIED"


def _facts(monkeypatch, services: frozenset[str], credentials: bool) -> None:
    """Pin the fact-store observation for a replayable scenario."""
    monkeypatch.setattr(support, "_observed_conditions", lambda target: (services, credentials))


def test_parse_accepts_adaptive_flag():
    """Given --adaptive on the command line, When parsed, Then the flag
    is accepted without errors (loud failures keep for strangers)."""
    args = parse_chain_args("demo 127.0.0.1 --adaptive")
    assert not args.errors
    assert args.adaptive


def test_adaptive_replanner_inserts_alternative_after_permission_wall(monkeypatch):
    """Given a permission-walled dcsync step with LDAP evidence, When the
    chain runs adaptive, Then exactly one alternative technique step is
    attempted and the run carries its lazyalt step."""
    _facts(monkeypatch, frozenset({"ldap"}), False)

    def executor(command: str) -> str:
        """Every command answers with an access-denied wall."""
        del command
        return "SMB SessionError: code 0xc0000022 (ACCESS_DENIED)"

    chain = _chain(
        [
            ChainStep(
                run="secretsdump.py demo /user:admin",
                id="dcsync",
                phase="exploit",
                timeout=5,
                expect="SHELL",
                continue_on_error=True,
            ),
        ]
    )
    runner = ChainRunner(
        chain,
        tokens={"target": "127.0.0.1"},
        executor=executor,
        replanner=build_adaptive_replanner(),
        approver=None,
    )
    result = runner.run()
    assert not result.ok
    alt_steps = [outcome for outcome in result.steps if outcome.id.startswith("lazyalt_")]
    assert len(alt_steps) == 1
    assert "atomic_exploit_bridge.py run --id ad_lab_" in alt_steps[0].run
    assert "delegation" in alt_steps[0].id


def test_lockout_walls_insert_nothing(monkeypatch):
    """Given a lockout verdict, When the chain runs adaptive, Then zero
    alternatives fire: no spray past a lockout."""
    _facts(monkeypatch, frozenset({"microsoft-ds"}), True)

    def executor(command: str) -> str:
        """Every command answers with an account lockout."""
        del command
        return "STATUS_ACCOUNT_LOCKED"

    chain = _chain(
        [
            ChainStep(
                run="kerberoast against dc01",
                id="kt",
                phase="exploit",
                timeout=5,
                expect="SHELL",
                continue_on_error=True,
            ),
        ]
    )
    runner = ChainRunner(
        chain,
        tokens={"target": "127.0.0.1"},
        executor=executor,
        replanner=build_adaptive_replanner(),
        approver=None,
    )
    result = runner.run()
    assert not result.ok
    assert not [outcome for outcome in result.steps if outcome.id.startswith("lazyalt_")]


def test_composed_replanners_run_in_order(monkeypatch):
    """Given an adaptive and a stub replanner, When composed, Then both
    fire for one outcome in declaration order."""
    _facts(monkeypatch, frozenset(), False)
    seen: list[str] = []

    def first(context):
        seen.append("first")

    def second(context):
        seen.append("second")

    composed = compose_replanners([first, second, None])

    class FakeOutcome:
        status = "failed"
        run = "x"
        output = "ACCESS_DENIED"
        reason = ""
        id = "s"

    composed(type("Ctx", (), {"outcome": FakeOutcome()})())
    assert seen == ["first", "second"]


def test_replanner_ignores_ok_outcomes():
    """Given a successful outcome, When the adaptive replanner runs,
    Then no alternative is inserted."""
    replanner = build_adaptive_replanner()
    inserted: list = []

    class Ctx:
        chain_name = "demo"
        target = "127.0.0.1"

        class Outcome:
            status = "ok"
            run = "secretsdump.py"
            output = "ok"
            reason = ""
            id = "s"

        outcome = Outcome()
        executed_ids: list[str] = []
        variables: dict[str, str] = {"target": "127.0.0.1"}

        def insert_step(self, step):
            inserted.append(step)

    replanner(Ctx())
    assert not inserted
