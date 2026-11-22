from __future__ import annotations

from abc import ABC, abstractmethod

from modules.selection.base import ActionDecision

CommandDecision = ActionDecision


class ICommandSelector(ABC):
    """Contract for command selection strategies."""

    @abstractmethod
    def select(
        self,
        target: str,
        phase: str,
        context: dict,
    ) -> CommandDecision | None:
        """Return a CommandDecision or None if this selector has no suggestion."""
