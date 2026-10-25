"""Specialised mediator for step-ordering feedback coordination.

Owns the ``modules.lazy_orchestrator_feedback`` interaction so the loop
planner requests ordering through this mediator instead of importing the
feedback module directly.
"""

from __future__ import annotations

from typing import Any


class FeedbackMediator:
    """Mediate orchestrator feedback used to order loop steps."""

    domain: str = "loop.feedback"

    def describe(self) -> dict[str, Any]:
        """Return mediator metadata for diagnostics."""
        return {"domain": self.domain}

    def order_steps(self, steps: list[str], stack: str = "") -> list[str]:
        """Reorder worker steps with cross-task priors.

        Args:
            steps: Command step strings in proposed order.
            stack: Target stack fingerprint for priors.

        Returns:
            Reordered steps, or the input order on failure.
        """
        try:
            from modules.lazy_orchestrator_feedback import order_steps

            return order_steps(list(steps), stack=stack)
        except Exception:
            return list(steps)
