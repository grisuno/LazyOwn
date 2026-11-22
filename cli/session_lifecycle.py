"""Session crypto + lifecycle wiring for ``LazyOwnShell``.

Owns the shell side of at-rest session protection and gym teardown:
installing signal handlers that encrypt session data when the process is
killed externally, the auto decrypt-on-login / encrypt-on-close pair, and
the interactive-only gym machine cleanup. The encryption itself lives in
:class:`cli.auto_crypto.AutoCryptoEngine` (bound as ``self._auto_crypto``)
and the teardown in :mod:`modules.gym_cleanup`; this mixin is only the
lifecycle glue.

Methods read shell state through ``self`` (``_auto_crypto``) and the
parsed startup namespace through :data:`utils.startup_ns`, and are invoked
from ``__init__``/``preloop``/``atexit`` of the shell, so the mixin keeps
the exact ``self`` semantics with no call-site rewrite.
"""

from __future__ import annotations

import os

from cli.ux_logging import ux_debug as _ux_debug
from utils import print_warn, startup_ns


class SessionLifecycleMixin:
    """Wire session encryption and gym teardown into :class:`LazyOwnShell`.

    Mixed into the shell; invoked at startup (decrypt, signal install),
    at close (encrypt), and on interactive exit (gym cleanup).
    """

    def _install_crypto_signal_handlers(self) -> None:
        """Encrypt session data when the process is terminated externally.

        SIGTERM/SIGHUP bypass ``atexit`` (closing the terminal, killing
        the shell), so both get a handler that runs the same encryption
        path and then re-raises the signal with its original disposition.
        """
        import signal

        for signum in (signal.SIGTERM, signal.SIGHUP):
            try:
                previous = signal.getsignal(signum)
            except (ValueError, OSError, AttributeError):
                continue
            if previous is not signal.SIG_DFL:
                continue

            def _handler(received, frame, _signum=signum):
                try:
                    self._run_gym_cleanup()
                finally:
                    try:
                        self._run_auto_encrypt()
                    finally:
                        signal.signal(_signum, signal.SIG_DFL)
                        os.kill(os.getpid(), _signum)

            signal.signal(signum, _handler)

    def _run_auto_decrypt(self) -> None:
        """Decrypt session data automatically on authenticated startup."""
        crypto = getattr(self, "_auto_crypto", None)
        if crypto is None or not crypto.enabled:
            return
        try:
            decrypted = crypto.decrypt_session()
            if decrypted:
                print("Session data decrypted successfully.", flush=True)
        except Exception as exc:
            _ux_debug("auto-crypto session decryption failed", exc)

    def _run_auto_encrypt(self) -> None:
        """Encrypt session data automatically on application close."""
        crypto = getattr(self, "_auto_crypto", None)
        if crypto is None or not crypto.enabled:
            return
        try:
            if not crypto.has_password():
                print_warn("session encryption skipped: no operator login and LAZYOWN_MASTER_PASSWORD is not set")
                return
            encrypted = crypto.encrypt_session()
            if encrypted:
                print("Session data encrypted for at-rest protection.", flush=True)
            else:
                print_warn("session encryption skipped: no protected files found")
        except Exception as exc:
            print_warn(f"session encryption failed: {exc}")

    def _run_gym_cleanup(self) -> None:
        """Stop gym lab and range machines on interactive shell exit.

        Headless and autonomous processes never stop gym machines: the
        dashboard loop subprocess and ``-c`` runs are transient — their
        exit must not tear down a lab a later run needs.
        """
        import os as _os

        if _os.environ.get("LAZYOWN_AUTONOMOUS", "") == "1":
            return
        if startup_ns.command or startup_ns.run_chain:
            return
        try:
            from modules.gym_cleanup import cleanup_gym_machines

            cleanup_gym_machines(verbose=True)
        except Exception as exc:
            _ux_debug("gym machine cleanup failed", exc)
