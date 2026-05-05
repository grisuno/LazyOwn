"""In-memory ring buffer for :class:`EventRecord`.

Centralising log retention here lets every backend feed events in and every
panel observe them without coupling the two sides directly. The buffer
imposes a hard cap (configured via :class:`EventLogConstants`) so a chatty
backend can never starve memory.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable

from PySide6.QtCore import QObject, Signal

from lazygui.config.constants import AppConstants
from lazygui.services.models import EventLevel, EventRecord


class EventLog(QObject):
    """Bounded, thread-safe-ish ring buffer of events with Qt signalling."""

    record_appended = Signal(EventRecord)
    cleared = Signal()

    def __init__(self, constants: AppConstants, parent: QObject | None = None) -> None:
        """Initialise the buffer using ``constants.event_log.max_records``."""
        super().__init__(parent)
        self._capacity = constants.event_log.max_records
        self._records: deque[EventRecord] = deque(maxlen=self._capacity)

    @property
    def capacity(self) -> int:
        """Maximum number of records retained before the oldest is dropped."""
        return self._capacity

    def append(self, record: EventRecord) -> None:
        """Append ``record`` and emit ``record_appended``."""
        self._records.append(record)
        self.record_appended.emit(record)

    def extend(self, records: Iterable[EventRecord]) -> None:
        """Append every entry in ``records`` in iteration order."""
        for record in records:
            self.append(record)

    def clear(self) -> None:
        """Drop all stored records and emit ``cleared``."""
        self._records.clear()
        self.cleared.emit()

    def snapshot(self, minimum_level: EventLevel | None = None) -> tuple[EventRecord, ...]:
        """Return a defensive tuple, optionally filtered by ``minimum_level``."""
        if minimum_level is None:
            return tuple(self._records)
        threshold = minimum_level.numeric
        return tuple(record for record in self._records if record.level.numeric >= threshold)
