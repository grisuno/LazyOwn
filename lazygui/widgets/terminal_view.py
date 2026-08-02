"""ANSI-aware terminal viewer.

Strips ANSI escape codes and control characters before appending text.
Handles cmd2 prompt rendering, colour codes, cursor positioning, and
carriage-return semantics.
"""

from __future__ import annotations

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeyEvent, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QWidget

from lazygui.config.constants import AppConstants

_ANSI_ESCAPE = re.compile(
    r"\x1b"                         # ESC
    r"(?:"
    r"\[[0-9;?]*[ -/]*[@-~]"       # CSI: ESC [ params... letter
    r"|\][^\x07\x1b]*(?:\x07|\x1b\\)"  # OSC: ESC ] ... BEL or ST
    r"|[()][AB012]"                 # charset select
    r"|[#>78=]"                     # keyboard/mode changes
    r"|[DP\]X^_]"                   # other single-char ESC sequences
    r")"
)
_CTRL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_CR_LF = re.compile(r"\r\n")
_CR = re.compile(r"\r(?!\n)")


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

    def append_output(self, text: str) -> None:
        """Append ``text`` after stripping ANSI control codes and control chars."""
        sanitized = self._sanitize(text)
        if not sanitized.strip():
            return
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(sanitized)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    @staticmethod
    def _sanitize(raw: str) -> str:
        text = _ANSI_ESCAPE.sub("", raw)
        text = _CR_LF.sub("\n", text)
        text = _CR.sub("\n", text)
        text = _CTRL_CHARS.sub("", text)
        lines = [line.strip() for line in text.split("\n")]
        lines = [line for line in lines if line]
        return "\n".join(lines)

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
