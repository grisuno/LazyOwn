"""Engine mediator: the loop's single coordination point to the engines.

Domain ``loop.engines``. The unified autonomous loop (``LazyLoopEngine``)
and the CLI/MCP exploit surfaces used to import the exploit engines
directly (``modules.autonomous_exploit_engine``,
``modules.reactive_engine``, ``modules.ai_exploit_chain``), which couples
the loop god file to every engine implementation. This mediator owns that
edge instead: consumers ask for a port, the mediator lazily resolves the
concrete engine at call time, so monkeypatching an engine stays effective
and import cycles die.

Ports:

- :class:`ExploitRetryPort` — feed captured credentials back into the
  autonomous exploit engine's retry queue (credential reuse).
- :class:`ReactionPort` — reactive-engine analysis of step output into
  next-action decisions.
- :class:`ReasoningPort` — exploit-chain strategy reasoning (direct,
  brute-force, path-traversal, ...) over a target profile.

Failure semantics: every port call degrades to a no-op answer (empty
list, empty string) when its engine import fails, so a missing engine
never breaks the loop round.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from modules.mediation.contracts import MediatorContract


@runtime_checkable
class ExploitRetryPort(Protocol):
    """Request-port for credential reuse through the exploit engine."""

    def retry_with_credentials(self, target: str, credentials: list[dict]) -> int:
        """Queue one retry attempt per captured credential pair.

        Args:
            target: Host the credentials were captured from.
            credentials: Captured credential dicts.

        Returns:
            Number of attempts queued; 0 when the engine is unavailable.
        """
        ...


@runtime_checkable
class ReactionPort(Protocol):
    """Request-port for reactive decision analysis."""

    def analyse(self, output: str, command: str, platform: str) -> list[Any]:
        """Analyse one command's output for next-action decisions.

        Args:
            output: Captured command output.
            command: The command that produced it.
            platform: Target platform hint.

        Returns:
            Decision objects; empty when the engine is unavailable.
        """
        ...


@runtime_checkable
class ReasoningPort(Protocol):
    """Request-port for exploit-chain strategy reasoning."""

    def reason(self, target: str) -> Any:
        """Return the next exploit strategy for a target.

        Args:
            target: Host under test.

        Returns:
            The strategy decision, or None when unavailable.
        """
        ...


class EngineMediator:
    """Mediate engine access for the autonomous loop and CLI surfaces."""

    domain = "loop.engines"

    def describe(self) -> dict[str, Any]:
        """Return introspection metadata for diagnostics."""
        return {
            "domain": self.domain,
            "ports": ["exploit_retry", "reaction", "reasoning"],
            "engines": ["autonomous_exploit_engine", "reactive_engine", "ai_exploit_chain"],
        }

    def retry_with_credentials(self, target: str, credentials: list[dict]) -> int:
        """Queue captured credentials into the exploit engine's retry loop.

        Args:
            target: Host the credentials were captured from.
            credentials: Credential dicts from the reaction bridge.

        Returns:
            Attempts queued, or 0 when the engine is unavailable.
        """
        if not target or not credentials:
            return 0
        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            engine = AutonomousExploitEngine.get_instance()
            engine.retry_with_credentials(target, credentials=credentials)
            return len(credentials)
        except Exception:
            return 0

    def analyse(self, output: str, command: str, platform: str) -> list[Any]:
        """Run reactive-engine analysis over one step's output.

        Args:
            output: Captured output of the executed command.
            command: Command line that produced the output.
            platform: Target platform hint for decision scoping.

        Returns:
            Decision objects, or an empty list when unavailable.
        """
        try:
            from modules.reactive_engine import get_engine

            return list(get_engine().analyse(output=output, command=command, platform=platform) or [])
        except Exception:
            return []

    def reason(self, target: str) -> Any:
        """Return the exploit-chain strategy for a target.

        Args:
            target: Host under test.

        Returns:
            The chainer's strategy decision, or None when unavailable.
        """
        if not str(target or "").strip():
            return None
        try:
            from modules.ai_exploit_chain import AIExploitChainer, ExploitChainContext
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            profile = AutonomousExploitEngine().profile(str(target).strip())
            chainer = AIExploitChainer()
            context = ExploitChainContext(
                target=str(target).strip(),
                profile=profile,
                attempted=[],
                available_strategies=chainer.build_chain_plan(
                    ExploitChainContext(target=str(target).strip(), profile=profile)
                ),
                current_phase="recon",
            )
            return chainer.reason(context)
        except Exception:
            return None


__all__ = ["EngineMediator", "ExploitRetryPort", "ReactionPort", "ReasoningPort"]
