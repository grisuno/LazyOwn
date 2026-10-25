"""specialised mediator for recon-intel coordination.

Owns every interaction with ``modules.lazy_intel`` and the loop activity
log so the loop, planners and observability code depend on this mediator
instead of importing the intel module (or the loop god file) directly.
"""

from __future__ import annotations

from typing import Any


class IntelMediator:
    """Mediate intel routing, masking, stack signatures and activity spans."""

    domain: str = "loop.intel"

    def __init__(self) -> None:
        """Start with no registered activity-log factory."""
        self._activity_log_factory: Any = None

    def register_activity_log_factory(self, factory: Any) -> None:
        """Register the loop-side activity log factory.

        Args:
            factory: Callable receiving ``task_id`` and returning a
                task-scoped object exposing ``read(limit)`` for activity
                records (``modules.lazy_loop.ActivityLog``).
        """
        self._activity_log_factory = factory

    def describe(self) -> dict[str, Any]:
        """Return mediator metadata for diagnostics."""
        return {
            "domain": self.domain,
            "activity_log_registered": self._activity_log_factory is not None,
        }

    def activity_records(self, task_id: str, limit: int = 200) -> list[dict]:
        """Return loop activity records for one task.

        The factory is task-scoped (``ActivityLog(task_id)``), so records
        return exactly as the per-task store yields them.

        Args:
            task_id: Loop task identifier.
            limit: Maximum records to return.

        Returns:
            Record dicts oldest-first, empty when no factory is registered.
        """
        if self._activity_log_factory is not None:
            try:
                return self._activity_log_factory(str(task_id)).read(limit)
            except Exception:
                return []
        try:
            from modules.lazy_loop import ActivityLog

            return ActivityLog(str(task_id)).read(limit)
        except Exception:
            return []

    def record_routing_decision(
        self,
        task_id: str,
        intent_id: int,
        command: str,
        intent_text: str = "",
        target: str = "",
        stack: str = "",
    ) -> None:
        """Record which verb the loop chose for one intent.

        Args:
            task_id: Loop task identifier.
            intent_id: Exploration node the command serves.
            command: Resolved shell command line.
            intent_text: Original intent summary for source inference.
            target: Bound target, if any.
            stack: Target stack fingerprint.
        """
        try:
            from modules.lazy_intel import record_routing_decision

            record_routing_decision(
                task_id,
                intent_id,
                command,
                intent_text=intent_text,
                target=target,
                stack=stack,
            )
        except Exception:
            pass

    def record_routing_outcome(
        self,
        task_id: str,
        intent_id: int,
        command: str,
        state: str = "",
        facts: int = 0,
        findings: int = 0,
        stack: str = "",
    ) -> None:
        """Record the terminal outcome of one executed command.

        Args:
            task_id: Loop task identifier.
            intent_id: Exploration node the command served.
            command: Executed shell command line.
            state: Terminal intent state.
            facts: Facts persisted by the intent.
            findings: Findings reported by the intent.
            stack: Target stack fingerprint.
        """
        try:
            from modules.lazy_intel import record_routing_outcome

            record_routing_outcome(
                task_id,
                intent_id,
                command,
                state=state,
                facts=facts,
                findings=findings,
                stack=stack,
            )
        except Exception:
            pass

    def mask_configured(self, text: str) -> str:
        """Strip operator-configured secrets from LLM-bound context.

        Args:
            text: Raw prompt context.

        Returns:
            Masked text, or the input when masking is unavailable.
        """
        try:
            from modules.lazy_intel import mask_configured

            return mask_configured(text)
        except Exception:
            return str(text or "")

    def stack_signature(self, assets: Any = None) -> str:
        """Return the target stack fingerprint string.

        Args:
            assets: Asset graph to fingerprint.

        Returns:
            Fingerprint string, empty when the graph is unreadable.
        """
        try:
            from modules.lazy_intel import stack_signature

            return stack_signature(assets)
        except Exception:
            return ""
