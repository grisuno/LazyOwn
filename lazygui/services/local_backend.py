"""Local backend that runs the LazyOwn cmd2 console on a PTY.

This backend fork-execs a shell process inside a PTY so the GUI can render
the cmd2 prompt with full ANSI semantics. It exposes the same interface as
the teamserver backend so panels can switch between the two transparently.
"""

from __future__ import annotations

import errno
import fcntl
import logging
import os
import pty
import signal
import struct
import termios
from typing import Sequence

from PySide6.QtCore import QObject, QSocketNotifier, QTimer

from lazygui.config.constants import AppConstants
from lazygui.config.paths import AppPaths
from lazygui.services.backend import Backend, BackendDescriptor, BackendStatus
from lazygui.services.models import EventLevel, EventRecord, Listener, Operator, Session

_logger = logging.getLogger(__name__)


class LocalPtyBackend(Backend):
    """Spawn a shell on a PTY and stream its output to the UI.

    The backend cannot enumerate sessions or listeners on its own — the cmd2
    console prints them to the terminal and the operator parses them
    visually. ``known_sessions`` / ``known_listeners`` therefore stay empty.
    """

    def __init__(
        self,
        constants: AppConstants,
        paths: AppPaths,
        parent: QObject | None = None,
    ) -> None:
        """Initialise the backend with the shared constants and paths."""
        descriptor = BackendDescriptor(
            identifier=constants.backend.local_id,
            display_name="Local console",
            summary="Run the LazyOwn cmd2 console in this process via a PTY.",
        )
        super().__init__(descriptor=descriptor, parent=parent)
        self._constants = constants
        self._paths = paths
        self._child_pid: int | None = None
        self._master_fd: int | None = None
        self._notifier: QSocketNotifier | None = None
        self._reaper: QTimer | None = None
        self._terminal_columns: int = constants.pty.initial_cols
        self._terminal_rows: int = constants.pty.initial_rows

    # --- Backend lifecycle -------------------------------------------------

    def start(self) -> None:
        """Fork-exec the cmd2 console behind a PTY."""
        if self._child_pid is not None:
            return
        self._set_status(BackendStatus.CONNECTING)
        try:
            child_pid, master_fd = pty.fork()
        except OSError as exc:
            self._emit_event(EventLevel.CRITICAL, f"PTY fork failed: {exc}")
            self._set_status(BackendStatus.ERROR)
            raise

        if child_pid == 0:
            self._exec_child_process()
            return

        self._child_pid = child_pid
        self._master_fd = master_fd
        self._configure_master_fd()
        self._install_window_size()
        self._install_read_notifier()
        self._install_reaper()
        self._set_status(BackendStatus.CONNECTED)
        self._emit_event(EventLevel.INFO, f"Local console started (pid={child_pid}).")

    def stop(self) -> None:
        """Send ``SIGTERM`` to the child and tear down notifiers."""
        if self._notifier is not None:
            self._notifier.setEnabled(False)
            self._notifier.deleteLater()
            self._notifier = None
        if self._reaper is not None:
            self._reaper.stop()
            self._reaper.deleteLater()
            self._reaper = None
        if self._child_pid is not None:
            try:
                os.kill(self._child_pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            self._child_pid = None
        if self._master_fd is not None:
            try:
                os.close(self._master_fd)
            except OSError:
                pass
            self._master_fd = None
        self._set_status(BackendStatus.DISCONNECTED)
        self._emit_event(EventLevel.INFO, "Local console stopped.")

    def send_command(self, command: str, target_session: str | None = None) -> None:
        """Write ``command`` followed by a newline to the PTY."""
        del target_session
        self.feed_terminal_input(command + "\n")

    def refresh(self) -> None:
        """No-op for the local backend; the operator drives data from cmd2."""
        self._emit_event(EventLevel.DEBUG, "Local backend refresh requested (no-op).")

    def resize_terminal(self, columns: int, rows: int) -> None:
        """Propagate the new size to the PTY using ``TIOCSWINSZ``."""
        self._terminal_columns = columns
        self._terminal_rows = rows
        self._install_window_size()

    def feed_terminal_input(self, data: str) -> None:
        """Encode ``data`` and write it to the master end of the PTY."""
        if self._master_fd is None:
            return
        encoded = data.encode(self._constants.pty.encoding, errors=self._constants.pty.encoding_errors)
        try:
            os.write(self._master_fd, encoded)
        except OSError as exc:
            self._emit_event(EventLevel.ERROR, f"PTY write failed: {exc}")

    def known_sessions(self) -> Sequence[Session]:
        """Local backend does not enumerate sessions."""
        return ()

    def known_listeners(self) -> Sequence[Listener]:
        """Local backend does not enumerate listeners."""
        return ()

    # --- Internals --------------------------------------------------------

    def _exec_child_process(self) -> None:
        """Replace the forked child with ``run`` inside the project root."""
        try:
            os.chdir(self._paths.project_root)
            os.execvp(self._constants.pty.spawn_executable, list(self._constants.pty.spawn_argv))
        except OSError as exc:
            os.write(2, f"Failed to spawn LazyOwn console: {exc}\n".encode())
            os._exit(127)

    def _configure_master_fd(self) -> None:
        """Mark the master fd non-blocking so reads can be polled."""
        if self._master_fd is None:
            return
        flags = fcntl.fcntl(self._master_fd, fcntl.F_GETFL)
        fcntl.fcntl(self._master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def _install_window_size(self) -> None:
        """Send the current terminal dimensions to the PTY."""
        if self._master_fd is None:
            return
        size_struct = struct.pack("HHHH", self._terminal_rows, self._terminal_columns, 0, 0)
        try:
            fcntl.ioctl(self._master_fd, termios.TIOCSWINSZ, size_struct)
        except OSError as exc:
            self._emit_event(EventLevel.WARNING, f"TIOCSWINSZ failed: {exc}")

    def _install_read_notifier(self) -> None:
        """Wire a ``QSocketNotifier`` to fire when the PTY has output."""
        if self._master_fd is None:
            return
        self._notifier = QSocketNotifier(self._master_fd, QSocketNotifier.Type.Read, self)
        self._notifier.activated.connect(self._on_master_readable)

    def _install_reaper(self) -> None:
        """Periodically waitpid() to detect when the cmd2 console exits."""
        self._reaper = QTimer(self)
        self._reaper.setInterval(self._constants.timing.pty_poll_interval_ms)
        self._reaper.timeout.connect(self._reap_child)
        self._reaper.start()

    def _on_master_readable(self) -> None:
        """Drain the PTY into ``terminal_output`` until ``EAGAIN``."""
        if self._master_fd is None:
            return
        chunk_size = self._constants.pty.read_chunk_bytes
        accumulator: list[bytes] = []
        while True:
            try:
                data = os.read(self._master_fd, chunk_size)
            except OSError as exc:
                if exc.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    break
                if exc.errno == errno.EIO:
                    self._handle_pty_eof()
                    return
                self._emit_event(EventLevel.ERROR, f"PTY read failed: {exc}")
                return
            if not data:
                self._handle_pty_eof()
                return
            accumulator.append(data)
        if accumulator:
            decoded = b"".join(accumulator).decode(
                self._constants.pty.encoding,
                errors=self._constants.pty.encoding_errors,
            )
            self.terminal_output.emit(decoded)

    def _handle_pty_eof(self) -> None:
        """Close the master fd once the child closes its end."""
        self._emit_event(EventLevel.WARNING, "PTY reached EOF; child closed its tty.")
        self.stop()

    def _reap_child(self) -> None:
        """Detect child termination so the UI can show the disconnected state."""
        if self._child_pid is None:
            return
        try:
            pid, _status = os.waitpid(self._child_pid, os.WNOHANG)
        except ChildProcessError:
            self._child_pid = None
            self._set_status(BackendStatus.DISCONNECTED)
            return
        if pid != 0:
            self._child_pid = None
            self._emit_event(EventLevel.INFO, "Local console process exited.")
            self.stop()

    def _emit_event(self, level: EventLevel, message: str) -> None:
        """Forward a structured log line to the GUI event log."""
        record = EventRecord.now(level=level, source="local", message=message)
        self.event_logged.emit(record)
        if level in (EventLevel.ERROR, EventLevel.CRITICAL):
            _logger.error(message)
        elif level is EventLevel.WARNING:
            _logger.warning(message)
        else:
            _logger.debug(message)

    # Operator info is irrelevant for the local console but the abstract
    # signal exists, so emit a placeholder once at startup so panels can
    # render their badge.
    def announce_local_operator(self) -> None:
        """Emit a synthetic :class:`Operator` describing the local user."""
        operator = Operator(
            name=os.getenv("USER", "operator"),
            role="local",
            is_authenticated=True,
            karma_name="local",
            elo=0,
        )
        self.operator_changed.emit(operator)
