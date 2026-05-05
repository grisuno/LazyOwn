"""ANSI-aware terminal viewer.

The widget is a write-only ``QPlainTextEdit`` that strips a small set of
ANSI control sequences before appending text. Real terminal emulation is
out of scope; the widget exists to surface cmd2 prompts, command output
and teamserver streams without rendering escape codes literally.

Keystrokes typed inside the widget are emitted as ``input_typed`` so the
backend can choose whether to feed them to a PTY or queue them as a
command.
"""

from __future__ import annotations

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeyEvent, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QWidget

from lazygui.config.constants import AppConstants


_ANSI_CSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_ANSI_OSC_PATTERN = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
_BACKSPACE_PATTERN = re.compile(r"[^\b]\b")
_CARRIAGE_RETURN_PATTERN = re.compile(r"^.*\r(?!\n)", re.MULTILINE)


class TerminalView(QPlainTextEdit):
    """Plain-text view that consumes backend output and emits keystrokes."""

    input_typed = Signal(str)

    def __init__(self, constants: AppConstants, parent: QWidget | None = None) -> None:
        """Configure the widget for log-style append-only behaviour."""
        super().__init__(parent)
        self._constants = constants
        self.setObjectName("TerminalView")
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.setMaximumBlockCount(self._constants.event_log.max_records)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTabChangesFocus(False)
        font = QFont(self._constants.font.monospace_stack[0])
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(self._constants.font.monospace_pt)
        self.setFont(font)

    # --- Output side -------------------------------------------------------

    def append_output(self, text: str) -> None:
        """Append ``text`` after stripping ANSI control codes."""
        sanitized = self._sanitize(text)
        if not sanitized:
            return
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(sanitized)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    @staticmethod
    def _sanitize(raw: str) -> str:
        """Strip a pragmatic subset of ANSI controls and resolve simple CR."""
        text = _ANSI_OSC_PATTERN.sub("", raw)
        text = _ANSI_CSI_PATTERN.sub("", text)
        while True:
            replaced = _BACKSPACE_PATTERN.sub("", text)
            if replaced == text:
                break
            text = replaced
        text = _CARRIAGE_RETURN_PATTERN.sub("", text)
        return text

    # --- Input side --------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Forward keystrokes to listeners instead of mutating the buffer."""
        text_segment = self._translate_key_event(event)
        if text_segment is not None:
            self.input_typed.emit(text_segment)
            event.accept()
            return
        super().keyPressEvent(event)

    @staticmethod
    def _translate_key_event(event: QKeyEvent) -> str | None:
        """Return the raw bytes a backend should receive, or ``None`` to ignore."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.key() in (
            Qt.Key.Key_C,
            Qt.Key.Key_V,
            Qt.Key.Key_A,
            Qt.Key.Key_Plus,
            Qt.Key.Key_Minus,
        ):
            return None
        key = event.key()
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            return "\n"
        if key == Qt.Key.Key_Backspace:
            return "\x7f"
        if key == Qt.Key.Key_Tab:
            return "\t"
        if key == Qt.Key.Key_Up:
            return "\x1b[A"
        if key == Qt.Key.Key_Down:
            return "\x1b[B"
        if key == Qt.Key.Key_Right:
            return "\x1b[C"
        if key == Qt.Key.Key_Left:
            return "\x1b[D"
        text = event.text()
        if text:
            return text
        return None
